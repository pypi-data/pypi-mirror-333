from .model import AO_ANN
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, RandomSampler, SubsetRandomSampler
import pandas as pd
from .loss import calculate_loss
import numpy as np
import json
import os
from sklearn.model_selection import train_test_split
from .utils import save_model_checkpoint
from .dataset import DS

import glob

def train_model(model: torch.nn.Module, train_loader, val_loader, criterion, optimizer, device, epochs):
    """Train the model with improved learning rate scheduling and regularization"""
    scheduler = torch.optim.lr_scheduler.OneCycleLR(
        optimizer,
        max_lr=optimizer.param_groups[0]['lr'],
        epochs=epochs,
        steps_per_epoch=len(train_loader),
        pct_start=0.3,
        anneal_strategy='cos'
    )

    train_losses = []
    val_losses = []
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        for batch_X, batch_y in train_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            optimizer.zero_grad()

            output = model(batch_X.float())
            target = batch_y.float().view_as(output)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            scheduler.step()
            train_loss += loss.item()

        avg_train_loss = train_loss / len(train_loader)
        train_losses.append(avg_train_loss)

        # validation phase
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch_X, batch_y in val_loader:
                batch_X, batch_y = batch_X.to(device), batch_y.to(device)
                output = model(batch_X.float())
                target = batch_y.float().view_as(output)
                loss = criterion(output, target)
                val_loss += loss.item()

        avg_val_loss = val_loss / len(val_loader)
        val_losses.append(avg_val_loss)
        print('Epoch {}: Train Loss {:.4f} Val Loss {:.4f}'.format(epoch + 1, avg_train_loss, avg_val_loss))
    return model, train_losses, val_losses



def evaluate_model(model, data_loader, criterion, device):
    model.eval()
    total_loss = 0
    predictions = []
    targets = []

    with torch.no_grad():
        for X, Y in data_loader:
            X, Y = X.to(device), Y.to(device)
            output = model(X)
            # Reshape target to match output dimensions
            target = Y.float().view_as(output)
            loss = criterion(output, target)
            total_loss += loss.item()

            # Store predictions and targets as flattened arrays
            predictions.extend(output.cpu().numpy().flatten())
            targets.extend(Y.cpu().numpy().flatten())  # Original target shape is preserved here for correct metrics

    avg_loss = total_loss / len(data_loader)
    return avg_loss, np.array(predictions), np.array(targets)

# Split existing dataset into training and validation sets
def train_val_split(dataset, val_size=0.2, random_state=42):
    # Get indices of the full dataset
    indices = list(range(len(dataset)))

    # Split indices into train and validation
    train_indices, val_indices = train_test_split(
        indices,
        test_size=val_size,
        random_state=random_state
    )

    # Create samplers for train and validation
    train_sampler = SubsetRandomSampler(train_indices)
    val_sampler = SubsetRandomSampler(val_indices)

    return train_sampler, val_sampler

def main(dataset_train, dataset_test, name, params_path):
    torch.set_float32_matmul_precision('high')
    num_workers = 6
    device = torch.device("cuda")
    print(f"Using device: {device}")
    params = json.load(open(params_path))
    lr = params['lr']
    weight_decay = params['weight_decay']
    batch_size = params['batch_size']

    epochs = params['epochs']
    target_scaler = dataset_train.target_scaler

    # Create samplers
    train_sampler, val_sampler = train_val_split(dataset_train, val_size=0.2)
    test_sampler = RandomSampler(dataset_test)

    # Create data loaders
    train_loader = DataLoader(dataset_train, batch_size=batch_size, sampler=train_sampler, num_workers=num_workers, pin_memory=True)
    val_loader = DataLoader(
        dataset_train,  # Using test dataset for validation
        batch_size=batch_size,
        sampler=val_sampler,
        num_workers=num_workers,
        pin_memory=True
    )
    test_loader = DataLoader(dataset_test, batch_size=batch_size, sampler=test_sampler, num_workers=num_workers, pin_memory=True)
    dropout_rate = params['dropout_rate']  # Increased dropout rate for stronger regularization
    # Model setup
    model = AO_ANN(dropout_rate=dropout_rate).to(device)
    #model = torch.compile(model)
    criterion = nn.HuberLoss()

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=lr,
        weight_decay=weight_decay,  # Increased weight decay for stronger L2 regularization
        betas=(0.9, 0.999),
        eps=1e-8
    )
    # Training
    trained_model, tl, vl = train_model(model, train_loader, val_loader, criterion, optimizer, device, epochs=epochs)

    # Evaluation
    train_loss, train_pred, train_target = evaluate_model(trained_model, train_loader, criterion, device)
    test_loss, test_pred, test_target = evaluate_model(trained_model, test_loader, criterion, device)

    # Convert predictions and targets to plain floats
    train_pred = [float(x) for x in train_pred]
    train_target = [float(x) for x in train_target]

    test_pred = [float(x) for x in test_pred]
    test_target = [float(x) for x in test_target]

    # Save results
    train_df = pd.DataFrame({
        'predictions': train_pred,
        'targets': train_target
    })
    train_df.to_csv('train_results.csv', index=False)

    test_df = pd.DataFrame({
        'predictions': test_pred,
        'targets': test_target
    })
    test_df.to_csv('test_results.csv', index=False)

    # Calculate and print loss details
    print("In-sample (Training) Performance:")
    train_loss_details = calculate_loss('train_results.csv', target_scaler)
    for key, value in train_loss_details.items():
        print(f"{key}: {value}")

    print("\nOut-of-sample (Test) Performance:")
    test_loss_details = calculate_loss('test_results.csv', target_scaler)
    for key, value in test_loss_details.items():
        print(f"{key}: {value}")

    # Save metrics
    metrics = {
        "in_sample": train_loss_details,
        "out_of_sample": test_loss_details
    }
    save_model_checkpoint(trained_model, name, metrics, tl, vl)




# if __name__ == '__main__':
#     datasets_dir = "../datasets/"
#     datasets = [DS(d, None, os.path.splitext(os.path.basename(d))[0]) for d in glob.glob(f"{datasets_dir}/*.csv")]
#     params_path = 'params.json'
#     for dataset in datasets:
#         ds_train, ds_test = dataset.datasets()
#         main(ds_train, ds_test, dataset.name, params_path)
