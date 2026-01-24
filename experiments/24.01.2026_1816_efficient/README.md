# Experiment: 24.01.2026_1816_efficient

## Date and time: 24.01.2026 1816

## Configuration:

augmentation:
  magnitude: 7
  num_ops: 2
  use_randaugment: false
data:
  batch_size: 16
  img_size: 224
  num_classes: 6
loss:
  label_smoothing: 0.1
model:
  name: efficientnet_b0
  from_huggingface: false
  freeze_backbone: True
  dropout_rate: 0.3
optimizer:
  name: AdamW
  weight_decay: 0.05
scheduler:
  T_max: 80
  name: CosineAnnealingLR
training:
  epochs: 50
  gradient_clip: 1.0
  lr: 0.0005
  unfreeze_epoch: 5
  patience: 10
  min_epochs: 15


## Metrics:

{
    "test_accuracy": 55.55555555555556,
    "test_top2_accuracy": 62.22222275204129,
    "test_loss": 1.384459137916565,
    "model_name": "efficientnet_b0",
    "species_names": [
        "american_swan",
        "black_necked_swan",
        "black_swan",
        "mute_swan",
        "trumpeter_swan",
        "whooper_swan"
    ]
}