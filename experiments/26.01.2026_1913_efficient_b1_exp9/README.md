# Experiment: 26.01.2026_1913_efficient_b1_exp9

## Date and time: 26.01.2026 1913

## Configuration:

data:
  batch_size: 8
  img_size: 240
  num_classes: 6

model:
  name: "efficientnet_b1"
  dropout_rate: 0.2
  freeze_backbone: true

augmentation:
  brightness_range: [0.9, 1.1]
  contrast_range: [0.9, 1.1]
  saturation_range: [0.9, 1.1]
  hue_range: [-0.03, 0.03]
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
  lr: 0.0002
  epochs: 80
  gradient_clip: 1.0
  unfreeze_epoch: 3
  patience: 12
  min_epochs: 30

optimizer:
  name: "AdamW"
  weight_decay: 0.01

scheduler:
  name: "ReduceLROnPlateau"
  mode: "max"
  factor: 0.5
  patience: 6
  min_lr: 0.000001

## Metrics:

{
    "test_accuracy": 51.111111111111114,
    "test_top2_accuracy": 62.22222228844961,
    "test_loss": 1.5432244340578716,
    "model_name": "efficientnet_b1",
    "species_names": [
        "mute_swan",
        "black_swan",
        "whooper_swan",
        "black_necked_swan",
        "trumpeter_swan",
        "american_swan"
    ]
}