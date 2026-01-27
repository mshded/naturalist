import torch
import yaml
import json
import argparse
from pathlib import Path
import sys
import os

sys.path.append(str(Path(__file__).parent))

from data import get_dataloaders
from models import SwanClassifier
from utils import validate, plot_confusion_matrix, save_metrics
import torch.nn as nn

def evaluate_model(model_path, config_path='params.yaml'):
    with open(config_path, 'r') as f:
        params = yaml.safe_load(f)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    os.makedirs('metrics', exist_ok=True)
    os.makedirs('plots', exist_ok=True)
    
    # loading model
    checkpoint = torch.load(model_path, map_location=device)

    model = SwanClassifier(
        num_classes=params['data']['num_classes'],
        dropout_rate=params['model']['dropout_rate'],
        freeze_backbone=True, # backbone не обучается при оценке
        model_name='efficientnet_b0'   
    )
    model.load_state_dict(checkpoint['model_state_dict']) # загружаем сохраненные веса
    model = model.to(device)
    model.eval()
    
    _, _, test_loader, species_names = get_dataloaders(params)
    
    criterion = nn.CrossEntropyLoss()
    
    print("Оценка модели на тестовом наборе")
    test_loss, test_acc, test_top2_acc, all_preds, all_labels = validate(model, test_loader, criterion, device, top_k=2)

    print(f"Обычная точность: {test_acc:.2f}%")
    print(f"Top-2 точность: {test_top2_acc:.2f}%")
    print(f"Потери: {test_loss:.4f}")
    
    # metrics
    test_metrics = {
        'test_accuracy': float(test_acc),
        'test_top2_accuracy': float(test_top2_acc),
        'test_loss': float(test_loss),
        'model_name': 'efficientnet_b0',
        'species_names': species_names
    }

    
    os.makedirs('metrics', exist_ok=True)
    save_metrics(test_metrics, 'metrics/test_metrics.json')
    
    # confusion matrix
    os.makedirs('plots', exist_ok=True)
    cm = plot_confusion_matrix(all_labels, all_preds, species_names, 
                              save_path='plots/confusion_matrix.png')
    
    # детальная оценка
    from sklearn.metrics import classification_report
    report = classification_report(all_labels, all_preds, 
                                  target_names=species_names, 
                                  output_dict=True)
    
    with open('metrics/evaluation.json', 'w') as f:
        json.dump({
            'test_metrics': test_metrics,
            'classification_report': report
        }, f, indent=4)
    
    return test_acc

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Оценка модели классификатора лебедей')
    parser.add_argument('--model', type=str, required=True, 
                       help='Путь к обученной модели')
    parser.add_argument('--config', type=str, default='params.yaml',
                       help='Путь к файлу конфигурации')
    
    args = parser.parse_args()
    evaluate_model(args.model, args.config)