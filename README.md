# Job Listing Web Scraper

## Description: This web scraper helps pull recent job listings from your favorite company's websites.

### Future plans: Add in the ability to use your existing Workday logins or Resume to automate the process of applying to jobs that match strict criteria.

### To Use: This project uses Docker containerization to both automate the setup process for the script as well as to help protect your computer from possible exploits.

1. Install Docker if you do not already have it installed.
    Windows: https://docs.docker.com/desktop/install/windows-install/
    Mac: https://docs.docker.com/desktop/install/mac-install/
    Linux: https://docs.docker.com/desktop/install/linux/
2. Open a terminal in the directory where your Dockerfile, requirements.txt, etc. files are located
3. Before running the script, locate the desired scrapers inside the websites folder, and update the scraper with a pre-filtered URL. What this means is you should go to the careers page for the company that you want to have scraped, and apply the filters you want before copying the URL and pasting it into the python file.
4. Build the scraper file with: `docker build -t playwright-scraper .`
5. Next, run the script with `docker run --rm playwright-scraper`
6. The scraper will run inside the container and output the found jobs
