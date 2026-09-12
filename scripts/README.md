# AI-Assisted Website Quality Auditor - Education Sector

An AI-powered tool that audits education-sector websites and generates a
professional, structured quality report - combining rule-based detection
(structural facts) with LLM-generated judgments (scores and recommendations).

This is a Week 4 portfolio project demonstrating AI-product thinking:
facts are separated from opinions, failures are handled gracefully, and the
output is a business-ready audit report.

---

## What It Does

1. Scrapes 6 education-sector websites (homepage only, politely).
2. Extracts facts - title, meta description, headings, links, images, contact info, load time.
3. Sends facts to an LLM (Groq / Llama) to get an AI-generated quality score, missing-feature list, and prioritized recommendations.
4. Generates a clean report in both CSV and HTML formats - with facts and AI judgments clearly separated.

---

## Architecture

```
targets.txt --> scraper.py --> ai_auditor.py --> report_generator.py
                    |              |                    |
                    v              v                    v
            data/raw_facts.json  data/ai_judgments.json  reports/*.{csv,html}
```

---

## Project Structure

```
edu-website-auditor/
|-- data/
|   |-- targets.txt
|   |-- raw_facts.json
|   +-- ai_judgments.json
|-- reports/
|   |-- audit_report.csv
|   +-- audit_report.html
|-- scripts/
|   |-- scraper.py
|   |-- ai_auditor.py
|   +-- report_generator.py
|-- .env
|-- .gitignore
|-- README.md
+-- requirements.txt
```

---

## Setup

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd edu-website-auditor
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Create a `.env` file in the root folder:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq key at: https://console.groq.com/keys

---

## How to Run

Run the three scripts in order:

```bash
# Step 1: Scrape websites for facts
python scripts/scraper.py

# Step 2: Ask the LLM to judge each site
python scripts/ai_auditor.py

# Step 3: Generate the final CSV + HTML report
python scripts/report_generator.py
```

Then open the report:

```bash
start reports/audit_report.html     # Windows
open reports/audit_report.html      # Mac
```

---

## Sample Results

| Website       | AI Score | Priority | Key Issue Detected               |
|---------------|----------|----------|----------------------------------|
| Khan Academy  | 15/100   | High     | Blocked by Cloudflare (bot wall) |
| Coursera      | 78/100   | Medium   | 18 images missing alt text       |
| edX           | 78/100   | High     | Missing H1 heading               |
| Udemy         | 70/100   | High     | Missing H1 + 8 alt texts         |
| Udacity       | 68/100   | High     | 99 images missing alt text       |
| FutureLearn   | N/A      | -        | HTTP 403 (blocked)               |

---

## Design Principles

### 1. Facts are not Opinions

Every report clearly separates:
- FACTS - objectively measured by the scraper (title, H1 count, image alt text count, etc.)
- AI JUDGMENT - subjective scores and recommendations from the LLM.

This makes the tool auditable - a human can verify any AI claim against the raw facts.

### 2. Graceful Failure

If a site returns a 403, times out, or gets blocked by Cloudflare, the
tool logs the failure and continues. It never crashes mid-run.

### 3. Specific Recommendations

The LLM is prompted to produce actionable advice (e.g., "Add a meta
description under 160 chars") rather than vague advice (e.g., "Improve SEO").

---

## Limitations and False Positives

| Limitation                | Impact                                                    |
|---------------------------|-----------------------------------------------------------|
| Static HTML scraping only | JS-heavy sites (React/Vue) may show incomplete data.      |
| Cloudflare / bot walls    | Sites like Khan Academy return a "Client Challenge" page. |
| Regex-based contact check | has_email_pattern can give false positives.               |
| No visual analysis        | The tool cannot judge design, colors, or UX quality.      |
| AI can hallucinate        | LLM recommendations should be reviewed by a human.        |

### What a human should still double-check:

- Whether an AI "missing feature" claim is actually correct.
- Whether a low score is due to the site's real quality or a scraping block.
- Whether recommendations align with the business's actual goals.

---

## Tech Stack

- Python 3.13
- requests + BeautifulSoup4 - scraping
- Groq SDK (Llama 3) - LLM judgments
- pandas - data structuring
- python-dotenv - API key management
- HTML + CSS - report presentation

---

## License

This project is for educational and portfolio purposes. Only publicly accessible
education-sector homepages are audited, read-only, with polite delays between requests.

---

## Author

Imbisaat Mahmood - Week 4 AI-Assisted Website Quality Auditor project.