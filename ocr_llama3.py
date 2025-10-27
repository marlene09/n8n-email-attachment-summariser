import os
import time
import psutil
from PIL import Image, ImageSequence
import pytesseract
import ollama
from concurrent.futures import ThreadPoolExecutor

# --- CONFIG ---
IMAGE_PATH = "/Users/marlenepostop/Documents/n8n-agent/data/Weekly Newsletter - 24 October 2025.png"
TEXT_DIR = "/Users/marlenepostop/Documents/n8n-agent/outputs/pdf_text"
SUMMARY_DIR = "/Users/marlenepostop/Documents/n8n-agent/outputs/pdf_summary"
MODEL_NAME = "llama3"

os.makedirs(TEXT_DIR, exist_ok=True)
os.makedirs(SUMMARY_DIR, exist_ok=True)

# --- OCR FUNCTION ---
from PIL import Image, ImageSequence
import io

def ocr_single_frame_bytes(frame_bytes, page_num):
    """OCR a single frame from bytes and save text."""
    frame = Image.open(io.BytesIO(frame_bytes)).convert("RGB")
    text = pytesseract.image_to_string(frame)
    txt_path = os.path.join(TEXT_DIR, f"page_{page_num}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    return page_num, text

def ocr_image_parallel(image_path):
    start_time = time.time()
    img = Image.open(image_path)
    frames = []

    # Convert each frame to bytes first
    for i, frame in enumerate(ImageSequence.Iterator(img), start=1):
        b = io.BytesIO()
        frame.save(b, format="PNG")  # Save as PNG in memory
        frames.append((b.getvalue(), i))

    # Use ThreadPoolExecutor safely
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        ocr_texts = list(executor.map(lambda args: ocr_single_frame_bytes(*args), frames))

    end_time = time.time()
    print(f"Total OCR time: {end_time - start_time:.2f} seconds")
    return ocr_texts

# --- SUMMARIZATION FUNCTION ---
def summarize_nursery_and_menu(text):
    """Send all text to Ollama LLM and get summary."""
    start_time = time.time()
    
    prompt = f"""
    From all pages, extract only the information relevant to the nursery year and the lunch menu for the week from the following text:

    {text}

    Provide a concise summary with clear headings for Nursery Year and Lunch Menu.
    """
    
    # Monitor CPU before inference
    cpu_before = psutil.cpu_percent(interval=None)
    
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    
    cpu_after = psutil.cpu_percent(interval=None)
    end_time = time.time()
    
    print(f"Summarization done in {end_time - start_time:.2f} seconds")
    print(f"CPU usage during inference: {cpu_after - cpu_before:.2f}%")
    
    return response.message.content

# --- MAIN WORKFLOW ---
overall_start = time.time()

# 1️⃣ OCR all pages
ocr_texts = ocr_image_parallel(IMAGE_PATH)

# 2️⃣ Combine text for a single summary
all_text = "\n".join([text for _, text in ocr_texts])

# 3️⃣ Summarize with Ollama (single call)
overall_summary = summarize_nursery_and_menu(all_text)

# 4️⃣ Save overall summary
overall_summary_path = os.path.join(SUMMARY_DIR, "overall_summary.txt")
with open(overall_summary_path, "w", encoding="utf-8") as f:
    f.write(overall_summary)
print("Saved overall summary")

overall_end = time.time()
print(f"Total script time: {overall_end - overall_start:.2f} seconds")
