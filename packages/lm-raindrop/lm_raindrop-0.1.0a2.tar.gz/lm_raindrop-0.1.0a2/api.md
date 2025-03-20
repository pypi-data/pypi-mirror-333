# Search

Types:

```python
from raindrop.types import SearchResponse, TextResult
```

Methods:

- <code title="get /v1/search">client.search.<a href="./src/raindrop/resources/search.py">get_results</a>(\*\*<a href="src/raindrop/types/search_get_results_params.py">params</a>) -> <a href="./src/raindrop/types/search_response.py">SearchResponse</a></code>
- <code title="post /v1/search">client.search.<a href="./src/raindrop/resources/search.py">perform</a>(\*\*<a href="src/raindrop/types/search_perform_params.py">params</a>) -> <a href="./src/raindrop/types/search_response.py">SearchResponse</a></code>

# DocumentQuery

Types:

```python
from raindrop.types import DocumentQueryCreateResponse
```

Methods:

- <code title="post /v1/document_query">client.document_query.<a href="./src/raindrop/resources/document_query.py">create</a>(\*\*<a href="src/raindrop/types/document_query_create_params.py">params</a>) -> <a href="./src/raindrop/types/document_query_create_response.py">DocumentQueryCreateResponse</a></code>

# ChunkSearch

Types:

```python
from raindrop.types import ChunkSearchCreateResponse
```

Methods:

- <code title="post /v1/chunk_search">client.chunk_search.<a href="./src/raindrop/resources/chunk_search.py">create</a>(\*\*<a href="src/raindrop/types/chunk_search_create_params.py">params</a>) -> <a href="./src/raindrop/types/chunk_search_create_response.py">ChunkSearchCreateResponse</a></code>

# SummarizePage

Types:

```python
from raindrop.types import SummarizePageCreateResponse
```

Methods:

- <code title="post /v1/summarize_page">client.summarize_page.<a href="./src/raindrop/resources/summarize_page.py">create</a>(\*\*<a href="src/raindrop/types/summarize_page_create_params.py">params</a>) -> <a href="./src/raindrop/types/summarize_page_create_response.py">SummarizePageCreateResponse</a></code>
