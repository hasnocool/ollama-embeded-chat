import asyncio
import logging
from ollama import AsyncClient
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
import uuid

# Set the logging level to DEBUG for verbose console messages
logging.basicConfig(level=logging.DEBUG)

def get_matching_documents():
    # Load documents from a text file with UTF-8 encoding
    loader = TextLoader("text.txt", encoding="utf-8")
    documents = loader.load()

    # Check if documents is empty
    if not documents:
        raise ValueError("No documents loaded from the file")

    # Split documents into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # Generate unique IDs for each document
    ids = [str(uuid.uuid4()) for _ in docs]

    # Create embeddings using SentenceTransformer
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create a Chroma vector store
    vectorstore = Chroma.from_documents(docs, embeddings, ids=ids)

    # Perform similarity search
    query = "Your query here"
    matching_docs = vectorstore.similarity_search(query)

    return matching_docs

async def chat():
    client = AsyncClient(host='http://192.168.1.25:11434')

    while True:
        prompt = input("Your question: ")
        message = {'role': 'user', 'content': prompt}

        # Retrieve matching documents for the prompt
        matching_docs = get_matching_documents()

        # Process the matching documents to create the context for the LLM
        context = [doc.page_content for doc in matching_docs]
        context_prompt = "Context: \n\n".join(context)

        # Include the context prompt in the input to the LLM
        message['content'] = f"{prompt}\n\n{context_prompt}"

        async for part in await client.chat(model='llama3', messages=[message], stream=True):
            print(part['message']['content'], end='', flush=True)
        print()  # Add a newline after the response

asyncio.run(chat())
