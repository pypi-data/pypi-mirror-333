import torch
import copy
import math
import time
import traceback
import json

from tlnp_lib.lambda_tuner import LambdaTuner
from tlnp_lib.training_logger import TrainingLogger
from tlnp_lib.training_utils import TrainingUtils
from tlnp_lib.point_selection_utils import PointSelectionUtils

class TransferLearningNeymanPearson:
    def __init__(self, config, data_dict, model, loss_function, optimizer, scheduler):
        # Store objects
        self.data_dict = data_dict
        self.model = model
        self.loss_function = loss_function
        self.optimizer = optimizer
        self.scheduler = scheduler

        # Set up logger and utils
        self.logger = TrainingLogger(config.get('debug_modes', {}))
        self.utils = TrainingUtils(self.logger)

        # Clone data to ensure the original data is not modified
        self.data_dict = {key: value.clone()
                          for key, value in data_dict.items()}

        # Unpack config with defaults
        defaults = {
            'num_epochs': 100,
            'batch_size': 16,
            'max_grad_norm': None,
            'early_stopping_patience': 30,
            'early_stopping_min_delta': 0.001,
            'lambda_source_list': [0, 0.05, 0.1, 0.5, 1, 5, 10, 20, 40, 60, 80, 100],
            'selection_constant': 0.5,
            'type1_error_upperbound': 0.2,
            'type1_error_lowerbound': None,
            'validation_split': 0.2,
            'data_standardization': False,
            'cols_to_standardize': None,  # If none, standardizes all columns
            'device': 'cuda' if torch.cuda.is_available() else 'cpu',
            'lambda_limit': 1e6,
            'max_tuning_tries': 30,
            'initial_increment_factor': 0.5,
            'seed': None,
            'model_save_path': None,
            'results_save_path': None,
            'restore_model_after_completion': True,
        }
        for key, default_value in defaults.items():
            setattr(self, key, config.get(key, default_value))

        # Ensure lambda_source_list is all floats
        self.lambda_source_list = [float(x) for x in self.lambda_source_list]

        # Dict to store all results and model states
        self.all_results = {'approach_name': 'tlnp', 'training_results': {}, 'config': config}
        self.all_model_states = {}

        # Set the seed
        self.utils.set_seed(self.seed, self.all_results)

        # Initialize the lambda limits
        self._set_lambda_limits()

        # Handle optional source data
        self.source_exists = 'source_abnormal_data' in self.data_dict
        if not self.source_exists:
            # If no source data, create an empty tensor to avoid checks
            feature_dim = self.data_dict['target_abnormal_data'].shape[1]
            self.data_dict['source_abnormal_data'] = torch.empty(
                (0, feature_dim))

        # Transfer data and model to device
        self.device = self.utils.transfer_to_device(
            self.device, self.model, self.data_dict)

        # Optional test datasets
        self.has_test_data = any(key in self.data_dict for key in [
                                 'target_abnormal_test_data', 'target_normal_test_data'])

        # Set and check error thresholds
        self._set_type1_lowerbound()
        self.utils.check_error_thresholds(
            self.data_dict['target_normal_data'], self.type1_error_lowerbound, self.type1_error_upperbound)

        # Standardize data, if required
        if self.data_standardization:
            self.utils.standardize_data(
                self.data_dict, self.cols_to_standardize)

        # Set up evaluation data
        self.X_evaluation, self.labels_evaluation = self.utils.prepare_evaluation_data(
            self.data_dict, self.device)

        # Set up lambda tuner
        self.lambda_tuner = LambdaTuner(self.train_one_lambda_pair, self.logger, self.type1_error_lowerbound,
                                        self.type1_error_upperbound, self.max_tuning_tries, self.initial_increment_factor, self.lambda_min, self.lambda_max)

        # Store initial states
        self._store_initial_states()

    ###########################################################################
    # Setup Functions
    ###########################################################################

    def _set_lambda_limits(self):
        if self.lambda_limit > 1:
            self.lambda_max = self.lambda_limit
            self.lambda_min = 1/self.lambda_limit
        else:
            self.lambda_max = 1/self.lambda_limit
            self.lambda_min = self.lambda_limit

    def _set_type1_lowerbound(self):
        if self.type1_error_upperbound <= 0 or self.type1_error_upperbound >= 1:
            raise ValueError(
                f"Type-I error upperbound must be between 0 and 1.")
        if not self.type1_error_lowerbound:
            epsilon = .5/math.sqrt(len(self.data_dict['target_normal_data']))
            self.type1_error_lowerbound = self.type1_error_upperbound - epsilon * 2
        else:
            if self.type1_error_lowerbound < 0 or self.type1_error_lowerbound >= self.type1_error_upperbound:
                raise ValueError(
                    f"Type-I error lowerbound must be between 0 and {self.type1_error_upperbound}.")
        self.logger.log(
            f"Using Type-I error range: [{round(self.type1_error_lowerbound,4)}, {round(self.type1_error_upperbound,4)}]")

    def _store_initial_states(self):
        self.initial_model_state = copy.deepcopy(self.model.state_dict())
        self.initial_optimizer_state = copy.deepcopy(
            self.optimizer.state_dict())
        self.initial_scheduler_state = copy.deepcopy(
            self.scheduler.state_dict()) if self.scheduler else None

    def _restore_initial_states(self):
        self.model.load_state_dict(self.initial_model_state)
        self.optimizer.load_state_dict(self.initial_optimizer_state)
        if self.scheduler:
            self.scheduler.load_state_dict(self.initial_scheduler_state)

    ###########################################################################
    # Training Helper Functions
    ###########################################################################

    def _update_scheduler_and_learning_rate(self, epoch, val_loss, lr_change_epochs):
        # Update scheduler and learning rate
        current_lr = self.optimizer.param_groups[0]['lr']

        # Scheduler step
        if isinstance(self.scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
            self.scheduler.step(val_loss)
        else:
            self.scheduler.step()

        # Check if the learning rate has changed
        new_lr = self.optimizer.param_groups[0]['lr']
        if new_lr != current_lr:
            self.logger.log_lr_changes(
                f"Epoch {epoch}/{self.num_epochs}: Learning rate changed to {new_lr:.2e}")
            lr_change_epochs.append(epoch)

        return lr_change_epochs

    def _check_early_stopping(self, val_loss, best_val_loss, best_model_state, epochs_without_improvement):
        # Early stopping check
        if val_loss < best_val_loss - self.early_stopping_min_delta:
            best_val_loss = val_loss
            best_model_state = self.model.state_dict()
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1

        return best_val_loss, best_model_state, epochs_without_improvement

    def _store_lambda_pair_results(self, lambda_source, lambda_normal, epoch_training_losses, epoch_validation_losses, evaluation_error_rates):
        # Generate a unique key for this lambda pair
        model_key = f"lambda_source_{lambda_source}_lambda_normal_{lambda_normal}"

        # Store the results for this specific lambda pair
        self.all_results["training_results"][model_key] = {
            'lambda_source': lambda_source,
            'lambda_normal': lambda_normal,
            'training_losses': epoch_training_losses,
            'validation_losses': epoch_validation_losses,
            'evaluation_metrics': {
                'type1_error_rate': evaluation_error_rates[0],
                'type2_error_rate_target': evaluation_error_rates[1],
                **({'type2_error_rate_source': evaluation_error_rates[2]} if len(evaluation_error_rates) > 2 else {}),
            }
        }

        # Print evaluation results
        output = f"Lambda Source: {lambda_source}, Lambda Normal: {lambda_normal}, Type-I Error Rate: {evaluation_error_rates[0]:.4f}, Type-II Error Rate (Target): {evaluation_error_rates[1]:.4f}"
        if len(evaluation_error_rates) > 2:
            output += f", Type-II Error Rate (Source): {round(evaluation_error_rates[2], 4)}"
        self.logger.log_training_progress(output)

        # Store the model's best state corresponding to this lambda pair for final testing
        if self.has_test_data:
            best_model_state = copy.deepcopy(self.model.state_dict())
            self.all_model_states[model_key] = best_model_state

    ###########################################################################
    # Core Training Functions
    ###########################################################################

    def train_one_lambda_pair(self, lambda_source, lambda_normal):
        self.logger.log_training_progress(
            f"Training with lambda_source={lambda_source}, lambda_normal={lambda_normal}")

        # Initialize tracking variables
        epoch_training_losses, epoch_validation_losses, lr_change_epochs = [], [], []
        total_epoch_time = 0
        best_val_loss, best_model_state, epochs_without_improvement = float(
            'inf'), None, 0

        for epoch in range(self.num_epochs):
            epoch_start_time = time.time()
            # Split data into training and validation sets
            X_train, labels_train, X_val, labels_val = self.utils.prepare_data_splits(
                self.data_dict, self.device, self.validation_split)

            # Train for one epoch
            loss = self._train_one_epoch(
                X_train, labels_train, lambda_source, lambda_normal)

            # Validate the model
            val_loss = self._validate_model(
                X_val, labels_val, lambda_source, lambda_normal)

            # Update losses
            epoch_training_losses.append(loss)
            epoch_validation_losses.append(val_loss)

            # End timer for the epoch and calculate epoch time
            epoch_end_time = time.time()
            epoch_time = epoch_end_time - epoch_start_time
            total_epoch_time += epoch_time

            # Print progress
            self.logger.log_training_progress_losses(
                epoch, loss, val_loss, total_epoch_time, self.num_epochs)

            # Learning rate scheduling and early stopping
            lr_change_epochs = self._update_scheduler_and_learning_rate(
                epoch, val_loss, lr_change_epochs)

            # Check for early stopping
            best_val_loss, best_model_state, epochs_without_improvement = self._check_early_stopping(
                val_loss, best_val_loss, best_model_state, epochs_without_improvement)
            if epochs_without_improvement >= self.early_stopping_patience:
                self.logger.log_training_progress(
                    f"Early stopping at epoch {epoch}")
                break

        # Show losses graph if required
        self.logger.show_training_loss_plot(
            epoch_training_losses, epoch_validation_losses, lr_change_epochs)

        # Restore the best model state for evaluation
        if best_model_state:
            self.model.load_state_dict(best_model_state)

        # Lambda pair evaluation
        evaluation_error_rates = self._evaluate_lambda_pair()

        # Store results
        self._store_lambda_pair_results(lambda_source, lambda_normal, epoch_training_losses,
                                        epoch_validation_losses, evaluation_error_rates)

        # Restore initial states
        self._restore_initial_states()

        return evaluation_error_rates

    def _train_one_epoch(self, X_train, labels_train, lambda_source, lambda_normal):
        self.model.train()
        total_loss = 0

        # Divide dataset into randomized batches
        indices = torch.randperm(X_train.size(0))
        X_train = X_train[indices]
        labels_train = labels_train[indices]
        num_batches = (len(X_train) + self.batch_size - 1) // self.batch_size

        for i in range(num_batches):
            # Get the batch
            start_idx = i * self.batch_size
            end_idx = min(start_idx + self.batch_size, len(X_train))
            X_batch = X_train[start_idx:end_idx]
            label_batch = labels_train[start_idx:end_idx]

            # Train the model
            self.optimizer.zero_grad()
            output = self.model(X_batch)
            loss = self.loss_function(
                output, label_batch, 1, lambda_source, lambda_normal)
            loss.backward()
            total_loss += loss.item()
            self.optimizer.step()

            # Clip gradients
            if self.max_grad_norm:
                torch.nn.utils.clip_grad_norm_(
                    self.model.parameters(), self.max_grad_norm)

        return total_loss / num_batches

    def _validate_model(self, X_val, labels_val, lambda_source, lambda_normal):
        # Validation performed after each epoch during one lambda pair training
        self.model.eval()
        val_loss = 0

        num_batches_val = (len(X_val) + self.batch_size - 1) // self.batch_size
        with torch.no_grad():
            for i in range(num_batches_val):
                start_idx = i * self.batch_size
                end_idx = min(start_idx + self.batch_size, len(X_val))
                X_batch_val = X_val[start_idx:end_idx]
                label_batch_val = labels_val[start_idx:end_idx]

                output_val = self.model(X_batch_val)
                val_loss += self.loss_function(output_val, label_batch_val,
                                               1, lambda_source, lambda_normal).item()

        self.model.train()
        return val_loss / num_batches_val

    def _evaluate_lambda_pair(self):
        # Lambda pair evaluation performed after training one lambda pair
        output_evaluation = []

        self.model.eval()
        with torch.no_grad():
            num_batches = (len(self.X_evaluation) +
                           self.batch_size - 1) // self.batch_size
            for i in range(num_batches):
                start_idx = i * self.batch_size
                end_idx = min(start_idx + self.batch_size,
                              len(self.X_evaluation))
                X_batch_evaluation = self.X_evaluation[start_idx:end_idx]
                output_evaluation.append(self.model(X_batch_evaluation))

        output_evaluation = torch.cat(output_evaluation, dim=0)
        self.model.train()

        return self._measure_evaluation_metrics(output_evaluation)

    def _measure_evaluation_metrics(self, output_evaluation):
        # Calculate error rates for lambda evaluation
        type1_error_rate = self.utils.calculate_type1_error_rate(
            output_evaluation[self.labels_evaluation == 0])
        type2_error_rate_target = self.utils.calculate_type2_error_rate(
            output_evaluation[self.labels_evaluation == 1])

        if self.source_exists:
            type2_error_rate_source = self.utils.calculate_type2_error_rate(
                output_evaluation[self.labels_evaluation == 2])
            return (type1_error_rate, type2_error_rate_target, type2_error_rate_source)

        return (type1_error_rate, type2_error_rate_target)

    def _evaluate_on_test_data(self, best_point, model_suffix=""):
        # Evaluate test data after all trainings have completed and the final point is chosen        
        test_error_dict = {}
        if not self.has_test_data:
            return test_error_dict
        output_string = f"\nEvaluation on test data:\n"

        # Load the best model state for the best point
        best_model_state = self.all_model_states[
            f"lambda_source_{best_point[0]}_lambda_normal_{best_point[1]}"]
        self.model.load_state_dict(best_model_state)

        # Evaluate on test data
        self.model.eval()
        with torch.no_grad():
            type1_error_test, type2_error_test = None, None
            test_datasets = ['target_normal_test_data',
                             'target_abnormal_test_data']

            # Evaluate on each of the test sets. Add results to the dict and log results
            for test_dataset in test_datasets:
                if test_dataset in self.data_dict:
                    output_test = self.model(self.data_dict[test_dataset])

                    # Subtract the threshold if it exists (for Naive NP)
                    if hasattr(self, "optimal_threshold"):
                        output_test = output_test - self.optimal_threshold
                        output_string += f"Threshold: {self.optimal_threshold}\n"

                    # Calculate Type-I Error from the target normal test data
                    if test_dataset == 'target_normal_test_data':
                        type1_error_test = self.utils.calculate_type1_error_rate(
                            output_test)
                        test_error_dict["type1_error_test"] = type1_error_test
                        output_string += f"     Type-I Error Rate: {type1_error_test}\n"

                    # Calculate Type-II Error from the target abnormal test data
                    elif test_dataset == 'target_abnormal_test_data':
                        type2_error_test = self.utils.calculate_type2_error_rate(
                            output_test)
                        test_error_dict["type2_error_test"] = type2_error_test
                        output_string += f"     Type-II Error Rate: {type2_error_test}\n"
            self.logger.log(output_string)

        # Save the model
        if self.model_save_path:
            model_save_path = self.model_save_path + model_suffix + ".pth"
            self.logger.log(f"Saving model to {model_save_path}")
            torch.save(self.model.state_dict(), model_save_path)

        # Reset initial states in case of further training
        if self.restore_model_after_completion:
            self._restore_initial_states()

        return test_error_dict

    ###########################################################################
    # Core Process Functions
    ###########################################################################

    def run_training_process(self):
        try:
            start_time = time.time()
            
            if self.source_exists:
                self.run_training_with_source()
            else:
                self.run_training_without_source()
                
            process_time = time.time() - start_time
            self.all_results['process_time'] = process_time

            if self.results_save_path:
                with open(self.results_save_path + '_tlnp.json', 'w') as f:
                    json.dump(self.all_results, f, indent=4)
            return self.all_results

        except Exception as e:
            print(f"Error occurred during training process: {e}")
            print(traceback.format_exc())

    def run_training_without_source(self):
        self.logger.log(f"No source data in data_dict. Training without source.")
        
        # Fine-tune with lambda_source fixed at 0
        best_point = self.lambda_tuner.fine_tune_lambda(
            lambda_source=0.0, lambda_normal=1.0, tune_lambda="normal")

        # If no suitable point could be found within the Type-I Error limits, choose the best one below the Type-I Error upperbound
        if not best_point:
            best_point = PointSelectionUtils.find_best_point_after_failures(
                self.all_results, self.type1_error_upperbound)

        # If no points were below the Type-I Error upperbound, raise an error
        if not best_point:
            raise ValueError(f"No suitable point could be found.")

        # Evaluate and store test results
        test_error_dict = self._evaluate_on_test_data(
            best_point, model_suffix="_tlnp")
        self.all_results["test_metrics"] = {
            'best_lambda_source': best_point[0],
            'best_lambda_normal': best_point[1],
            **test_error_dict,
            'num_trainings': len(self.all_results["training_results"])
        }

    def run_training_with_source(self):
        low_magnitude = min([x for x in self.lambda_source_list if x != 0])
        high_magnitude = max(self.lambda_source_list)
        lambda_normal = 1.0
        num_tuned_points = 0

        # Iterate through the lambda_source_list, tuning lambda_normal for each lambda_source
        while self.lambda_source_list:
            # Tune lambda_normal with the next lambda_source
            lambda_source = self.lambda_source_list.pop(0)
            tuned_point = self.lambda_tuner.fine_tune_lambda(
                lambda_source, lambda_normal, tune_lambda='normal')

            if tuned_point:
                # Start next lambda_source tuning at previously converged lambda_normal
                lambda_normal = tuned_point[1]

                # Track points that converged
                num_tuned_points += 1
                
            # If fewer than 5 points converged, expand the lambda_source_list and continue
            self._update_lambda_list(
                low_magnitude, high_magnitude, num_tuned_points)

        num_trainings = len(self.all_results["training_results"])
        self.logger.log(
            f"Number of trainings completed during process: {num_trainings}")

        # Choose the final point
        final_point, num_points_threshold1, num_points_threshold2, target_type2_upperbound = PointSelectionUtils.choose_final_point_constant_method(
            self.logger, self.all_results, self.data_dict, self.type1_error_upperbound, self.selection_constant)

        # Evaluate and store results
        self._evaluate_and_store_results(
            final_point=final_point,
            num_points_threshold1=num_points_threshold1,
            num_points_threshold2=num_points_threshold2,
            type1_upperbound=self.type1_error_upperbound,
            target_type2_upperbound=target_type2_upperbound
        )
        self.all_results['test_metrics']['num_trainings'] = num_trainings

    ###########################################################################
    # Helper Functions for Core Process
    ###########################################################################

    def _update_lambda_list(self, low_magnitude, high_magnitude, num_tuned_points):
        # If fewer than 5 points converged, expand the lambda_source_list by one magnitude
        if len(self.lambda_source_list) == 0 and num_tuned_points < 5:
            low_magnitude -= 1
            high_magnitude += 1
            if 10**low_magnitude > self.lambda_min:
                self.lambda_source_list.append(10**low_magnitude)
            if 10**high_magnitude < self.lambda_max:
                self.lambda_source_list.append(10**high_magnitude)

    def _evaluate_and_store_results(self, final_point, num_points_threshold1, num_points_threshold2, type1_upperbound, target_type2_upperbound):
        # Evaluate the final model on the test dataset
        final_point = (final_point["lambda_source"],
                       final_point["lambda_normal"])
        test_error_dict = self._evaluate_on_test_data(
            final_point, model_suffix="_tlnp")

        # Store results in self.all_results
        result_entry = {
            'best_lambda_source': final_point[0],
            'best_lambda_normal': final_point[1],
            **test_error_dict,
            'type1_upperbound': type1_upperbound,
            'num_points_threshold1': num_points_threshold1,
            'target_type2_upperbound': target_type2_upperbound,
            'num_points_threshold2': num_points_threshold2
        }

        self.all_results[f"test_metrics"] = result_entry
