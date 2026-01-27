# Experiment: 26.01.2026_1228_efficient_exp7

## Date and time: 26.01.2026 1228

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
  brightness_range: [0.9, 1.1]
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
  lr: 0.001
  epochs: 30
  gradient_clip: 1.0
  unfreeze_epoch: 25
  patience: 100
  min_epochs: 15

optimizer:
  name: "AdamW"
  weight_decay: 0.005

scheduler:
  name: "CosineAnnealingLR"
  T_max: 30
  eta_min: 0.00001


## Metrics:

{
    "test_accuracy": 46.666666666666664,
    "test_top2_accuracy": 60.000000132454765,
    "test_loss": 1.9383726318677266,
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