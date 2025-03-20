from typing import Optional
from dataclasses import dataclass
from playwright.async_api import Locator, Playwright, BrowserType


@dataclass(frozen=True)
class Job:
    title: str
    company: str
    location: str
    job_url: str
    salary: Optional[str] = None
    posted_date: Optional[str] = None
    employment_type: Optional[str] = None


class JobSraper:
    def __init__(
        self,
        playwright: Playwright,
        browser_name: str,
        base_url: str
    ):
        self.jobs = []
        self.job_set = set()
        self.base_url = base_url
        self.browser_type: BrowserType = getattr(playwright, browser_name)

    async def _safe_text_content(self, locator: Locator) -> str:
        if await locator.count() > 0:
            return await locator.text_content()

        return None

    async def _safe_evaluate(self, locator: Locator, script: str) -> str:
        if await locator.count() > 0:
            return await locator.evaluate(script)

        return None

    async def _scrape_job(self, job_item: Locator) -> dict[str, str]:
        await job_item.locator('.jobListHeaderPanel .jobListPosition').click()
        await self.page.wait_for_load_state('networkidle')

        job = {
            'title': await self._safe_text_content(self.page.locator('#td_jobpositionnolink')),
            'salary': await self._safe_text_content(self.page.locator('#md_rate')),
            'company': await self._safe_evaluate(
                self.page.locator('#td_posted_by'),
                'node => node.lastChild.textContent.trim()'
            ),
            'location': await self._safe_text_content(self.page.locator('#md_location')),
            'job_url': await self._safe_text_content(self.page.locator('#md_permalink')),
            'posted_date': await self._safe_evaluate(
                self.page.locator('#td_posted_date'),
                'node => node.lastChild.textContent.trim()'
            ),
            'employment_type': await self._safe_text_content(self.page.locator('#td_job_type'))
        }

        await self.page.go_back()
        return job

    def _validate_job_fields(self, job: dict[str, str]) -> bool:
        required_fields = ['title', 'company', 'job_url', 'location']
        fields = self._to_clean_dict(job)
        return all(field in fields for field in required_fields)

    def _to_clean_dict(self, data: dict[str, str]) -> dict[str, str]:
        return {k: v for k, v in data.items() if v is not None}

    def _is_job_unique(self, job: dict[str, str]) -> bool:
        cleaned_job = {}
        job = self._to_clean_dict(job)
        for field_name, value in job.items():
            cleaned = value.strip().lower()
            cleaned_job[field_name] = cleaned

        job = Job(**cleaned_job)
        if job in self.job_set:
            return False

        self.job_set.add(job)
        return True

    async def run(self):
        browser = await self.browser_type.launch(headless=True)
        self.page = await browser.new_page()

        await self.page.goto(self.base_url, timeout=60000)
        await self.page.wait_for_load_state('networkidle')
        await self.page.locator('text=Classic View').click()
        await self.page.wait_for_load_state('networkidle')

        while True:
            job_items = self.page.locator('div.jobListItem.newjobsum')
            count = await job_items.count()
            for i in range(count):
                job = await self._scrape_job(job_items.nth(i))
                if self._validate_job_fields(job) and self._is_job_unique(job):
                    self.jobs.append(self._to_clean_dict(job))

            next_btn = self.page.locator('#jobListPagingControl a[title="Next Page"]')
            if await next_btn.count() == 0:
                break

            await next_btn.click()
            await self.page.wait_for_load_state('networkidle')

        await browser.close()
