import json
import asyncio
from scraper import JobSraper
from playwright.async_api import async_playwright

BASE_URL = 'https://jobserve.com/gb/en/JobSearch.aspx?shid=1733D5765A89D1D1D78F&l=United+Kingdom'


async def main():
    async with async_playwright() as playwright:
        job_scraper = JobSraper(playwright, 'chromium', BASE_URL)
        await job_scraper.run()

        jobs = {'jobs': job_scraper.jobs}
        with open("jobserve_jobs.json", "w",  encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=4)

        print(jobs)
        print(f"Scraping complete. Total jobs scraped: {len(job_scraper.jobs)}")
        print("Output saved to jobserve_jobs.json")


if __name__ == '__main__':
    asyncio.run(main())
