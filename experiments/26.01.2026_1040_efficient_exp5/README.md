# Experiment: 26.01.2026_1040_efficient_exp5

## Date and time: 26.01.2026 1040

## Configuration:

data:
  batch_size: 4
  img_size: 224
  num_classes: 6

model:
  name: "efficientnet_b0"
  dropout_rate: 0.3
  freeze_backbone: false

augmentation:
  brightness_range: [0.85, 1.15]
  contrast_range: [0.9, 1.1]
  saturation_range: [0.9, 1.1]
  hue_range: [-0.05, 0.05]
  rotation_degrees: 10
  focus_saturation: false
  focus_contrast: false

loss:
  use_focal_loss: false
  focal_gamma: 2.0
  focal_alpha: [1.0, 2.5, 1.0, 3.0, 1.0, 1.0]
  label_smoothing: 0.05

training:
  lr: 0.0003
  epochs: 120
  gradient_clip: 1.0
  unfreeze_epoch: 5
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
    "test_accuracy": 53.333333333333336,
    "test_top2_accuracy": 71.11111111111111,
    "test_loss": 1.7519527015586693,
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