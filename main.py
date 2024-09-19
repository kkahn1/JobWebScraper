from asyncio import run as async_run
from websites.nvidia_scraper import nvidia_jobs

# Main function to run the scraper
async def run_scrapers():
    print("Starting NVIDIA job scraper...")
    await website_jobs()

if __name__ == "__main__":
    async_run(run_scrapers())
