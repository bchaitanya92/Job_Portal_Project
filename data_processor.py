import pandas as pd
import re
from datetime import datetime
import numpy as np

def clean_salary(salary_str):
    """
    Clean and standardize salary format
    """
    if pd.isna(salary_str) or salary_str == '':
        return "Salary not specified"
    
    # Remove common suffixes
    salary_str = str(salary_str).replace('(Glassdoor est.)', '').replace('(Employer est.)', '').strip()
    
    # Extract salary range
    salary_match = re.search(r'\$(\d+K?)\s*-\s*\$(\d+K?)', salary_str)
    if salary_match:
        min_salary = salary_match.group(1)
        max_salary = salary_match.group(2)
        
        # Convert K to thousands
        min_salary = min_salary.replace('K', '000') if 'K' in min_salary else min_salary
        max_salary = max_salary.replace('K', '000') if 'K' in max_salary else max_salary
        
        return f"${min_salary} - ${max_salary}"
    
    # Handle single salary values
    single_match = re.search(r'\$(\d+K?)', salary_str)
    if single_match:
        salary = single_match.group(1)
        salary = salary.replace('K', '000') if 'K' in salary else salary
        return f"${salary}"
    
    return salary_str

def clean_location(location_str):
    """
    Clean and standardize location format
    """
    if pd.isna(location_str) or location_str == '':
        return "Location not specified"
    
    location = str(location_str).strip()
    
    # Handle common variations
    if location.lower() in ['remote', 'united states']:
        return location.title()
    
    return location

def clean_company_score(score):
    """
    Clean company score
    """
    if pd.isna(score) or score == '':
        return 0.0
    
    try:
        return float(score)
    except:
        return 0.0

def clean_date(date_str):
    """
    Clean and standardize date format
    """
    if pd.isna(date_str) or date_str == '':
        return "Date not specified"
    
    date_str = str(date_str).strip()
    
    # Handle common date formats
    if 'd' in date_str:
        days = date_str.replace('d', '').replace('+', '')
        try:
            days = int(days)
            if days == 1:
                return "1 day ago"
            elif days < 7:
                return f"{days} days ago"
            elif days < 30:
                return f"{days} days ago"
            else:
                return "30+ days ago"
        except:
            return date_str
    
    return date_str

def process_job_data(csv_file_path):
    """
    Process and clean the job data from CSV
    """
    try:
        # Read CSV file
        df = pd.read_csv(csv_file_path)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Clean each column
        df['Company'] = df['Company'].fillna('Unknown Company').str.strip()
        df['Job Title'] = df['Job Title'].fillna('Unknown Position').str.strip()
        df['Location'] = df['Location'].apply(clean_location)
        df['Salary'] = df['Salary'].apply(clean_salary)
        df['Company Score'] = df['Company Score'].apply(clean_company_score)
        df['Date'] = df['Date'].apply(clean_date)
        
        # Add a unique ID for each job
        df['id'] = range(1, len(df) + 1)
        
        # Convert to list of dictionaries for easier template rendering
        jobs_list = df.to_dict('records')
        
        return jobs_list
        
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        return []

def get_jobs_by_page(jobs_list, page=1, per_page=12):
    """
    Get jobs for a specific page (for pagination)
    """
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    return jobs_list[start_idx:end_idx]

def get_total_pages(jobs_list, per_page=12):
    """
    Calculate total number of pages
    """
    return (len(jobs_list) + per_page - 1) // per_page

if __name__ == "__main__":
    # Test the data processing
    jobs = process_job_data('SE salaries final.csv')
    print(f"Processed {len(jobs)} jobs")
    if jobs:
        print("Sample job:", jobs[0]) 