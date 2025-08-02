import scrapy

## Remember not to run the code here, use bash: 'scrapy crawl amazon_jobs -o jobs.json'

# To run the spider <
class AmazonSpider(scrapy.Spider):
    name = "amazon_jobs"

    # Restrict crawling to this domain only
    allowed_domains = ["amazon.jobs"]

    # Amazon jobs url to filter by US
    start_urls = [
        "https://www.amazon.jobs/en/search?job_function_id[]=software-development&loc_query=United+States"
    ]

    def parse(self, response):
        # Select all job cards using CSS selector, obtain with Devtools
        job_cards = response.css("div.job-tile")

        for job in job_cards:
            job_url = job.css("a::attr(href)").get() # Extract the job detail link 
            full_url = response.urljoin(job_url) 

            # Follow the job detail page
            yield scrapy.Request(
                full_url,
                callback=self.parse_job_detail,
                meta={'job_url': full_url} 
            )

        # Handle pagination 
        next_page = response.css("a.pagination-button[aria-label=Next]::attr(href)").get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_job_detail(self, response):
        # Extract data
        yield {
            "Job Title": response.css("h1::text").get(),  
            "Job Location": response.css("p.location-and-id::text").get(),  
            "Job URL": response.meta['job_url'],  
            "Description": response.css("div#job-description *::text").getall(),  
            "Basic Qualifications": response.xpath(
                "//h2[contains(text(), 'Basic Qualifications')]/following-sibling::ul[1]/li//text()"
            ).getall(),  
            "Preferred Qualifications": response.xpath(
                "//h2[contains(text(), 'Preferred Qualifications')]/following-sibling::ul[1]/li//text()"
            ).getall(), 
            "Job ID": response.xpath(
                "//p[contains(text(), 'Job ID')]/text()"
            ).re_first(r'Job ID: (.+)') 
        }
