import torch
import torch.nn as nn
import torch.optim as optim
import yaml
import os
import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# добавляем путь к src для импорта
sys.path.append(str(Path(__file__).parent))

from data import get_dataloaders
from models import SwanClassifier
from utils import train_epoch, validate, plot_training_history, save_metrics


def load_params(config_path='params.yaml'):
    with open(config_path, 'r') as f:
        params = yaml.safe_load(f)
    return params


def main(config_path='params.yaml'):
    params = load_params(config_path)

    # директории
    os.makedirs('models', exist_ok=True)
    os.makedirs('plots', exist_ok=True)
    os.makedirs('metrics', exist_ok=True)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Устройство: {device}")
    print(f"Используем конфигурацию: {config_path}")

    train_loader, val_loader, test_loader, species_names = get_dataloaders(params)

    model = SwanClassifier(
        num_classes=params['data']['num_classes'],
        model_name=params['model']['name'],
        dropout_rate=params['model']['dropout_rate'],
        freeze_backbone=params['model']['freeze_backbone']
    ).to(device)

    criterion = nn.CrossEntropyLoss(
        label_smoothing=params['loss']['label_smoothing']
    )

    lr = params['training']['lr']

    # optimizer
    if params['optimizer']['name'] == 'AdamW':
        optimizer = optim.AdamW(
            [
                {
                    "params": model.backbone.features.parameters(),
                    "lr": lr * 0.1
                },
                {
                    "params": model.backbone.classifier.parameters(),
                    "lr": lr
                }
            ],
            weight_decay=params['optimizer']['weight_decay']
        )
    elif params['optimizer']['name'] == 'Adam':
        optimizer = optim.Adam(
            model.parameters(),
            lr=lr,
            weight_decay=params['optimizer']['weight_decay']
        )
    else:
        optimizer = optim.SGD(
            model.parameters(),
            lr=lr,
            momentum=0.9,
            weight_decay=params['optimizer']['weight_decay']
        )

    # scheduler
    if params['scheduler']['name'] == 'ReduceLROnPlateau':
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode='min',
            patience=params['scheduler']['patience'],
            factor=params['scheduler']['factor'],
            min_lr=params['scheduler']['min_lr'],
        )
    elif params['scheduler']['name'] == 'StepLR':
        scheduler = optim.lr_scheduler.StepLR(
            optimizer,
            step_size=params['scheduler'].get('step_size', 30),
            gamma=params['scheduler'].get('gamma', 0.1)
        )
    elif params['scheduler']['name'] == 'CosineAnnealingLR':
        scheduler = optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=params['training']['epochs']
        )
    else:
        scheduler = None

    train_losses = []
    val_losses = []
    train_accs = []
    val_accs = []

    best_val_acc = 0.0

    for epoch in range(params['training']['epochs']):
        print(f"\nEpoch {epoch + 1}/{params['training']['epochs']}")

        # fine-tuning
        if epoch == params['training']['unfreeze_epoch']:
            print("🔓 Unfreezing backbone for fine-tuning")

            model.unfreeze_backbone()

            # backbone — очень маленький LR
            optimizer.param_groups[0]['lr'] = lr * 0.01
            # classifier — обычный LR
            optimizer.param_groups[1]['lr'] = lr

        # тренировка
        train_loss, train_acc = train_epoch(
            model=model,
            loader=train_loader,
            criterion=criterion,
            optimizer=optimizer,
            device=device,
            gradient_clip=params['training']['gradient_clip']
        )
        train_losses.append(train_loss)
        train_accs.append(train_acc)

        # валидация
        val_loss, val_acc, _, _ = validate(
            model=model,
            loader=val_loader,
            criterion=criterion,
            device=device
        )
        val_losses.append(val_loss)
        val_accs.append(val_acc)

        # сохранение лучшей модели
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(
                {
                    'epoch': epoch,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'val_acc': val_acc,
                    'params': params,
                    'species_names': species_names
                },
                'models/best_model.pth'
            )
            print(f"Сохраняем лучшую модель с точностью: {val_acc:.2f}%")

        # scheduler
        if scheduler is not None:
            if isinstance(scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
                scheduler.step(val_loss)
            else:
                scheduler.step()

        print(
            f"Epoch {epoch + 1:3d}/{params['training']['epochs']} | "
            f"Train Acc: {train_acc:.2f}% | "
            f"Val Acc: {val_acc:.2f}% | "
            f"LR backbone: {optimizer.param_groups[0]['lr']:.2e} | "
            f"LR classifier: {optimizer.param_groups[1]['lr']:.2e}"
        )

    # сохранение истории
    history = {
        'train_losses': train_losses,
        'val_losses': val_losses,
        'train_accs': train_accs,
        'val_accs': val_accs,
        'best_val_acc': best_val_acc
    }
    torch.save(history, 'models/training_history.pth')

    plot_training_history(
        train_losses,
        val_losses,
        train_accs,
        val_accs,
        save_path='plots/training_history.png'
    )

    train_metrics = {
        'best_val_accuracy': float(best_val_acc),
        'final_train_accuracy': float(train_accs[-1]),
        'final_val_accuracy': float(val_accs[-1]),
        'final_train_loss': float(train_losses[-1]),
        'final_val_loss': float(val_losses[-1]),
        'total_epochs': len(train_losses)
    }
    save_metrics(train_metrics, 'metrics/train_metrics.json')

    print(f"\nЛучшая точность на валидации: {best_val_acc:.2f}%")

    return model, best_val_acc


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Обучение классификатора лебедей')
    parser.add_argument(
        '--config',
        type=str,
        default='params.yaml',
        help='Путь к файлу конфигурации'
    )

    args = parser.parse_args()
    main(args.config)
