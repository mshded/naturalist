import streamlit as st
import torch
import json
from PIL import Image
from torchvision import transforms
from pathlib import Path
import sys
import os

BASE_DIR = Path(__file__).parent 

src_path = BASE_DIR / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from models import SwanClassifier  

st.set_page_config(
    page_title="Swan Species Classifier",
    layout="centered"
)

device = torch.device("cpu")
with open(BASE_DIR / "data" / "swan_species.json", "r", encoding="utf-8") as f: classes = json.load(f)

species_keys = list(classes.keys())

@st.cache_resource
def load_model():
    model = SwanClassifier(
        num_classes=len(species_keys),
        dropout_rate=0.3,
        freeze_backbone=False,
        model_name='efficientnet_b0'
    )
    checkpoint = torch.load(BASE_DIR / "models" / "best_model.pth", map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()
    return model

model = load_model()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

st.title("Swan Species Classifier")
st.write("Upload a photo of a swan and get its species")

language = st.selectbox(
    "Choose language / Выберите язык",
    ["Latin", "English", "Русский"]
)

uploaded_file = st.file_uploader(
    "Upload image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    if model is None:
        st.error("Model not loaded. Please check if best_model.pth exists in models/ folder.")
    else:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded image", use_container_width=True)

        x = transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            logits = model(x)
            probs = torch.softmax(logits, dim=1)
            top_probs, top_idxs = torch.topk(probs, k=2, dim=1)

        st.markdown("---")
        st.subheader("Prediction (Top-2)")

        for rank in range(2):
            idx = top_idxs[0, rank].item()
            prob = top_probs[0, rank].item()

            key = species_keys[idx]
            species = classes[key]

            if language == "Latin":
                name = species["latin_name"]
            elif language == "English":
                name = species["common_name_en"]
            else:
                name = species["common_name_ru"]

            st.markdown(
                f"**{rank + 1}. {name}**  \n"
                f"Confidence: **{prob:.2%}**"
            )
