import os
import json
from datetime import datetime
import torch
import matplotlib.pyplot as plt
def save_model_checkpoint(trained_model, name, metrics, tl, vl):
    # Create base directory
    base_dir = "saved_models"
    os.makedirs(base_dir, exist_ok=True)

    # Create timestamped subfolder
    timestamp = datetime.now().strftime("%Y%m%d")
    save_dir = os.path.join(base_dir, f"{name}_{timestamp}")
    # Create directory structure
    os.makedirs(save_dir, exist_ok=True)

        # Define paths
    metrics_path = os.path.join(save_dir, "metrics.json")
    model_path = os.path.join(save_dir, "model.pt")
    graph_path = os.path.join(save_dir, "learning_curve.png")

        # Save metrics
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)

        # Save model
    scripted_model = torch.jit.script(trained_model)
    scripted_model.save(model_path)

        # Save learning curve
    plt.figure(figsize=(8, 6))
    plt.plot(tl, label="Train Loss")
    plt.plot(vl, label="Validation Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.title("Training vs Validation Loss")
    plt.legend()
    plt.savefig(graph_path)
    plt.close()

    print("\nSaved successfully to:")
    print(f"📁 {save_dir}/")
    print("├── 📄 metrics.json")
    print("└── 🧠 model.pt\n")
    print("└── 📉 learning_curve.png\n")
