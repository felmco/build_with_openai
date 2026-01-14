"""
01_embeddings.py - Work with text embeddings
"""

import os
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def get_embedding(text, model="text-embedding-3-small"):
    """Get embedding for text"""
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def semantic_search_example():
    """Demonstrate semantic search with embeddings"""
    print("\n" + "="*60)
    print("SEMANTIC SEARCH WITH EMBEDDINGS")
    print("="*60)

    # Sample documents
    documents = [
        "Python is a high-level programming language",
        "Machine learning is a subset of artificial intelligence",
        "The cat sat on the mat",
        "Deep learning uses neural networks with multiple layers",
        "JavaScript is used for web development"
    ]

    # Create embeddings for all documents
    doc_embeddings = [get_embedding(doc) for doc in documents]

    # Search query
    query = "artificial intelligence and neural networks"
    query_embedding = get_embedding(query)

    # Calculate similarities
    similarities = [
        cosine_similarity(query_embedding, doc_emb)
        for doc_emb in doc_embeddings
    ]

    # Get most similar documents
    ranked_docs = sorted(
        zip(documents, similarities),
        key=lambda x: x[1],
        reverse=True
    )

    print(f"\nQuery: {query}\n")
    print("Top 3 Matches:")
    for i, (doc, score) in enumerate(ranked_docs[:3]):
        print(f"{i+1}. {doc} (Score: {score:.4f})")


def main():
    print("Embeddings Demo")
    semantic_search_example()


if __name__ == "__main__":
    main()
