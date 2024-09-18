import csv
from jobspy import scrape_jobs
import pandas as pd
from datetime import datetime, timedelta
import os

CATEGORIES = {
        "软件工程": [
            '"Software Engineer Intern"',
            '"Software Developer Intern"',
            '"Programmer Intern"',
            '"Web Developer Intern"',
            '"Mobile App Developer Intern"'
        ],
        "数据科学": [
            '"Data Scientist Intern"',
            '"Data Analyst Intern"',
            '"Machine Learning Intern"',
            '"Big Data Intern"'
        ],
        "人工智能": [
            '"AI Intern"',
            '"Artificial Intelligence Intern"',
            '"Deep Learning Intern"',
            '"NLP Intern"',
            '"Computer Vision Intern"'
        ],
        "音频工程": [
            '"Audio Engineer Intern"',
            '"Sound Engineer Intern"',
        ],
        "游戏开发": [
            '"Game Developer Intern"',
            '"Game Programmer Intern"',
            '"Game Designer Intern"',
            '"Game Animator Intern"'
        ],
        "商业分析": [
            '"Business Analyst Intern"',
            '"Market Research Intern"',
            '"Financial Analyst Intern"',
            '"Operations Research Intern"'
        ],
    }

def extract_job_type(title):
    types = ["INTERN", "CO-OP", "FULL-TIME", "PART-TIME"]
    for job_type in types:
        if job_type.lower() in title.lower():
            return job_type
    return "N/A"


def format_job_info(row):
    title = row['title'].split('(')[0].strip()
    location = row['location'] if pd.notna(row['location']) else "N/A"
    job_type = row['job_type'] if pd.notna(row['job_type']) else extract_job_type(row['title'])
    date_posted = row['date_posted'] if pd.notna(row['date_posted']) else "N/A"
    job_url = row['job_url'] if pd.notna(row['job_url']) else "N/A"

    return f"""🏢 Company: {row['company']}
💼 岗位: {title}
📍 地点: {location}
📅 发布日期: {date_posted}{' 🔥' if (datetime.now().date() - datetime.strptime(str(date_posted), '%Y-%m-%d').date()).days < 2 else ''}
👋 类型: {job_type}
🔗 Link: {job_url}
----------------------------
"""


def is_recent(date_posted):
    if pd.isna(date_posted):
        return False
    today = datetime.now().date()
    four_days_ago = today - timedelta(days=4)
    return str(date_posted) >= str(four_days_ago)


def run_job_search(category, search_terms, location):
    all_jobs = pd.DataFrame()

    for term in search_terms:
        jobs = scrape_jobs(
            site_name=["indeed", "linkedin", "glassdoor"],
            search_term=term,
            location=location,
            results_wanted=4,
            hours_old=72,
            country_indeed='USA',
        )
        all_jobs = pd.concat([all_jobs, jobs], ignore_index=True)

    print(f"Found {len(all_jobs)} jobs for {category}")

    if all_jobs.empty:
        print("----------WARNING-----------")
        print(f"No jobs found for {category}. Skipping further processing.")
        return all_jobs

    # Remove duplicates
    all_jobs.drop_duplicates(subset=['job_url'], inplace=True)

    # Check if 'date_posted' column exists
    if 'date_posted' not in all_jobs.columns:
        print(f"Warning: 'date_posted' column not found for {category}. Skipping filtering.")
        filtered_jobs = all_jobs
    else:
        # Filter recent jobs
        filtered_jobs = all_jobs[all_jobs['date_posted'].apply(is_recent)]

    # Save raw results
    today = datetime.now().strftime('%Y-%m-%d')
    raw_file = f'raw_jobs_{category}_{today}.csv'
    raw_path = os.path.join('jobs', raw_file)
    all_jobs.to_csv(raw_path, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)

    # Format and save filtered results
    formatted_jobs = f"📢 今天的{category}工作机会来啦! 快去Apply👉  \n 时间: {today} \n----------------------------\n\n"
    print(filtered_jobs)
    formatted_jobs += filtered_jobs.apply(format_job_info, axis=1).str.cat(sep='\n')

    formatted_file = f'formatted_jobs_{category}_{today}.txt'
    formatted_path = os.path.join('jobs', formatted_file)
    with open(formatted_path, "w", encoding='utf-8') as f:
        f.write(formatted_jobs)

    print(f"{category} job information saved to {raw_path} and {formatted_path}")
    return all_jobs

def get_jobs():
    total_data = []
    for category, terms in CATEGORIES.items():
        for term in terms:
            jobs = scrape_jobs(
                site_name=["indeed", "linkedin", "glassdoor"],
                search_term=term,
                location="USA",
                results_wanted=20,
                hours_old=72,
                country_indeed='USA',
            )
            for index, row in jobs.iterrows():
                url = row['job_url'] if pd.notna(row['job_url']) else "N/A"
                title = row['title'] if pd.notna(row['title']) else "N/A"
                company = row['company'] if pd.notna(row['company']) else "N/A"
                type = row['job_type'] if pd.notna(row['job_type']) else "N/A"

                field = category
                description = row['description'] if pd.notna(row['description']) else "N/A"
                location = row['location'] if pd.notna(row['location']) else "N/A"
                date_posted = row['date_posted'] if pd.notna(row['date_posted']) else "N/A"

                datum = {
                    "url": url,
                    "title": title,
                    "comp": company,
                    "type": type,
                    "field": field,
                    "description": description,
                    "location": location,
                    "date": date_posted
                }
                total_data.append(datum)
    return total_data


def main():
    # Ensure output directory exists
    if not os.path.exists('jobs'):
        os.makedirs('jobs')

    # Define search categories and corresponding precise search terms
    categories = {
        "软件工程": [
            '"Software Engineer Intern"',
            '"Software Developer Intern"',
            '"Programmer Intern"',
            '"Web Developer Intern"',
            '"Mobile App Developer Intern"'
        ],
        "数据科学": [
            '"Data Scientist Intern"',
            '"Data Analyst Intern"',
            '"Machine Learning Intern"',
            '"Big Data Intern"'
        ],
        "人工智能": [
            '"AI Intern"',
            '"Artificial Intelligence Intern"',
            '"Deep Learning Intern"',
            '"NLP Intern"',
            '"Computer Vision Intern"'
        ],
        "音频工程": [
            '"Audio Engineer Intern"',
            '"Sound Engineer Intern"',
        ],
        "游戏开发": [
            '"Game Developer Intern"',
            '"Game Programmer Intern"',
            '"Game Designer Intern"',
            '"Game Animator Intern"'
        ],
        "商业分析": [
            '"Business Analyst Intern"',
            '"Market Research Intern"',
            '"Financial Analyst Intern"',
            '"Operations Research Intern"'
        ],

    }

    # Set location
    location = "USA"

    # Perform search for each category
    all_results = pd.DataFrame()
    for category, search_terms in categories.items():
        category_jobs = run_job_search(category, search_terms, location)
        all_results = pd.concat([all_results, category_jobs], ignore_index=True)

    if all_results.empty:
        print("No jobs found for any category or location.")
        return

    # Save all results
    today = datetime.now().strftime('%Y-%m-%d')
    all_results_file = f'all_jobs_{today}.csv'
    all_results_path = os.path.join('jobs', all_results_file)
    all_results.to_csv(all_results_path, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
    print(f"All job information saved to {all_results_path}")


if __name__ == "__main__":
    get_jobs()