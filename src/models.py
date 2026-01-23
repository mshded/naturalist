import torch
import torch.nn as nn
from torchvision import models
import timm

class SwanClassifier(nn.Module):
    def __init__(self, num_classes=6, model_name='efficientnet_b0', dropout_rate=0.5, freeze_backbone=True):
        super().__init__()
        self.model_name = model_name
        
        if model_name == 'resnet18':
            self.backbone = models.resnet18(pretrained=True) # загружаем веса, обученные на ImageNet
            if freeze_backbone:
                for param in self.backbone.parameters():
                    param.requires_grad = False 
            
            in_features = self.backbone.fc.in_features # меняем последний слой под 6 классов
            self.backbone.fc = nn.Sequential(
                nn.Dropout(dropout_rate),
                nn.Linear(in_features, 512),
                nn.ReLU(),
                nn.BatchNorm1d(512),
                nn.Dropout(dropout_rate/2),
                nn.Linear(512, num_classes)
            )
            
        elif model_name == 'mobilenet_v2':
            self.backbone = models.mobilenet_v2(pretrained=True)
            if freeze_backbone:
                for param in self.backbone.parameters():
                    param.requires_grad = False
            
            in_features = self.backbone.classifier[1].in_features
            self.backbone.classifier = nn.Sequential(
                nn.Dropout(dropout_rate),
                nn.Linear(in_features, 512),
                nn.ReLU(),
                nn.BatchNorm1d(512),
                nn.Dropout(dropout_rate/2),
                nn.Linear(512, num_classes)
            )
            
        elif model_name == 'efficientnet_b0':
            self.backbone = models.efficientnet_b0(pretrained=True)
            if freeze_backbone:
                for param in self.backbone.parameters():
                    param.requires_grad = False
            
            in_features = self.backbone.classifier[1].in_features
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
    
    def unfreeze_backbone(self, unfreeze_all=False):
        
        if self.model_name == 'resnet18':
            if unfreeze_all:
                for param in self.backbone.parameters():
                    param.requires_grad = True
            else:
                for param in self.backbone.layer4.parameters():
                    param.requires_grad = True
                for param in self.backbone.layer3.parameters():
                    param.requires_grad = True
        
        elif self.model_name in ['mobilenet_v2', 'efficientnet_b0']:
            for param in self.backbone.parameters():
                param.requires_grad = True
        
        elif hasattr(self, 'classifier'):
            for param in self.backbone.parameters():
                param.requires_grad = True
    
    def freeze_backbone(self):
        for param in self.backbone.parameters():
            param.requires_grad = False
        
        # Классификатор всегда остается размороженным
        if self.model_name == 'resnet18':
            for param in self.backbone.fc.parameters():
                param.requires_grad = True
        elif hasattr(self, 'classifier'):
            for param in self.classifier.parameters():
                param.requires_grad = True
        else:
            for param in self.backbone.classifier.parameters():
                param.requires_grad = True