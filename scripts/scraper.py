import requests
from bs4 import BeautifulSoup
import time
import json
import os

def audit_website(url):
    """Fetch a website and extract factual data (no AI, no opinions)."""
    result = {
        "url": url,
        "status": "success",
        "data": {}
    }

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Educational Audit Bot; student project)"
        }
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=10)
        load_time = round(time.time() - start_time, 2)

        if response.status_code != 200:
            result["status"] = "error"
            result["data"]["error"] = f"HTTP {response.status_code}"
            return result

        soup = BeautifulSoup(response.text, "html.parser")

        # 1. Title
        title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"

        # 2. Meta description
        meta_tag = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta_tag["content"].strip() if meta_tag and meta_tag.get("content") else "Missing"

        # 3. Headings
        h1_count = len(soup.find_all("h1"))
        h2_count = len(soup.find_all("h2"))

        # 4. Links
        all_links = soup.find_all("a", href=True)
        total_links = len(all_links)

        # 5. Images and alt text
        images = soup.find_all("img")
        total_images = len(images)
        images_missing_alt = len([img for img in images if not img.get("alt")])

        # 6. Contact info detection (simple pattern search)
        page_text = soup.get_text().lower()
        has_email = "@" in page_text and any(ext in page_text for ext in [".com", ".org", ".edu", ".net"])
        has_phone = any(char.isdigit() for char in page_text)

        # 7. Language attribute
        lang = soup.html.get("lang") if soup.html else None

        result["data"] = {
            "title": title,
            "meta_description": meta_desc,
            "load_time_seconds": load_time,
            "h1_count": h1_count,
            "h2_count": h2_count,
            "total_links": total_links,
            "total_images": total_images,
            "images_missing_alt": images_missing_alt,
            "has_email_pattern": has_email,
            "has_phone_pattern": has_phone,
            "html_lang": lang,
            "http_status": response.status_code
        }

    except requests.exceptions.Timeout:
        result["status"] = "error"
        result["data"]["error"] = "Timeout - site took too long"
    except requests.exceptions.ConnectionError:
        result["status"] = "error"
        result["data"]["error"] = "Connection error - site unreachable"
    except Exception as e:
        result["status"] = "error"
        result["data"]["error"] = f"Unexpected: {str(e)}"

    return result


def main():
    # Read target URLs
    with open("data/targets.txt", "r") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    print(f"Found {len(urls)} target websites.\n")

    all_results = []

    for url in urls:
        print(f"Auditing: {url}")
        result = audit_website(url)
        all_results.append(result)

        if result["status"] == "success":
            d = result["data"]
            print(f"   ✓ Title: {d['title'][:50]}")
            print(f"   ✓ Load time: {d['load_time_seconds']}s")
            print(f"   ✓ H1: {d['h1_count']} | H2: {d['h2_count']}")
        else:
            print(f"   ✗ Failed: {result['data'].get('error')}")

        print()
        time.sleep(1.5)  # Polite delay between requests

    # Save raw results to JSON
    os.makedirs("data", exist_ok=True)
    with open("data/raw_facts.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"Done! Raw facts saved to data/raw_facts.json")


if __name__ == "__main__":
    main()