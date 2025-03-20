import pandas as pd
import torch
from torch.utils.data import Dataset
from sklearn.preprocessing import MinMaxScaler
import sklearn.model_selection as sklearn
scaler = MinMaxScaler(feature_range=(0, 1))


class OptionDataset(Dataset):
    def __init__(self, dataframe, is_train=False, target_scaler=None):
        self.data = dataframe.copy().reset_index(drop=True)  # Ensure clean indexing
        self.is_train = is_train
        self.base_features = ["S0", "m", "r", "T", "corp",
                              "alpha", "beta", "omega", "gamma", "lambda"]
        self.target_scaler = target_scaler if target_scaler is not None else scaler
        if is_train:
            target_values = self.data[["V"]]
            self.target_scaler.fit(target_values)

        # Precompute constant features for faster access later
        self.epsilon = 1e-6  # To avoid division by zero in calculations
        self.data["strike"] = self.data["S0"] * self.data["m"]
        # Convert Series to Tensor for operations like log and sqrt
        gamma_values = self.data["gamma"].values
        self.data["log_gamma"] = torch.log(torch.tensor(gamma_values, dtype=torch.float32) + self.epsilon)
        
        m_values = self.data["m"].values
        self.data["log_m"] = torch.log(torch.tensor(m_values, dtype=torch.float32))
        
        omega_values = self.data["omega"].values
        self.data["sqrt_omega"] = torch.sqrt(torch.tensor(omega_values, dtype=torch.float32) + self.epsilon)
        
        T_values = self.data["T"].values
        self.data["inv_T"] = 1 / (torch.tensor(T_values, dtype=torch.float32) + self.epsilon)
        
        alpha_values = self.data["alpha"].values
        beta_values = self.data["beta"].values
        self.data["alpha_beta"] = torch.tensor(alpha_values, dtype=torch.float32) * torch.tensor(beta_values, dtype=torch.float32)
        
        # self.data["risk_adjusted"] = (torch.tensor(self.data["corp"].values) * torch.tensor(self.data["omega"].values)) / (torch.tensor(self.data["gamma"].values) + self.epsilon)
        self.data["time_decay"] = torch.exp(-0.05 * torch.tensor(T_values, dtype=torch.float32))
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        # Ensure idx is an integer for proper DataFrame indexing
        if not isinstance(idx, int):
            idx = int(idx)
            
        # Directly access precomputed features for this sample
        row = self.data.iloc[idx]
        
        # Extract base features - row is a Series, so we can directly index it
        base_values = [row[feature] for feature in self.base_features]
        base_features = torch.tensor(base_values, dtype=torch.float32)

        # Extract precomputed engineered features
        engineered_features = torch.tensor([
            row["strike"],
            row["log_gamma"].item(),  # Use .item() to convert from tensor scalar
            row["sqrt_omega"].item(),
            row["inv_T"].item(),
            row["alpha_beta"].item(),
            row["time_decay"].item(),
        ], dtype=torch.float32)

        # Concatenate base features with engineered features
        X = torch.cat([base_features, engineered_features])

        # Scale target variable
        target_value = row["V"]
        target_df = pd.DataFrame([[target_value]], columns=["V"])
        scaled_target = self.target_scaler.transform(target_df).flatten()
        Y = torch.tensor(scaled_target, dtype=torch.float32)

        return X, Y

class DS:
    def __init__(self, path, path2, name):
        self.path = path
        self.path2 = path2
        self.name = name
    def datasets(self):
        if self.path2 is None:
            # Load and clean the dataset
            df = cleandataset(dataset_file(self.path))

            # Split into train and test - train_test_split already returns OptionDataset objects
            ds_train, ds_test = train_test_split(df)

            return ds_train, ds_test
        else:
            # Load and clean both datasets
            train_df = cleandataset(dataset_file(self.path))
            test_df = cleandataset(dataset_file(self.path2))
            
            # Use train_test_split to create the training dataset
            # Setting test_size=0 to keep all data in the training set
            ds_train, _ = train_test_split(train_df, test_size=0)
            
            # Create test dataset using the same scaler from training
            ds_test = OptionDataset(test_df, is_train=False, target_scaler=ds_train.target_scaler)

            return ds_train, ds_test


def train_test_split(data, test_size=0.3, random_state=42):
    """
    Split the dataset into training and validation sets.

    Args:
        data (pd.DataFrame): Input DataFrame containing the dataset
        test_size (float): Proportion of the dataset to include in the validation split (0 to 1)
        random_state (int): Random state for reproducibility

    Returns:
        tuple: (train_dataset, val_dataset) containing OptionDataset objects
    """
    # Split the data using sklearn's train_test_split
    train_data, val_data = sklearn.train_test_split(
        data,
        test_size=test_size,
        random_state=random_state,
        shuffle=True
    )

    # Create OptionDataset objects
    train_dataset = OptionDataset(train_data, is_train=True)
    val_dataset = OptionDataset(val_data, is_train=False,
                                target_scaler=train_dataset.target_scaler)

    return train_dataset, val_dataset


def dataset_file(filename):
    return pd.read_csv(filename)


def cleandataset(data):
    return data[data['V'] > 0.5].reset_index(drop=True)
