import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import pandas as pd
from PIL import Image
from pathlib import Path
import json


class SwanDataset(Dataset):
    def __init__(self, subset='train', transform=None, data_dir=None):
        self.subset = subset
        self.transform = transform

        if data_dir is None:
            data_dir = 'notebooks/data/processed/swans_dataset'

        self.data_dir = Path(data_dir) / subset

        metadata_path = Path(data_dir) / f'{subset}_metadata.csv'
        self.metadata = pd.read_csv(metadata_path, encoding='utf-8')

        # загрузка информации о видах
        info_path = Path(data_dir) / 'dataset_info.json'
        with open(info_path, 'r', encoding='utf-8') as f:
            dataset_info = json.load(f)

        self.species_names = sorted(dataset_info['species_info'].keys())
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
        transform = transforms.Compose([
            transforms.Resize((img_size + 32, img_size + 32)),
            transforms.RandomResizedCrop(img_size, scale=(0.7, 1.0)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.2,contrast=0.2,saturation=0.2),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406],[0.229, 0.224, 0.225])
        ])

        if params['augmentation']['use_randaugment']:
            from torchvision.transforms import autoaugment
            transform.transforms.insert(5,autoaugment.RandAugment(
                    num_ops=params['augmentation']['num_ops'],
                    magnitude=params['augmentation']['magnitude']
                )
            )

    else:
        transform = transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406],[0.229, 0.224, 0.225])
        ])

    return transform


def get_dataloaders(params, data_dir=None):
    if data_dir is None:
        data_dir = 'notebooks/data/processed/swans_dataset'

    train_transform = get_transforms(params, 'train')
    val_transform = get_transforms(params, 'val')
    test_transform = get_transforms(params, 'test')

    train_dataset = SwanDataset('train', train_transform, data_dir)
    val_dataset = SwanDataset('val', val_transform, data_dir)
    test_dataset = SwanDataset('test', test_transform, data_dir)

    batch_size = params['data']['batch_size']

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=2,
        pin_memory=torch.cuda.is_available()
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=2,
        pin_memory=torch.cuda.is_available()
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=2,
        pin_memory=torch.cuda.is_available()
    )

    return train_loader, val_loader, test_loader, train_dataset.species_names
