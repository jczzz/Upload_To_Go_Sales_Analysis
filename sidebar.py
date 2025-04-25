import streamlit as st
import pandas as pd


#侧边栏组件(过滤器和控制选项)
def sidebar_config(data_frame):
    """
       Configure the sidebar for filtering options and generate a filtered DataFrame.

       Args:
           data_frame (pd.DataFrame): The original DataFrame containing the data.

       Returns:
           pd.DataFrame: The filtered DataFrame based on the sidebar selections.
       """
    # Set the sidebar's header
    st.sidebar.header('Please Filter Here:')

    # Get the inputs from the selects and checkboxes
    full_name, item_name, category, printing = init_sidebar_selects(data_frame)

    # Double end slider for the ages range
    age_slider = st.sidebar.slider('Choose Range of Ages:', value=[8, 90], max_value=120)

    male_check, female_check, winter_check, summer_check = init_sidebar_checkboxes()
    # A divider
    st.sidebar.markdown('---')

    # Get the input from the date inputs
    start_date, end_date = init_sidebar_dates_pickers(data_frame)

    # Get the values from the checkboxes item tags and season
    gender, season = get_value_from_checkbox_sidebar(male_check, female_check, winter_check, summer_check)
    
    try:
        # Convert start_date and end_date to datetime
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        # Basic filters that should always be applied
        df_filtered = data_frame.copy()
        
        # Apply age filter
        df_filtered = df_filtered[
            (df_filtered['age'] >= age_slider[0]) & 
            (df_filtered['age'] <= age_slider[1])
        ]
        
        # Apply gender filter
        if gender:
            df_filtered = df_filtered[df_filtered['gender'].isin(gender)]
            
        # Apply season filter
        if season:
            df_filtered = df_filtered[df_filtered['season'].isin(season)]
            
        # Apply date filter
        df_filtered = df_filtered[
            (df_filtered['order_date'] >= start_date) & 
            (df_filtered['order_date'] <= end_date)
        ]
        
        # Apply optional filters
        if full_name:
            df_filtered = df_filtered[df_filtered['full_name'].isin(full_name)]
            
        if item_name:
            df_filtered = df_filtered[df_filtered['item_name'].isin(item_name)]
            
        if category:
            df_filtered = df_filtered[df_filtered['category'].isin(category)]
            
        if printing:
            df_filtered = df_filtered[df_filtered['printing'].isin(printing)]
        
        return df_filtered
        
    except Exception as e:
        st.error(f"Error in filtering: {str(e)}")
        return data_frame


def init_selects_queries_dict():
    """
        Initialize a dictionary of filtering queries for select options.

        Returns:
            dict: A dictionary containing the filtering queries for select options.
        """
    queries = {}
    queries['item_name_query'] = ' item_name == @item_name '
    queries['client_name_query'] = ' full_name == @full_name '
    queries['printing_query'] = ' printing == @printing '
    queries['category_query'] = ' category == @category '
    return queries


def build_final_query_string(full_name, item_name, category, printing, queries_dict):
    """
    Build the final query string based on the selected values.

    Args:
        full_name (list): The selected client names.
        item_name (list): The selected item names.
        category (list): The selected categories.
        printing (list): The selected printing options.
        queries_dict (dict): The dictionary of queries for select options.

    Returns:
        conditions_query (str): The final query string.
    """
    conditions = []
    # Check if client names are selected and add the corresponding query
    if full_name:
        conditions.append(queries_dict['client_name_query'])

    # Check if item names are selected and add the corresponding query
    if item_name:
        conditions.append(queries_dict['item_name_query'])

    # Check if categories are selected and add the corresponding query
    if category:
        conditions.append(queries_dict['category_query'])

    # Check if printing options are selected and add the corresponding query
    if printing:
        conditions.append(queries_dict['printing_query'])

    # Join all the conditions using 'and' to form the final query string
    conditions_query = ' and '.join(conditions)

    return conditions_query



def init_sidebar_selects(data_frame):
    """
        Initialize the sidebar select options.

        Args:
            data_frame (pd.DataFrame): The original DataFrame containing the data.

        Returns:
            tuple: The selected client names, item names, categories, and printing options.
        """
    # Initialize the sidebar select options for client names, item names, printing options, and categories
    full_name = st.sidebar.multiselect(
        'Select the client name:',
        options=data_frame['full_name'].unique(),
    )

    item_name = st.sidebar.multiselect(
        'Select a specific item:',
        options=data_frame['item_name'].unique()
    )
    printing = st.sidebar.multiselect(
        'Select the Texture:',
        options=data_frame['printing'].unique(),
    )
    category = st.sidebar.multiselect(
        'Select the category:',
        options=data_frame['category'].unique(),
    )
    # Return the selected values as a tuple
    return full_name, item_name, category, printing


def init_sidebar_checkboxes():
    """
        Initialize the sidebar checkboxes.

        Returns:
            tuple: The selected checkbox values.
        """
    # Initialize the sidebar checkboxes and return the values
    st.sidebar.header('Gender:')
    male_check = st.sidebar.checkbox('Male', value=True)
    female_check = st.sidebar.checkbox('Female', value=True)


    st.sidebar.header('Select a Season:')
    winter_check = st.sidebar.checkbox('fall/winter', value=True)
    summer_check = st.sidebar.checkbox('spring/summer', value=True)
    return male_check, female_check, winter_check, summer_check


def init_sidebar_dates_pickers(data_frame):
    """
        Initialize the sidebar date pickers.

        Args:
            data_frame (pd.DataFrame): The original DataFrame containing the data.

        Returns:
            tuple: The selected start and end dates.
        """
    # Convert the order_date column to datetime for manipulation and find the min and max value
    data_frame['order_date'] = pd.to_datetime(data_frame['order_date'])
    min_date = data_frame['order_date'].min()
    max_date = data_frame['order_date'].max()
    # Initialize the sidebar date pickers and define the min and max value to choose from
    start_date = st.sidebar.date_input('Start date', min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.sidebar.date_input('End date', min_value=min_date, max_value=max_date, value=max_date)
    # Return the values
    return start_date, end_date


def get_value_from_checkbox_sidebar(male_check, female_check, winter_check, summer_check):
    """
       Get the values from the checkbox sidebar.

       Args:
           male_check (bool): The value of the Male checkbox.
           female_check (bool): The value of the Female checkbox.
           winter_check (bool): The value of the winter checkbox.
           summer_check (bool): The value of the summer checkbox.

       Returns:
           tuple: The selected item tags and season values. To show in the data frame
       """
    item_tags = []
    season = []
    # Check the values of the checkboxes if true add them to the filtering query (all included will show)
    if male_check:
        item_tags.append('male')
    if female_check:
        item_tags.append('female')
    if winter_check:
        season.append('fall/winter')
    if summer_check:
        season.append('spring/summer')
    return item_tags, season
