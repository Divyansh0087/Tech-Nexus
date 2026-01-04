import feedparser
import arxiv
import requests
from bs4 import BeautifulSoup

def get_techcrunch_news():
    print("\n--- 📰 BUSINESS & STARTUPS (Source: TechCrunch) ---")
    # TechCrunch provides a free RSS feed
    feed = feedparser.parse('https://techcrunch.com/feed/')
    
    # We only want the top 3 latest stories
    for entry in feed.entries[:3]:
        print(f"🔹 {entry.title}")
        print(f"   🔗 {entry.link}")
        print(f"   📅 {entry.published[:16]}") # Trimming the date for cleaner look
        print("-" * 40)

def get_arxiv_research():
    print("\n--- 🔬 LATEST RESEARCH (Source: ArXiv CS.AI) ---")
    # Query for the latest 3 papers in Artificial Intelligence
    client = arxiv.Client()
    search = arxiv.Search(
        query = "cat:cs.AI", # Category: Computer Science / AI
        max_results = 3,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )

    for result in client.results(search):
        print(f"🔹 {result.title}")
        print(f"   🔗 {result.pdf_url}")
        # Printing just the first sentence of the abstract
        summary = result.summary.replace('\n', ' ').split('.')[0]
        print(f"   📝 {summary}...") 
        print("-" * 40)

def get_github_trending():
    print("\n--- 💻 TRENDING CODE (Source: GitHub) ---")
    # GitHub doesn't have a simple API for trending, so we "scrape" it
    url = "https://github.com/trending"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Finding the repo boxes (This structure is based on GitHub's current HTML)
    repos = soup.find_all('article', class_='Box-row')
    
    for repo in repos[:3]:
        # Extracting the repo name (Owner / Name)
        name_tag = repo.find('h2').find('a')
        repo_name = name_tag.text.strip().replace('\n', '').replace(' ', '')
        link = "https://github.com" + name_tag['href']
        
        # Extracting the description (if it exists)
        desc_tag = repo.find('p', class_='col-9')
        description = desc_tag.text.strip() if desc_tag else "No description."

        print(f"🔹 {repo_name}")
        print(f"   🔗 {link}")
        print(f"   📝 {description}")
        print("-" * 40)

# --- THE MAIN EXECUTION ---
if __name__ == "__main__":
    print("🚀 INITIALIZING 'LAB TO MARKET' PROTOTYPE...\n")
    
    try:
        get_techcrunch_news()
        get_arxiv_research()
        get_github_trending()
        
    except Exception as e:
        print(f"⚠️ An error occurred: {e}")
        print("Tip: If GitHub scraping fails, they might have changed their HTML structure.")