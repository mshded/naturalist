# Experiment: 27.01.2026_0946_efficient_b0_best_2

## Date and time: 27.01.2026 0946

## Configuration:

data:
  batch_size: 8
  img_size: 224
  num_classes: 6

model:
  name: "efficientnet_b0"
  dropout_rate: 0.4
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
  focal_gamma: 2.0
  focal_alpha: [1.0, 2.5, 1.0, 1.0, 1.0, 1.0]
  label_smoothing: 0.0

training:
  lr: 0.0005
  epochs: 160
  gradient_clip: 1.0
  unfreeze_epoch: 30
  patience: 35
  min_epochs: 50

optimizer:
  name: "AdamW"
  weight_decay: 0.005

scheduler:
  name: "ReduceLROnPlateau"
  mode: "max"
  factor: 0.5
  patience: 10
  min_lr: 0.000001


## Metrics:

{
    "test_accuracy": 51.111111111111114,
    "test_top2_accuracy": 64.44444470935397,
    "test_loss": 1.4258048236370087,
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