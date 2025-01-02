from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_core.documents import Document

from pathlib import Path

from configs import get_configs, get_google_api_key
from dependecies import chat_model, vector_store, text_spliter


GOOGLE_API_KEY = get_google_api_key()
configs = get_configs()

docs_suff_loader_mapping = {
    ".pdf": PyPDFLoader,
}


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
    doc_suffix = Path(document_path).suffix.lower()

    if docs_suff_loader_mapping.get(doc_suffix, False):
        DocLoader = docs_suff_loader_mapping[doc_suffix]
        loader = DocLoader(document_path)
        pages = loader.load()
        pages = text_spliter.split_documents(pages)

        return pages
    
    raise Exception(f"document {document_path} passed is not supported!")

# ask command
def ask(argv: list[str]) -> None: 
    print(f"------------Asking without AI------------")
    print(f"Use '\q' for quitting")

    while True:
        question = input(">>> ")

        if question.lower() == r"\q":
            break

        results = vector_store.similarity_search(
            question, 
            k=configs.vector_store.search.k, 
            fetch_k=configs.vector_store.search.fetch_k, 
        )

        print(f"Question: {question}")
        for i in range(len(results)):
            print(f"Answer {i+1}: ")
            print(f"{results[i]}")

# askWithAI command
def ask_with_ai(argv: list[str]) -> None:
    print("------------Asking with AI------------")
    print("Use '\q' for quitting")

    while True:
        question = input(">>> ")

        if question.lower() == r"\q":
            break

        retriever = vector_store.as_retriever(search_kwargs={
            "k": configs.retrieval.k, 
            "fetch_k": configs.retrieval.fetch_k,
        })

        qa_chain = RetrievalQA.from_chain_type(
            llm=chat_model, 
            retriever=retriever, 
            chain_type=configs.retrieval.chain_type, 
        )

        response = qa_chain.invoke(question)

        print(f"Question: {response["query"]}")
        print(f"Response: \n{response["result"]}")