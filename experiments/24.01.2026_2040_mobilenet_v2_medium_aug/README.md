# Experiment: 24.01.2026_2040_mobilenet_v2_medium_aug

## Date and time: 24.01.2026 2040

## Configuration:

augmentation:
  use_targeted_aug: true 
  magnitude: 7
data:
  batch_size: 8
  img_size: 224
  num_classes: 6
loss:
  label_smoothing: 0.1
  use_focal_loss: true
  focal_gamma: 2.0
  focal_alpha: [0.7, 0.5, 0.3, 0.7, 0.3, 0.7]
model:
  name: mobilenet_v2
  from_huggingface: false
  freeze_backbone: True
  dropout_rate: 0.2
optimizer:
  name: AdamW
  weight_decay: 0.01
scheduler:
  T_max: 80
  name: CosineAnnealingLR
training:
  epochs: 80
  gradient_clip: 1.0
  lr: 0.0008
  unfreeze_epoch: 2
  patience: 10
  min_epochs: 15


## Metrics:

{
    "test_accuracy": 53.333333333333336,
    "test_top2_accuracy": 73.3333334657881,
    "test_loss": 1.2704322238763173,
    "model_name": "mobilenet_v2",
    "species_names": [
        "american_swan",
        "black_necked_swan",
        "black_swan",
        "mute_swan",
        "trumpeter_swan",
        "whooper_swan"
    ]
}