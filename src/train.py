import torch
import torch.nn as nn
import torch.optim as optim
import yaml
import os
import sys
from pathlib import Path
from collections import Counter
import warnings

warnings.filterwarnings("ignore")

# добавляем путь к src
sys.path.append(str(Path(__file__).parent))

from data import get_dataloaders
from models import SwanClassifier
from utils import train_epoch, validate, plot_training_history, save_metrics


def load_params(config_path="params.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def main(config_path="params.yaml"):
    params = load_params(config_path)

    os.makedirs("models", exist_ok=True)
    os.makedirs("plots", exist_ok=True)
    os.makedirs("metrics", exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Устройство: {device}")
    print(f"Конфигурация: {config_path}")

    train_loader, val_loader, test_loader, species_names = get_dataloaders(params)

    model = SwanClassifier(
        num_classes=params["data"]["num_classes"],
        model_name=params["model"]["name"],
        dropout_rate=params["model"]["dropout_rate"],
        freeze_backbone=params["model"]["freeze_backbone"],
    ).to(device)

    #class weights
    labels = train_loader.dataset.metadata["species_key"]
    class_counts = Counter(labels)

    weights = [1.0 / class_counts[cls] for cls in species_names]
    class_weights = torch.tensor(weights, dtype=torch.float).to(device)

    criterion = nn.CrossEntropyLoss(
        weight=class_weights,
        label_smoothing=params["loss"]["label_smoothing"],
    )

    # optimizer
    lr = params["training"]["lr"]

    backbone_params = []
    classifier_params = []

    for name, param in model.named_parameters():
        if "classifier" in name or "fc" in name:
            classifier_params.append(param)
        else:
            backbone_params.append(param)

    optimizer = optim.AdamW(
        [
            {"params": backbone_params, "lr": lr * 0.1},
            {"params": classifier_params, "lr": lr},
        ],
        weight_decay=params["optimizer"]["weight_decay"],
    )
    #scheduler
    scheduler = optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=params["training"]["epochs"]
    )

    train_losses, val_losses = [], []
    train_accs, val_accs = [], []

    best_val_acc = 0.0
    epochs_no_improve = 0

    for epoch in range(params["training"]["epochs"]):
        print(f"\nEpoch {epoch + 1}/{params['training']['epochs']}")

        # unfreeze backbone
        if epoch == params["training"]["unfreeze_epoch"]:
            print("Unfreezing backbone")
            model.unfreeze_backbone()
            optimizer.param_groups[0]["lr"] = lr * 0.1
            optimizer.param_groups[1]["lr"] = lr

        # train
        train_loss, train_acc = train_epoch(
            model=model,
            loader=train_loader,
            criterion=criterion,
            optimizer=optimizer,
            device=device,
            gradient_clip=params["training"]["gradient_clip"],
        )

        # validate
        val_loss, val_acc, _, _ = validate(
            model=model,
            loader=val_loader,
            criterion=criterion,
            device=device,
        )

        train_losses.append(train_loss)
        val_losses.append(val_loss)
        train_accs.append(train_acc)
        val_accs.append(val_acc)

        print(
            f"Train Acc: {train_acc:.2f}% | "
            f"Val Acc: {val_acc:.2f}% | "
            f"LR backbone: {optimizer.param_groups[0]['lr']:.2e}"
        )

        # сохраняем лучшую модель
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            epochs_no_improve = 0

            torch.save(
                {
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "val_acc": val_acc,
                    "params": params,
                    "species_names": species_names,
                },
                "models/best_model.pth",
            )
            print(f"Сохранена лучшая модель с точностью: {val_acc:.2f}%")

        else:
            epochs_no_improve += 1

        scheduler.step()

        # early stopping
        if epoch >= params["training"]["min_epochs"]:
            if epochs_no_improve >= params["training"]["patience"]:
                print("Early stopping")
                break

    history = {
        "train_losses": train_losses,
        "val_losses": val_losses,
        "train_accs": train_accs,
        "val_accs": val_accs,
        "best_val_acc": best_val_acc,
    }

    torch.save(history, "models/training_history.pth")

    plot_training_history(
        train_losses,
        val_losses,
        train_accs,
        val_accs,
        save_path="plots/training_history.png",
    )

    save_metrics(
        {
            "best_val_accuracy": float(best_val_acc),
            "final_train_accuracy": float(train_accs[-1]),
            "final_val_accuracy": float(val_accs[-1]),
            "final_train_loss": float(train_losses[-1]),
            "final_val_loss": float(val_losses[-1]),
        },
        "metrics/train_metrics.json",
    )

    print(f"\nЛучшая точность валидации: {best_val_acc:.2f}%")
    return model, best_val_acc


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train swan classifier")
    parser.add_argument(
        "--config",
        type=str,
        default="params.yaml",
        help="Path to config file",
    )

    args = parser.parse_args()
    main(args.config)
