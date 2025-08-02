# Amazon Job Listings Scraping

Scrapes job listings from the Amazon Software Development job category page.

[Amazon jobs URL](https://www.amazon.jobs/content/en/job-categories/software-development#search)

---

## Objective

Develop a Scrapy spider to extract job listing data from the Amazon careers page, specifically focusing on **Software Development** positions within the **United States**.

---

## Tasks

1. **Set Up Scrapy Project**  
   - Initialize a new Scrapy project (if not already done).

2. **Inspect the Target Page**  
   - Visit the [Amazon Job Categories](https://www.amazon.jobs/content/en/job-categories/software-development#search) page.  
   - Identify the structure of each job listing (e.g., title, location, link, description snippet).  
   - Apply filters to focus on **US-based jobs**.

3. **Develop the Spider**  
   Extract the following fields:
   - Job Title  
   - Location  
   - Job URL  
   - Description Snippet (if available)  
   - Last Updated (if available)

   Additionally, follow each job's detail page to extract:
   - Full Job Description  
   - Basic Qualifications  
   - Preferred Qualifications  
   - Job ID  

4. **Implement Pagination**  
   - Ensure the spider can navigate through all available pages.

5. **Save the Data**  
   - Export the data in structured **JSON** format.

6. **Handle Dynamic Content (if present)**  
   - If the site uses JavaScript to render data, describe how you would approach this using Scrapy (e.g., using Splash or Selenium integration).

---

## Installation & Setup

Install Scrapy via **conda**:

```bash
conda install -c conda-forge scrapy
```

Or using pip:

```bash
pip install scrapy
```

To create the Scrapy project: 

```bash
scrapy startproject amazon_jobs
```

Project Structure:

```markdown
amazon_jobs/
├── .gitignore
├── scrapy.cfg
├── README.md
├── jobs.json
├── amazon_jobs/
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders/
│       ├── __init__.py
│       └── amazon.py
```
