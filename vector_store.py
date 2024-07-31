from langchain_chroma import Chroma
from langchain_voyageai import VoyageAIEmbeddings
import dotenv
import os

# load VoyageAI key
dotenv.load_dotenv()

class VectorStore:
    def __init__(self) -> None:
        self.embeddings = VoyageAIEmbeddings(dotenv.get_key("VOYAGEAI_KEY"), model="voyage-2")

        

    def embed_text(self, text: str) -> list:
        return self.embeddings.embed_text(text)

    def run(self, embeddings: list) -> list:
        return self.chroma.run(embeddings)