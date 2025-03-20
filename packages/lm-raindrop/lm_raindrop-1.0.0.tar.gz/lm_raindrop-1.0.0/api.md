# Search

Types:

```python
from lm_raindrop.types import SearchResponse, TextResult
```

Methods:

- <code title="get /v1/search">client.search.<a href="./src/lm_raindrop/resources/search.py">get_results</a>(\*\*<a href="src/lm_raindrop/types/search_get_results_params.py">params</a>) -> <a href="./src/lm_raindrop/types/search_response.py">SearchResponse</a></code>
- <code title="post /v1/search">client.search.<a href="./src/lm_raindrop/resources/search.py">perform</a>(\*\*<a href="src/lm_raindrop/types/search_perform_params.py">params</a>) -> <a href="./src/lm_raindrop/types/search_response.py">SearchResponse</a></code>

# DocumentQuery

Types:

```python
from lm_raindrop.types import DocumentQueryCreateResponse
```

Methods:

- <code title="post /v1/document_query">client.document_query.<a href="./src/lm_raindrop/resources/document_query.py">create</a>(\*\*<a href="src/lm_raindrop/types/document_query_create_params.py">params</a>) -> <a href="./src/lm_raindrop/types/document_query_create_response.py">DocumentQueryCreateResponse</a></code>

# ChunkSearch

Types:

```python
from lm_raindrop.types import ChunkSearchCreateResponse
```

Methods:

- <code title="post /v1/chunk_search">client.chunk_search.<a href="./src/lm_raindrop/resources/chunk_search.py">create</a>(\*\*<a href="src/lm_raindrop/types/chunk_search_create_params.py">params</a>) -> <a href="./src/lm_raindrop/types/chunk_search_create_response.py">ChunkSearchCreateResponse</a></code>

# SummarizePage

Types:

```python
from lm_raindrop.types import SummarizePageCreateResponse
```

Methods:

- <code title="post /v1/summarize_page">client.summarize_page.<a href="./src/lm_raindrop/resources/summarize_page.py">create</a>(\*\*<a href="src/lm_raindrop/types/summarize_page_create_params.py">params</a>) -> <a href="./src/lm_raindrop/types/summarize_page_create_response.py">SummarizePageCreateResponse</a></code>

# Object

Types:

```python
from lm_raindrop.types import ObjectDeleteResponse, ObjectUploadResponse
```

Methods:

- <code title="delete /v1/object/{bucket}/{key}">client.object.<a href="./src/lm_raindrop/resources/object.py">delete</a>(key, \*, bucket) -> <a href="./src/lm_raindrop/types/object_delete_response.py">ObjectDeleteResponse</a></code>
- <code title="get /v1/object/{bucket}/{key}">client.object.<a href="./src/lm_raindrop/resources/object.py">download</a>(key, \*, bucket) -> BinaryAPIResponse</code>
- <code title="put /v1/object/{bucket}/{key}">client.object.<a href="./src/lm_raindrop/resources/object.py">upload</a>(key, \*, bucket, \*\*<a href="src/lm_raindrop/types/object_upload_params.py">params</a>) -> <a href="./src/lm_raindrop/types/object_upload_response.py">ObjectUploadResponse</a></code>
