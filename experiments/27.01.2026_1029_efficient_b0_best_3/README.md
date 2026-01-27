# Experiment: 27.01.2026_1029_efficient_b0_best_3

## Date and time: 27.01.2026 1029

## Configuration:

data:
  batch_size: 8
  img_size: 224
  num_classes: 6

model:
  name: "efficientnet_b0"
  dropout_rate: 0.3
  freeze_backbone: true

augmentation:
  brightness_range: [0.85, 1.15]
  contrast_range: [0.9, 1.1]
  saturation_range: [0.9, 1.1]
  hue_range: [-0.05, 0.05]
  rotation_degrees: 10
  horizontal_flip: false
  vertical_flip: false

  mixup_alpha: 0.0
  cutmix_alpha: 0.0
  apply_mixup_cutmix_prob: 0.0

loss:
  use_focal_loss: true
  focal_gamma: 1.5
  focal_alpha: null
  label_smoothing: 0.0

training:
  lr: 0.0003
  epochs: 120
  gradient_clip: 1.0
  unfreeze_epoch: 15
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
    "test_accuracy": 46.666666666666664,
    "test_top2_accuracy": 64.44444457689922,
    "test_loss": 1.652255117893219,
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