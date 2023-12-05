import pandas as pd
import streamlit as st
import schedule 
import time 
import random

# Define the numbered_books dictionary before using it in functions
books = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation']
st.title("Daily New Testament Verse")

# Function to get a random item from the specified column each day
def get_item_daily(dataframes, column_name, common_random_key, display_columns):
    # Display the random items and selected columns with separation
    for i, (df, title) in enumerate(zip(dataframes, titles)):
        # Use the common random key to ensure the same random item is selected for all dataframes
        random.seed(common_random_key)
        random_item_index = random.randint(0, len(df) - 1)
        random_item = df.at[random_item_index, column_name]

        # Replace 'b' value with the corresponding book name from the numbered_books dictionary
        book_name = books[df.at[random_item_index, 'b'] - 40]

        # Create a container for each item with a title
        with st.container():
            st.markdown("---")
            st.subheader(title)  # Add the title for the card

            # Display the selected columns as text above the random item
            for col in display_columns:
                if col == 'b':
                    display_value = book_name
                elif col == 'c':
                    display_value = f"Chapter: {df.at[random_item_index, col]}"
                elif col == 'v':
                    display_value = f"Verse: {df.at[random_item_index, col]}"
                else:
                    display_value = df.at[random_item_index, col]

                st.write(display_value)

            st.write(random_item)

            st.text("\n")  # Add a line break for separation

        # Schedule a daily task to update the displayed item
        schedule.every().day.at("00:00").do(update_daily_item, df=df, column_name=column_name, common_random_key=common_random_key, display_columns=display_columns)

    # Run the Streamlit app
    while True:
        schedule.run_pending()
        time.sleep(1)

# Function to update the displayed random item daily
def update_daily_item(df, column_name, common_random_key, display_columns):
    # Use the common random key to ensure the same random item is selected for all dataframes
    random.seed(common_random_key)
    today_item_index = random.randint(0, len(df) - 1)
    today_item = df.at[today_item_index, column_name]

    # Replace 'b' value with the corresponding book name from the numbered_books dictionary
    book_name = books[df.at[today_item_index, 'b'] - 40]

    # Create a container for the updated item with a title
    with st.container():
        st.markdown("---")
        st.subheader(f"{titles} - Updated")  # Add the title for the card

        # Display the selected columns as text above the random item
        for col in display_columns:
            if col == 'b':
                display_value = book_name
            elif col == 'c':
                display_value = f"Chapter: {df.at[today_item_index, col]}"
            elif col == 'v':
                display_value = f"Verse: {df.at[today_item_index, col]}"
            else:
                display_value = df.at[today_item_index, col]
            
            st.subheader(display_value)

        st.subheader(today_item)


df_AmericanStandard = pd.read_csv('t_asv.csv')
df_BibleInBasic = pd.read_csv('t_bbe.csv')
df_KingJames = pd.read_csv('t_kjv.csv')
df_WebsterBible = pd.read_csv('t_web.csv')
df_YoungLiteral = pd.read_csv('t_ylt.csv')

# filter to new testament and reset index
df_AmericanStandard = df_AmericanStandard[df_AmericanStandard['b'] >= 40].reset_index(drop=True)
df_BibleInBasic = df_BibleInBasic[df_BibleInBasic['b'] >= 40].reset_index(drop=True)
df_KingJames = df_KingJames[df_KingJames['b'] >= 40].reset_index(drop=True)
df_WebsterBible = df_WebsterBible[df_WebsterBible['b'] >= 40].reset_index(drop=True)
df_YoungLiteral = df_YoungLiteral[df_YoungLiteral['b'] >= 40].reset_index(drop=True)

# Save filtered DataFrames in session_state
st.session_state.filtered_dataframes = {
    "American Standard Version": df_AmericanStandard,
    "Bible in basic": df_BibleInBasic,
    "King James Version": df_KingJames,
    "Webster Bible": df_WebsterBible,
    "Young Literal": df_YoungLiteral,
}

# books = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation']

# numbered_books = {book: index + 40 for index, book in enumerate(books)}

dataframes = [
    df_KingJames,
    df_AmericanStandard,
    df_BibleInBasic,
    df_WebsterBible,
    df_YoungLiteral
]

titles = [
    "King James Version",
    "American Standard Version",
    "Bible in basic",
    "Webster Bible",
    "Young Literal"
]

display_columns = ['b', 'c', 'v']

# Generate a common random key
common_random_key = random.randint(1, 1000)

# Call the get_item_daily function with the list of DataFrames and column name
get_item_daily(dataframes, 't', common_random_key, display_columns)

