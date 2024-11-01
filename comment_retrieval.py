# GRPC
import aiohttp
import re
import os
import html
from typing import Tuple
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# API client library
import googleapiclient.discovery

# API information
CLIENT_SECRETS_FILE = os.getenv("CLIENT_SECRETS_FILE")

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = os.getenv("YOUTUBE_READ_WRITE_SSL_SCOPE")
YOUTUBE_API_SERVICE_NAME = os.getenv("YOUTUBE_API_SERVICE_NAME")
YOUTUBE_API_VERSION = os.getenv("YOUTUBE_API_VERSION")

# API key
DEVELOPER_KEY = os.getenv("DEVELOPER_KEY")
youtube = googleapiclient.discovery.build(
    YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY
)

BASE_URL_COMMENTS = os.getenv("BASE_URL_COMMENTS")
BASE_URL_VIDEOS = os.getenv("BASE_URL_VIDEOS")


async def fetch_video_details(video_id):
    """Fetch video details including the title asynchronously."""
    params = {
        "part": "snippet",
        "id": video_id,
        "key": DEVELOPER_KEY,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL_VIDEOS, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data["items"][0]["snippet"]["title"]
            else:
                response.raise_for_status()


def clean_text(text):
    """
    Function to clean text data by removing HTML entities, URLs, and unwanted characters.
    """
    # Decode HTML entities to their corresponding characters (e.g., &#39; -> ')
    text = html.unescape(text)

    # Remove URLs (http or https)
    text = re.sub(r"http\S+|www.\S+", "", text)

    # Remove HTML tags (e.g., <a href=...>)
    text = re.sub(r"<.*?>", "", text)

    # Remove unwanted characters or multiple spaces
    text = re.sub(r'[^a-zA-Z0-9\s.,!?\'"]', "", text)

    # Normalize whitespace to single spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


async def process_comments(video_id) -> Tuple[str, VectorStoreRetriever]:
    # Retrieve all comments asynchronously
    video_title, comments = await comment_retrieval(video_id)
    print(f"Total Comments Fetched: {len(comments)}")
    
    # Clean each comment
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    chunks = text_splitter.split_documents([Document(page_content=" ".join(comments))])

    vector_db = FAISS.from_documents(chunks, OpenAIEmbeddings())

    return video_title, vector_db.as_retriever()


async def fetch_comments_page(session, video_id, page_token=None):
    """Fetch a page of comments asynchronously."""
    # Construct the parameters for the request, excluding pageToken if it's None
    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": 100,
        "key": DEVELOPER_KEY,
    }

    if page_token is not None:
        params["pageToken"] = page_token

    async with session.get(BASE_URL_COMMENTS, params=params) as response:
        if response.status == 200:
            return await response.json()
        else:
            response.raise_for_status()


async def get_all_comments(video_id):
    comments = []
    next_page_token = None

    async with aiohttp.ClientSession() as session:
        video_title = await fetch_video_details(video_id)
        while True:
            # Fetch the next page of comments
            response = await fetch_comments_page(session, video_id, next_page_token)

            # Extract comments from the response
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)

            # Check for next page token
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

    return video_title, comments


# Main entry point for asyncio
async def comment_retrieval(video_id):
    video_title, comments = await get_all_comments(video_id)
    return video_title, comments
