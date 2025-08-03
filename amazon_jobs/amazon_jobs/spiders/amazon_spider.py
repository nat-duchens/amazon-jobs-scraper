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
            "size": 20, # To obtain only the first 20 jobs
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
        import json
        from datetime import datetime

        # Parse the JSON response body
        data = json.loads(response.text)

        # Loop through the list of job entries returned by the API
        for job in data.get("searchHits", []):
            fields = job.get("fields", {})

            job_id = fields.get("artJobId", [""])[0]  # Extract the real job ID
            posted_timestamp = fields.get("updatedDate", [""])[0] # Convert the posted date timestamp format
            try:
                posted_date = datetime.utcfromtimestamp(int(posted_timestamp)).isoformat() # ISO format 
            except:
                posted_date = ""

            # Produce a dictionary with the extracted job data 
            yield {
                "Job Title": fields.get("title", [""])[0],
                "Location": fields.get("normalizedLocation", [""])[0],
                "Job ID": job_id,
                "Job URL": f"https://www.amazon.jobs/en/jobs/{job_id}",
                "Description Snippet": fields.get("shortDescription", [""])[0],
                "Posted Date": posted_date
            }