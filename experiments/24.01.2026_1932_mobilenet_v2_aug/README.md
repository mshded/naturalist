# Experiment: 24.01.2026_1932_mobilenet_v2_aug

## Date and time: 24.01.2026 1932

## Configuration:

augmentation:
  use_strong_aug: true 
  magnitude: 7
data:
  batch_size: 8
  img_size: 224
  num_classes: 6
loss:
  label_smoothing: 0.1
model:
  name: mobilenet_v2
  from_huggingface: false
  freeze_backbone: True
  dropout_rate: 0.3
optimizer:
  name: AdamW
  weight_decay: 0.02
scheduler:
  T_max: 80
  name: CosineAnnealingLR
training:
  epochs: 70
  gradient_clip: 1.0
  lr: 0.0006
  unfreeze_epoch: 6
  patience: 12
  min_epochs: 20


## Metrics:

{
    "test_accuracy": 55.55555555555556,
    "test_top2_accuracy": 73.33333333333333,
    "test_loss": 1.2650099893411,
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