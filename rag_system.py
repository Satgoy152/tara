from langchain_voyageai import VoyageAIEmbeddings
import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_anthropic import ChatAnthropic
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from chunking import Chunker

class RAGSystem:
    def __init__(self) -> None:
        self.chunked_files = Chunker(load_data=True)

    def run(self, text: str) -> str:
        chunked_text = self.chunker.chunk_text([text])
        embeddings = self.embedder.embed_text(chunked_text)
        chroma_output = self.chroma.run(embeddings)
        hub_output = self.hub.run(chroma_output)
        output = self.output_parser.parse(hub_output)
        return output

    def run_pdf(self, pdf_path: str) -> str:
        pdf_loader = PyPDFLoader(pdf_path)
        text = pdf_loader.load()
        return self.run(text)

    def chat(self, text: str) -> str:
        return self.chat_anthropic.chat(text)

    def split_text(self, text: str) -> list:
        return self.text_splitter.split_documents(text)

