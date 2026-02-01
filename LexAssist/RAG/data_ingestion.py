from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

#data loading

DATA_DIR = "data"

loader = DirectoryLoader(
    path=DATA_DIR,
    glob="**/*.pdf",
    loader_cls=PyMuPDFLoader
)

documents = loader.load()

print(f"Loaded {len(documents)} pages from PDFs")

#Splitting into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=250,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print(f"Created {len(chunks)} text chunks")

#embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

#creating FAISS vector store
vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local("legal_faiss_db")

print("FAISS vector store saved successfully")
