import numpy as np
import pandas as pd

def calculate_loss(data_file, target_scaler):
    """
    Calculate various performance metrics between predictions and targets.

    Parameters:
    data_file (str): Path to the CSV file containing predictions and targets.

    Returns:
    dict: A dictionary containing detailed performance metrics.
    """
    # Load the CSV file
    data = pd.read_csv(data_file)

    # Extract predictions and targets as numpy arrays
    predictions = data['predictions'].to_numpy()
    targets = data['targets'].to_numpy()

    # Inverse transform the scaled targets
    targets = target_scaler.inverse_transform(targets.reshape(-1, 1)).flatten()
    predictions = target_scaler.inverse_transform(predictions.reshape(-1, 1)).flatten()

    # Calculate various metrics
    absolute_errors = np.abs(predictions - targets)  # Absolute errors
    squared_errors = (predictions - targets) ** 2   # Squared errors

    # Mean Squared Error (MSE)
    mse = np.mean(squared_errors)

    # Mean Absolute Error (MAE)
    mae = np.mean(absolute_errors)

    # Root Mean Squared Error (RMSE)
    rmse = np.sqrt(mse)

    # R^2 score
    r2 = 1 - (np.sum(squared_errors) / np.sum((targets - np.mean(targets)) ** 2))

    # Mean Relative Error (MRE)
    # Avoid division by zero by adding a small epsilon to the denominator
    epsilon = 1e-8
    relative_errors = absolute_errors / (np.abs(targets) + epsilon)
    mre = np.mean(relative_errors)

    # Mean of predictions and targets
    mean_predicted = np.mean(predictions)
    mean_target = np.mean(targets)

    # Prepare detailed loss information
    loss_info = {
        'total_samples': len(predictions),
        'Mean of Predicted': mean_predicted,
        'Mean of Targets': mean_target,
        'MSE': mse,
        'MAE': mae,
        'RMSE': rmse,
        'R^2': r2,
        'MRE': mre,  # Mean Relative Error
        'min_error': np.min(absolute_errors),
        'max_error': np.max(absolute_errors),
        'std_error': np.std(absolute_errors)
    }

    return loss_info
