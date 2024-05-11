import asyncio
import redis
from ollama import AsyncClient
from langchain_community.document_loaders import DirectoryLoader, SeleniumURLLoader
from bs4 import BeautifulSoup as Soup
import config
import hashlib
import json
import os

# Define the cache directory
cache_dir = './cache/'

# Define the Redis connection
redis_client = redis.Redis(host='192.168.1.25', port=6379, db=0)

# Function to fetch URLs from configuration
def get_urls():
    urls = os.getenv('URLS')
    if urls:
        return urls.split(',')
    else:
        return []

# Function to check if a URL has already been processed
def is_url_processed(url):
    return redis_client.exists(f"url:{url}")

# Function to mark a URL as processed
def mark_url_processed(url):
    redis_client.set(f"url:{url}", 1)

# Function to cache the loaded documents in Redis# Custom JSON encoder to handle Document objects
class DocumentJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Document):
            # Customize the serialization of Document objects
            return {
                'metadata': obj.metadata,
                'page_content': obj.page_content,
                # Add other attributes of Document as needed
            }
        return super().default(obj)

def cache_documents_redis(docs):
    encoder = DocumentJSONEncoder()
    
    for doc in docs:
        file_name = hashlib.md5(doc.metadata['source'].encode()).hexdigest()
        content = json.dumps(doc, cls=encoder)  # Use the custom encoder
        redis_client.set(f"doc:{file_name}", content)

async def handle_send(prompt):
    client = AsyncClient(host=config.OLLAMA_HOST)

    # Load documents from a directory
    dir_loader = DirectoryLoader('./', glob="**/*.py", use_multithreading=True, show_progress=True)
    dir_docs = dir_loader.load()
    print(f"Number of documents loaded from directory: {len(dir_docs)}")

    # Cache the directory documents in Redis
    cache_documents_redis(dir_docs)

    # Load documents from URLs using Selenium
    urls = get_urls()
    for url in urls:
        if not is_url_processed(url):
            url_loader = SeleniumURLLoader([url])
            url_docs = url_loader.load()
            cache_documents_redis(url_docs)
            mark_url_processed(url)

    # Combine all documents
    all_docs = dir_docs + [json.loads(redis_client.get(key)) for key in redis_client.scan_iter("doc:*")]
    
    # Ensure that all_docs contains only Document objects
    all_docs = [doc for doc in all_docs if isinstance(doc, Document)]
    
    context = "\n\n".join([doc.page_content for doc in all_docs])
    message = {'role': 'user', 'content': f"{prompt}\n\nContext: \n\n{context}"}

    response = ""
    async for part in await client.chat(model='llama3', messages=[message], stream=True):
        response += part['message']['content']
    print()
    return response

async def chat():
    while True:
        prompt = await asyncio.get_event_loop().run_in_executor(None, input, "Your question: ")
        asyncio.create_task(display_response(prompt))

async def display_response(prompt):
    response = await handle_send(prompt)
    print(f"AI: {response}")

async def main():
    await asyncio.gather(
        chat(),
    )

if __name__ == "__main__":
    asyncio.run(main())


