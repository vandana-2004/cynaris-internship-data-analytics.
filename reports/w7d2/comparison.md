# AutoViz vs SweetViz — Business Recommendation

Both tools automate exploratory data analysis, but their generated outputs differ.

AutoViz produced five HTML visualizations for the 9,994-row Superstore dataset: categorical plots, numeric distributions, heatmaps, pair scatter plots, and violin plots. It completed successfully, although its logs reported classification limitations for several string columns and no detected date variables.

SweetViz generated a structured HTML report using a reproducible sample of 5,000 rows. Its report is a convenient single artifact for sharing variable summaries and visualizations with stakeholders.

**Recommendation:** Use SweetViz as the primary stakeholder-facing report because it offers a consolidated report that is straightforward to share. Keep AutoViz as a complementary tool for exploring specific visual patterns. Validate automated outputs and add business context before making decisions.
