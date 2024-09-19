'''
Scraper for your desired Careers page.

Please change the filtered_url variable to reflect the URL with the basic website filters you want applied.
'''

from asyncio import gather, sleep as async_sleep, Semaphore, CancelledError
from json import load as json_load, dump as json_dump
from playwright.async_api import async_playwright
from random import uniform, randint
from re import search as re_search


# Global Variables
## Base URL for your career/job website
base_url = "https://nvidia.wd5.myworkdayjobs.com"
## Filtered URL for your jobs website
filtered_url = "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?locationHierarchy1=2fcb99c455831013ea52fb338f2932d8&locationHierarchy2=0c3f5f117e9a0101f63dc469c3010000&timeType=5509c0b5959810ac0029943377d47364&jobFamilyGroup=0c40f6bd1d8f10ae43ffaefd46dc7e78&jobFamilyGroup=0c40f6bd1d8f10ae43ffbd1459047e84&workerSubType=0c40f6bd1d8f10adf6dae161b1844a15&workerSubType=0c40f6bd1d8f10adf6dae2cd57444a16"


# CAPTCHA Avoidance
## Add "Human-like" delays
async def human_like_delay(min_delay=1.5, max_delay=3.5):
    delay = uniform(min_delay, max_delay)
    await async_sleep(delay)

## Simulates mouse movements
async def mimic_mouse_movements(page):
    width, height = await page.evaluate('() => [window.innerWidth, window.innerHeight]')
    for _ in range(randint(5, 10)):
        x = randint(0, width)
        y = randint(0, height)
        try:
            await page.mouse.move(x, y, steps=randint(10, 25))
            await human_like_delay(0.1, 0.5)
        except CancelledError:
            print("Task was cancelled prematurely in mimic_mouse_movements()")
            raise
        except Exception as e:
            print(f"Error in mimic_mouse_movements() {e}")

## Simulates scrolling
async def scroll_page(page):
    for _ in range(randint(2, 5)):
        try:
            await page.evaluate(f'window.scrollBy(0, {randint(200, 400)});')
            await human_like_delay(0.5, 1)
        except CancelledError:
            print("Task was cancelled prematurely in scroll_page()")
            raise
        except Exception as e:
            print(f"Error in scroll_page(): {e}")

## Load cookies from a JSON file
async def load_cookies(page):
    try:
        with open('cookies.json', 'r') as f:
            cookies = json_load(f)
            await page.context.add_cookies(cookies)
    except FileNotFoundError:
        pass
    except CancelledError:
        print("Task was cancelled prematurely in scroll_page()")
        raise
    except Exception as e:
        print(f"Error in load_cookies(): {e}")

## Save cookies to a JSON file
async def save_cookies(page):
    try:
        cookies = await page.context.cookies()
        with open('cookies.json', 'w') as f:
            json_dump(cookies, f)
    except CancelledError:
        print("Task was cancelled prematurely in save_cookies()")
        raise
    except Exception as e:
        print(f"Error in save_cookies(): {e}")


# Website scraping and parsing
## Extract job details from the job details page
async def extract_job_details(page):
    try:       
        # Extract salary using regex
        salary_regex = r"The base salary range is ([\d,]+ USD - [\d,]+ USD)"
        page_text = await page.content()
        match = re_search(salary_regex, page_text)
        salary = match.group(1) if match else "Not specified"
        
        return {"salary": salary}
    except Exception as e:
        return {"salary": "Not specified"}

## Scrape web page and parallel tab loading
async def website_jobs():
    try: 
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Load cookies if they exist
            await load_cookies(page)

            # Set "human-like" user-agent
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })

            # Navigate to the careers website
            await page.goto(filtered_url, wait_until='networkidle')

            # Simulate "human-like" behaviors
            await human_like_delay(2, 4)
            await scroll_page(page)
            await mimic_mouse_movements(page)

            # Wait for job titles to load
            await page.wait_for_selector("a[data-automation-id='jobTitle']")

            # Extract all job titles and links
            jobs = await page.query_selector_all("a[data-automation-id='jobTitle']")
            job_data = []

            # Limit number of tabs open
            semaphore = Semaphore(5)

            # Parse job details
            async def process_job(job):
                async with semaphore:
                    try:
                        title = await job.text_content()
                        relative_link = await job.get_attribute('href')
                        link = base_url + relative_link

                        # Open a new tab for each job
                        detail_page = await browser.new_page()
                        await detail_page.goto(link, wait_until='networkidle')

                        # Extract salary from the job details page
                        job_details = await extract_job_details(detail_page)
                        await detail_page.close()

                        # Append job data
                        job_data.append({
                            'title': title,
                            'link': link,
                            'salary': job_details['salary'],
                        })

                    except Exception as e:
                        print(f"Error processing job: {e}")

            # Process all jobs concurrently
            await gather(*[process_job(job) for job in jobs])

            # Save cookies for future sessions
            await save_cookies(page)

            # Close the browser
            await browser.close()

            # Print the job results
            print("\n--- Scraped Jobs ---")
            for idx, job in enumerate(job_data, start=1):
                print(f"{idx}. Title: {job['title']}")
                print(f"   Link: {job['link']}")
                print(f"   Salary: {job['salary']}")
                print("-" * 30)

            return job_data
    except CancelledError:
        print("Task was cancelled prematurely in website_jobs()")
        raise
    except Exception as e:
        print(f"Error in website_jobs() {e}")
