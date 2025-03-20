# 📚 MedQueryPy - Fetch PubMed Research Papers with AI

🚀 **MedQueryPy** is a Python package designed to fetch research papers from PubMed and filter those with non-academic authors affiliated with pharmaceutical or biotech companies. Now, with **AI-powered author classification and research paper summarization**, the package is smarter than ever!

---

## 📌 Features
✅ Fetches research papers using the **PubMed API**  
✅ Identifies papers with **non-academic authors** from biotech/pharma companies using **AI**  
✅ Uses **GPT-4** to summarize research papers 📄  
✅ Saves results in **CSV format**  
✅ Provides a **command-line interface & Python module**  
✅ **Poetry-based dependency management**  
✅ Optimized for **fast and efficient queries**  

---

## 🛠 Installation
You can install **MedQueryPy** via pip:
```bash
pip install medquerypy
```

---

## 🚀 Usage

### **🔍 Import as a Python Module**
```python
from medquerypy import PubMedFetcher

# Define a search query
query = "COVID-19 vaccines"

# Fetch paper IDs
paper_ids = PubMedFetcher.fetch_pubmed_papers(query)
print("Paper IDs:", paper_ids)

# Fetch details of each paper
results = [PubMedFetcher.get_paper_details(pid) for pid in paper_ids]
print("Paper Details:", results)

# Check if an affiliation is non-academic using AI
affiliation = "XYZ Biotech"
print("Is non-academic:", PubMedFetcher.is_non_academic(affiliation))

# Summarize a research paper using AI
abstract = "This study investigates the effect of COVID-19 vaccines on different age groups..."
summary = PubMedFetcher.summarize_paper(abstract)
print("Summary:", summary)

# Save results to CSV
PubMedFetcher.save_to_csv(results, "output.csv")
print("Results saved to output.csv")
```

### **📂 Use as a Command-Line Tool**
#### Fetch papers and print results:
```bash
get-papers-list "COVID-19 vaccines"
```

#### Save results to a CSV file:
```bash
get-papers-list "COVID-19 vaccines" -f results.csv
```

#### Enable Debug Mode:
```bash
get-papers-list "COVID-19 vaccines" -d
```

---

## 🏗 Project Structure
```
medquerypy/
│── medquerypy/        # Package directory
│   │── __init__.py    # Makes the folder a Python package
│   │── fetcher.py     # Module for fetching PubMed papers & AI processing
│── cli.py             # Command-line interface script
│── README.md          # Documentation
│── pyproject.toml     # Poetry configuration
│── poetry.lock        # Poetry lock file
│── .gitignore         # Git ignore file
```

---

## 🤖 Technology Stack
- **Python** 🐍
- **Requests** (for API calls) 🌐
- **OpenAI GPT-4** (for AI-based filtering & summarization) 🧠
- **CSV** (for saving results) 📊
- **Poetry** (for package management) 📦

---

## ⚡ How It Works
1. The CLI takes a **search query** as input.
2. Fetches **PubMed papers** matching the query.
3. Uses **AI to identify non-academic authors**.
4. Uses **AI to summarize research papers**.
5. Outputs results to **console or CSV**.

---

## 🌟 Contributing
🎯 Contributions are welcome! Feel free to fork the repo and submit a PR.

---

## 📄 License
📝 MIT License. See [LICENSE](LICENSE) for details.
