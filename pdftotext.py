from pdf2image import convert_from_path
import pytesseract
import ollama

# # handling multiple pdfs in a directory
# for pdf_file in os.listdir("path_to_pdf_directory"):
#     convert_from_path(os.path.join("path_to_pdf_directory", pdf_file))
#     text = ""
#     for i, page in enumerate(pages):
#         page_text = pytesseract.image_to_string(page)
#         text += page_text + "\n"    
#     with open(f"{pdf_file}_output.txt", "w", encoding="utf-8") as f:
#         f.write(text)

    





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