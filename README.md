Upload & Go Sales Analytics Dashboard for Retail (Streamlit, Pandas, Plotly)

Empower data-driven decisions in your retail business with this interactive dashboard! Analyze sales data to understand trends, customer behavior, and product performance.

## Live Demo Site
https://upload-to-sales-analysis.streamlit.app/



## Features

- **Dynamic Filtering**: Users can filter the sales data by various criteria, including:
    * Client names 
    * Item names
    * Categories
    * Date range (start and end date pickers)
    * Age range (using a slider)
    * Gender (through checkboxes)
    * Season (through checkboxes)
- **Local Excel File Upload & Real-time Analysis**: Users can upload their own Excel files directly through the dashboard interface, enabling immediate analysis and visualization of their sales data without any preprocessing required.
- **Interactive Visualizations:** The dashboard utilizes Plotly to create a variety of interactive charts and tables, allowing users to drill down into the data and gain clearer understanding. Chart types include:
    * **Pie charts:** Visualize sales distribution across categories or for a specific category.
    * **Scatter plots:** Examine the relationship between customer age and total spending, differentiated by gender.
    * **Grouped bar charts:** Illustrate monthly spending trends by gender (Male/Female).
    * **Horizontal bar charts:** Highlight the top-selling items for 2022.
- **Data Cleaning and Analysis (Pandas):** The dashboard utilizes Pandas for cleaning and analyzing the sales data loaded from CSV files. This may involve handling missing values, formatting data types, or filtering outliers to ensure accurate and insightful visualizations.



## Run Locally

Clone the project

```bash
  git clone https://github.com/jczzz/Upload_To_Go_Sales_Analysis.git
```

Go to the project directory

```bash
  cd Upload_To_Go_Sales_Analysis
```

Create a virtual environment:
  •	On macOS and Linux:
    ```bash
      python3 -m venv venv
    ```
  •	On Windows:
    ```bash
      python -m venv venv
    ```

Activate the virtual environment:
  •	On macOS and Linux:
    ```bash
      source venv/bin/activate
    ```
  •	On Windows:
    ```bash
      venv\Scripts\activate
    ```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  streamlit run main.py
```


