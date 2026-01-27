# Experiment: 26.01.2026_1242_efficient_exp8

## Date and time: 26.01.2026 1242

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
  focus_saturation: false
  focus_contrast: false

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
    "test_accuracy": 55.55555555555556,
    "test_top2_accuracy": 77.77777777777777,
    "test_loss": 1.5364426374435425,
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