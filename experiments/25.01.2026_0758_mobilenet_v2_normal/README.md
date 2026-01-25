# Experiment: 25.01.2026_0758_mobilenet_v2_normal

## Date and time: 25.01.2026 0758

## Configuration:

augmentation:
  use_strong_aug: false
  magnitude: 7
  brightness_range: [0.7, 1.3]    
  contrast_range: [0.8, 1.2]
  saturation_range: [0.8, 1.2]
  hue_range: [-0.1, 0.1]          
  rotation_degrees: 20
data:
  batch_size: 16
  img_size: 224
  num_classes: 6
loss:
  label_smoothing: 0.1
  use_focal_loss: false
model:
  name: mobilenet_v2
  from_huggingface: false
  freeze_backbone: True
  dropout_rate: 0.3
optimizer:
  name: AdamW
  weight_decay: 0.01
scheduler:
  T_max: 80
  name: CosineAnnealingLR
training:
  epochs: 80
  gradient_clip: 1.0
  lr: 0.001
  unfreeze_epoch: 3
  patience: 20
  min_epochs: 20


## Metrics:

{
    "test_accuracy": 53.333333333333336,
    "test_top2_accuracy": 73.33333373069763,
    "test_loss": 1.467610279719035,
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