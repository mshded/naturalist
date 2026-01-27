import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import pandas as pd
from PIL import Image
from pathlib import Path
import json
from collections import Counter


class SwanDataset(Dataset):
    def __init__(self, subset='train', transform=None, data_dir=None):
        self.subset = subset
        self.transform = transform

        if data_dir is None:
            data_dir = 'data/processed/swans_dataset'

        self.data_dir = Path(data_dir) / subset

        metadata_path = Path(data_dir) / f'{subset}_metadata.csv'
        self.metadata = pd.read_csv(metadata_path, encoding='utf-8')

        info_path = Path(data_dir) / 'dataset_info.json'
        with open(info_path, 'r', encoding='utf-8') as f:
            dataset_info = json.load(f)

        self.species_names = list(dataset_info['species_info'].keys())
        self.species_to_idx = {
            cls: idx for idx, cls in enumerate(self.species_names)
        }

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, idx):
        row = self.metadata.iloc[idx]
        img_path = self.data_dir / row['species_key'] / row['filename']

        image = Image.open(img_path).convert('RGB')

        if self.transform:
            image = self.transform(image)

        label = self.species_to_idx[row['species_key']]
        return image, label, str(img_path)


def get_transforms(params, subset='train'):
    img_size = params['data']['img_size']

    if subset == 'train':
        aug = params.get('augmentation', {})

        transforms_list = []

        # Resize / Crop
        if aug.get('random_resized_crop', True):
            transforms_list.extend([
                transforms.Resize((img_size + 32, img_size + 32)),
                transforms.RandomResizedCrop(img_size, scale=(0.6, 1.0),ratio=(0.75,1.33)),
            ])
        else:
            transforms_list.append(
                transforms.Resize((img_size, img_size))
            )

        # ColorJitter
        brightness = max(
            abs(1 - aug.get('brightness_range', [0.85, 1.15])[0]),
            abs(1 - aug.get('brightness_range', [0.85, 1.15])[1])
        )
        contrast = max(
            abs(1 - aug.get('contrast_range', [0.9, 1.1])[0]),
            abs(1 - aug.get('contrast_range', [0.9, 1.1])[1])
        )
        saturation = max(
            abs(1 - aug.get('saturation_range', [0.9, 1.1])[0]),
            abs(1 - aug.get('saturation_range', [0.9, 1.1])[1])
        )
        hue = max(
            abs(aug.get('hue_range', [-0.05, 0.05])[0]),
            abs(aug.get('hue_range', [-0.05, 0.05])[1])
        )

        transforms_list.append(
            transforms.ColorJitter(
                brightness=brightness,
                contrast=contrast,
                saturation=saturation,
                hue=hue
            )
        )

        # Rotation
        if aug.get('rotation_degrees', 0) > 0:
            transforms_list.append(
                transforms.RandomRotation(degrees=aug['rotation_degrees'])
            )

        transforms_list.append(
            transforms.RandomAffine(
                degrees=0,
                translate=(0.1, 0.1),
                scale=(0.9, 1.1)
            )
        )

        transforms_list.extend([
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

        return transforms.Compose(transforms_list)

    else:
        return transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])


def get_dataloaders(params,data_dir=None):
    if data_dir is None:
            data_dir = 'data/processed/swans_dataset'
    data_params = params["data"]
    batch_size = data_params["batch_size"]
    img_size = data_params["img_size"]

    train_transform = get_transforms(params, 'train') 
    val_transform = get_transforms(params, 'val') 
    test_transform = get_transforms(params, 'test')

    train_dataset = SwanDataset('train', train_transform, data_dir) 
    val_dataset = SwanDataset('val', val_transform, data_dir) 
    test_dataset = SwanDataset('test', test_transform, data_dir)

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0,         
        pin_memory=False,
        persistent_workers=False
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
        pin_memory=False
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
        pin_memory=False
    )

    return train_loader, val_loader, test_loader, train_dataset.species_names