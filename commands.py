from langchain_community.document_loaders import PyPDFLoader, ChatGPTLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.vectorstores import FAISS
import faiss
from langchain_community.docstore import InMemoryDocstore
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_google_genai.llms import GoogleGenerativeAI
from langchain_core.documents import Document

import os
import getpass


class ConfigObj:
    """
    Temporary config class
    """
    def __init__(self) -> None:
        self.model_chat = "gemini-1.5-pro"
        self.chat_model_temperature = 0.7
        self.chat_model_top_p = None
        self.chat_model_top_k = None
        self.model_embeddings = "models/embedding-001"

        self.text_splitter_chunk_size = 1000
        self.text_splitter_chunk_overlap = 50
        self.text_splitter_length_function = len

        self.vector_store_search_k = 1
        self.vector_store_search_fetch_k = 20

        self.retrieval_chain_type = "stuff"


configs = ConfigObj()

GOOGLE_API_KEY = os.environ.get("GOOGLE_AISTUDIO_API_KEY", "")

if not GOOGLE_API_KEY:
    GOOGLE_API_KEY = getpass.getpass("Provide your google ai api key: ")


chat_model = GoogleGenerativeAI(
    model=configs.model_chat,
    api_key=GOOGLE_API_KEY,
    temperature=configs.chat_model_temperature,
    top_p=configs.chat_model_top_p,
    top_k=configs.chat_model_top_k,
)
embeddings_model = GoogleGenerativeAIEmbeddings(
    model=configs.model_embeddings, 
    google_api_key=GOOGLE_API_KEY,
    )

index = faiss.IndexFlatL2(len(embeddings_model.embed_query("hello world")))
vector_store = FAISS(
    embedding_function=embeddings_model,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

text_spliter = CharacterTextSplitter(
    chunk_size=configs.text_splitter_chunk_size, 
    chunk_overlap=configs.text_splitter_chunk_overlap,
    length_function=configs.text_splitter_length_function,
)

# train command
def train(argv: list[str]) -> None:
    for arg in argv:
        if arg.startswith("@"):
            print(f"Loading document {arg} to memory.")
            doc_pages = load_documents(arg[1:])
            print(f"document loaded to memory!")
            print(f"Loading document {arg} to vectorDB.")
            vector_store.add_documents(doc_pages)
            print(f"Document loaded to vectorDB!")
        else:
            print(f"Splitting text.")
            text_splitted = text_spliter.split_text(arg)
            print(f"Text splitted!")

            print(f"Storing text on vectorDB.")
            vector_store.add_texts(text_splitted)
            print(f"Text stored on vectorDB.")


def load_documents(document_path: str) -> list[Document]:

    if document_path.endswith(".pdf"):
        loader = PyPDFLoader(document_path)
        pages = loader.load()
        pages = text_spliter.split_documents(pages)

        return pages
    
    raise Exception(f"document {document_path} passed is not supported!")

def ask(argv: list[str]) -> None:
    if len(argv) != 1:
        raise Exception("ask, without ai, command accept only one param!")
    
    results = vector_store.similarity_search(
        argv[0], 
        k=configs.vector_store_search_k, 
        fetch_k=configs.vector_store_search_fetch_k, 
    )

    print(f"------------Asking without ai------------")
    print(f"Question: {argv[0]}")
    for i in range(len(results)):
        print(f"Answer {i+1}: ")
        print(f"{results[i]}")

def ask_with_ai(argv: list[str]) -> None:
    if len(argv) != 1:
        raise Exception("askWithAi command don't accept more than one arg!")

    retriever = vector_store.as_retriever()

    qa_chain = RetrievalQA.from_chain_type(
        llm=chat_model, 
        retriever=retriever, 
        chain_type=configs.retrieval_chain_type, 
    )

    response = qa_chain.invoke(argv[0])

    print("------------Asking with ai------------")
    print(f"Question: {response["query"]}")
    print(f"Response: \n{response["result"]}")