from pypdf import PdfReader
from pdf2markdown4llm import PDF2Markdown4LLM


def extract_text_fromaudit(uploaded_file)->str:
    """
    Extract text from uploaded degree audit
    """
    
    # Initialize converter
    converter = PDF2Markdown4LLM(remove_headers=False, skip_empty_tables=True, table_header="### Table")


    # Convert PDF to Markdown
    markdown_content = converter.convert(uploaded_file)

    concat_text = markdown_content.replace(" * ", "[IN PROGRESS]")

    return concat_text