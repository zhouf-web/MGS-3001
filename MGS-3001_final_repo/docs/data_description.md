# Data Description

## Source

Public job postings from 51job: https://we.51job.com

## Collection Method

Data were collected using HTML scraping and browser automation. List pages were collected with Selenium and browser performance logs. Detail pages were collected with undetected-chromedriver and proxy rotation. List-page and detail-page data were merged by the job detail URL.

## Collection Date

2026-05-12, Beijing Time.

## Sample Size

The cleaned dataset contains 805 valid postings. The final analytical sample contains 797 postings after excluding 8 records whose URL slugs indicated cities outside Beijing, Shanghai, Guangzhou, and Shenzhen.

## Raw Variables

| Raw column | Analysis name | Type | Description | Example |
| --- | --- | --- | --- | --- |
| 标题 | title | String | Job posting title | 数据分析师 |
| 标题链接 | job_url | URL | Detail-page URL and merge key | https://jobs.51job.com/shanghai/... |
| sal | salary_raw | String | Raw posted salary | 1-1.5万·13薪 |
| er | company | String | Company name | 上海某教育科技公司 |
| er1 | company_type | String | Company ownership type | 民营 |
| 字段1 | company_size | String | Company size category | 150-500人 |
| 抓取时间 | scrape_time | Timestamp | Scraping timestamp | 2026-05-12 18:49:19 |
| 职位信息_全文 | job_text | Text | Full job responsibilities and requirements | 负责业务数据分析... |

## Derived Variables

| Variable | Description |
| --- | --- |
| city | Parsed from the 51job URL slug. |
| salary_mid | Monthly midpoint parsed from the posted salary range. |
| log_salary | Natural log of `salary_mid` for valid monthly salary records. |
| ai_skill | Indicator equal to 1 if at least one AI-related keyword appears in the title or job description. English abbreviations use word-boundary matching to avoid false positives inside longer words. |
| advanced_ai_skill | Indicator for advanced AI terms such as LLM, RAG, machine learning, deep learning, NLP, and Chinese equivalents. |
| ai_exposure_score | Count of AI keyword categories mentioned in the posting. |
| traditional_skill_count | Count of traditional data-analysis skill categories: SQL, Python, Excel, BI/visualization, big data, statistics/modeling, and databases. |

## Known Data Quality Issues

- `salary_raw` is a mixed Chinese salary string and must be parsed before salary analysis.
- Some salary records are negotiable, daily wage, hourly wage, or missing; these are excluded from salary regressions.
- `company_size` has missing values and is coded as `Unknown` in regression models.
- City is parsed from the URL and filtered to Beijing, Shanghai, Guangzhou, and Shenzhen.
- Job-description text may contain extra whitespace or residual boilerplate.
- Keyword-based skill measurement may miss synonyms or overstate requirements when postings use broad buzzwords.
