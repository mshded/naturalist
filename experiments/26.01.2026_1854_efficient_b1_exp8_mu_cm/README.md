# Experiment: 26.01.2026_1854_efficient_b1_exp8_mu_cm

## Date and time: 26.01.2026 1854

## Configuration:

data:
  batch_size: 8
  img_size: 240
  num_classes: 6

model:
  name: "efficientnet_b1"
  dropout_rate: 0.25
  freeze_backbone: true

augmentation:
  brightness_range: [0.9, 1.1]
  contrast_range: [0.9, 1.1]
  saturation_range: [0.9, 1.1]
  hue_range: [-0.03, 0.03]
  rotation_degrees: 15
  horizontal_flip: true
  vertical_flip: false
  mixup_alpha: 0.2
  cutmix_alpha: 0.0
  apply_mixup_cutmix_prob: 0.3

loss:
  use_focal_loss: false
  label_smoothing: 0.05

training:
  lr: 0.0002
  epochs: 90
  gradient_clip: 1.0
  unfreeze_epoch: 10
  patience: 15
  min_epochs: 40

optimizer:
  name: "AdamW"
  weight_decay: 0.01

scheduler:
  name: "ReduceLROnPlateau"
  mode: "max"
  factor: 0.5
  patience: 8
  min_lr: 0.000001

## Metrics:

{
    "test_accuracy": 51.111111111111114,
    "test_top2_accuracy": 66.6666669315762,
    "test_loss": 1.3917515873908997,
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