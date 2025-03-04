import os
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image, ImageEnhance
import cv2
import numpy as np

# ✅ Set Hugging Face cache directory
os.environ["HF_HOME"] = "E:/huggingface_cache"
os.environ["TRANSFORMERS_CACHE"] = "E:/huggingface_cache"

# ✅ Load improved TrOCR model (LARGE model for better accuracy)
MODEL_NAME = "microsoft/trocr-large-handwritten"
processor = TrOCRProcessor.from_pretrained(MODEL_NAME)
model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME)

# ✅ Move model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

if device == "cuda":
    model.half()  # Use FP16 for faster inference

def preprocess_image(image_path):
    """Preprocess image: denoise, enhance, and convert to RGB."""
    image_path = os.path.abspath(image_path)

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ Image not found: {image_path}")

    # ✅ Load Image
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"❌ Failed to read image: {image_path}")

    # ✅ Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ✅ Remove noise using Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # ✅ Adaptive Thresholding for better contrast
    binary = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # ✅ Convert to PIL Image & Enhance
    pil_image = Image.fromarray(binary).convert("RGB")

    # ✅ Increase contrast & sharpness
    contrast_enhancer = ImageEnhance.Contrast(pil_image)
    pil_image = contrast_enhancer.enhance(2)  # Increase contrast

    sharpness_enhancer = ImageEnhance.Sharpness(pil_image)
    pil_image = sharpness_enhancer.enhance(2)  # Increase sharpness

    # ✅ Resize for better OCR results
    pil_image = pil_image.resize((1024, 1024))

    return pil_image

def extract_text(image_path):
    """Extract handwritten text from an image using TrOCR."""
    try:
        # ✅ Preprocess Image
        image = preprocess_image(image_path)

        # ✅ Convert to tensor & move to device
        pixel_values = processor(image, return_tensors="pt").pixel_values.to(device)

        # ✅ Run inference
        with torch.no_grad():
            generated_ids = model.generate(pixel_values)
            text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        print("\n🔍 Extracted Text:", text)
        return text

    except Exception as e:
        print(f"❌ Error in OCR processing: {e}")
        return None

if __name__ == "__main__":
    # ✅ Sample Image Path
    sample_image = r"E:\Minor2\prescription_reader\data\1.jpg"

    try:
        extracted_text = extract_text(sample_image)
        if extracted_text:
            print("\n✅ Final Extracted Text:", extracted_text)
        else:
            print("⚠️ No text extracted.")
    except Exception as e:
        print(f"❌ Critical Error: {e}")
