import pandas as pd
import streamlit as st

books = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation']

# Function to search for matches in the DataFrames and display results
def search_and_display(user_input, dataframes):
    st.title("Bible Text Search")

    # Iterate through each DataFrame
    for i, (title, df) in enumerate(dataframes.items(), start=1):
        st.header(title)

        # Search for matches in the 't' column
        matching_rows = df[df['t'].str.contains(user_input, case=False)]

        # Display matching rows in card format
        for _, row in matching_rows.iterrows():
            book_name = books[df.at[_, 'b'] - 40]
            st.write(f"Text: {row['t']}")
            st.write(f"Book: {book_name}, Chapter: {row['c']}, Verse: {row['v']}")
            st.markdown("___")

# Load your Bible DataFrames (replace these with your actual file paths)
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

dataframes = {
    "King James Version" : df_KingJames,
    "American Standard Version" : df_AmericanStandard,
    "Bible in basic" : df_BibleInBasic,
    "Webster Bible" : df_WebsterBible,
    "Young Literal" : df_YoungLiteral
}

# Streamlit app
def main():
    user_input = st.text_input("Enter text to search for:")
    if user_input:
        search_and_display(user_input, dataframes)

if __name__ == "__main__":
    main()

