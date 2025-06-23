# Version 2.8.2: Enhanced HTTP headers to better emulate real browsers

import feedparser, json, uuid, os, csv, requests
from datetime import datetime, timedelta, timezone
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AzureOpenAI
from dotenv import load_dotenv
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv("OPENAI_API_BASE")
)

model_name = os.getenv("OPENAI_DEPLOYMENT")
search_client = SearchClient(
    endpoint=os.getenv("SEARCH_API_ENDPOINT"),
    index_name="news-articles-index",
    credential=AzureKeyCredential(os.getenv("SEARCH_API_KEY"))
)

feeds = [
    # News & Science
    "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
    "https://www.sciencedaily.com/rss/matter_energy/nuclear_energy.xml",
    "https://www.sciencedaily.com/rss/matter_energy/quantum_physics.xml",
    "https://www.nasa.gov/rss/dyn/breaking_news.rss",
    "https://phys.org/rss-feed/breaking/",
    "https://www.sciencedaily.com/rss/all.xml",
    "https://www.newscientist.com/feed/home",
    "https://www.science.org/rss/news_current.xml",
    "https://www.the-scientist.com/rss",
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/rss",
    "https://feeds.arstechnica.com/arstechnica/index",
    "https://www.engadget.com/rss.xml",

    # Global News
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms",
    "https://www3.nhk.or.jp/rss/news/cat0.xml",
    "https://www.cbc.ca/cmlink/rss-world",
    "https://canarymedia.com/rss.rss",
    "https://apnews.com/index.rss",
    "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",

    # Nuclear Policy, Regulation, and Advocacy
    "https://nuclear-news.net/feed/",
    "https://neutronbytes.com/feed/",
    "https://www.iaea.org/rss/news.xml",
    "http://thebulletin.org/search-feed",
    "https://carnegieendowment.org/feed/proliferation-news"
]

keywords = [
    # Core nuclear terms
    "nuclear", "LPO", "DOE", "NRC", "IAEA", "tritium", "uranium", "atomic", "fusion", "fission", "reactor",
    "plasma", "neutron", "isotope", "radiation", "particle", "quantum",

    # Advanced technical terms
    "deuterium", "tokamak", "breeder reactor", "high energy physics", "radioisotope", "criticality",
    "chain reaction", "nuclear waste", "spent fuel", "containment", "reprocessing",
    "coolant leak", "thermal neutron", "cross-section", "nuclear fuel cycle",

    # Policy & disarmament
    "arms control", "nuclear treaty", "non-proliferation", "START", "CTBT", "NPT", "deterrence", "disarmament",

    # Emerging science terms
    "muon", "stellarator", "quark", "superconducting", "fusion ignition", "neutrino", "synchrotron"
]
one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
excel_file = f"news_results_{timestamp}.xlsx"
headers = ["Title", "Summary", "URL", "Author", "Tags", "PublishedDate", "Source"]

if not os.path.exists(excel_file):
    wb = Workbook()
    ws = wb.active
    ws.append(headers)
    wb.save(excel_file)
print(f"📁 Excel output saved to: {os.path.abspath(excel_file)}")

wb = load_workbook(excel_file)
ws = wb.active

existing_urls = {row[2] for row in ws.iter_rows(min_row=2, values_only=True) if row[2]}

def fetch_feed_with_timeout(url, timeout=10):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/",
        "DNT": "1",
    }
    try:
        resp = requests.get(url, timeout=timeout, headers=headers)
        resp.raise_for_status()
        return feedparser.parse(resp.content)
    except Exception as e:
        print(f"⚠️ Failed to fetch {url} → {e}")
        return None

def matches_keywords(text):
    text = text.lower()
    return any(k in text for k in keywords)

for url in feeds:
    print(f"\n📡 Parsing feed: {url}")
    feed = fetch_feed_with_timeout(url)
    if not feed:
        continue

    print(f"→ Found {len(feed.entries)} entries.")

    for entry in feed.entries:
        published_str = entry.get("published", None)
        try:
            published_dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc) if published_str else datetime.now(timezone.utc)
        except:
            published_dt = datetime.now(timezone.utc)

        if published_dt < one_week_ago:
            print(f"🕒 Skipping old article: {entry.title}")
            continue

        combined_text = entry.title + " " + entry.get("summary", "")
        if not matches_keywords(combined_text):
            print(f"⏭️ Skipping (no keyword match): {entry.title}")
            continue

        if entry.link in existing_urls:
            print(f"⏭️ Skipping duplicate URL: {entry.title}")
            continue

        print(f"🔍 Matched article: {entry.title}")

        content = entry.get("summary", "")
        if not content:
            print("⚠️ No summary available in RSS feed.")
            continue

        try:
            translation_prompt = f"Translate this to English (if not already), then summarize:\n{content[:4000]}"
            print("💬 Sending translation + summary request to OpenAI...")
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": translation_prompt}],
                temperature=0.3
            )
            summary = response.choices[0].message.content.strip()
            print(f"✅ Got summary (preview): {summary[:200]}...")
        except Exception as e:
            print(f"❌ Error summarizing article: {e}")
            continue

        doc = {
            "id": str(uuid.uuid4()),
            "title": entry.title,
            "summary": summary,
            "url": entry.link,
            "author": entry.get("author", "Unknown"),
            "tags": [k for k in keywords if k in content.lower()],
            "publishedDate": published_dt.isoformat(),
            "source": feed.feed.get("title", "RSS Source"),
            "content": content[:8000]
        }

        try:
            result = search_client.upload_documents(documents=[doc])
            print("📤 Uploaded:", doc["title"], "Status:", result[0].status_code if hasattr(result[0], 'status_code') else "Success")
        except Exception as e:
            print(f"❌ Error uploading to Azure Search: {e}")
            continue

        ws.append([
            doc["title"],
            summary,
            doc["url"],
            doc["author"],
            ", ".join(doc["tags"]),
            doc["publishedDate"],
            doc["source"]
        ])
        existing_urls.add(doc["url"])

        with open("upload.log", "a", encoding="utf-8") as logf:
            logf.write(json.dumps(doc, indent=2) + "\n\n")

wb.save(excel_file)
print("✅ Job complete.")
print(f"📁 Excel output saved to: {os.path.abspath(excel_file)}")