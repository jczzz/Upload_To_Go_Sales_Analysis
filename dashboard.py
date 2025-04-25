import streamlit as st
import pandas as pd
import datetime
from sidebar import sidebar_config
from category_sales_pie_chart import create_pie_chart
from scatter_graph import create_scatter_plot2
from grouped_bar_chart import create_grouped_bar_chart
from top_selling_items import create_horizontal_bar_chart

def init_dashboard(projection):
    """
    The start-up function wait for the user to upload the Excel file then start the dashboard
    Params:
     projection: the columns to project in the data frame
    Return:
         None
    """
    # Create the Tab configuration for the page
    st.set_page_config(page_title='Upload & Go Sales Analytics', page_icon=':bar_chart:', layout='wide')
    # Create the main header of the page
    header()
    
    # Create the container for file upload
    holder = st.empty()
    
    # The upload file container with instructions
    st.info("Please upload an Excel file containing sheets: 'users', 'transactions', and 'items'")
    
    # File upload section
    uploaded_file = st.file_uploader("Choose upload the sales analytics excel file", type="xlsx", accept_multiple_files=False)
    
    # Add a divider and default data option
    #st.markdown("---")
    use_default = st.button("📊 Load Sample Data", 
                           help="Load sample data from sales_analytics_2024.xlsx",
                           use_container_width=True)
    
    # Process the file (either uploaded or default)
    if uploaded_file is not None or use_default:
        try:
            # Read the file (sheet_name=None -> read all the sheets in the file)
            if use_default and uploaded_file is None:
                default_file = "Excel_file_to_upload/sales_analytics_2024.xlsx"
                try:
                    df = pd.read_excel(default_file, sheet_name=None)
                    st.success("Successfully loaded default data file!")
                except Exception as e:
                    st.error(f"Error loading default file: {str(e)}")
                    return
            else:
                df = pd.read_excel(uploaded_file, sheet_name=None)
            
            # Verify required sheets exist
            required_sheets = ['users', 'transactions', 'items']
            if not all(sheet in df.keys() for sheet in required_sheets):
                st.error("Error: The Excel file must contain sheets named: 'users', 'transactions', and 'items'")
                return
                
            # Merge all the sheets to a data frame
            merged_df = merge_sheets_in_excel_file(df)
            if merged_df is not None:
                # Start the dashboard configuration with the data frame
                dashboard_config(merged_df, projection)
            
        except Exception as e:
            st.error(f"Error processing the file: {str(e)}")
            return
    else:
        # Show example data format when no file is uploaded
        st.markdown("""
        ### Expected Excel File Format:
        Your Excel file should contain three sheets:
        1. **users**: Contains user information with columns:
        - user_id
        - full_name
        - birth_date
        - gender
        2. **transactions**: Contains transaction details with columns:
        - user_id
        - item_id
        - amount
        - order_date
        3. **items**: Contains item information with columns:
        - item_id
        - item_name
        - category
        - item_tags
        - season
        - printing
        - price
        """)

def merge_sheets_in_excel_file(df):
    """
    Merge the sheets and perform a join on the user_id and item_id to the desired data frame
    Args:
     df: an unfiltered data frame
    Return:
         merged_df: a merged data frame
    """
    try:
        sheet_dict = {sheet_name: data_frame for sheet_name, data_frame in df.items()} #字典生成/推导式Dict Comprehension
        
        # Clean up column names (remove any whitespace and convert to lowercase)
        for sheet_name in sheet_dict:
            # Convert column names to strings and then apply transformations 列名处理方式，确保能处理各种格式的Excel文件
            sheet_dict[sheet_name].columns = [str(col).strip().lower() for col in sheet_dict[sheet_name].columns] #列表推导式List Comprehension
        
        # Ensure data types are correct before merging  (合并前的数据类型转换和验证)
        # Users sheet
        if 'birth_date' in sheet_dict['users'].columns:
            sheet_dict['users']['birth_date'] = pd.to_datetime(sheet_dict['users']['birth_date'])
        sheet_dict['users']['user_id'] = sheet_dict['users']['user_id'].astype(str)
        
        # Transactions sheet
        sheet_dict['transactions']['user_id'] = sheet_dict['transactions']['user_id'].astype(str)
        sheet_dict['transactions']['item_id'] = sheet_dict['transactions']['item_id'].astype(str)
        if 'order_date' in sheet_dict['transactions'].columns:
            sheet_dict['transactions']['order_date'] = pd.to_datetime(sheet_dict['transactions']['order_date'])
        sheet_dict['transactions']['amount'] = pd.to_numeric(sheet_dict['transactions']['amount'], errors='coerce')
        
        # Items sheet
        sheet_dict['items']['item_id'] = sheet_dict['items']['item_id'].astype(str)
        sheet_dict['items']['price'] = pd.to_numeric(sheet_dict['items']['price'], errors='coerce')
        
        # Perform the merges  执行合并
        merged_df = pd.merge(sheet_dict['users'], sheet_dict['transactions'], on='user_id', how='inner')
        merged_df = pd.merge(merged_df, sheet_dict['items'], on='item_id', how='inner')
        
        # Verify the merged dataframe has data
        if merged_df.empty:
            st.error("Error: No matching data found between sheets. Please check if the join keys (user_id, item_id) match.")
            return None
            
        return merged_df
        
    except Exception as e:
        st.error(f"Error merging sheets: {str(e)}")
        return None


def dashboard_config(main_data_frame, projection):
    """
    Configure the sales dashboard. The main body of the page

    Args:
        main_data_frame (pd.DataFrame): The DataFrame containing the transactions and user information.
        projection (list): The list of string representing the selected columns to project in the DataFrame.

    Returns:
        None
    """
    if main_data_frame is None:
        st.error("No data to display. Please check your Excel file format and try again.")
        return

    # Convert column names to lowercase for case-insensitive matching  转换确保列名
    main_data_frame.columns = [str(col).strip().lower() for col in main_data_frame.columns]
    projection = [str(col).strip().lower() for col in projection]

    # Convert the birth_date column to age column for easier manipulations.
    main_data_frame = convert_birth_date_to_age_column(main_data_frame)

    # Pass the data through the sidebar's filters and get back the filtered data frame
    filtered_data_frame = sidebar_config(main_data_frame[projection])

    if filtered_data_frame.empty:
        st.warning("No data matches the current filters. Try adjusting the filter criteria.")
        return

    # Convert the order date to format: dd/mm/yyyy
    if 'order_date' in filtered_data_frame.columns:
        filtered_data_frame['order_date'] = filtered_data_frame['order_date'].dt.strftime('%m/%d/%Y')

    # The top row kpi(avg, total and amount of transactions), plus add the 'total' column to the data frame
    top_row_kpi(filtered_data_frame)

    # Display the table data frame
    st.dataframe(filtered_data_frame, use_container_width=True, hide_index=True)

    # Create the charts from the filtered data_frame
    pie_chart, horizontal_bar, grouped_bar, scatter_plot = create_charts(filtered_data_frame)

    # Create a Divider under the main table
    st.markdown('---')

    # Create the first row containing the pie chart and the horizontal bar chart
    left_col, right_col = st.columns(2)
    with left_col:
        st.plotly_chart(pie_chart)
    with right_col:
        st.plotly_chart(horizontal_bar)

    # Create the second row containing the grouped bar chart and the scatter plot
    left_col, right_col = st.columns(2)
    with left_col:
        st.plotly_chart(grouped_bar)
    with right_col:
        st.plotly_chart(scatter_plot)


def convert_birth_date_to_age_column(main_data_frame):
    # Convert birth_date column to datetime
    main_data_frame['birth_date'] = pd.to_datetime(main_data_frame['birth_date'])

    # Calculate age based on birthdate
    current_year = datetime.datetime.now().year
    main_data_frame['age'] = current_year - main_data_frame['birth_date'].dt.year

    return main_data_frame


def create_charts(data_frame: pd.DataFrame):
    """
    Creates various charts based on the filtered data frame.
    Args:
     data_frame (pd.DataFrame): The DataFrame containing the filtered data.
    Returns:
        tuple: A tuple containing the pie chart, horizontal bar chart, grouped bar chart, and scatter plot.
    """
    pie_chart = create_pie_chart(data_frame)
    horizontal_bar = create_horizontal_bar_chart(data_frame)
    grouped_bar = create_grouped_bar_chart(data_frame)
    scatter_plot = create_scatter_plot2(data_frame)
    return pie_chart, horizontal_bar, grouped_bar, scatter_plot


def top_row_kpi(data_frame):
    """
    Display key performance indicators (KPIs) in the top row. And add the total column to the
    data frame representing the total amount of the transaction.

    Args:
        data_frame (pd.DataFrame): The DataFrame containing the sales data.

    Returns:
        None
    """
    # Calculate the total amount for each transaction by multiplying 'amount' and 'price' columns
    data_frame['total'] = data_frame['amount'] * data_frame['price']

    # Check if only a single item is selected
    is_single_item_selected = len(data_frame.groupby('item_name').count()) <= 1

    # Calculate the total sum, average sale, total sales amount, and number of transactions
    total_sum = int(data_frame['total'].sum())
    avg_sale = round(data_frame['total'].mean(), 2)
    avg_sale = avg_sale if avg_sale > 0 else 0
    total_sales_amount = int(data_frame['amount'].sum())
    transactions_amount = len(data_frame)

    # Set the title and value based on whether a single item is selected or not
    if not is_single_item_selected:
        title = 'Total Transactions:'
        value = transactions_amount
    else:
        title = 'Total Units Sold:'
        value = total_sales_amount

    # Display the KPIs in three columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Total Sales:")
        st.subheader(f'💲 {total_sum:,.2f}')
    with col2:
        st.subheader("Avg Sale:")
        st.subheader(f'💲 {avg_sale:,.2f}')
    with col3:
        st.subheader(title)
        st.subheader(f':hash: {value:,}')


def header():
    """
    Display the header of the sales dashboard.

    Returns:
        None
    """
    st.title(':bar_chart: Upload & Go Sales Analytics')
    st.markdown('---')
