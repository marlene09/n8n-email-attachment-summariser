from pdf2image import convert_from_path
import pytesseract
import ollama

# Convert PDF pages to images
pages = convert_from_path("/Users/marlenepostop/Documents/n8n-agent/data/Weekly Newsletter - 24 October 2025 (2).pdf")

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


def summarize_text(text):
    prompt = f"""
    From all pages, extract only the information relevant to the nursery year and the lunch menu for the week from the following text:

    {text}
    """
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response.message.content


summary = summarize_text(text)
with open("summary.txt", "w", encoding="utf-8") as f:
    f.write(summary)
print("Summarization complete!")