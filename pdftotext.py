from pdf2image import convert_from_path
import pytesseract
import ollama

import time
#make ouputs directory for pdftxt
import os

os.makedirs("./n8n-agent/outputs_pdftotext/pdf_summary", exist_ok= True)

pdf_path = "./pdfs/"
ocr_text_dir = "./n8n-agent/outputs_pdftotext/pdf_text"
os.makedirs(ocr_text_dir, exist_ok=True)

input_dir = "./pdfs"
output_dir = "./output_text/texts/"
os.makedirs(output_dir, exist_ok=True)


def pdf_to_text(pdf_path, output_txt_path):
    """Convert PDF to text using OCR and save to output_txt_path."""
    start_time = time.time()
    pages = convert_from_path(pdf_path, dpi=300)
    ocr_text = ""
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page)
        ocr_text += f"\n--- Page {i + 1} ---\n{text.strip()}\n"
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(ocr_text)
    end_time = time.time()
    print(f"OCR completed in {end_time - start_time:.2f} seconds")    


# pdf_to_text(pdf_path, os.path.join(ocr_text_dir, "pdf_text.txt"))


def pdf_to_text_all(input_dir, output_dir):
    """Convert all PDFs in input_dir to text files in output_dir."""
    for pdf_file in os.listdir(input_dir):
        if pdf_file.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, pdf_file)
            output_path = os.path.join(output_dir, f"{os.path.splitext(pdf_file)[0]}.txt")
            pdf_to_text(pdf_path, output_path)
            print(f"Converted {pdf_file} to text.")


if __name__ == "__main__":
    input_dir = input_dir
    output_dir = output_dir
    pdf_to_text_all(input_dir, output_dir)

    





# Convert PDF pages to images
pages = convert_from_path("./n8n-agent/data/Weekly Newsletter - 24 October 2025 (2).pdf")

text = ""
for i, page in enumerate(pages):
    # Perform OCR on each page
    page_text = pytesseract.image_to_string(page)
    text += page_text + "\n"

# Save the extracted text

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Text extraction complete!")

# Ollama LLM summarization can be done in a similar way as in ocr_llama3.py after extracting the text.

#change prompt
def summarize_text(text):
    prompt = f"""
    You are a parent that reads school newsletters and extracts key information for parents of children attending Nursery.

    You are analysing a school newsletter. Your job is to extract information useful for a parent with a child in Nursery.

    From the text below, identify and summarise:

    1. **Nursery Information**
   - Include all details mentioning Nursery, EYFS, or early years.
   - Include learning themes, activities, class events, assemblies, reminders, or messages from teachers.
   - If the newsletter includes a section that seems related to Nursery but doesn't explicitly say "Nursery", include it too.
   - If information is unclear or partial, summarise what you can instead of saying “no specific news mentioned.”

    2. **Lunch Menu**
   - List the meals for the week, snacks, or any mention of menu weeks.
   - If menu details are missing, mention that explicitly.

    3. **Important Dates and Events**
   - Include any dates, meetings, closures, or celebrations that would affect Nursery children or parents.
   - Include Parents’ Evenings, assemblies, or holiday reminders.

    4. **Reminders for Parents**
    - Note anything parents are asked to bring or do (e.g., coats, donations, photos, labelled clothes).

    Return your answer in this format:

    ### Nursery Updates
    <summary>

    ### Lunch Menu
    <summary>

    ### Key Dates & Events
    <summary>

    ### Parent Reminders
    <summary>

    If a section has no direct details, infer possible related information (for example, if the text mentions “younger children” or “EYFS”, assume relevance to Nursery).
    Avoid saying “no news mentioned”.

    Here is the newsletter text:

    {text}
    """
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response.message.content


summary = summarize_text(text)
with open("summary.txt", "w", encoding="utf-8") as f:
    f.write(summary)
print("Summarization complete!")
