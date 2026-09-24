import os
import json
from datetime import datetime, timedelta
from app import app, init_db, get_db, set_password_hash

def get_data_analytics_curriculum():
    """
    Carefully designed 7-day Data Analytics curriculum crafted by a professional
    educator. Real-world business applications, zero fluff, rigorous pedagogy.
    """
    return [
        {
            "day": 1,
            "title": "Foundations of Exploratory Data Analysis & Analytical Thinking",
            "subtopics": [
                {
                    "title": "Problem Framing & The Business Intelligence Lifecycle",
                    "brief": "Learn how raw transactional events transform into decision-grade intelligence. We examine the full BI lifecycle: data capture, ingestion pipelines, dimensional staging, and analytics consumption. Master the MECE (Mutually Exclusive, Collectively Exhaustive) framework to translate ambiguous business complaints (e.g. 'churn is accelerating') into structured, testable analytical questions.",
                    "takeaways": [
                        "Differentiate between passive descriptive reporting and root-cause diagnostic analytics.",
                        "Structure complex business investigations using the MECE hypothesis framework.",
                        "Map the journey of raw tabular data from transactional systems (OLTP) to analytical datamarts (OLAP)."
                    ],
                    "prompt_seed": "How can an analyst translate an executive question like 'Why did our gross margins drop 8% last month?' into a structured 4-step data analysis roadmap?"
                },
                {
                    "title": "Data Types, Schemas & Quality Audit Metrics",
                    "brief": "Before computing any KPI, a professional analyst performs a rigorous data audit. Understand the mathematical implications of nominal, ordinal, interval, and ratio scales. Learn systematic techniques to audit missingness (MCAR vs MAR vs MNAR), detect silent schema coercions, resolve timezone offsets, and handle duplicate entity records.",
                    "takeaways": [
                        "Perform pre-analysis data health audits covering completeness, validity, uniqueness, and consistency.",
                        "Distinguish between structural nulls (e.g. missing discount on non-promotional item) and data capture failures.",
                        "Identify and remedy common timezone and date-boundary distortions in daily metric rollups."
                    ],
                    "prompt_seed": "Provide a practical checklist of data quality checks every analyst must run when receiving an unverified CSV export before computing summary KPIs."
                },
                {
                    "title": "Summary Statistics, Percentiles & Skewness",
                    "brief": "Explore the reality of skewed real-world business data where naive averages mislead stakeholders. Master non-parametric summary statistics: medians, Interquartile Ranges (IQR), and percentile distributions (P50, P90, P99). Learn how to detect outliers, quantify metric variance, and communicate risk and distribution shape to non-technical stakeholders.",
                    "takeaways": [
                        "Recognize heavily skewed metrics (order values, customer spend, SLA response times) where median and IQR are mandatory.",
                        "Calculate and interpret IQR-based statistical fences to identify genuine anomalies vs extreme normal behavior.",
                        "Explain the dangers of optimizing business operations against a simple arithmetic mean."
                    ],
                    "prompt_seed": "Explain why reporting the average customer purchase value can be deceptive for an e-commerce platform with a long tail of high spenders, and how percentiles solve this."
                }
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "Which analytical approach specifically focuses on understanding the underlying drivers and root causes of a past historical anomaly?",
                    "options": [
                        "Descriptive Analytics",
                        "Diagnostic Analytics",
                        "Predictive Analytics",
                        "Prescriptive Analytics"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 2,
                    "question": "When examining user session duration in an app, the data is heavily right-skewed with extreme long-session outliers. Which measure of central tendency is most reliable?",
                    "options": [
                        "Arithmetic Mean",
                        "Median",
                        "Mode",
                        "Mid-range"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 3,
                    "question": "Under the standard 1.5 × IQR rule, what defines an outlier data point on the upper tail?",
                    "options": [
                        "Value > Q1 + 1.5 × IQR",
                        "Value > Q3 + 1.5 × IQR",
                        "Value > Median + 1.5 × IQR",
                        "Value > Mean + 1.5 × Standard Deviation"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 4,
                    "question": "What does the MECE principle stand for in problem-structuring?",
                    "options": [
                        "Most Effective Critical Evaluation",
                        "Mutually Exclusive, Collectively Exhaustive",
                        "Maximum Efficiency, Complete Execution",
                        "Metric Evaluation and Correlation Estimation"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 5,
                    "question": "Why is it dangerous to simply delete rows containing NULL values during data preparation?",
                    "options": [
                        "SQL databases will crash if tables lose rows",
                        "Deleting NULLs can introduce systematic selection bias and distort metric distributions",
                        "NULL values always automatically convert into zero in all aggregations",
                        "Deleting rows alters the primary key sequence irreversibly"
                    ],
                    "correct_index": 1
                }
            ]
        },
        {
            "day": 2,
            "title": "Advanced Tabular Modeling & Excel for Analysts",
            "subtopics": [
                {
                    "title": "Dynamic Multi-Condition Lookups (XLOOKUP & Index-Match)",
                    "brief": "Transition beyond legacy, fragile VLOOKUPs to resilient lookup architectures. Master INDEX-MATCH for two-way matrix coordinate lookups across arbitrary row and column headers. Implement modern XLOOKUP with search modes, wildcard matching, default fallback values, and approximate match lookup tables for tiered pricing and commission slabs.",
                    "takeaways": [
                        "Build resilient, bidirectional table lookups that do not break when columns are inserted or reordered.",
                        "Implement exact-match multi-criteria lookups using Boolean arrays inside XLOOKUP.",
                        "Configure approximate lookups for bracketed calculations (tax tiers, performance bonuses, shipping rate cards)."
                    ],
                    "prompt_seed": "How do you structure an INDEX-MATCH formula in Excel to retrieve a metric located at the intersection of a specific month column and a specific department row?"
                },
                {
                    "title": "Dimensional Pivot Tables, Slicers & Calculated Fields",
                    "brief": "Transform large transaction logs into responsive analytical matrices. Learn how to group continuous date sequences into custom fiscal periods, build calculated fields without modifying source records, configure custom 'Show Values As' calculations (% of row total, difference from previous period), and connect multiple pivots to unified visual slicers.",
                    "takeaways": [
                        "Summarize multidimensional datasets without writing redundant helper columns.",
                        "Leverage built-in relative calculations to compute Month-over-Month (MoM) deltas directly in Pivot Tables.",
                        "Design linked interactive dashboard slices with synchronized timeline and category controls."
                    ],
                    "prompt_seed": "What is the key difference between a Calculated Field and a Calculated Item in an Excel Pivot Table, and when should each be used?"
                },
                {
                    "title": "Automating Tabular Pipelines with Power Query",
                    "brief": "Automate routine data ingestion, unpivoting, and transformation using Power Query's M-engine. Learn to unpivot cross-tabulated reports into clean, normalized tabular formats (tidy data). Standardize casing, parse embedded text structures, merge multiple CSV files dynamically, and build zero-maintenance refreshable workflows.",
                    "takeaways": [
                        "Convert wide matrix reports into normalized, query-ready 3-column schemas (Date, Dimension, Value).",
                        "Build automated data ingestion queries that refresh automatically when source files update.",
                        "Standardize messy string anomalies and split compound product codes using Power Query transformations."
                    ],
                    "prompt_seed": "Walk me through the exact steps in Power Query to unpivot a wide 12-month budget table into a tidy format suitable for relational database ingestion."
                }
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "What major architectural advantage does INDEX-MATCH have over the classic VLOOKUP formula?",
                    "options": [
                        "INDEX-MATCH works without needing parentheses",
                        "INDEX-MATCH can look to the left and is immune to column insertion/deletion breakages",
                        "VLOOKUP cannot handle text values, while INDEX-MATCH can",
                        "INDEX-MATCH automatically formats the resulting cells as currency"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 2,
                    "question": "In XLOOKUP, what happens if the optional [if_not_found] argument is omitted and no match exists?",
                    "options": [
                        "It returns 0",
                        "It returns an empty string",
                        "It returns the #N/A error",
                        "It returns the closest approximate match"
                    ],
                    "correct_index": 2
                },
                {
                    "id": 3,
                    "question": "In spreadsheet data modeling, what does 'unpivoting' columns achieve?",
                    "options": [
                        "It sorts the columns in alphabetical order",
                        "It transforms repeating attribute columns into normalized attribute-value pairs (tidy data)",
                        "It removes all formula references and converts data to static values",
                        "It creates a 3D bar chart from the tabular matrix"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 4,
                    "question": "When creating a Calculated Field in an Excel Pivot Table, what data does the formula operate upon?",
                    "options": [
                        "The raw individual rows before any grouping occurs",
                        "The sum of the underlying data fields after grouping",
                        "Only cells currently highlighted by the user's cursor",
                        "External data loaded in other workbooks"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 5,
                    "question": "What is the primary benefit of using Power Query over manual copy-paste spreadsheet consolidation?",
                    "options": [
                        "It removes all gridlines in Excel automatically",
                        "It creates a repeatable, documented data transformation pipeline that updates on refresh",
                        "It increases the maximum number of rows in Excel from 1 million to infinity",
                        "It prevents other users from ever viewing the worksheet"
                    ],
                    "correct_index": 1
                }
            ]
        },
        {
            "day": 3,
            "title": "Relational Data Extraction & SQL Foundations",
            "subtopics": [
                {
                    "title": "Logical Query Processing Order & Selective Filtering",
                    "brief": "Master the logical lifecycle of SQL execution. Understand why queries execute in the order: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT, rather than the lexical order in which they are written. Master predicate pushdown, SARGable filter expressions (avoiding functions in WHERE clauses), and distinguishing WHERE from HAVING.",
                    "takeaways": [
                        "Understand SQL engine execution sequence to troubleshoot aliasing and scoping errors.",
                        "Apply pre-aggregation filtering with WHERE to reduce working dataset size before grouping.",
                        "Write SARGable queries that utilize B-tree indexes rather than forcing full table scans."
                    ],
                    "prompt_seed": "Explain why `WHERE COUNT(order_id) > 2` triggers a SQL syntax error, and show how to correctly filter aggregated groups."
                },
                {
                    "title": "Relational Joins, Cardinality & Cartesian Traps",
                    "brief": "Join disparate tables while preserving analytical truth. Dive deep into INNER, LEFT, RIGHT, and FULL OUTER joins. Understand join cardinality (1:1, 1:N, N:M) and learn how unintentional many-to-many joins cause catastrophic cartesian explosions that silently double-count financial totals.",
                    "takeaways": [
                        "Select the appropriate join type based on whether non-matching parent records must be preserved.",
                        "Audit record counts before and after joins to verify that cardinality matches domain expectations.",
                        "Join transactional fact tables to dimensional entity tables without creating metric inflation."
                    ],
                    "prompt_seed": "You have a Customers table (1,000 rows) and an Orders table (5,000 rows). A LEFT JOIN returns 6,200 rows. Explain why this happened and how to investigate it."
                },
                {
                    "title": "Multi-Metric Conditional Aggregations with CASE WHEN",
                    "brief": "Transform vertical records into horizontal summary dashboards in a single SQL pass. Master conditional aggregation using SUM(CASE WHEN ... THEN 1 ELSE 0 END) and COUNT(DISTINCT CASE WHEN ...). Calculate funnel conversion rates, status breakdowns, and cohort metrics without writing multiple separate queries.",
                    "takeaways": [
                        "Pivot status categories into dedicated KPI columns in a single table scan.",
                        "Compute conversion ratios and retention fractions directly within SQL SELECT statements.",
                        "Safely manage division-by-zero errors using NULLIF within aggregate calculations."
                    ],
                    "prompt_seed": "Write a single SQL query that calculates: Total Orders, Total Revenue, Completed Orders, Cancelled Orders, and Cancellation Rate (%) grouped by month."
                }
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "In what order does a SQL engine logically evaluate a query containing WHERE, GROUP BY, FROM, and HAVING clauses?",
                    "options": [
                        "FROM -> WHERE -> GROUP BY -> HAVING",
                        "SELECT -> FROM -> WHERE -> GROUP BY",
                        "WHERE -> FROM -> HAVING -> GROUP BY",
                        "FROM -> GROUP BY -> HAVING -> WHERE"
                    ],
                    "correct_index": 0
                },
                {
                    "id": 2,
                    "question": "What is the primary difference between a WHERE clause and a HAVING clause?",
                    "options": [
                        "WHERE works only with numbers; HAVING works with text strings",
                        "WHERE filters individual rows prior to grouping; HAVING filters aggregated groups after grouping",
                        "WHERE can only be used with INNER JOIN; HAVING is for OUTER JOIN",
                        "There is no difference; they are interchangeable aliases"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 3,
                    "question": "Why does evaluating `WHERE status = NULL` always evaluate to UNKNOWN/False in standard SQL?",
                    "options": [
                        "Because NULL must always be capitalized",
                        "Because NULL represents an unknown value, requiring the `IS NULL` predicate rather than equality",
                        "Because strings cannot be compared to NULL",
                        "Because SQLite automatically converts NULL to an empty string"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 4,
                    "question": "If Table A has 5 rows and Table B has 4 rows, how many rows are produced by a CROSS JOIN without a condition?",
                    "options": [
                        "9 rows",
                        "20 rows",
                        "5 rows",
                        "1 row"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 5,
                    "question": "Which SQL construct safely prevents a division-by-zero error when calculating conversion rate `completed_orders / total_orders`?",
                    "options": [
                        "completed_orders / IFNULL(total_orders, 1)",
                        "completed_orders / NULLIF(total_orders, 0)",
                        "completed_orders / ZEROIF(total_orders)",
                        "completed_orders / COALESCE(total_orders, 0)"
                    ],
                    "correct_index": 1
                }
            ]
        },
        {
            "day": 4,
            "title": "Analytical SQL: Window Functions & Common Table Expressions",
            "subtopics": [
                {
                    "title": "Modular Query Design with Common Table Expressions (CTEs)",
                    "brief": "Deconstruct complex business logic into readable, maintainable, and modular CTE pipelines. Compare the execution characteristics of CTEs (`WITH` clauses) vs subqueries and temporary staging tables. Learn how to structure analytical scripts into clean semantic layers: data extraction, cleaning, metric aggregation, and final presentation.",
                    "takeaways": [
                        "Replace unreadable nested subqueries with linear, self-documenting CTE stages.",
                        "Improve collaborative code maintainability and peer review readability across analytics teams.",
                        "Structure complex multi-pass transformations into modular analytical pipelines."
                    ],
                    "prompt_seed": "Refactor a multi-level nested query calculating the average spend of top 10% customers into a clean, two-step Common Table Expression (CTE)."
                },
                {
                    "title": "Ranking & Value Window Functions (ROW_NUMBER, DENSE_RANK, LAG/LEAD)",
                    "brief": "Perform sophisticated intra-group analytical calculations without collapsing row cardinality. Master the OVER clause with PARTITION BY and ORDER BY. Use ROW_NUMBER() for precise deduplication, DENSE_RANK() for top-N ranking, and LAG()/LEAD() to compute Period-over-Period growth and user lifecycle intervals.",
                    "takeaways": [
                        "Isolate top N records per dimensional category using `ROW_NUMBER() OVER(PARTITION BY ... ORDER BY ...)`.",
                        "Differentiate the behavior of RANK (gaps on ties) and DENSE_RANK (continuous sequence).",
                        "Calculate Month-over-Month (MoM) revenue growth using `LAG(revenue, 1)`."
                    ],
                    "prompt_seed": "Write a SQL query using window functions that returns each employee's salary along with the difference between their salary and the average salary of their department."
                },
                {
                    "title": "Rolling Aggregates & Dynamic Window Framing",
                    "brief": "Smooth volatile business metrics and track trajectory trends using rolling window frames. Master window framing specifications (`ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`). Build running year-to-date (YTD) cumulative sums, 7-day moving averages for operational pacing, and 30-day churn baselines.",
                    "takeaways": [
                        "Calculate running totals and cumulative metric trajectories without self-joins.",
                        "Build rolling moving averages to distinguish true trend signals from weekday/weekend noise.",
                        "Understand the critical difference between ROWS (physical rows) and RANGE (logical value offsets)."
                    ],
                    "prompt_seed": "Construct a SQL query that calculates a 7-day rolling moving average of daily active users (DAU) from an activity table."
                }
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "If three items tie for the 1st position, what rank does the next item receive when using the `RANK()` window function?",
                    "options": [
                        "2",
                        "3",
                        "4",
                        "1"
                    ],
                    "correct_index": 2
                },
                {
                    "id": 2,
                    "question": "What is the primary function of the `PARTITION BY` clause in a window function?",
                    "options": [
                        "It deletes duplicate rows in the table",
                        "It divides the query result set into partitions where the window function applies independently",
                        "It physically re-partitions the disk storage of the database",
                        "It groups and collapses rows similar to GROUP BY"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 3,
                    "question": "Which window frame specification calculates a cumulative running total from the beginning of a partition up to the current row?",
                    "options": [
                        "ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING",
                        "ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW",
                        "ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING",
                        "ROWS 10 PRECEDING"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 4,
                    "question": "Which function would you use to fetch the revenue value from the immediately preceding month in an ordered time-series?",
                    "options": [
                        "LEAD(revenue, 1)",
                        "LAG(revenue, 1)",
                        "PREV(revenue)",
                        "OFFSET(revenue, -1)"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 5,
                    "question": "What happens to the row count of a table when a window function is evaluated in the SELECT list?",
                    "options": [
                        "The row count is reduced to the number of distinct partition keys",
                        "The row count remains unchanged; individual rows are preserved with their computed window value",
                        "The row count is doubled",
                        "Only rows with non-null values are returned"
                    ],
                    "correct_index": 1
                }
            ]
        },
        {
            "day": 5,
            "title": "Python for Data Analysis: Vectorized NumPy & Pandas",
            "subtopics": [
                {
                    "title": "Vectorized Computing & Boolean Indexing with NumPy",
                    "brief": "Explore the foundation of modern high-performance data manipulation in Python. Understand how NumPy ndarrays store homogeneous data contiguously in memory. Compare C-speed vectorized operations against slow interpreted Python loops. Master boolean masking, broadcasting rules, and numerical aggregation across multidimensional axes.",
                    "takeaways": [
                        "Eliminate slow `for` loops in Python by replacing them with SIMD-accelerated vectorized operations.",
                        "Filter and transform large numerical arrays instantaneously using boolean masks.",
                        "Understand array broadcasting rules when operating on arrays with differing dimensions."
                    ],
                    "prompt_seed": "Demonstrate with a code snippet how to normalize an array of financial prices (zero mean, unit variance) using vectorized NumPy functions without loops."
                },
                {
                    "title": "Data Wrangling, Slicing & Method Chaining with Pandas",
                    "brief": "Master idiomatic Pandas operations. Understand the internal anatomy of DataFrames and Series. Differentiate between label-based indexing (`.loc`) and positional indexing (`.iloc`). Avoid the notorious `SettingWithCopyWarning` through explicit view vs copy handling. Structure elegant, readable data pipelines using method chaining (`.assign()`, `.pipe()`, `.query()`).",
                    "takeaways": [
                        "Confidently slice, filter, and modify DataFrames using `.loc` and `.iloc` without accidental side-effects.",
                        "Diagnose and eliminate `SettingWithCopyWarning` by using `.copy()` and proper index assignment.",
                        "Write expressive, maintainable data pipelines using fluent method chaining."
                    ],
                    "prompt_seed": "Explain the exact cause of Pandas' `SettingWithCopyWarning` and demonstrate the correct syntax to filter and modify a column safely."
                },
                {
                    "title": "Multi-Table Joins, GroupBy Aggregations & Reshaping",
                    "brief": "Merge heterogeneous data sources and reshape datasets into analytical form. Master `pd.merge()` with join validation (`validate='1:m'`). Leverage `.groupby()` paired with custom `.agg()` dictionaries to compute multiple metrics per dimension simultaneously. Learn how to pivot and melt between wide reporting formats and tidy tables.",
                    "takeaways": [
                        "Perform relational joins in Pandas while enforcing cardinality constraints using the `validate` parameter.",
                        "Compute multi-metric aggregations (mean, median, count, percentiles) across groups in a single call.",
                        "Reshape DataFrames seamlessly using `.melt()` and `.pivot_table()` for visualization readiness."
                    ],
                    "prompt_seed": "Write a Pandas code snippet to load two DataFrames (orders, customers), merge them on 'customer_id', and calculate total spend, order count, and average order value per customer city."
                }
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "What is the primary difference between `.loc` and `.iloc` in Pandas?",
                    "options": [
                        "`.loc` is for Series; `.iloc` is for DataFrames",
                        "`.loc` selects by labels/names; `.iloc` selects by integer position indices",
                        "`.loc` is faster than `.iloc` in all scenarios",
                        "`.loc` operates in-place; `.iloc` creates a deep copy"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 2,
                    "question": "Why are vectorized NumPy operations significantly faster than standard Python `for` loops on lists?",
                    "options": [
                        "NumPy automatically uses AI to predict calculations",
                        "NumPy operations run in compiled C/Fortran code with contiguous memory and vectorized CPU instructions",
                        "Python lists cannot store numbers larger than 1,000",
                        "NumPy skips mathematical validation checks"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 3,
                    "question": "In Pandas, what does the `SettingWithCopyWarning` typically indicate?",
                    "options": [
                        "The computer is running out of RAM",
                        "An assignment was made on a slice/view of a DataFrame where it is ambiguous whether the original DataFrame was modified",
                        "A column name contains spaces or special characters",
                        "A file path could not be resolved"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 4,
                    "question": "Which Pandas method transforms a wide DataFrame into a long format by unpivoting columns into rows?",
                    "options": [
                        "`.pivot()`",
                        "`.melt()`",
                        "`.stack_cols()`",
                        "`.explode()`"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 5,
                    "question": "When using `df.groupby('region').agg({'sales': ['sum', 'mean'], 'order_id': 'count'})`, what type of column index is produced?",
                    "options": [
                        "Single-level string index",
                        "MultiIndex (hierarchical columns)",
                        "Categorical index",
                        "Integer range index"
                    ],
                    "correct_index": 1
                }
            ]
        },
        {
            "day": 6,
            "title": "Exploratory Visualization & Dashboard Architecture",
            "subtopics": [
                {
                    "title": "Visual Encodings & Chart Selection Frameworks",
                    "brief": "Explore the science of visual perception and graphical integrity. Learn how human vision processes pre-attentive attributes (position, length, color hue, size). Master the taxonomy of chart selection: scatter plots for correlation, line charts for continuous temporal trend, bar charts for discrete comparison, and heatmaps for matrix density. Avoid deceptive visual anti-patterns.",
                    "takeaways": [
                        "Select visual encodings based on data relationship types rather than aesthetic whim.",
                        "Adhere to baseline rules: why bar charts strictly require zero baselines while line charts can be cropped.",
                        "Minimize cognitive load and non-data ink by applying Edward Tufte's design principles."
                    ],
                    "prompt_seed": "Explain why truncating the y-axis on a bar chart distorts data perception, whereas doing so on a line chart tracking temperature or stock fluctuations can be valid."
                },
                {
                    "title": "Actionable Business Dashboard Architecture (Power BI / Tableau)",
                    "brief": "Learn how enterprise BI developers build decision-oriented dashboards. Explore the visual hierarchy: Executive KPI cards at the top, trend context in the middle, and dimensional granular breakdowns at the bottom. Master interactive filtering flows, drill-through paths, and designing for executive decision-makers who spend under 30 seconds scanning a screen.",
                    "takeaways": [
                        "Structure layout hierarchy using standard F-pattern viewing conventions.",
                        "Design rich KPI cards combining current values, benchmark targets, and sparkline trajectories.",
                        "Implement synchronized cross-filtering to enable intuitive root-cause exploration."
                    ],
                    "prompt_seed": "What are the 3 essential components every executive KPI card should display to be immediately actionable for a VP or Director?"
                },
                {
                    "title": "Statistical Plotting with Seaborn & Interactive Plotly",
                    "brief": "Bridge exploratory code and stakeholder presentation. Leverage Seaborn to visualize statistical distributions (KDE, boxplots with overlaid strip plots, violin plots) and correlation heatmaps with annotated coefficients. Use Plotly to create web-ready, interactive charts with hover tooltips and dynamic zooming.",
                    "takeaways": [
                        "Build correlation heatmaps with annotated Pearson/Spearman coefficients to identify multicollinearity.",
                        "Combine boxplots with jittered strip plots to display both statistical summaries and true sample density.",
                        "Generate interactive HTML visualization widgets using Plotly for stakeholder distribution."
                    ],
                    "prompt_seed": "Write a Python snippet using Seaborn to plot a correlation heatmap of numeric features in a DataFrame with custom diverging color palette and annotations."
                }
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "Which visual encoding attribute is processed most accurately by human visual perception according to Cleveland and McGill's graphical hierarchy?",
                    "options": [
                        "Color saturation",
                        "Position along a common aligned scale",
                        "Area and volume",
                        "Angle and curvature"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 2,
                    "question": "Why must bar charts strictly have their quantitative axis start at zero?",
                    "options": [
                        "Because bar charts cannot render negative numbers otherwise",
                        "Because human perception judges the values by the physical length/height of the bar; non-zero baselines distort visual ratios",
                        "Because software will throw an error if zero is not included",
                        "To prevent the chart from overlapping with the legend"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 3,
                    "question": "What is the primary design purpose of a sparkline in an executive dashboard?",
                    "options": [
                        "To act as a decorative graphic without analytical meaning",
                        "To provide an ultra-compact, word-sized historical trend context alongside a headline KPI",
                        "To display 3D animated data transitions",
                        "To highlight statistical p-values"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 4,
                    "question": "When inspecting a correlation heatmap, what does a Pearson coefficient of -0.87 indicate between two variables?",
                    "options": [
                        "A very weak, statistically insignificant relationship",
                        "A strong negative linear relationship (as one variable increases, the other decreases)",
                        "A calculation error in the correlation formula",
                        "That 87% of the data consists of negative numbers"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 5,
                    "question": "What advantage does combining a jittered strip plot with a boxplot provide over a standalone boxplot?",
                    "options": [
                        "It turns the plot into an interactive 3D model",
                        "It reveals underlying sample size, clustering, and bi-modal distributions that standard boxplot quartiles conceal",
                        "It removes the need for axis labels",
                        "It automatically recalculates the mean"
                    ],
                    "correct_index": 1
                }
            ]
        },
        {
            "day": 7,
            "title": "End-to-End Analytics Capstone & Executive Communication",
            "subtopics": [
                {
                    "title": "Formulating Analytical Hypotheses & Project Charters",
                    "brief": "Transition from individual technical tasks to leading an end-to-end analytical project. Learn how to draft a structured data project charter: problem statement, measurable success criteria, primary and guardrail metrics, and risk assessment. Formulate testable, falsifiable business hypotheses before writing a single line of query code.",
                    "takeaways": [
                        "Establish clear primary North Star metrics and counter-balancing guardrail metrics to prevent unintended business harm.",
                        "Write testable analytical hypotheses with explicitly defined success/failure thresholds.",
                        "Align project scope, stakeholder expectations, and timeline milestones before commencing exploration."
                    ],
                    "prompt_seed": "How do you define guardrail metrics to ensure that a project aimed at increasing ad revenue doesn't silently destroy customer retention?"
                },
                {
                    "title": "End-to-End Analytics Pipeline: Ingestion to RFM Modeling",
                    "brief": "Execute a complete customer analytics case study. Ingest raw multi-table e-commerce data, sanitize timestamps and null values, build a Recency, Frequency, Monetary (RFM) segmentation engine in SQL and Python, score customer cohorts into tiers (Champions, At-Risk, Hibernating), and identify specific actionable revenue opportunities.",
                    "takeaways": [
                        "Compute Recency (days since last purchase), Frequency (order count), and Monetary value (total spend) scores.",
                        "Segment customer populations into distinct behavioral tiers to tailor commercial interventions.",
                        "Translate raw cluster metrics into concrete business implications (e.g. churn prevention vs re-activation)."
                    ],
                    "prompt_seed": "Explain the step-by-step mathematical logic for computing quintile-based RFM scores (1 to 5) for a database of 50,000 customers."
                },
                {
                    "title": "Executive Data Storytelling & The SCR Communication Framework",
                    "brief": "Deliver findings that drive executive decisions. Learn the Barbara Minto Pyramid Principle and the Situation-Complication-Resolution (SCR) storytelling framework. Master the one-page executive memo format. Practice leading with recommendations rather than technical methodology, handling executive skepticism, and quantifying financial business impact.",
                    "takeaways": [
                        "Lead communications with the core bottom-line recommendation (Pyramid Principle), not the step-by-step methodology.",
                        "Structure compelling business narratives using Situation, Complication, and Resolution (SCR).",
                        "Quantify financial ROI and operational effort so leadership can make immediate, confident decisions."
                    ],
                    "prompt_seed": "Draft a 3-paragraph executive memo for a Chief Operating Officer using the Situation-Complication-Resolution (SCR) format recommending an operational change based on delivery delay data."
                }
            ],
            "quiz": [
                {
                    "id": 1,
                    "question": "In customer analytics, what do the three dimensions of an RFM model evaluate?",
                    "options": [
                        "Revenue, Forecasting, and Marketing",
                        "Recency of last activity, Frequency of purchases, and Monetary spend value",
                        "Risk tolerance, Financial capability, and Market capitalization",
                        "Retention rate, Feedback score, and Margin percentage"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 2,
                    "question": "What is the primary role of a 'guardrail metric' in an analytical experiment or project charter?",
                    "options": [
                        "To protect the database server from CPU overheating",
                        "To ensure that optimizing the primary goal metric does not cause unintended negative side effects to core business health",
                        "To prevent junior analysts from running queries without approval",
                        "To automatically lock files against unauthorized modifications"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 3,
                    "question": "According to Barbara Minto's Pyramid Principle, how should findings be presented to senior executive stakeholders?",
                    "options": [
                        "Start with raw data, explain every cleaning step chronologically, and reveal conclusions at the very end",
                        "Start with the core recommendation/answer first, followed by supporting arguments grouped logically",
                        "Present only mathematical code and let executives determine their own conclusions",
                        "Always deliver a minimum 50-slide presentation before taking questions"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 4,
                    "question": "In the SCR communication framework, what does 'Complication' represent?",
                    "options": [
                        "A complex Python error traceback",
                        "The change, challenge, or emerging problem that disrupts the status quo and demands action",
                        "The mathematical difficulty of the algorithm used",
                        "The financial fee charged by external consultants"
                    ],
                    "correct_index": 1
                },
                {
                    "id": 5,
                    "question": "A customer has a high Monetary spend and high Frequency, but their Recency score is very low (has not purchased in 9 months). In RFM strategy, what segment do they belong to?",
                    "options": [
                        "New Customer",
                        "At-Risk / Can't Lose Them",
                        "Active Champion",
                        "Low-Value Transient"
                    ],
                    "correct_index": 1
                }
            ]
        }
    ]


def seed():
    with app.app_context():
        init_db()
        with get_db() as conn:
            # 1. Base test accounts
            p = set_password_hash("Password123")
            
            # Intern
            conn.execute(
                "INSERT OR IGNORE INTO intern_accounts (name, email, password_hash, password_set, is_active) VALUES (?,?,?,1,1)",
                ("Test Intern", "intern@example.com", p)
            )
            conn.execute("UPDATE intern_accounts SET password_hash=?, password_set=1, is_active=1 WHERE email=?", (p, "intern@example.com"))
            intern_row = conn.execute("SELECT id FROM intern_accounts WHERE email=?", ("intern@example.com",)).fetchone()
            intern_id = intern_row["id"]
            
            # Default Company
            conn.execute(
                "INSERT OR IGNORE INTO companies (name, email, password_hash, is_active, is_approved) VALUES (?,?,?,1,1)",
                ("Test Corp", "company@example.com", p)
            )
            conn.execute("UPDATE companies SET password_hash=?, is_active=1, is_approved=1 WHERE email=?", (p, "company@example.com"))
            
            # Staff & Admin
            conn.execute(
                "INSERT OR IGNORE INTO staff_accounts (name, email, password_hash, is_active) VALUES (?, ?, ?, 1)",
                ("Test Staff", "staff@example.com", p)
            )
            conn.execute("UPDATE staff_accounts SET password_hash=?, is_active=1 WHERE email=?", (p, "staff@example.com"))
            
            conn.execute(
                "INSERT OR IGNORE INTO staff_accounts (name, email, password_hash, is_active) VALUES (?, ?, ?, 1)",
                ("Test Admin", "admin@example.com", p)
            )
            conn.execute("UPDATE staff_accounts SET password_hash=?, is_active=1 WHERE email=?", (p, "admin@example.com"))
            
            # Mentor
            conn.execute(
                "INSERT OR IGNORE INTO mentors (name, email, password_hash) VALUES (?, ?, ?)",
                ("Test Mentor", "mentor@example.com", p)
            )
            conn.execute("UPDATE mentors SET password_hash=? WHERE email=?", (p, "mentor@example.com"))

            # 2. Company: AivaraTech InfoMatics
            aivara_email = "contactus@aivaratech.online"
            aivara_name = "AivaraTech InfoMatics"
            aivara_about = (
                "AivaraTech InfoMatics (AIVARA Technologies) operates under incubation with DBERT, "
                "delivering project-driven technology solutions, AI automation, and advanced data analytics "
                "across enterprise and research domains."
            )
            aivara_site = "https://aivaratechnologies.com"
            
            conn.execute(
                """
                INSERT OR IGNORE INTO companies (name, email, phone, website, about, password_hash, is_approved, is_active)
                VALUES (?, ?, ?, ?, ?, ?, 1, 1)
                """,
                (aivara_name, aivara_email, "+91 9998887776", aivara_site, aivara_about, p)
            )
            conn.execute(
                """
                UPDATE companies 
                SET name=?, website=?, about=?, password_hash=?, is_approved=1, is_active=1
                WHERE email=?
                """,
                (aivara_name, aivara_site, aivara_about, p, aivara_email)
            )
            
            company_row = conn.execute("SELECT id FROM companies WHERE email=?", (aivara_email,)).fetchone()
            company_id = company_row["id"]

            # 3. Post: Data Analytics Internship
            post_title = "Data Analytics Intern"
            post_slug = "data-analytics-intern-aivaratech"
            post_domain = "Data Analyst"
            post_type = "internship"
            post_openings = 50
            post_work_mode = "remote"
            post_location = "Remote"
            post_duration = "2 months"
            post_stipend = 5000
            
            post_description = (
                "Think of this as a working, learning-first role in a genuine, project-driven technology environment "
                "incubated with DBERT. As a Data Analytics Intern at AivaraTech InfoMatics, you will build up your analytical "
                "capabilities, work through assigned structured learning modules, and move into live project contribution "
                "across enterprise datasets, reporting pipelines, and BI dashboards.\n\n"
                "Internship Pathway:\n"
                "1. Learn: Orientation and structured technical learning covering Python, SQL, and data transformation concepts.\n"
                "2. Practise: Hands-on assignments, exploratory data analysis exercises, and reviewed mentor feedback.\n"
                "3. Contribute: Live project contributions across Aivara's data repositories and client analytics pipelines.\n"
                "4. Complete: Final project assessment, technical documentation, and formal exit clearances.\n\n"
                "Expected participation is approximately 10 hours per week, with full remote flexibility."
            )
            
            post_responsibilities = (
                "• Perform exploratory data analysis (EDA) on structured and semi-structured datasets to uncover actionable business insights.\n"
                "• Write and optimize clean SQL queries to extract, transform, and aggregate data across relational databases.\n"
                "• Build, maintain, and automate interactive dashboards and performance reports using Power BI, Tableau, or Python (Streamlit/Dash).\n"
                "• Develop Python data cleaning and preprocessing pipelines using Pandas and NumPy.\n"
                "• Collaborate closely with assigned mentors and technical supervisors on live client analytics deliverables.\n"
                "• Maintain clear data documentation, schema definitions, and version control via Git and GitHub."
            )
            
            post_skills = "Python, SQL, Excel, Power BI, Tableau, Pandas, NumPy, Data Visualization, EDA, Git"
            post_eligibility = "Pursuing or completed Bachelor's or Master's degree in Engineering, Computer Science, IT, BCA/MCA, Statistics, Mathematics, or related quantitative fields. Basic knowledge of Python, SQL, and Excel required."
            
            now = datetime.now()
            published_at = now.strftime("%Y-%m-%d %H:%M:%S")
            expires_at = (now + timedelta(days=90)).strftime("%Y-%m-%d %H:%M:%S")
            apply_by = (now + timedelta(days=30)).strftime("%Y-%m-%d")
            
            conn.execute("DELETE FROM posts WHERE company_id=? AND title=?", (company_id, post_title))
            conn.execute(
                """
                INSERT INTO posts (
                    company_id, post_type, domain, title, slug, description,
                    responsibilities, skills, location, work_mode,
                    stipend_min, stipend_max, pay_period, is_unpaid,
                    duration, openings, apply_by, certifications_json,
                    eligibility, status, published_at, expires_at, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'published', ?, ?, ?, ?)
                """,
                (
                    company_id, post_type, post_domain, post_title, post_slug, post_description,
                    post_responsibilities, post_skills, post_location, post_work_mode,
                    post_stipend, post_stipend, "monthly", 0,
                    post_duration, post_openings, apply_by, "[]",
                    post_eligibility, published_at, expires_at, published_at, published_at
                )
            )

            # 4. Course: Free 7-Day Professional Data Analytics Accelerated Course
            course_title = "Data Analytics Accelerated: Practical EDA, SQL & Business Intelligence"
            course_slug = "data-analytics-accelerated"
            course_domain = "Data Analyst"
            course_level = "Beginner to Intermediate"
            banner_gradient = "linear-gradient(135deg, #0284c7, #2563eb)"
            
            # Check if course exists
            existing_course = conn.execute("SELECT id FROM courses WHERE slug=?", (course_slug,)).fetchone()
            if existing_course:
                course_id = existing_course["id"]
                conn.execute(
                    """
                    UPDATE courses SET 
                        title=?, domain=?, company_id=?, is_paid=0, price_inr=0,
                        content_status='approved', source='custom', is_active=1,
                        level=?, estimated_hours=14, author_type='company', author_id=?,
                        requires_project=1, banner_gradient=?, updated_at=?
                    WHERE id=?
                    """,
                    (course_title, course_domain, company_id, course_level, company_id, banner_gradient, published_at, course_id)
                )
            else:
                cur = conn.execute(
                    """
                    INSERT INTO courses (
                        title, slug, domain, company_id, is_paid, price_inr,
                        content_status, source, is_active, level, estimated_hours,
                        author_type, author_id, requires_project, banner_gradient, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, 0, 0, 'approved', 'custom', 1, ?, 14, 'company', ?, 1, ?, ?, ?)
                    """,
                    (course_title, course_slug, course_domain, company_id, course_level, company_id, banner_gradient, published_at, published_at)
                )
                course_id = cur.lastrowid
            
            # Clear existing chapters, subtopics, and quizzes for this course to ensure clean idempotence
            old_chapters = conn.execute("SELECT id FROM course_chapters WHERE course_id=?", (course_id,)).fetchall()
            for ch in old_chapters:
                conn.execute("DELETE FROM course_subtopics WHERE chapter_id=?", (ch["id"],))
            conn.execute("DELETE FROM course_chapters WHERE course_id=?", (course_id,))
            conn.execute("DELETE FROM course_day_quizzes WHERE course_id=?", (course_id,))

            # Insert all 7 days of curriculum
            curriculum = get_data_analytics_curriculum()
            for day_data in curriculum:
                day_num = day_data["day"]
                ch_title = day_data["title"]
                
                ch_cur = conn.execute(
                    "INSERT INTO course_chapters (course_id, day_number, title, created_at) VALUES (?, ?, ?, ?)",
                    (course_id, day_num, ch_title, published_at)
                )
                chapter_id = ch_cur.lastrowid
                
                # Insert subtopics
                for idx, st in enumerate(day_data["subtopics"], 1):
                    conn.execute(
                        """
                        INSERT INTO course_subtopics (
                            chapter_id, sort_order, title, brief, key_takeaways_json, prompt_seed, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (chapter_id, idx, st["title"], st["brief"], json.dumps(st["takeaways"]), st["prompt_seed"], published_at)
                    )
                
                # Insert day quiz
                conn.execute(
                    "INSERT INTO course_day_quizzes (course_id, day_number, questions_json, created_at) VALUES (?, ?, ?, ?)",
                    (course_id, day_num, json.dumps(day_data["quiz"]), published_at)
                )

            # Seed Full Stack, AI Agent, and Python Automation courses
            from deploy.seed_all_courses import (
                seed_course,
                get_full_stack_curriculum,
                get_ai_agent_curriculum,
                get_python_automation_curriculum
            )
            for c_getter in [get_full_stack_curriculum, get_ai_agent_curriculum, get_python_automation_curriculum]:
                seed_course(conn, c_getter())

            # 5. Seed Lifecycle Interns (Covering all stages of the intern lifecycle)
            post_row = conn.execute("SELECT id FROM posts WHERE company_id=? AND title=?", (company_id, post_title)).fetchone()
            aivara_post_id = post_row["id"] if post_row else None
            
            lifecycle_accounts = [
                {
                    "stage": "Applied / Under Review",
                    "name": "Aarav Sharma",
                    "email": "applied.intern@example.com",
                    "phone": "+91 9876543210",
                    "city": "New Delhi",
                    "college": "Delhi Technological University",
                    "course": "B.Tech CSE",
                    "semester": "6",
                    "year_of_passing": "2027",
                    "domain": "Data Analyst",
                    "app_status": "Under Review",
                    "mentor_note": "Application received. Reviewing resume, portfolio, and screening test.",
                    "enrollment": None,
                    "attendance": None,
                    "job_app": None
                },
                {
                    "stage": "On Hold",
                    "name": "Priya Patel",
                    "email": "onhold.intern@example.com",
                    "phone": "+91 9876543211",
                    "city": "Pilani",
                    "college": "BITS Pilani",
                    "course": "B.E. Computer Science",
                    "semester": "8",
                    "year_of_passing": "2026",
                    "domain": "Data Analyst",
                    "app_status": "On Hold",
                    "mentor_note": "Application on hold pending next cohort capacity allocation window.",
                    "enrollment": None,
                    "attendance": None,
                    "job_app": None
                },
                {
                    "stage": "Selected (Deposit Required)",
                    "name": "Rohan Verma",
                    "email": "selected.intern@example.com",
                    "phone": "+91 9876543212",
                    "city": "Roorkee",
                    "college": "IIT Roorkee",
                    "course": "B.Tech",
                    "semester": "6",
                    "year_of_passing": "2027",
                    "domain": "Data Analyst",
                    "app_status": "Selected",
                    "mentor_note": "Selected for Data Analytics track! Please pay refundable commitment deposit to confirm seat.",
                    "enrollment": None,
                    "attendance": None,
                    "job_app": None
                },
                {
                    "stage": "Enrolled (Verification Pending)",
                    "name": "Sneha Kulkarni",
                    "email": "enrolled.intern@example.com",
                    "phone": "+91 9876543213",
                    "city": "Pune",
                    "college": "COEP Pune",
                    "course": "B.Tech IT",
                    "semester": "8",
                    "year_of_passing": "2026",
                    "domain": "Data Analyst",
                    "app_status": "Enrolled",
                    "mentor_note": "Payment proof uploaded; pending admin banking verification.",
                    "enrollment": {
                        "payment_status": "Pending Verification",
                        "joining_date": (now + timedelta(days=5)).strftime("%Y-%m-%d"),
                        "batch_label": "DA-Spring-2026-Batch",
                        "payment_screenshot": "uploads/sample_proof.jpg"
                    },
                    "attendance": None,
                    "job_app": None
                },
                {
                    "stage": "Accepted (Active Live Intern)",
                    "name": "Vikram Malhotra",
                    "email": "accepted.intern@example.com",
                    "phone": "+91 9876543214",
                    "city": "Tiruchirappalli",
                    "college": "NIT Trichy",
                    "course": "B.Tech",
                    "semester": "6",
                    "year_of_passing": "2027",
                    "domain": "Data Analyst",
                    "app_status": "Accepted",
                    "mentor_note": "Verified & Accepted. Welcome to AivaraTech InfoMatics Data Analytics team!",
                    "enrollment": {
                        "payment_status": "Verified",
                        "joining_date": (now - timedelta(days=14)).strftime("%Y-%m-%d"),
                        "batch_label": "DA-Alpha-2026",
                        "payment_screenshot": "uploads/verified_payment.jpg"
                    },
                    "attendance": {
                        "weeks": [
                            {"offset_weeks": 0, "mins": 435},  # Current week (7h 15m)
                            {"offset_weeks": 1, "mins": 690},  # Week -1 (11h 30m - Met)
                            {"offset_weeks": 2, "mins": 615},  # Week -2 (10h 15m - Met)
                            {"offset_weeks": 3, "mins": 480},  # Week -3 (8h 0m - Below 10h)
                        ]
                    },
                    "job_app": None
                },
                {
                    "stage": "Rejected (With Reapply & Paid Options)",
                    "name": "Ananya Roy",
                    "email": "rejected.intern@example.com",
                    "phone": "+91 9876543215",
                    "city": "Kolkata",
                    "college": "Jadavpur University",
                    "course": "B.Sc Computer Science",
                    "semester": "4",
                    "year_of_passing": "2028",
                    "domain": "Data Analyst",
                    "app_status": "Rejected",
                    "mentor_note": "Thank you for applying. At this stage, candidates with more advanced SQL/Python experience were prioritized. You may reapply in 18 days or join our Paid Guaranteed Placement Track.",
                    "rejected_at": (now - timedelta(days=12)).strftime("%Y-%m-%d %H:%M:%S"),
                    "enrollment": None,
                    "attendance": None,
                    "job_app": None
                },
                {
                    "stage": "Paid-Enrolled (Direct Placement Track)",
                    "name": "Kabir Mehta",
                    "email": "paidenrolled.intern@example.com",
                    "phone": "+91 9876543216",
                    "city": "Pune",
                    "college": "Symbiosis Institute",
                    "course": "BCA / MCA",
                    "semester": "6",
                    "year_of_passing": "2027",
                    "domain": "Data Analyst",
                    "app_status": "Paid-Enrolled",
                    "mentor_note": "Enrolled in Paid Direct Track. Career mentor assigned.",
                    "enrollment": {
                        "payment_status": "Verified",
                        "joining_date": (now - timedelta(days=2)).strftime("%Y-%m-%d"),
                        "batch_label": "Paid-Guaranteed-Placement-Batch-A",
                        "payment_screenshot": "uploads/paid_track_receipt.jpg"
                    },
                    "attendance": {
                        "cur_mins": 300,
                        "prev_mins": 0
                    },
                    "job_app": None
                },
                {
                    "stage": "Job Board Hired (__JOB_ONLY__)",
                    "name": "Neha Gupta",
                    "email": "jobhired.intern@example.com",
                    "phone": "+91 9876543217",
                    "city": "Vellore",
                    "college": "VIT Vellore",
                    "course": "B.Tech CSE",
                    "semester": "8",
                    "year_of_passing": "2026",
                    "domain": "Data Analyst",
                    "app_status": None,  # No standard portal application
                    "mentor_note": None,
                    "enrollment": None,
                    "attendance": None,
                    "job_app": {
                        "post_id": aivara_post_id,
                        "status": "Hired",
                        "decision_note": "Congratulations! Selected for Data Analytics Intern position at AivaraTech InfoMatics."
                    }
                }
            ]

            from app import get_week_bounds
            week_start, week_end = get_week_bounds(now.date())
            ws_str = week_start.strftime("%Y-%m-%d")
            we_str = week_end.strftime("%Y-%m-%d")
            
            prev_ws_dt, prev_we_dt = get_week_bounds(week_start - timedelta(days=2))
            prev_ws_str = prev_ws_dt.strftime("%Y-%m-%d")
            prev_we_str = prev_we_dt.strftime("%Y-%m-%d")

            print("\nSeeding Lifecycle Intern Accounts:")
            for acc in lifecycle_accounts:
                em = acc["email"]
                nm = acc["name"]
                
                # 1. Create intern account
                conn.execute(
                    """
                    INSERT OR IGNORE INTO intern_accounts (
                        name, email, phone, city, college, course, semester,
                        year_of_passing, domain, password_hash, password_set, is_active
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 1)
                    """,
                    (nm, em, acc["phone"], acc["city"], acc["college"], acc["course"], acc["semester"], acc["year_of_passing"], acc["domain"], p)
                )
                conn.execute(
                    """
                    UPDATE intern_accounts SET 
                        name=?, phone=?, city=?, college=?, course=?, semester=?,
                        year_of_passing=?, domain=?, password_hash=?, password_set=1, is_active=1
                    WHERE email=?
                    """,
                    (nm, acc["phone"], acc["city"], acc["college"], acc["course"], acc["semester"], acc["year_of_passing"], acc["domain"], p, em)
                )
                acct_row = conn.execute("SELECT id FROM intern_accounts WHERE email=?", (em,)).fetchone()
                acc_id = acct_row["id"]

                # 2. Application (if applicable)
                if acc["app_status"]:
                    rej_at = acc.get("rejected_at")
                    conn.execute("DELETE FROM applications WHERE email=?", (em,))
                    conn.execute(
                        """
                        INSERT INTO applications (
                            name, email, phone, city, college, course, semester,
                            year_of_passing, domain, why_join, status, mentor_note,
                            reviewed_at, rejected_at, created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            nm, em, acc["phone"], acc["city"], acc["college"], acc["course"],
                            acc["semester"], acc["year_of_passing"], acc["domain"],
                            "Passionate about applying data analytics to drive business decisions.",
                            acc["app_status"], acc["mentor_note"],
                            published_at, rej_at, published_at, published_at
                        )
                    )
                    app_row = conn.execute("SELECT id FROM applications WHERE email=?", (em,)).fetchone()
                    app_id = app_row["id"]
                    conn.execute("UPDATE intern_accounts SET application_id=? WHERE id=?", (app_id, acc_id))
                else:
                    conn.execute("DELETE FROM applications WHERE email=?", (em,))
                    app_id = None

                # 3. Enrollment row (if applicable)
                if acc["enrollment"]:
                    e_info = acc["enrollment"]
                    conn.execute("DELETE FROM enrollments WHERE email=?", (em,))
                    conn.execute(
                        """
                        INSERT INTO enrollments (
                            application_id, timestamp, name, email, phone,
                            city, college, course, semester, year_of_passing, domain,
                            joining_date, batch_label, payment_screenshot, payment_status,
                            created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            app_id, published_at, nm, em, acc["phone"],
                            acc["city"], acc["college"], acc["course"], acc["semester"],
                            acc["year_of_passing"], acc["domain"], e_info["joining_date"],
                            e_info["batch_label"], e_info["payment_screenshot"],
                            e_info["payment_status"], published_at, published_at
                        )
                    )

                # 4. Attendance (if applicable)
                if acc["attendance"]:
                    conn.execute("DELETE FROM attendance WHERE intern_id=?", (acc_id,))
                    weeks_list = acc["attendance"].get("weeks")
                    if weeks_list:
                        for w_item in weeks_list:
                            off = w_item["offset_weeks"]
                            w_start, w_end = get_week_bounds(now.date() - timedelta(days=7 * off))
                            conn.execute(
                                "INSERT INTO attendance (intern_id, week_start, week_end, total_minutes, updated_at) VALUES (?, ?, ?, ?, ?)",
                                (acc_id, w_start.strftime("%Y-%m-%d"), w_end.strftime("%Y-%m-%d"), w_item["mins"], published_at)
                            )
                    else:
                        att = acc["attendance"]
                        # Current week
                        if att.get("cur_mins", 0) > 0:
                            conn.execute(
                                "INSERT INTO attendance (intern_id, week_start, week_end, total_minutes, updated_at) VALUES (?, ?, ?, ?, ?)",
                                (acc_id, ws_str, we_str, att["cur_mins"], published_at)
                            )
                        # Previous week
                        if att.get("prev_mins", 0) > 0:
                            conn.execute(
                                "INSERT INTO attendance (intern_id, week_start, week_end, total_minutes, updated_at) VALUES (?, ?, ?, ?, ?)",
                                (acc_id, prev_ws_str, prev_we_str, att["prev_mins"], published_at)
                            )

                # 5. Course enrollment for active intern
                if acc["app_status"] in ("Accepted", "Paid-Enrolled"):
                    conn.execute("DELETE FROM course_enrollments WHERE intern_id=? AND course_id=?", (acc_id, course_id))
                    cur_d = 3 if acc["app_status"] == "Accepted" else 1
                    conn.execute(
                        """
                        INSERT INTO course_enrollments (intern_id, course_id, enrolled_at, last_accessed_at, current_day)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (acc_id, course_id, published_at, published_at, cur_d)
                    )

                # 6. Job application (if applicable)
                if acc["job_app"] and aivara_post_id:
                    ja = acc["job_app"]
                    conn.execute("DELETE FROM post_applications WHERE intern_id=? AND post_id=?", (acc_id, aivara_post_id))
                    cur_ja = conn.execute(
                        """
                        INSERT INTO post_applications (
                            post_id, intern_id, comment, status, created_at
                        ) VALUES (?, ?, 'Eager to contribute my analytical skills at AivaraTech InfoMatics.', ?, ?)
                        """,
                        (aivara_post_id, acc_id, ja["status"], published_at)
                    )
                    ja_id = cur_ja.lastrowid
                    # Also create pending deposit prompt
                    conn.execute("DELETE FROM post_hire_deposits WHERE post_application_id=?", (ja_id,))
                    conn.execute(
                        """
                        INSERT INTO post_hire_deposits (
                            post_application_id, intern_id, post_id, amount, status, created_at
                        ) VALUES (?, ?, ?, 499, 'pending', ?)
                        """,
                        (ja_id, acc_id, aivara_post_id, published_at)
                    )

                print(f" • [{acc['stage']}] {nm} -> {em}")

            conn.commit()
            print("==========================================================")
            print("Successfully seeded full Data Analytics course ecosystem:")
            print(f" • Company: {aivara_name} (ID: {company_id})")
            print(f" • Internship: {post_title} (Openings: {post_openings}, Status: published)")
            print(f" • Course: {course_title} (ID: {course_id}, Slug: {course_slug})")
            print("   - Cost: FREE (price_inr=0, is_paid=0)")
            print("   - Chapters: 7 structured daily modules")
            print("   - Subtopics: 21 comprehensive lesson briefs with prompt seeds")
            print("   - Quizzes: 7 daily assessments (35 questions total)")
            print("   - All 8 Lifecycle Stage Interns Seeded with Password123")
            print("==========================================================")

if __name__ == "__main__":
    seed()
