# AI Nuclear News Feed Indexer

A Python automation tool that scans a curated list of international and technical RSS feeds for nuclear-related news, translates and summarizes the content using Azure OpenAI, and indexes the results into Azure Cognitive Search. Results are also saved to an Excel file. SonarCloud is integrated for static code analysis and code quality.

---

## Features

- **RSS Aggregation**: Parses news from over 25 major science, technology, and global news sources.
- **Keyword Filtering**: Only indexes articles containing nuclear science, energy, regulation, or policy keywords.
- **Translation & Summarization**: Uses Azure OpenAI to translate and summarize non-English or long articles.
- **Deduplication**: Skips articles already indexed based on their URLs.
- **Azure Cognitive Search Integration**: Uploads summarized articles to a custom index.
- **Excel Output**: Logs all indexed articles to a timestamped `.xlsx` file for easy auditing.
- **SonarCloud Quality Gate**: Integrated configuration for static code analysis with SonarCloud.

---

## Requirements

- **Python 3.8+**
- [Azure OpenAI credentials](https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart?tabs=command-line&pivots=programming-language-python)
- [Azure Cognitive Search credentials](https://learn.microsoft.com/en-us/azure/search/search-get-started-python)
- **SonarScanner** CLI if running static code analysis

Python packages (`pip install`):
- `feedparser`
- `requests`
- `openpyxl`
- `python-dotenv`
- `azure-core`
- `azure-search-documents`
- `openai`

---

## Environment Variables

The script loads environment variables via a `.env` file. These variables are required:

- `OPENAI_API_KEY`
- `OPENAI_API_BASE`
- `OPENAI_DEPLOYMENT`
- `SEARCH_API_ENDPOINT`
- `SEARCH_API_KEY`

Example `.env`:
```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_BASE=https://your-openai-endpoint.openai.azure.com
OPENAI_DEPLOYMENT=your-openai-deployment-name
SEARCH_API_ENDPOINT=https://your-search-service.search.windows.net
SEARCH_API_KEY=your-azure-search-key
