---
name: ai-rag-patterns
description: Retrieval-Augmented Generation (RAG) patterns for LLM applications. Use when building RAG systems, vector search, embeddings, semantic search, or document retrieval pipelines.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 2.0
---

# AI RAG Patterns - Retrieval-Augmented Generation

> **Philosophy:** Retrieval quality determines generation quality. Garbage in, garbage out.

---

## When to Use This Skill

| ✅ Use                           | ❌ Don't Use                  |
| -------------------------------- | ----------------------------- |
| Building Q&A over documents      | Pure generative tasks         |
| Semantic search implementation   | Dataset too small (<100 docs) |
| Reducing LLM hallucinations      | Data privacy restrictions     |
| Domain-specific knowledge access | Simple keyword search         |
| Document processing pipelines    | Real-time streaming data      |

---

## Core Rules (Non-Negotiable)

1. **Semantic chunking first** - Chunk by meaning, not token counts
2. **DataLoader always** - Batch embedding generation
3. **Hybrid search default** - Combine dense + sparse retrieval
4. **Reranking required** - Never trust first-stage retrieval alone
5. **Evaluation mandatory** - Measure retrieval quality separately

---

## RAG Architecture Overview

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Documents  │───▷│   Chunking  │───▷│  Embedding  │
└─────────────┘    └─────────────┘    └─────────────┘
                                            │
                                            ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Response  │◁───│     LLM     │◁───│  Retrieval  │
└─────────────┘    └─────────────┘    └─────────────┘
                         ▲
                         │
                   ┌─────────────┐
                   │  Reranking  │
                   └─────────────┘
```

---

## Vector Database Selection

| Database     | Type        | Best For                     | Pricing     |
| ------------ | ----------- | ---------------------------- | ----------- |
| **Pinecone** | Managed     | Production, scalable         | Pay-per-use |
| **Weaviate** | Open-source | Hybrid search, self-hosted   | Free (OSS)  |
| **Chroma**   | Embedded    | Prototyping, local dev       | Free        |
| **Qdrant**   | Open-source | Fast filtering, on-premise   | Free (OSS)  |
| **pgvector** | Extension   | PostgreSQL integration       | Free        |
| **Milvus**   | Open-source | High performance, enterprise | Free (OSS)  |

### Decision Tree

```
What's your scale?
│
├─ Prototyping / Small scale?
│  └─ → Chroma (embedded, zero setup)
│
├─ Already using PostgreSQL?
│  └─ → pgvector (integrated, no new infra)
│
├─ Production, managed service?
│  └─ → Pinecone (scalable, low ops)
│
└─ Self-hosted, enterprise?
   └─ → Qdrant or Milvus (full control)
```

---

## Embedding Model Selection

| Model                    | Dimensions | Speed   | Quality | Cost         |
| ------------------------ | ---------- | ------- | ------- | ------------ |
| `text-embedding-3-small` | 1536       | Fast    | Good    | $0.02/1M     |
| `text-embedding-3-large` | 3072       | Medium  | Best    | $0.13/1M     |
| `bge-large-en-v1.5`      | 1024       | Fast    | Best    | Free (local) |
| `all-MiniLM-L6-v2`       | 384        | Fastest | Good    | Free (local) |
| `e5-large-v2`            | 1024       | Medium  | Best    | Free (local) |

**Recommendation:** Start with `text-embedding-3-small`, evaluate, upgrade if needed.

---

## Chunking Strategies

### 1. Recursive Character Splitting (Default)

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)
chunks = splitter.split_documents(documents)
```

### 2. Semantic Chunking (Recommended)

```python
from langchain.text_splitter import SemanticChunker
from langchain.embeddings import OpenAIEmbeddings

splitter = SemanticChunker(
    embeddings=OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile"
)
chunks = splitter.split_documents(documents)
```

### 3. Markdown/Code Aware

```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

headers = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
]
splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers)
```

### Chunking Best Practices

| Parameter  | Recommended    | Why                            |
| ---------- | -------------- | ------------------------------ |
| Chunk size | 500-1000 chars | Balance context vs specificity |
| Overlap    | 10-20%         | Preserve context at boundaries |
| Separators | Semantic       | Respect document structure     |

---

## Retrieval Strategies

### 1. Dense Retrieval (Vector Similarity)

```python
# Basic vector search
results = vectorstore.similarity_search(query, k=5)

# With score threshold
results = vectorstore.similarity_search_with_relevance_scores(
    query,
    k=10,
    score_threshold=0.7
)
```

### 2. Sparse Retrieval (BM25/Keyword)

```python
from langchain.retrievers import BM25Retriever

bm25 = BM25Retriever.from_documents(documents)
bm25.k = 5
results = bm25.get_relevant_documents(query)
```

### 3. Hybrid Search (Recommended)

```python
from langchain.retrievers import EnsembleRetriever

ensemble = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.3, 0.7]  # Favor semantic
)
results = ensemble.get_relevant_documents(query)
```

### 4. Multi-Query Retrieval

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm
)
# Generates multiple query variations automatically
```

---

## Reranking Patterns

### Cross-Encoder Reranking

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# Get initial candidates
candidates = vectorstore.similarity_search(query, k=20)

# Rerank
pairs = [[query, doc.page_content] for doc in candidates]
scores = reranker.predict(pairs)

# Sort by score
reranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)[:5]
```

### Maximal Marginal Relevance (MMR)

```python
# Balance relevance + diversity
results = vectorstore.max_marginal_relevance_search(
    query,
    k=5,
    fetch_k=20,
    lambda_mult=0.5  # 0=diversity, 1=relevance
)
```

---

## Advanced RAG Patterns

### Parent Document Retriever

```python
from langchain.retrievers import ParentDocumentRetriever

# Small chunks for retrieval, large for context
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
)
```

### Contextual Compression

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

compressor = LLMChainExtractor.from_llm(llm)

retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever()
)
# Returns only relevant parts of documents
```

### Hypothetical Document Embedding (HyDE)

```python
from langchain.chains import HypotheticalDocumentEmbedder

hyde = HypotheticalDocumentEmbedder.from_llm(
    llm=llm,
    embeddings=embeddings,
    prompt=hyde_prompt
)
# Generate hypothetical answer, then search for similar
```

---

## RAG Prompt Patterns

### Basic with Citations

```python
prompt = """Answer based on the context below. Include citations [1], [2], etc.

Context:
{context}

Question: {question}

Answer (with citations):"""
```

### Grounded with Confidence

```python
prompt = """Use ONLY the provided context. If you cannot answer, say "I don't know."

Context:
{context}

Question: {question}

Answer:
Confidence (0-100%):
Sources used:"""
```

### Chain-of-Thought RAG

```python
prompt = """Given the context, reason step by step to answer.

Context:
{context}

Question: {question}

Let me think step by step:
1. First, I'll identify relevant information...
2. Then, I'll synthesize...
3. Finally, I'll conclude...

Answer:"""
```

---

## Evaluation Metrics

```python
def evaluate_rag(qa_chain, test_cases):
    metrics = {
        'retrieval_precision': [],  # Relevant in top-k
        'retrieval_recall': [],     # Found all relevant
        'answer_relevance': [],     # Answer matches question
        'groundedness': [],         # Answer from context only
        'faithfulness': [],         # No hallucination
    }

    for test in test_cases:
        result = qa_chain({"query": test['question']})

        # Retrieval metrics
        retrieved_ids = [d.id for d in result['source_documents']]
        precision = len(set(retrieved_ids) & set(test['relevant_ids'])) / len(retrieved_ids)
        recall = len(set(retrieved_ids) & set(test['relevant_ids'])) / len(test['relevant_ids'])

        metrics['retrieval_precision'].append(precision)
        metrics['retrieval_recall'].append(recall)

        # Use LLM-as-judge for semantic metrics
        # ...

    return {k: sum(v)/len(v) for k, v in metrics.items()}
```

---

## Production Considerations

### Metadata for Filtering

```python
# Add metadata during indexing
for doc in documents:
    doc.metadata = {
        "source": doc.metadata.get("source"),
        "date": doc.metadata.get("date"),
        "category": classify(doc.page_content),
        "author": extract_author(doc),
    }

# Filter during retrieval
results = vectorstore.similarity_search(
    query,
    filter={"category": "technical", "date": {"$gte": "2024-01-01"}},
    k=5
)
```

### Caching Strategy

```python
from langchain.cache import RedisSemanticCache

langchain.llm_cache = RedisSemanticCache(
    redis_url="redis://localhost:6379",
    embedding=embeddings,
    score_threshold=0.95
)
```

---

## Anti-Patterns

| ❌ Don't                       | ✅ Do                               |
| ------------------------------ | ----------------------------------- |
| Fixed-size chunking only       | Semantic chunking + structure-aware |
| Pure vector search             | Hybrid search (dense + sparse)      |
| Use first retrieval results    | Rerank before generation            |
| Same embedding for all content | Evaluate per content type           |
| Cram max context into prompt   | Use relevance thresholds            |
| Measure only final answer      | Evaluate retrieval separately       |
| Ignore metadata                | Add rich metadata for filtering     |

---

## Production Checklist

Before deployment:

- [ ] Semantic chunking implemented?
- [ ] Hybrid search configured?
- [ ] Reranking step added?
- [ ] Metadata extraction automated?
- [ ] Retrieval quality measured?
- [ ] Embedding refresh strategy?
- [ ] Access control for documents?
- [ ] Caching for repeated queries?

---

## Related Skills

| Need                 | Skill                |
| -------------------- | -------------------- |
| LLM prompt design    | `prompt-engineering` |
| Vector DB (Postgres) | `postgres-patterns`  |
| Redis caching        | `redis-patterns`     |
| API design           | `api-patterns`       |

---

> **Remember:** RAG is only as good as your retrieval. Invest 80% of effort in retrieval quality, 20% in generation.
