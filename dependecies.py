from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_google_genai.llms import GoogleGenerativeAI
from langchain_community.vectorstores import FAISS
import faiss
from langchain_community.docstore import InMemoryDocstore
from langchain.text_splitter import CharacterTextSplitter

from configs import get_configs, get_google_api_key


GOOGLE_API_KEY = get_google_api_key()
configs = get_configs()

chat_model = GoogleGenerativeAI(
    model=configs.chat_model.name,
    api_key=GOOGLE_API_KEY,
    temperature=configs.chat_model.temperature,
    top_p=configs.chat_model.top_p,
    top_k=configs.chat_model.top_k,
)
embeddings_model = GoogleGenerativeAIEmbeddings(
    model=configs.embeddings_model.name, 
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
    chunk_size=configs.text_splitter.chunk_size, 
    chunk_overlap=configs.text_splitter.chunk_overlap,
    length_function=len,
)