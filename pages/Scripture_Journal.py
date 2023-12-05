import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# Function to save entry to CSV
def save_to_csv(title, date, text):
    entry = {'Title': title, 'Date': date, 'Text': text}
    
    # Check if the file exists
    if os.path.exists('journal_entries.csv'):
        df = pd.read_csv('journal_entries.csv', parse_dates=['Date'])
    else:
        df = pd.DataFrame(columns=['Title', 'Date', 'Text'])
    
    df = df.append(entry, ignore_index=True)
    df.to_csv('journal_entries.csv', index=False)

# Function to filter entries based on title and date range
def filter_entries(df, title_filter, start_date, end_date):
    filtered_df = df.copy()
    
    if title_filter:
        filtered_df = filtered_df[filtered_df['Title'].str.contains(title_filter, case=False, na=False)]
    
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)  # Convert date to datetime
        end_date = pd.to_datetime(end_date)  # Convert date to datetime
        filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]
    
    return filtered_df

# Streamlit app
def main():
    st.title("Journal App")

    # Sidebar
    st.sidebar.header("Filters")
    title_filter = st.sidebar.text_input("Filter by Title:")
    start_date = st.sidebar.date_input("Filter by Start Date:")
    
    # Set the maximum date to a date far in the future
    max_date = datetime.now() + timedelta(days=3650)  # Adding 10 years
    end_date = st.sidebar.date_input("Filter by End Date:", max_date)

    # Form for adding entries
    st.header("Add Entry")
    title = st.text_input("Title:")
    date = st.date_input("Date:")
    text = st.text_area("Journal Entry:", height=200)
    if st.button("Save Entry"):
        save_to_csv(title, date, text)
        st.success("Entry saved successfully!")

    # View Entries button
    if st.button("View Entries", key='view_entries'):
        st.header("Journal Entries")

        # Read CSV and filter entries
        if os.path.exists('journal_entries.csv'):
            df = pd.read_csv('journal_entries.csv', parse_dates=['Date'])
            filtered_df = filter_entries(df, title_filter, start_date, end_date)

            # Display filtered entries
            for index, row in filtered_df.iterrows():
                st.subheader(f"Title: {row['Title']}")
                st.write(f"Entry {index + 1}")
                st.write(f"Date: {row['Date'].strftime('%Y-%m-%d')}")
                st.write(row['Text'])
                st.markdown("---")
        else:
            st.info("No entries found.")

if __name__ == "__main__":
    main()