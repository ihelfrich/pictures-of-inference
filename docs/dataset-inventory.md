# Dataset Inventory

We need four core datasets. They will recur throughout the book — introduced in early chapters, returned to in later ones, the substrate against which the reader's growing competence is exercised.

The criteria for a core dataset:

- **Real.** Not simulated. Not toy data. Real data with real questions attached.
- **Rich.** Enough variables and observations to support multiple analyses. A reader meeting it in chapter 4 should still be able to learn something new from it in chapter 30.
- **Clean enough.** Documented, processed, ready to analyze. The reader should not drown in data preparation.
- **Legally available.** Public domain, or licensed for educational use, or yours to share.
- **Interesting.** The reader should care about the questions the data lets them ask.

## The four slots

**Slot 1. A country panel.** A cross-section of countries observed over time. Development, demographics, governance, environment, trade. The vehicle for cross-country comparisons, panel methods, and macro questions.

**Slot 2. Microdata on people.** A worker panel, household survey, or comparable individual-level dataset. The vehicle for labor questions, demographic analysis, sample design, microeconometrics. Real survey weights ideally.

**Slot 3. A high-frequency time series.** Financial, macroeconomic, or otherwise. The vehicle for time-series methods, volatility, cointegration, structural breaks.

**Slot 4. A research design.** Either a published quasi-experiment with replicable data, or an experimental dataset, or a setting with a clear identification strategy. The vehicle for causal inference. Card-Krueger, Project STAR, Lalonde, MTO, the National Supported Work demonstration, or your own work if you have something appropriate.

## What I need from you

For each slot, tell me:

- **Do you have something on hand?** If yes, what is it, what's its source, and what's its rough shape (rows, columns, time span)?
- **If yes, can you share it?** Is it your data, public data, or something proprietary? Can it go in a public GitHub repo?
- **If no, what would you reach for?** Given your research and teaching, what dataset would you actually use if you were teaching this material yourself?

## Specific things you mentioned having

You've mentioned:

- The EffDist_V2026 bilateral trade cost panel (your research data).
- Geospatial economics work and trade network data.
- Various tutoring and teaching examples.

Some of these might be perfect for some slots. The trade-cost panel could anchor the country-panel slot if it's structured for cross-country variation. Your geospatial work could appear in specific chapters even if it's not a core dataset.

## What I'd suggest if you don't have ready candidates

These are public, clean, well-documented, and have been used effectively in pedagogy elsewhere:

**For Slot 1:**

- The Penn World Tables (10.0 or later). 183 countries, 1950-2019, 50+ macro variables.
- World Bank World Development Indicators. Broader country coverage, more variables, less consistent quality.
- The Maddison Project Database. Historical GDP per capita going back centuries. Limited scope, beautiful for long-run questions.

**For Slot 2:**

- The Current Population Survey, monthly or annual files. Workhorse of US labor economics.
- The General Social Survey. Smaller, longer panel, attitudes and demographics.
- The PSID. Genuine panel, decades long.
- The IPUMS extracts of historical census data. Massive, beautifully curated.

**For Slot 3:**

- FRED macroeconomic series. The standard for time series teaching.
- CRSP-style stock returns. Better for volatility and finance applications.
- High-frequency exchange rates from public APIs.

**For Slot 4:**

- Card and Krueger 1994 (NJ-PA minimum wage). Replication data is published.
- Lalonde 1986 / Dehejia-Wahba (job training). Canonical for matching methods.
- Project STAR (class size in Tennessee). Genuine experiment, rich data.
- The MTO (Moving to Opportunity) data. Available with appropriate access.

## Take a pass and respond

Look through your drives. Tell me what you have. We'll match it to slots, supplement where needed, and commit. Once committed, I will write the dataset documentation and processing pipeline and we will not change cores again.
