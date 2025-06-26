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

## Dependency Security

- All production and development dependencies are regularly reviewed for security vulnerabilities.
- Vulnerable packages are pinned to secure versions as soon as fixes are available.
- Notable pins:
  - `azure-identity>=1.16.1` (security fix)
  - `zipp>=3.19.1` (security fix)
  - `black>=24.3.0` (security fix, dev only)
- See `requirements.txt` and `requirements-dev.txt` for current versions.

---

## Code Quality & Formatting Tools

This project uses the following tools to ensure code quality and consistency:

- **Black**: Python code formatter. Pinned to `>=24.3.0` in `requirements-dev.txt` for security. To maintain compatibility with flake8's strict line length, always run Black with `--line-length 79`:
  ```sh
  black --line-length 79 nuclear_news_indexer.py
  ```
  You can check for changes without modifying files using:
  ```sh
  black --diff --line-length 79 nuclear_news_indexer.py
  ```
- **flake8**: Enforces PEP8 compliance, including a strict 79-character line limit (E501). Run:
  ```sh
  flake8 nuclear_news_indexer.py
  ```
- **isort**: Automatically sorts and groups imports. Run:
  ```sh
  isort nuclear_news_indexer.py
  ```
- **zipp**: Pinned to `>=3.19.1` in both `requirements.txt` and `requirements-dev.txt` for security.

> **Note:** Black's default line length is 88, which will cause conflicts with flake8's E501. Always use `--line-length 79` with Black for this project.

---

## AI Assistance

This project leverages agentic AI coding support via GitHub Copilot and related tools for code review, refactoring, and automation. AI assistance is used to:
- Refactor and modularize code
- Enforce code style and best practices
- Generate and improve documentation
- Accelerate development and testing

---

## Continuous Integration (CI), SonarCloud & Snyk

This project uses GitHub Actions for continuous integration. Every push and pull request to the `main` branch automatically triggers a workflow that:
- Checks code formatting and style (isort, black, flake8)
- Runs unit tests
- Runs a SonarCloud static analysis scan for code quality and security
- **Runs Snyk security scans on both `requirements.txt` and `requirements-dev.txt` to detect vulnerabilities in all dependencies**

### Snyk Security Scanning

Snyk is integrated into the CI pipeline to automatically check for vulnerabilities in both production and development dependencies:
- The workflow uses the official Snyk GitHub Action to scan `requirements.txt` and `requirements-dev.txt` on every CI run.
- The Snyk token is provided via the `SNYK_TOKEN` GitHub Actions secret. To set it up, run:
  ```sh
  gh secret set SNYK_TOKEN --repo rjglabs/ai-nuke-newsfeed --body "YOUR_TOKEN_HERE"
  ```
- If vulnerabilities are found, the workflow will fail and details will be shown in the Actions log.

The SonarCloud scan is triggered by the GitHub Actions workflow and results are visible on the SonarCloud dashboard for this project.

---

## Commit Signing & GPG Public Key

All commits and tags in this repository are signed with a GPG key for authenticity and integrity. The public key is provided in the file `GPG-KEY.txt` at the root of this repository.

**To import the public key and verify signatures:**

1. Import the key:
   ```sh
   gpg --import GPG-KEY.txt
   ```
2. After importing, you can verify signed commits and tags using GitHub or the command line:
   ```sh
   git log --show-signature
   git show --show-signature <commit-hash>
   git tag -v <tagname>
   ```

> **Note:** On GitHub, a "Verified" badge will appear next to signed commits and tags if the key is also added to the committer's GitHub account.

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
- `azure-identity>=1.16.1`
- `azure-keyvault-secrets`
- `zipp>=3.19.1`
- `black>=24.3.0`  # dev tool, included for unified security scanning
- `flake8`          # dev tool, included for unified security scanning
- `isort`           # dev tool, included for unified security scanning
- `coverage`        # dev tool, included for unified security scanning

# pip install feedparser requests openpyxl python-dotenv azure-core azure-search-documents openai azure-identity>=1.16.1 azure-keyvault-secrets zipp>=3.19.1 black>=24.3.0 flake8 isort coverage

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
   poetry install
   # Or, if you need a requirements.txt for pip:
   poetry export -f requirements.txt --output requirements.txt --without-hashes
   pip install -r requirements.txt
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

## Output & Logging

- **Excel Output**: All results are saved in the `output/` folder with a timestamped filename (e.g., `output/news_results_YYYYMMDD_HHMMSS.xlsx`).
- **Logs**: All logs are written to the `logs/` folder and also printed to the console for real-time monitoring.

## Testing

- Unit tests are provided in the `tests/` folder. Run all tests with:
  ```sh
  python -m unittest discover tests
  ```

## Code Coverage

To measure and report code coverage (and integrate with SonarCloud):

1. Install the required tools (in your virtual environment):
   ```sh
   pip install coverage pytest
   ```
2. Run your tests with coverage:
   ```sh
   coverage run -m pytest
   ```
3. See a coverage summary in the terminal:
   ```sh
   coverage report
   ```
4. (Optional) Generate an HTML report:
   ```sh
   coverage html
   # Open htmlcov/index.html in your browser
   ```
5. Generate a coverage XML report for SonarCloud:
   ```sh
   coverage xml
   ```
   This creates `coverage.xml` in your project root. The CI workflow and SonarCloud are configured to pick this up automatically.

## Development & Contribution

- All dependencies are managed in `pyproject.toml` via Poetry.
- If you need a `requirements.txt` for legacy tools, export it using Poetry as described above.
- Please ensure new code is covered by tests and passes static analysis.

---

## CI Test Quick Fix for Azure Key Vault

If you see errors in GitHub Actions or CI like:

```
ValueError: vault_url must be the URL of an Azure Key Vault
```

add this step to your GitHub Actions workflow before running tests to set a dummy Key Vault URL:

```yaml
- name: Set dummy Key Vault URL for tests
  run: echo "KEY_VAULT_URL=https://dummy.vault.azure.net/" >> $GITHUB_ENV
```

This allows your tests to import the code without requiring a real Azure Key Vault during CI. For best practice, refactor your code so that Azure clients are only created when needed, not at import time.

---

## License

MIT License
