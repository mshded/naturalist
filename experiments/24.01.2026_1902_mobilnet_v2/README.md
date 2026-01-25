# Experiment: 24.01.2026_1902_mobilnet_v2

## Date and time: 24.01.2026 1902

## Configuration:

augmentation:
  magnitude: 6
  num_ops: 3
  use_randaugment: false
data:
  batch_size: 8
  img_size: 256
  num_classes: 6
loss:
  label_smoothing: 0.15
model:
  name: mobilenet_v2
  from_huggingface: false
  freeze_backbone: True
  dropout_rate: 0.25
optimizer:
  name: AdamW
  weight_decay: 0.01
scheduler:
  T_max: 80
  name: CosineAnnealingLR
training:
  epochs: 60
  gradient_clip: 1.0
  lr: 0.0009
  unfreeze_epoch: 4
  patience: 10
  min_epochs: 15


## Metrics:

{
    "test_accuracy": 60.0,
    "test_top2_accuracy": 77.77777777777777,
    "test_loss": 1.112091213464737,
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