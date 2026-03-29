import streamlit as st
import pandas as pd

st.set_page_config(page_title="WI Election Integrity Dashboard", layout="wide")
st.title("🗳️ Wisconsin Election Integrity Intelligence Feed")
st.markdown("**Your Product Owner View** — Tracking legal inflection points, constitutional linkages (Art. III, Elections Clause), and suggested next steps")

# Load data from your CSV
csv_file = "WI Election Integrity Tracker - Sheet1.csv"

try:
    df = pd.read_csv(csv_file)
    st.success(f"✅ Loaded {len(df)} inflection points from your spreadsheet")
except FileNotFoundError:
    st.error(f"❌ Could not find the file: {csv_file}")
    st.error("Make sure the CSV is saved in the wi-election-dashboard folder.")
    st.stop()
except Exception as e:
    st.error(f"❌ Error reading CSV: {e}")
    st.stop()

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    strength_filter = st.multiselect(
        "Filter by Upstream Strength", 
        options=sorted(df["Upstream Strength"].unique().tolist()), 
        default=df["Upstream Strength"].unique().tolist()
    )
with col2:
    waukesha_filter = st.selectbox("Waukesha Focus", ["All", "Yes", "No"])
with col3:
    st.write("")

# Apply filters
filtered_df = df.copy()
if strength_filter:
    filtered_df = filtered_df[filtered_df["Upstream Strength"].isin(strength_filter)]
if waukesha_filter != "All":
    if "Waukesha Focus" in df.columns:
        filtered_df = filtered_df[filtered_df["Waukesha Focus"] == waukesha_filter]

# Display the table
st.dataframe(filtered_df, use_container_width=True)

# Constitutional Analyst section
st.subheader("🤖 Quick Constitutional Analyst")
query = st.text_input("Ask about a case or statute (e.g., 'Frame upstream argument against Ch. 6 using Art. III §1')", 
                      key="analyst_query")
if st.button("Get Framing & Next Steps"):
    if query:
        st.info(f"""**Agent Analysis for:** "{query}"

**Sample Output (placeholder - we'll add real AI soon):**
This issue ties directly to the plain text of Wisconsin Constitution Art. III §1, which defines qualified electors strictly as U.S. citizens age 18+ who are residents. 

Any statute or WEC practice that dilutes or fails to enforce this definition is subordinate and repugnant to the constitutional text.

**Recommended upstream framing:**
'The statute in question is void insofar as it conflicts with Art. III §1. The Elections Clause assigns the manner of elections to the Legislature, not agencies or third-party databases.'

**High-ROI Next Step:** Supplemental mandamus in the Cerny line or declaratory judgment focused on this textual violation.""")
    else:
        st.warning("Please enter a query above.")

st.caption("Local MVP • Edit your Google Sheet → re-export CSV → refresh browser to update • Next: Real AI agent + free deployment")