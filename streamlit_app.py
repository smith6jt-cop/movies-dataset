import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="HHP Data", page_icon="")
st.title("HHP Data Visualization")
st.write(
    """
    This app visualizes data from that csv file.
    It shows bunches of data! Just 
    click on the widgets below to explore!
    """
)


# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_csv("data/majors_summary.csv")
    return df


df = load_data()

# Show a multiselect widget with the genres using `st.multiselect`.
major = st.multiselect(
    "Major",
    df.Major.unique(),
    ["DAT", "Doctoral", "Masters", "APK-Res", "AT-Res", "HEB-Res", "REC-Res", "SPM-Res", "TRM-Res"]
)

# Show a slider widget with the years using `st.slider`.
terms = st.select_slider("Term", ["Spring 2013", "Fall 2013", "Spring 2014", "Fall 2014", "Spring 2015", "Fall 2015", "Spring 2016", "Fall 2016", "Spring 2017", "Fall 2017", "Spring 2018", "Fall 2018", "Spring 2019", "Fall 2019", "Spring 2020", "Fall 2020", "Spring 2021", "Fall 2021", "Spring 2022", "Fall 2022", "Spring 2023", "Fall 2023", "Spring 2024", "Fall 2024", "Spring 2025"], ["Spring 2016", "Spring 2025"])

# Filter the dataframe based on the widget input and reshape it.
df_filtered = df[(df["Major"].isin(major)) & (df["Term"].between(terms[0], terms[1]))]
df_reshaped = df_filtered.pivot_table(
    index="Term", columns="Major", values="Count", aggfunc="sum", fill_value=0
)
df_reshaped = df_reshaped.sort_values(by="Term", ascending=False)


# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_reshaped,
    use_container_width=True,
    column_config={"Term": st.column_config.TextColumn("Term")},
)

# Display the data as an Altair chart using `st.altair_chart`.
df_chart = pd.melt(
    df_reshaped.reset_index(), id_vars="Term", var_name="Major", value_name="Count"
)
chart = (
    alt.Chart(df_chart)
    .mark_line()
    .encode(
        x=alt.X("Term:N", title="Term"),
        y=alt.Y("Count:Q", title="Count"),
        color="Major:N",
    )
    .properties(height=320)
)
st.altair_chart(chart, use_container_width=True)
