import scrapy
import json

## Remember not to run the code here, use bash: 'scrapy crawl amazon_jobs -o jobs.json'

# To run the spider
class AmazonJobsAPISpider(scrapy.Spider):
    name = "amazon_jobs"
    allowed_domains = ["www.amazon.jobs"]  # Restrict crawling to this domain only

    def start_requests(self):
        url = "https://www.amazon.jobs/api/jobs/search?is_als=true" # API endpoint to fetch job listings 
       
       # JSON payload to send with the POST request
        payload = { 
            "accessLevel": "EXTERNAL",
            "contentFilterFacets": [
                {"name": "primarySearchLabel", "requestedFacetCount": 9999}
            ],
            "excludeFacets": [
                {
                    "name": "isConfidential",
                    "values": [{"name": "1"}]
                },
                {
                    "name": "businessCategory",
                    "values": [{"name": "a-confidential-job"}]
                }
            ],
            "filterFacets": [
                {
                    "name": "category",
                    "requestedFacetCount": 9999,
                    "values": [{"name": "Software Development"}]
                }
            ],
            "includeFacets": [],
            "jobTypeFacets": [],
            "locationFacets": [[
                {"name": "country", "requestedFacetCount": 9999,
                 "values": [{"name": "US"}]},
                {"name": "normalizedStateName", "requestedFacetCount": 9999},
                {"name": "normalizedCityName", "requestedFacetCount": 9999}
            ]],
            "query": "",
            "size": 20,
            "start": 0,
            "treatment": "OM",
            "sort": {"sortOrder": "DESCENDING", "sortType": "SCORE"}
        }

        # Request headers to simulate a browser    
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        # Send a POST request to the API endpoint
        yield scrapy.Request(
            url=url,
            method="POST",
            body=json.dumps(payload),
            headers=headers,
            callback=self.parse
        )

    def parse(self, response):
        try:
            data = json.loads(response.text) # Parse the JSON response
        except Exception as e:
            self.logger.error(f"JSON parsing failed: {e}")
            return

        # Extract data
        for job in data.get("jobs", []):
            yield {
                "Job Title": job.get("title"),
                "Location": job.get("location"),
                "Job ID": job.get("id"),
                "Job URL": f"https://www.amazon.jobs/en/jobs/{job.get('id')}",
                "Description Snippet": job.get("descriptionSnippet"),
                "Posted Date": job.get("postedDate")
            }