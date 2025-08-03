import scrapy
import json
from datetime import datetime

## Remember not to run the code here, use bash: 'scrapy crawl amazon_jobs_test -o jobs_test.json'

### Since there is no limit on the number of returned jobs, it will return more than 1000 ###

# To run the spider
class AmazonJobsAPISpider(scrapy.Spider):
    name = "amazon_jobs_test"
    allowed_domains = ["www.amazon.jobs"]  # Restrict crawling to this domain only

    def start_requests(self):
        # Base API endpoint
        self.url = "https://www.amazon.jobs/api/jobs/search?is_als=true"

        # Define headers globally for reuse
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        # Request size and start index for pagination
        self.size = 20
        self.start_index = 0

        # Start crawling with initial index
        yield self.build_request(self.start_index)

    # Function to construct and return a request with a given pagination index
    def build_request(self, start_index):
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
            "start": start_index,  # Inject pagination start index
            "treatment": "OM",
            "sort": {"sortOrder": "DESCENDING", "sortType": "SCORE"}
        }

        return scrapy.Request(
            url=self.url,
            method="POST",
            body=json.dumps(payload),
            headers=self.headers,
            callback=self.parse,
            cb_kwargs={"start_index": start_index}  # Pass current index to parse method
        )

    def parse(self, response, start_index):
        data = json.loads(response.text)

        # Retrieve current job results and total count
        jobs = data.get("searchHits", [])
        total_found = data.get("found", 0)

        # Loop through each job record and yield a structured item
        for job in jobs:
            fields = job.get("fields", {})
            job_id = fields.get("artJobId", [""])[0]
            posted_timestamp = fields.get("updatedDate", [""])[0]

            try:
                posted_date = datetime.utcfromtimestamp(int(posted_timestamp)).isoformat()
            except:
                posted_date = ""

            yield {
                "Job Title": fields.get("title", [""])[0],
                "Location": fields.get("normalizedLocation", [""])[0],
                "Job ID": job_id,
                "Job URL": f"https://www.amazon.jobs/en/jobs/{job_id}",
                "Description Snippet": fields.get("shortDescription", [""])[0],
                "Posted Date": posted_date
            }

        
        # If there are more jobs to fetch, recursively yield another request
        if start_index + self.size < total_found:
            yield self.build_request(start_index + self.size)