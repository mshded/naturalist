# Experiment: 25.01.2026_2008_efficient_exp9

## Date and time: 25.01.2026 2008

## Configuration:

data:
  batch_size: 8
  img_size: 224
  num_classes: 6

model:
  name: "efficientnet_b0"
  dropout_rate: 0.5
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
  focal_alpha: [1.0, 1.2, 1.5, 1.5, 1.0, 1.3]

training:
  lr: 0.0003
  epochs: 160
  gradient_clip: 1.0
  unfreeze_epoch: 40
  patience: 35
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
    "test_accuracy": 57.77777777777778,
    "test_top2_accuracy": 73.33333359824286,
    "test_loss": 1.3041149775187175,
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