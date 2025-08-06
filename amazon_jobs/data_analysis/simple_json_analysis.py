import pandas as pd
import matplotlib.pyplot as plt  # ← FIX: importar pyplot correctamente

# Convert JSON → DataFrame
df = pd.read_json('C:/Users/HP/Documents/localGitHub/amazon-jobs-scraper/amazon_jobs/jobs_test.json')

## General Cleaning and Data Analysis

# Convert Date to Date time
df['Posted Date'] = pd.to_datetime(df['Posted Date'])

# Extract all cities 
df['City'] = df['Location'].apply(lambda x: x.split(',')[0].strip())

# Total job listings
print("Total job listings:", len(df)) 

# Top job titles (before the comma only)
print("\n Top job titles:") 
df['Job Role'] = df['Job Title'].apply(lambda x: x.split(',')[0].strip())
print(df['Job Role'].value_counts().head(10))

# Top cities
print("\n Top cities:")
print(df['City'].value_counts().head(10))

# Date range
print("\n Date range:")
print("Since:", df['Posted Date'].min())
print("To:", df['Posted Date'].max())

## Visualizations

# Top 10 cities with more offers
df['City'].value_counts().head(10).plot(kind='bar', title='Top 10 Cities with More Offers')
plt.ylabel('Quantity')
plt.xlabel('City')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Top 10 job titles
df['Job Role'].value_counts().head(10).plot(kind='barh', title='Top 10 Most Frequent Job Roles')
plt.xlabel('Quantity')
plt.ylabel('Job Role')
plt.tight_layout()
plt.show()