# Experiment: 25.01.2026_1229_mobilenet_v2_analized

## Date and time: 25.01.2026 1229

## Configuration:

data:
  batch_size: 16
  img_size: 224
  num_classes: 6

model:
  name: "mobilenet_v2"
  dropout_rate: 0.4
  freeze_backbone: true

augmentation:
  brightness_range: [0.7, 1.3]   
  contrast_range: [0.8, 1.2]      
  saturation_range: [0.8, 1.2]  
  hue_range: [-0.1, 0.1]         
  rotation_degrees: 20            

loss:
  label_smoothing: 0.1
  use_focal_loss: true
  focal_gamma: 1.5
  focal_alpha: [1.2, 1.8, 1.0, 1.3, 0.8, 1.2]

optimizer:
  name: "AdamW"
  weight_decay: 0.01

training:
  epochs: 100
  lr: 0.001
  gradient_clip: 1.0
  unfreeze_epoch: 8
  patience: 25
  min_epochs: 15

scheduler:
  name: "CosineAnnealingLR"
  T_max: 100
## Metrics:

{
    "test_accuracy": 60.0,
    "test_top2_accuracy": 71.11111164093018,
    "test_loss": 1.4874895016352336,
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