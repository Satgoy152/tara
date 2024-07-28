from langchain_community.document_loaders import PyPDFLoader

#loading pdf
pdf_loader = PyPDFLoader("rag_data/*.pdf")
pages = pdf_loader.load()