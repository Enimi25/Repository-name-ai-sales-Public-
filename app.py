from fastapi import FastAPI
import requests
import re
from urllib.parse import urlparse

app = FastAPI()

TAVILY_KEY = "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"

BAD_DOMAINS = [
    "amazon", "aliexpress", "ebay", "walmart", "etsy",
    "reddit", "quora", "zhihu", "medium", "youtube",
    "facebook", "twitter", "pinterest", "wikipedia",
    "wixpress", "sentry", "fda.gov", "amgen.com",
    "target.com", "shopify.com", "wix.com",
    "woocommerce.com", "bigcommerce.com",
    "help.", "support.", "docs.", "forum", "community"
]

BAD_EMAIL_PARTS = [
    "noreply", "no-reply", "donotreply",
    "jpg", "jpeg", "png", "webp", "gif", "svg",
    "example", "test@", "sentry", "wixpress"
]

GOOD_EMAIL_PREFIXES = [
    "info@", "hello@", "sales@", "contact@",
    "support@", "service@", "orders@", "team@"
]

QUERIES = [
    '"shop online" "contact us"',
    '"buy online" "contact us"',
    '"add to cart" "contact us"',
    '"online store" "contact"',
    '"our products" "contact us"',
    'inurl:shop "contact us"',
    'inurl:product "contact us"',
    '"free shipping" "contact us" "shop"',
    '"checkout" "contact us" "store"'
]


@app.get("/")
def root():
    return {"status": "ok", "version": "clean-leads-v2"}


def get_domain(url):
    try:
        return urlparse(url).netloc.replace("www.", "")
    except:
        return ""


def is_bad_url(url):
    u = url.lower()
    return any(bad in u for bad in BAD_DOMAINS)


def fetch(url):
    try:
        r = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=6
        )
        return r.text
    except:
        return ""


def extract_emails(text):
    emails = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text or ""
    )

    clean = []

    for email in emails:
        e = email.lower().strip()

        if len(e) > 80:
            continue

        if any(bad in e for bad in BAD_EMAIL_PARTS):
            continue

        clean.append(e)

    return list(set(clean))


def extract_contacts(url):
    base = url.rstrip("/")

    pages = [
        base,
        base + "/contact",
        base + "/contact-us",
        base + "/about",
        base + "/pages/contact",
        base + "/pages/contact-us"
    ]

    emails = []

    for page in pages:
        html = fetch(page)
        emails += extract_emails(html)

    return list(set(emails))


def looks_like_store(url, title, content):
    text = (url + " " + title + " " + content).lower()

    signals = [
        "shop", "store", "product", "products",
        "cart", "checkout", "buy online",
        "add to cart", "free shipping",
        "our products"
    ]

    return any(signal in text for signal in signals)


def email_quality_score(emails):
    if not emails:
        return 0

    score = 0

    for email in emails:
        if any(email.startswith(prefix) for prefix in GOOD_EMAIL_PREFIXES):
            score += 20
        else:
            score += 10

    return min(score, 40)


def score_lead(url, title, content, emails):
    text = (url + " " + title + " " + content).lower()
    score = 0

    if "shop" in text:
        score += 15

    if "store" in text:
        score += 15

    if "product" in text:
        score += 15

    if "add to cart" in text:
        score += 20

    if "checkout" in text:
        score += 15

    if "free shipping" in text:
        score += 10

    score += email_quality_score(emails)

    return min(score, 100)


@app.get("/pipeline")
def pipeline(limit: int = 10):
    leads = []
    seen_domains = set()

    for query in QUERIES:
        try:
            r = requests.post(
                "https://api.tavily.com/search",
                headers={"Authorization": f"Bearer {TAVILY_KEY}"},
                json={
                    "query": query,
                    "search_depth": "basic",
                    "max_results": limit
                },
                timeout=10
            )

            data = r.json()

            for item in data.get("results", []):
                url = item.get("url", "")
                title = item.get("title", "")
                content = item.get("content", "")

                if not url:
                    continue

                domain = get_domain(url)

                if not domain:
                    continue

                if domain in seen_domains:
                    continue

                if is_bad_url(url):
                    continue

                if not looks_like_store(url, title, content):
                    continue

                seen_domains.add(domain)

                emails = extract_contacts(url)
                lead_score = score_lead(url, title, content, emails)

                if lead_score < 30:
                    continue

                leads.append({
                    "lead_score": lead_score,
                    "domain": domain,
                    "url": url,
                    "title": title,
                    "emails": emails,
                    "has_email": len(emails) > 0,
                    "source_query": query
                })

        except:
            continue

    leads = sorted(leads, key=lambda x: x["lead_score"], reverse=True)

    return {
        "total": len(leads),
        "results": leads
    }


@app.get("/raw")
def raw(limit: int = 10):
    results = []

    for query in QUERIES:
        try:
            r = requests.post(
                "https://api.tavily.com/search",
                headers={"Authorization": f"Bearer {TAVILY_KEY}"},
                json={
                    "query": query,
                    "search_depth": "basic",
                    "max_results": limit
                },
                timeout=10
            )

            data = r.json()

            for item in data.get("results", []):
                results.append({
                    "query": query,
                    "url": item.get("url"),
                    "title": item.get("title"),
                    "content": item.get("content")
                })

        except:
            continue

    return {
        "total": len(results),
        "results": results
    }
