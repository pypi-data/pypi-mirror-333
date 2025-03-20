# Tasnif Soliq UZ Client

A Python client for the tasnif.soliq.uz API, which provides access to the MXIK (National Classifier of Products by Activity) database in Uzbekistan.

## Installation

```bash
pip install tasnif-solig-uz
```

## Requirements

- Python 3.8+
- requests
- pydantic

## Usage

### Basic Usage

```python
from tasnif_solig_uz import Client

# Initialize the client
client = Client()

# Search for MXIK codes
results = client.search_mxik("компьютер")

# Print the results
for item in results.data:
    print(f"MXIK Code: {item.mxikCode}")
    print(f"Name (UZ): {item.groupNameUz}")
    print(f"Name (RU): {item.groupNameRu}")
    print("---")
```

### Advanced Search

```python
from tasnif_solig_uz import Client, ElasticSearch, SearchParams

# Initialize the client
client = Client()

# Search using ElasticSearch
search_params = ElasticSearch(
    search="телефон",
    size=50,
    page=0,
    lang="ru"
)
results = client.search(search_params)

# Search using parameters
params = SearchParams(
    params={"mxikCode": "12345"},
    size=20,
    page=0,
    lang="uz"
)
results_by_params = client.search_by_params(params)

```

### Custom Base URL

```python
from tasnif_solig_uz import Client

# Initialize the client with a custom base URL
client = Client(base_url="https://custom-tasnif-api.example.com/api")
```

## API Reference

### Client

The main client class for interacting with the tasnif.soliq.uz API.

#### Constructor

```python
Client(base_url: str = "https://tasnif.soliq.uz/api/cls-api")
```

- `base_url`: The base URL for the API. Defaults to the official API endpoint.

#### Methods

##### search_mxik

```python
search_mxik(query: str, limit: int = 10) -> MXIKSearchResponse
```

Search for MXIK codes by a simple text query.

- `query`: The search query text.
- `limit`: Maximum number of results to return. Defaults to 10.

##### search

```python
search(params: ElasticSearch) -> List[MxikData]
```

Search using ElasticSearch parameters.

- `params`: An `ElasticSearch` object containing search parameters.

##### search_by_params

```python
search_by_params(params: SearchParams) -> List[MxikData]
```

Search by specific parameters.

- `params`: A `SearchParams` object containing search parameters.

##### search_dv_cert

```python
search_dv_cert(params: SearchParams) -> List[MxikData]
```

Search by DV certificate number.

- `params`: A `SearchParams` object containing search parameters.

### Models

#### ElasticSearch

```python
ElasticSearch(
    search: str,
    size: int = 20,
    page: int = 0,
    lang: str = "uz"
)
```

- `search`: The search query text.
- `size`: Number of results per page. Defaults to 20.
- `page`: Page number (0-based). Defaults to 0.
- `lang`: Language code ("uz", "ru", or "en"). Defaults to "uz".

#### SearchParams

```python
SearchParams(
    params: Dict[str, Any],
    size: int = 20,
    page: int = 0,
    lang: str = "uz"
)
```

- `params`: Dictionary of search parameters.
- `size`: Number of results per page. Defaults to 20.
- `page`: Page number (0-based). Defaults to 0.
- `lang`: Language code ("uz", "ru", or "en"). Defaults to "uz".

#### MxikData

Represents MXIK data returned by the API.

#### MxikResponse

Represents a response from the API containing a single MXIK item.

#### MXIKSearchResponse

Represents a response from the API containing a list of MXIK items.

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/tasnif-solig-uz.git
cd tasnif-solig-uz

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
python -m test.run_tests

# Run with pytest
pytest
```

## License

MIT License 