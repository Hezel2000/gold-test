import streamlit as st
import pandas as pd
from mag4 import get_data

# Conversion constants
SECONDS_PER = {
    "ka": 1e3 * 365.25 * 24 * 60 * 60,
    "Ma": 1e6 * 365.25 * 24 * 60 * 60,
    "Ga": 1e9 * 365.25 * 24 * 60 * 60,
}

# Load and prepare data
@st.cache_data
def load_data():
    df = get_data("nucbasics")
    df["half life (s)"] = pd.to_numeric(df["half life (s)"], errors="coerce")
    df["mass number"] = df["z"] + df["n"]
    df["nuclide"] = df.apply(lambda row: f"<sup>{int(row['mass number'])}</sup>{row['symbol']}", axis=1)
    return df

df = load_data()

st.title("☢️ Nuclide Half-Life Explorer")

# Sidebar controls
st.sidebar.header("Half-Life Filters")

# Lower bound
unit_lower = st.sidebar.selectbox("Lower unit", ["ka", "Ma", "Ga"], index=1)
lower_bound = st.sidebar.slider(f"Lower half-life in {unit_lower}", 0.000001, 10000.0, 0.1)

# Upper bound
unit_upper = st.sidebar.selectbox("Upper unit", ["ka", "Ma", "Ga"], index=1)
upper_bound = st.sidebar.slider(f"Upper half-life in {unit_upper}", 0.000001, 10000.0, 5000.0)

# Convert bounds to seconds
lo_seconds = lower_bound * SECONDS_PER[unit_lower]
hi_seconds = upper_bound * SECONDS_PER[unit_upper]

# Filter dataset
filtered = df[(df["half life (s)"] >= lo_seconds) & (df["half life (s)"] <= hi_seconds)].copy()

# Choose display unit
unit_display = st.selectbox("Display half-life in", ["ka", "Ma", "Ga"], index=1)
filtered[f"half life ({unit_display})"] = filtered["half life (s)"] / SECONDS_PER[unit_display]

# Show filtered table
st.markdown(f"### Filtered Nuclides ({len(filtered)} shown)")
st.write(
    filtered[["nuclide", f"half life ({unit_display})"]]
    .round(6)
    .rename(columns={"nuclide": "Nuclide", f"half life ({unit_display})": f"Half-life ({unit_display})"})
    .to_html(escape=False, index=False),
    unsafe_allow_html=True
)