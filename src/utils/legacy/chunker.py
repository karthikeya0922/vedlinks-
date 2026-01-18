"""
Text chunker with token-based splitting and overlap.
"""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Get chunking parameters from environment
MAX_CHUNK_TOKENS = int(os.getenv("MAX_CHUNK_TOKENS", "800"))
MIN_CHUNK_TOKENS = int(os.getenv("MIN_CHUNK_TOKENS", "200"))


def estimate_tokens(text: str) -> int:
    """
    Rough token estimation (1 token ≈ 4 characters for English).
    For more accurate counting, use a tokenizer.
    """
    return len(text) // 4


def chunk_text(text: str, max_tokens: int = None, min_tokens: int = None, overlap_ratio: float = 0.1) -> List[str]:
    """
    Split text into chunks based on token count with overlap.
    
    Args:
        text: Input text to chunk
        max_tokens: Maximum tokens per chunk (default from env)
        min_tokens: Minimum tokens per chunk (default from env)
        overlap_ratio: Fraction of overlap between consecutive chunks
    
    Returns:
        List of text chunks
    """
    if max_tokens is None:
        max_tokens = MAX_CHUNK_TOKENS
    if min_tokens is None:
        min_tokens = MIN_CHUNK_TOKENS
    
    # Split by paragraphs first (double newline)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    for para in paragraphs:
        para_tokens = estimate_tokens(para)
        
        # If single paragraph exceeds max_tokens, split by sentences
        if para_tokens > max_tokens:
            sentences = [s.strip() + '.' for s in para.split('.') if s.strip()]
            for sent in sentences:
                sent_tokens = estimate_tokens(sent)
                
                if current_tokens + sent_tokens > max_tokens:
                    # Save current chunk if it meets minimum
                    if current_tokens >= min_tokens:
                        chunks.append('\n\n'.join(current_chunk))
                    
                    # Start new chunk with overlap
                    if current_chunk:
                        overlap_size = max(1, int(len(current_chunk) * overlap_ratio))
                        current_chunk = current_chunk[-overlap_size:]
                        current_tokens = sum(estimate_tokens(c) for c in current_chunk)
                    else:
                        current_chunk = []
                        current_tokens = 0
                
                current_chunk.append(sent)
                current_tokens += sent_tokens
        else:
            # Normal paragraph processing
            if current_tokens + para_tokens > max_tokens:
                # Save current chunk if it meets minimum
                if current_tokens >= min_tokens:
                    chunks.append('\n\n'.join(current_chunk))
                
                # Start new chunk with overlap
                if current_chunk:
                    overlap_size = max(1, int(len(current_chunk) * overlap_ratio))
                    current_chunk = current_chunk[-overlap_size:]
                    current_tokens = sum(estimate_tokens(c) for c in current_chunk)
                else:
                    current_chunk = []
                    current_tokens = 0
            
            current_chunk.append(para)
            current_tokens += para_tokens
    
    # Add remaining chunk
    if current_chunk and current_tokens >= min_tokens:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks


def chunk_documents(documents: List[tuple[str, str]], **chunk_kwargs) -> List[dict]:
    """
    Chunk multiple documents.
    
    Args:
        documents: List of (filename, text) tuples
        **chunk_kwargs: Additional arguments to pass to chunk_text
    
    Returns:
        List of dicts with 'source', 'chunk_id', 'text' keys
    """
    all_chunks = []
    
    for filename, text in documents:
        chunks = chunk_text(text, **chunk_kwargs)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                'source': filename,
                'chunk_id': i,
                'text': chunk,
                'tokens': estimate_tokens(chunk)
            })
    
    return all_chunks
