---
name: investment-analysis
display-name: Investment Opportunity Analysis
description: Deep-dive analysis of quarterly financial reports to identify
  undervalued stocks and political insider investments.
user-invocable: true
---

# Investment Opportunity Analysis

This skill is designed to perform deep-dive analysis on corporate financial reports (e.g., 10-Qs, 10-Ks) and provide investment insights, specifically focusing on undervalued opportunities and political insider activity.

## Goals
- Analyze quarterly reports to extract key metrics (Revenue Growth, Debt-to-Equity Ratio, Net Income, Free Cash Flow, EBITDA, etc.).
- Identify "undervalued" stocks based on valuation multiples and fundamental health.
- Track "political insider" investments (US Senators and House of Representatives).
- Provide a comprehensive bull/bear thesis for each identified opportunity.

## Workflow

### 1. Initial Request & Clarification
- Ask the user for a company name, ticker, or a specific filing URL.
- Ask for the user's investment horizon (short-term vs. long-term) and risk tolerance to tailor the analysis.

### 2. Data Gathering
- Use `web_search` or `firecrawl_search` to locate the most recent quarterly reports (SEC filings) or financial news.
- Use `firecrawl_scrape` to extract content from the reports.
- Specifically search for:
    - **Revenue Growth**: YoY and QoQ comparison.
    - **Debt-to-Equity Ratio**: Assess leverage.
    - **Management Discussion & Analysis (MD&A)**: Extract qualitative insights on risks, goals, and guidance.
    - **Political Insider Tracking**: Search for reports on US Senator and House of Representatives stock disclosures (e.g., via news, specialized trackers, or SEC filings).

### 3. Source Review
- Before finalizing the analysis, **you must present a list of all URLs found during the research to the user.**
- Ask the user to confirm which sources to prioritize or if any should be excluded.

### 4. Analysis & Visualization
- **Metric Ranking**:
    1. Revenue Growth (Primary)
    2. Debt-to-Equity Ratio (Primary)
    3. Net Income
    4. Free Cash Flow
    5. EBITDA
    6. Other relevant valuation multiples (P/E, EV/EBITDA).
- **Visualization**: Use `run_python` (with `matplotlib` or `plotly` if available, or just `matplotlib` via the provided environment) or `document-processing-and-graphics` to generate charts for:
    - Revenue trends.
    - Debt-to-equity trends.
    - Comparison of valuation metrics against industry peers.
- Create charts for easy consumption as requested by the user.

### 5. Outcome Presentation
Provide a structured report including:
- **Executive Summary**: A 3-sentence overview of the opportunity.
- **Key Metrics Table**: Ranked list of the primary and secondary metrics.
- **Deep Dive Insights**: Summary of the MD&A section, highlighting management's focus.
- **Political Insider Activity**: Summary of any detected investments by US Senators or House members.
- **Bull Case vs. Bear Case**: Balanced view of the investment.
- **Undervaluation Thesis**: Explanation of why the stock is considered undervalued.
- **Citations**: Every data point, metric, and claim must be cited with a Markdown link to the source URL.

## Instructions for the Agent
- Always be concise but thorough in "deep dive" sections.
- If data is missing for a metric, state "Data not available in current filing."
- When generating charts, ensure they are clearly labeled and easy to read.
- If you find conflicting information between sources, highlight the discrepancy to the user.
