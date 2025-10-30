#pip install langchain_community langchain pypdf
#ollama serve
#ollama pull llama3


from langchain_community.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

# ====== CONFIG ======
PDF_PATH = "your_file.pdf"
MODEL = "llama3"  # or any model you have locally (phi3, mistral, etc.)

# ====== STEP 1: Load and split PDF ======
print("📘 Loading and splitting PDF...")
loader = PyPDFLoader(PDF_PATH)
pages = loader.load()

# Split into manageable chunks (approx. 2k chars each)
splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
docs = splitter.split_documents(pages)
print(f"✅ Loaded {len(docs)} chunks")

# ====== STEP 2: Set up local Ollama model ======
llm = Ollama(model=MODEL)

# ====== STEP 3: Map-Reduce summarisation ======
print("🧠 Summarising (map-reduce)...")
chain = load_summarize_chain(
    llm,
    chain_type="map_reduce",  # summarises each chunk, then merges results
    map_prompt=None,          # uses sensible defaults
    combine_prompt=None
)

summary = chain.run(docs)

print("\n🧾 FINAL SUMMARY:")
print("------------------")
print(summary.strip())
