import torch
import torch.nn as nn
from torchvision import models
import timm

class SwanClassifier(nn.Module):
    def __init__(self, num_classes=6, dropout_rate=0.3, freeze_backbone=False, model_name='efficientnet_b0'):
        super().__init__()
        self.model_name = model_name
        self.backbone = timm.create_model(model_name, pretrained=True, num_classes=num_classes)

        if freeze_backbone:
            for param in self.backbone.parameters():
                param.requires_grad = False
            
        in_features = self.backbone.classifier.in_features
        
        self.backbone.classifier = nn.Sequential(
            nn.Dropout(dropout_rate),
            nn.Linear(in_features, 512),
            nn.ReLU(),
            nn.BatchNorm1d(512),
            nn.Dropout(dropout_rate/2),
            nn.Linear(512, num_classes)
        )

    
    def forward(self, x):
        return self.backbone(x)
    
    def unfreeze_backbone(self, unfreeze_all=False, n_last_layers=3):
        if unfreeze_all:
            for param in self.backbone.parameters():
                param.requires_grad = True
        else:
            # Размораживаем n_last_layers параметров backbone
            backbone_params = list(self.backbone.parameters())
            for param in backbone_params[-n_last_layers:]:
                param.requires_grad = True


    
    def freeze_backbone(self):
        # Замораживаем все параметры backbone
        for param in self.backbone.parameters():
            param.requires_grad = False
        
        # Размораживаем классификатор
        if self.model_name == 'efficientnet_b0':
                if hasattr(self.backbone, 'classifier'):
                    for param in self.backbone.classifier.parameters():
                        param.requires_grad = True

