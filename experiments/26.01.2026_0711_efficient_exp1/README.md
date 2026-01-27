# Experiment: 26.01.2026_0711_efficient_exp1

## Date and time: 26.01.2026 0711

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
  focus_saturation: false
  focus_contrast: false

loss:
  use_focal_loss: true
  focal_gamma: 2.0
  focal_alpha: [1.0, 2.5, 1.0, 1.0, 1.0, 1.0]

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
    "test_accuracy": 62.22222222222222,
    "test_top2_accuracy": 77.77777791023254,
    "test_loss": 1.531052440404892,
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