# Experiment: 26.01.2026_1528_efficient_v1_exp1

## Date and time: 26.01.2026 1528

## Configuration:

data:
  batch_size: 8
  img_size: 240     
  num_classes: 6

model:
  name: "efficientnet_b1"
  dropout_rate: 0.45  
  freeze_backbone: true  

augmentation:
  brightness_range: [0.85, 1.15]
  contrast_range: [0.85, 1.15]
  saturation_range: [0.85, 1.15]
  hue_range: [-0.05, 0.05]
  rotation_degrees: 15
  horizontal_flip: true
  focus_saturation: false
  focus_contrast: false

loss:
  use_focal_loss: true
  focal_gamma: 1.5
  focal_alpha: [1.0, 2.0, 1.0, 3.0, 1.0, 1.0] 
  label_smoothing: 0.0

training:
  lr: 0.0002
  epochs: 90
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
    "test_accuracy": 57.77777777777778,
    "test_top2_accuracy": 77.77777804268732,
    "test_loss": 1.1962999006112416,
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