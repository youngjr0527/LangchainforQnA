#pip install unstructured  (공식문서에서는 !pip install unstructured > /dev/null 를 하라고 한다.)
#pip install markdown
from dotenv import load_dotenv
load_dotenv()
from langchain.document_loaders import UnstructuredMarkdownLoader 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

class QARetrieval:
    def __init__(self, db_path):  # model_name도 인자로 받기
        self.db_path = db_path
        self.embedding_function = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    def ingest_documents(self, md_path=False): # Markdown 뿐만 아니라 pdf, docx 등 다양한 형식의 문서를 지원하도록 수정해야 함
        logging.info(f"Ingesting documents from {md_path if md_path else 'all markdown files'}")
        try:
            if md_path:
                ps = Path(md_path)
                if not ps.exists():
                    logging.warning(f"The path {md_path} does not exist.")
                    return None
            else:
                ps = list(Path('.').glob("**/*.md"))
                if not ps:
                    logging.warning("No markdown files found.")
                    return None
        except Exception as e:
            logging.error(f"An error occurred while accessing the path: {e}")
            return
        for p in ps:
            logging.info(f"Processing file: {p}")
            loader = UnstructuredMarkdownLoader(str(p))
            pages = loader.load_and_split()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=300,
                chunk_overlap=20,
                length_function=len,
                is_separator_regex=False,
            )
            texts = text_splitter.split_documents(pages)

            Chroma.from_documents(texts, self.embedding_function, persist_directory=self.db_path)

    def generate_answer(self, question):
        logging.info(f"Generating answer for question: {question}")
        db_from_disk = Chroma(persist_directory=self.db_path, embedding_function=self.embedding_function)
        qa_chain = RetrievalQA.from_chain_type(self.llm, retriever=db_from_disk.as_retriever())
        result = qa_chain({"query": question})
        return result['result']


if __name__ == "__main__":
    qa_system = QARetrieval(db_path="./chroma_db")
    qa_system.ingest_documents()

    question = "시립대에는 편의 시설 뭐 있어?"
    result = qa_system.generate_answer(question=question)
    print(result)
