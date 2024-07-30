from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class Chunker:
    def __init__(self, load_data: bool = False) -> list:
        if load_data:
            #loading pdfs
            print("Loading PDFs")
            print("Course description...", end="\r", flush=True)
            pdf_loader = PyPDFLoader("rag_data/Umich_FA2024_course_description.pdf")
            course_description_text = pdf_loader.load()
            print("Loaded course description")
            print("Degree requirements...", end="\r", flush=True)
            pdf_loader = PyPDFLoader("rag_data/Umich_FA2024_LSA_degree_requ.pdf")
            degree_requirements_text = pdf_loader.load()
            print("Loaded degree requirements")
            print("Major minor description...", end="\r", flush=True)
            pdf_loader = PyPDFLoader("rag_data/Umich_FA2024_major_minor_description.pdf")
            major_minor_description_text = pdf_loader.load()
            print("Loaded major minor description")

            print("Subject mapping...", end="\r", flush=True)
            pdf_loader = PyPDFLoader("rag_data/Umich_FA2024_subject_mapping.pdf")
            subject_mapping_text = pdf_loader.load()
            print("Loaded subject mapping")

            pages = [course_description_text, degree_requirements_text, major_minor_description_text, subject_mapping_text]
            chunked_pages = self.recursive_chunk(pages)
            print("Chunked pages")
            return chunked_pages

    @staticmethod
    def recursive_chunk(pages: list, chunk_size: int = 1000, chunk_overlap: int = 200, delimiters: list[str] = None) -> list:
        """
        Arguments:
            pages: list of strings, each string is a page of text
            delimiters: list of strings, each string is a delimiter to split the text by
        """
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        chunked_pages = []
        for page in pages:
            chunks = text_splitter.split_documents(page)
            chunked_pages.append(chunks)

        return chunked_pages


