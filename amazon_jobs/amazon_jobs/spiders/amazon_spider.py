import scrapy
import json
from datetime import datetime

## Remember NOT to run the code here!
## Use bash an run in root directory: 'scrapy crawl amazon_jobs -o jobs.json'

# (CONFIG) → Define the spider for crawling Amazon Jobs API
class AmazonJobsAPISpider(scrapy.Spider):
    name = "amazon_jobs"
    allowed_domains = ["www.amazon.jobs"]  # Restrict crawling to this domain only

    MAX_jobs = 25 # To define a limit of total number of job fetch and control pagination

    # (FETCHING) → Send the initial POST request to the API endpoint
    def start_requests(self):
        self.url = "https://www.amazon.jobs/api/jobs/search?is_als=true"  # Base API endpoint (found with Devtools)

        # (CONFIG) → HTTP headers to simulate a browser
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        # (CONFIG) → Define pagination parameters
        self.size = 20
        self.start_index = 0
        self.job_count = 0 # Counter for total jobs collected

        # (FETCHING) → Start crawling with initial index
        yield self.build_request(self.start_index)

    # Function to construct and return a request with a given pagination index
    def build_request(self, start_index):

        # (CLEANING and STRUCTURING) → Prepare JSON payload to filter jobs (US + Software Development)
        payload = { 
            "accessLevel": "EXTERNAL",
            "contentFilterFacets": [{"name": "primarySearchLabel", "requestedFacetCount": 9999}],
            "excludeFacets": [
                {"name": "isConfidential", "values": [{"name": "1"}]},
                {"name": "businessCategory", "values": [{"name": "a-confidential-job"}]}
            ],
            "filterFacets": [
                {"name": "category", "requestedFacetCount": 9999, "values": [{"name": "Software Development"}]}
            ],
            "includeFacets": [],
            "jobTypeFacets": [],
            "locationFacets": [[
                {"name": "country", "requestedFacetCount": 9999, "values": [{"name": "US"}]},
                {"name": "normalizedStateName", "requestedFacetCount": 9999},
                {"name": "normalizedCityName", "requestedFacetCount": 9999}
            ]],
            "query": "",
            "size": self.size,
            "start": start_index,  # (PAGINATION) → Set the starting index for the request
            "treatment": "OM",
            "sort": {"sortOrder": "DESCENDING", "sortType": "SCORE"}
        }

        # (FETCHING) → Return the constructed POST request with callback and pagination context
        return scrapy.Request(
            url=self.url,
            method="POST",
            body=json.dumps(payload),
            headers=self.headers,
            callback=self.parse,
            cb_kwargs={"start_index": start_index}  # (PAGINATION) → Pass current index to parse method
        )
    
    # (PARSING and EXTRACTION) → Process the API response and extract job data
    def parse(self, response, start_index):
        data = json.loads(response.text) # Load JSON response

        # (EXTRACTION) → Get job listings and total count
        jobs = data.get("searchHits", [])
        total_found = data.get("found", 0)

        # (LOOPING) → Iterate over each job entry
        for job in jobs:
            if self.job_count >= self.MAX_jobs:
                return  # (CONTROL) → Stop if the job limit is reached

            fields = job.get("fields", {})
            job_id = fields.get("icimsJobId", [""])[0] # (EXTRACTION) → Get the job ID 
            posted_timestamp = fields.get("updatedDate", [""])[0] # (EXTRACTION) →Get posted timestamp

            # (CLEANING) → Convert timestamp to readable ISO date
            try:
                posted_date = datetime.utcfromtimestamp(int(posted_timestamp)).isoformat()
            except:
                posted_date = ""

            # (STRUCTURING) → Yield a clean job object with relevant fields
            yield {
                "Job Title": fields.get("title", [""])[0],
                "Location": fields.get("normalizedLocation", [""])[0],
                "Job ID": job_id,
                "Job URL": f"https://www.amazon.jobs/en/jobs/{job_id}",
                "Description Snippet": fields.get("shortDescription", [""])[0],
                "Posted Date": posted_date
            }

            self.job_count += 1 # Increment job counter 

        # (PAGINATION) → Continue crawling next page if job limit not reached and more jobs are available
        if self.job_count < self.MAX_jobs and start_index + self.size < total_found:
            yield self.build_request(start_index + self.size)    