# Experiment: 27.01.2026_0816_efficient_b0_best

## Date and time: 27.01.2026 0816

## Configuration:

data:
  batch_size: 8
  img_size: 224
  num_classes: 6

model:
  name: "efficientnet_b0"
  dropout_rate: 0.25
  freeze_backbone: false

augmentation:
  brightness_range: [0.85, 1.15]
  contrast_range: [0.9, 1.1]
  saturation_range: [0.9, 1.1]
  hue_range: [-0.05, 0.05]
  rotation_degrees: 10
  horizontal_flip: true
  vertical_flip: false

  mixup_alpha: 0.0
  cutmix_alpha: 0.0
  apply_mixup_cutmix_prob: 0.0

loss:
  use_focal_loss: false
  label_smoothing: 0.05

training:
  lr: 0.0003
  epochs: 90
  gradient_clip: 1.0
  unfreeze_epoch: null   
  patience: 20
  min_epochs: 50

optimizer:
  name: "AdamW"
  weight_decay: 0.01

scheduler:
  name: "ReduceLROnPlateau"
  mode: "max"
  factor: 0.5
  patience: 10
  min_lr: 0.000001

## Metrics:

{
    "test_accuracy": 51.111111111111114,
    "test_top2_accuracy": 68.88888902134366,
    "test_loss": 1.6151160995165508,
    "model_name": "efficientnet_b0",
    "species_names": [
        "mute_swan",
        "black_swan",
        "whooper_swan",
        "black_necked_swan",
        "trumpeter_swan",
        "american_swan"
    ]
}