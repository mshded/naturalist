# Experiment: 24.01.2026_1836_mobilenet_v2

## Date and time: 24.01.2026 1836

## Configuration:

augmentation:
  magnitude: 5
  num_ops: 2
  use_randaugment: false
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
  dropout_rate: 0.2
optimizer:
  name: AdamW
  weight_decay: 0.01
scheduler:
  T_max: 80
  name: CosineAnnealingLR
training:
  epochs: 50
  gradient_clip: 1.0
  lr: 0.001
  unfreeze_epoch: 3
  patience: 10
  min_epochs: 15


## Metrics:

{
    "test_accuracy": 57.77777777777778,
    "test_top2_accuracy": 80.00000013245477,
    "test_loss": 1.0953943034013112,
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