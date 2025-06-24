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
- `azure-identity`
- `azure-keyvault-secrets`

# pip install feedparser requests openpyxl python-dotenv azure-core azure-search-documents openai azure-identity azure-keyvault-secrets

---

## Environment Variables and Azure Key Vault

The script now loads secrets securely from Azure Key Vault. Only the Key Vault URL is required in your `.env` file:

- `KEY_VAULT_URL` (e.g. `https://kv-ai-rjglabs.vault.azure.com/`)

Example `.env`:
```env
KEY_VAULT_URL=https://kv-ai-rjglabs.vault.azure.com/
```

All other secrets (OpenAI keys, endpoints, deployment names, and Azure Search credentials) must be stored as secrets in your Azure Key Vault with the following names:
- `AI-OPENAI-KEY`
- `AI-OPENAI-ENDPOINT`
- `AI-OPENAI-DEPLOYMENT`
- `AI-SEARCH-PRIMARY-KEY`
- `AI-SEARCH-ENDPOINT`

---

## Professional Best Practices

- **Enterprise-Grade Security**: All sensitive credentials are managed via Azure Key Vault, never stored in code or local files.
- **Cloud-Ready**: Uses Azure DefaultAzureCredential for seamless local and cloud authentication.
- **Static Code Analysis**: SonarCloud integration for code quality and security.
- **Logging**: Key events and errors are logged for traceability.
- **Modular & Maintainable**: Code is organized for clarity and easy extension.
- **Documentation**: This README is kept up to date with all configuration and security changes.

---

## Quick Start

1. Clone the repository and install requirements:
   ```sh
   pip install -r requirements.txt
   # or manually install: feedparser requests openpyxl python-dotenv azure-core azure-search-documents openai azure-identity azure-keyvault-secrets
   ```
2. Create a `.env` file with your Key Vault URL:
   ```env
   KEY_VAULT_URL=https://kv-ai-rjglabs.vault.azure.com/
   ```
3. Add all required secrets to your Azure Key Vault (see above).
4. Run the script:
   ```sh
   python nuclear_news_indexer.py
   ```

---

## Azure Key Vault Setup Example

To add a secret to your Key Vault:
```sh
az keyvault secret set --vault-name <YourKeyVaultName> --name AI-OPENAI-KEY --value <your-openai-key>
```
Repeat for each required secret.

---

## License

MIT License
