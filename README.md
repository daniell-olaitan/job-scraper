# JobServe Scraper - Web Data Extraction Project

## Project Description
This project is a **web scraper** built using **Python** and **Playwright**. It extracts job listings from [JobServe UK](https://jobserve.com/gb/en/JobSearch.aspx?shid=1733D5765A89D1D1D78F&l=United+Kingdom) based on the provided specifications.

The scraper collects the following details from each job post:
- Job Title
- Company
- Location
- Salary (if available)
- Job URL
- Posted Date (if available)
- Employment Type (if available)

The extracted data is saved in a structured **JSON file** following the required schema.

---

## Tech Stack
- **Python >= 3.9**
- **Playwright**
- **JSON**

---

## Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/daniell-olaitan/job-scraper.git
   cd job-scraper
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers (if not installed):**
   ```bash
   playwright install
   ```

---

## Usage
Run the scraper using:
```bash
python main.py
```
The output will be generated in `jobserve_jobs.json`.

---

## Output
The final output is stored in [jobserve_jobs.json](./jobserve_jobs.json) and follows the required schema:
```json
{
  "jobs": [
    {
      "title": "Delivery Manager - AI innovation",
      "salary": "£525 per day",
      "company": "Digital Skills Ltd",
      "location": "London, UK",
      "job_url": "http://www.jobserve.com/cFBY5",
      "posted_date": "Monday, 17 March 2025",
      "employment_type": "Contract"
    },
    ...
  ]
}
```
