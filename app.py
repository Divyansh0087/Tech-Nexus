import streamlit as st
import feedparser
import arxiv
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Tech-Nexus", layout="wide")

st.title("Tech-Nexus")
st.caption("From research → code → startups, in one place")

# ---------- TechCrunch ----------
def get_techcrunch():
    feed = feedparser.parse("https://techcrunch.com/feed/")
    return feed.entries[:3]

# ---------- arXiv ----------
def get_arxiv():
    client = arxiv.Client()
    search = arxiv.Search(
        query="LLM inference OR AI chips",
        max_results=3,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    return list(client.results(search))

# ---------- GitHub ----------
def get_github():
    url = "https://github.com/trending"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    return soup.find_all("article", class_="Box-row")[:3]


col1, col2, col3 = st.columns(3)

# BUSINESS
with col1:
    st.subheader("📰 Business & Startups")
    for entry in get_techcrunch():
        st.markdown(f"**{entry.title}**")
        st.markdown(f"[Read →]({entry.link})")
        st.divider()

# RESEARCH
with col2:
    st.subheader("🔬 Research (AI)")
    for paper in get_arxiv():
        summary = paper.summary.replace("\n", " ").split(".")[0]
        st.markdown(f"**{paper.title}**")
        st.markdown(f"[PDF →]({paper.pdf_url})")
        st.caption(summary + "...")
        st.divider()

# CODE
with col3:
    st.subheader("💻 Trending Code")
    for repo in get_github():
        name = repo.find("h2").text.strip().replace("\n", "")
        link = "https://github.com" + repo.find("a")["href"]
        desc = repo.find("p")
        st.markdown(f"**{name}**")
        st.markdown(f"[Repo →]({link})")
        st.caption(desc.text.strip() if desc else "No description")
        st.divider()