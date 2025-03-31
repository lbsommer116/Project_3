# Project 3 - US Real Estate Dashboard

## Purpose

In our analysis, we used Zillow data to create a dynamic dashboard that visualizes housing market trends in major metropolitan cities across the United States. The dashboard features a plethora of interactive visuals—including maps, bar charts, and a line graph—that enable users to explore various aspects of the housing market. This interactivity provides a comprehensive and user-friendly way to analyze how market conditions have evolved over time nationwide.

## Instructions for Repository
---
- **Data Folder**: Raw csv files (from database)
- **data_pipeline**: Jupyter notebook showing data transformations
- **final_csv_clean**: Jupyter notebook used to create final avg CSVs to use for our visualizations
- **avg CSVs**: Final CSVs used for visualizations (output from final_csv_clean)
- **real_estate_app.py**: This is where our Dash visualization code lives and where the our app can be run to generate our live dashboard.
  
## Instructions for Using the Dashboard Visuals

### Map Visualization (Neighborhood Price Heatmap)

- **Dropdown Menu**: Use the dropdown to select the dataset you’re interested in (e.g., Home Values, Rent Prices, Inventory Levels).
- **Year Toggle**: Adjust the year toggle to explore how the data has changed over time.
- **Interpretation**: The map will update to show color-coded neighborhoods based on their selected metric, allowing you to quickly compare prices across different areas. Darker or lighter shades represent higher or lower values, depending on the dataset.

### Bar Chart (Cities vs. U.S. Average)

- **Dropdown Menu**: Choose your dataset (e.g., Median Home Value, Rent Price, etc.) from the dropdown to change the metric being displayed.
- **Year Toggle**: Use the toggle to switch between years and see how city rankings and values have changed over time.
- **Interpretation**: The user has the ability to sort cities by highest or lowest value and choose the number of cities shown on the bar chart based on the selected dataset. There is a line that represents the U.S. average, providing quick insight into which cities are above or below national trends.

### Line Graph (Time Series Trends)

- **Dropdown Menu**: Select a dataset to explore long-term trends (e.g., Home Prices Over Time).
- **City Selection**: Choose one or more cities to compare their trends across years.
- **Interpretation**: The line graph will display how your selected metric has evolved over time, helping identify growth, dips, or stability in different markets.

---

## Summary of Efforts for Ethical Considerations

Throughout the development of this project, we prioritized ethical considerations to ensure responsible data use and representations. We relied on available public data from Zillow, carefully reviewing usage rights and only using the data that is publicly available to us. We did not intend this for monetary value; we have utilized this data solely for educational purposes.

---

## References from Data Sources

- **Zillow**: [https://www.zillow.com/research/data/](https://www.zillow.com/research/data/)
- **GeoApify**: [https://www.geoapify.com/](https://www.geoapify.com/)

---

## References for Code Used

- **Dash (Plotly)**: [https://dash.plotly.com/](https://dash.plotly.com/)
- **ChatGPT**: Assistance was provided in writing parts of the code for the dashboard.

## See link for the Slide Deck: 
https://docs.google.com/presentation/d/13yfYbopridL7EYdFsRZsaducQ8QHRasq4QYWzmIYnXI/edit?usp=sharing

