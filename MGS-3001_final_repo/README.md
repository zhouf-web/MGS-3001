# MGS 3001 Final Project: Generative AI and Data Analyst Job Requirements

**Author:** Feiyu Zhou  
**Course:** MGS 3001 WHS01  
**Research question:** Is the rise of generative AI reshaping the demand structure of data analyst positions in China's first-tier cities in terms of required skills, job responsibilities, and compensation?

## Dataset

The dataset contains 805 public job postings collected from 51job on 2026-05-12. The search was restricted to the Data Analysis function category (`7501`) and the four target cities: Beijing, Shanghai, Guangzhou, and Shenzhen. After excluding 8 postings whose URLs indicated other cities, the final analytical sample contains 797 postings.

The cleaned CSV is stored at:

`data/51job_cleaned.csv`

## Repository Structure

```text
MGS-3001_final_repo/
├── README.md
├── data/
│   └── 51job_cleaned.csv
├── code/
│   ├── 01_list_spider.ipynb
│   ├── 02_detail_spider.ipynb
│   ├── 03_merge_jobs.py
│   ├── 04_clean_jobs.py
│   └── 05_analysis.ipynb
├── docs/
│   └── data_description.md
└── outputs/
```

## Analysis Workflow

1. Run `code/05_analysis.ipynb`.
2. The notebook standardizes column names, parses city from URLs, parses monthly salary, constructs AI-skill indicators with word-boundary matching for English abbreviations, constructs traditional-skill counts, creates figures, and estimates regression models.
3. Generated charts, regression summaries, the main regression table, and the salary robustness table are saved in `outputs/`.

## Main Hypotheses

- **H1:** AI-related skills are meaningfully present in data analyst job postings in China's first-tier cities, and the AI-skill penetration rate differs across Beijing, Shanghai, Guangzhou, and Shenzhen.
- **H2:** Job postings requiring AI-related skills also require more traditional data analysis skills, suggesting complementarity.
- **H3:** Job postings requiring AI-related skills are associated with higher posted salaries after controlling for city, company type, and company size.

## Required Python Packages

```bash
pip install pandas numpy matplotlib seaborn statsmodels
```

## Notes

The analysis is cross-sectional. Regression coefficients should be interpreted as conditional associations rather than causal effects.
