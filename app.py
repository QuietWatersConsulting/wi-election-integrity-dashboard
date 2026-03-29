import streamlit as st
import pandas as pd

st.set_page_config(page_title="Wisconsin Election Integrity Dashboard", layout="wide")

st.title("🗳️ Wisconsin Election Integrity Dashboard")
st.markdown("Tracking key legal inflection points, constitutional linkages to Art. III §1 and the Elections Clause, and potential next steps.")

# Load data
csv_file = "WI Election Integrity Tracker - Sheet1.csv"

try:
    df = pd.read_csv(csv_file, index_col=0)   # Keeps your numbered column as the first column
except Exception as e:
    st.error(f"❌ Error reading CSV: {e}")
    st.stop()

# Color coding for Upstream Strength
def color_strength(val):
    if val == "High":
        return "background-color: #d4edda; color: #155724;"   # green
    elif val == "Medium-High":
        return "background-color: #fff3cd; color: #856404;"   # orange
    return ""

# Filter
strength_filter = st.multiselect(
    "Filter by Upstream Strength", 
    options=sorted(df["Upstream Strength"].unique().tolist()), 
    default=df["Upstream Strength"].unique().tolist()
)

# Apply filter
filtered_df = df.copy()
if strength_filter:
    filtered_df = filtered_df[filtered_df["Upstream Strength"].isin(strength_filter)]

# Display table
styled_df = filtered_df.style.applymap(color_strength, subset=["Upstream Strength"])
st.dataframe(styled_df, use_container_width=True)

# Constitutional Analyst
st.subheader("🤖 Constitutional Analyst")
query = st.text_input(
    "Ask about a case, statute, or provision (e.g., 'Frame upstream argument on Ch. 6 using Art. III §1')",
    key="analyst_query"
)
if st.button("Analyze & Suggest Next Steps"):
    if query:
        st.info(f"""**Analysis for:** "{query}"

This issue centers on the plain text of **Wisconsin Constitution Art. III §1**, which defines qualified electors strictly as U.S. citizens age 18 or older who are residents of the state.

**Recommended upstream framing:**
'The challenged provision is subordinate to and repugnant with Art. III §1. Any conflict must be resolved in favor of the constitutional text. The Elections Clause assigns the manner of elections to the Legislature, not to administrative agencies or third-party entities.'

**Potential high-ROI next steps:**
• Declaratory judgment or supplemental mandamus focused on the textual violation
• Amicus support in ongoing litigation (e.g., Cerny line)
• Legislative clarification or REINS-style oversight of WEC guidance""")
    else:
        st.warning("Please enter a query.")

# Version number bottom right
st.markdown(
    "<div style='text-align: right; color: #666; font-size: 0.85em;'>Version 1.2</div>",
    unsafe_allow_html=True
)