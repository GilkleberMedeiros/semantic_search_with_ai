from langchain_community.document_loaders import PyPDFLoader, ChatGPTLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.vectorstores import FAISS
import faiss
from langchain_community.docstore import InMemoryDocstore
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_google_genai.llms import GoogleGenerativeAI
from langchain_core.documents import Document

from configs import get_configs, get_google_api_key


# TODO: Extract configs from a json config file.
# TODO: Put object dependencies loading in other file.
# TODO: Make load_documents func get loader class from dict map with .suf: Loader

GOOGLE_API_KEY = get_google_api_key()
configs = get_configs()

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
    print(f"------------Asking without AI------------")
    print(f"Use '\q' for quitting")

    while True:
        question = input(">>> ")

        if question.lower() == r"\q":
            break

        results = vector_store.similarity_search(
            question, 
            k=configs.vector_store_search_k, 
            fetch_k=configs.vector_store_search_fetch_k, 
        )

        print(f"Question: {question}")
        for i in range(len(results)):
            print(f"Answer {i+1}: ")
            print(f"{results[i]}")

def ask_with_ai(argv: list[str]) -> None:
    print("------------Asking with AI------------")
    print("Use '\q' for quitting")

    while True:
        question = input(">>> ")

        if question.lower() == r"\q":
            break

        retriever = vector_store.as_retriever()

        qa_chain = RetrievalQA.from_chain_type(
            llm=chat_model, 
            retriever=retriever, 
            chain_type=configs.retrieval_chain_type, 
        )

        response = qa_chain.invoke(question)

        print(f"Question: {response["query"]}")
        print(f"Response: \n{response["result"]}")