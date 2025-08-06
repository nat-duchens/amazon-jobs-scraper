# Data Analysis of the JSON File

This project performs a very simple data analysis of the resulting JSON file from web crawling and web scraping using the Scrapy framework.

The Python code to analyze the extracted job listings is available here:  
[`simple_json_analysis.py`](amazon_jobs/data_analysis/simple_json_analysis.py)

---

## Analysis Performed

- **Converted** the JSON file into a Pandas DataFrame  
- **Parsed** and standardized the "Posted Date" field to datetime  
- **Extracted** city names from full location strings  
- **Extracted** simplified job roles from full job titles (before the comma)  
- **Printed**:
  - Total job listings
  - Top job titles
  - Top cities by job postings
  - Date range of the job listings
- **Visualized**:
  - Top 10 cities with the most job offers
  - Top 10 most frequent job titles

### Considerations

There are opportunities for improvement in data cleansing, such as:
- **Normalized** roles (Sr. → Senior, Developer → Developer, SDE → Software Development Engineer)

---

## Example Visualizations

- *Bar chart*: Top 10 cities with the most job offers  
- *Horizontal bar chart*: Most common job roles (before comma)  

---

## Useful Links

- [Pandas - Read JSON](https://www.w3schools.com/python/pandas/pandas_json.asp)  
- [Pandas - Analyzing DataFrames](https://www.w3schools.com/python/pandas/pandas_analyzing.asp)
- [Matplotlib - Bars](https://www.w3schools.com/python/matplotlib_bars.asp)

---