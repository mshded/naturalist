# Experiment: 25.01.2026_0844_mobilenet_v2_fix

## Date and time: 25.01.2026 0844

## Configuration:

augmentation:
  use_strong_aug: true 
  magnitude: 7
  special_classes:
    black_necked_swan:
      saturation_range: [0.5, 1.5] 
      brightness_range: [0.7, 1.3]
    american_swan:
      random_perspective: true 
      distortion_scale: 0.2  
  brightness_range: [0.7, 1.3]
  saturation_range: [0.8, 1.2]
  hue_range: [-0.1, 0.1]
  rotation_degrees: 20
data:
  batch_size: 32
  img_size: 256
  num_classes: 6
loss:
  label_smoothing: 0.1
  use_focal_loss: true
  focal_gamma: 1.5
  focal_alpha: [1.2, 1.8, 1.0, 1.3, 0.8, 1.2]
model:
  name: mobilenet_v2
  from_huggingface: false
  freeze_backbone: True
  dropout_rate: 0.4
optimizer:
  name: AdamW
  weight_decay: 0.01
scheduler:
  T_max: 80
  name: CosineAnnealingLR
training:
  epochs: 120
  gradient_clip: 1.0
  lr: 0.0006
  unfreeze_epoch: 8
  patience: 25
  min_epochs: 15


## Metrics:

{
    "test_accuracy": 51.111111111111114,
    "test_top2_accuracy": 73.33333399560716,
    "test_loss": 1.4626892805099487,
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