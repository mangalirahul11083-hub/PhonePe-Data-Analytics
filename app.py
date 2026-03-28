import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# --- PAGE SETUP ---
st.set_page_config(page_title="PhonePe Pulse Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- DATABASE CONNECTION ---
@st.cache_data
def load_data(query):
    conn = sqlite3.connect('phonepe_pulse.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("💸 PhonePe Pulse")
st.sidebar.subheader("Data Analytics Dashboard")
st.sidebar.divider()

st.sidebar.markdown("**Navigate to:**")

# 1. Setup 'memory' so the app remembers which page we are on
if 'current_page' not in st.session_state:
    st.session_state.current_page = "📊 Overview"

# 2. Create full-width buttons instead of radio circles
if st.sidebar.button("📊 Overview", use_container_width=True):
    st.session_state.current_page = "📊 Overview"
if st.sidebar.button("🗺️ Geo-Visualizations", use_container_width=True):
    st.session_state.current_page = "🗺️ Geo-Visualizations"
if st.sidebar.button("🏆 Top Insights", use_container_width=True):
    st.session_state.current_page = "🏆 Top Insights"

# 3. Tell the app to show whichever page is currently saved in memory
page = st.session_state.current_page

st.sidebar.divider()
st.sidebar.caption("Built with Python, Plotly, and Streamlit.")

# ==========================================
# PAGE 1: OVERVIEW
# ==========================================
if page == "📊 Overview":
    st.title("Overall Platform Performance")
    st.markdown("A high-level look at transaction categories, user devices, and growth over time.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Transaction Categories")
        df_cat = load_data("SELECT Transaction_Type, SUM(Amount) as Total_Amount FROM Aggregated_transaction GROUP BY Transaction_Type")
        fig1 = px.pie(df_cat, values='Total_Amount', names='Transaction_Type', hole=0.4, color_discrete_sequence=px.colors.sequential.Purp)
        fig1.update_traces(textinfo='percent+label', showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Top Smartphone Brands")
        df_brands = load_data("SELECT Device_Brand, SUM(Device_Count) as Total_Users FROM Aggregated_user WHERE Device_Brand != 'Unknown' GROUP BY Device_Brand ORDER BY Total_Users DESC LIMIT 10")
        fig2 = px.bar(df_brands, x='Device_Brand', y='Total_Users', color='Total_Users', color_continuous_scale=px.colors.sequential.Teal)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("Growth Over Time")
    col3, col4 = st.columns(2)
    with col3:
        df_time_amt = load_data("SELECT Year, SUM(Amount) as Total_Amount FROM Aggregated_transaction GROUP BY Year ORDER BY Year")
        df_time_amt['Year'] = df_time_amt['Year'].astype(str)
        fig3 = px.line(df_time_amt, x='Year', y='Total_Amount', markers=True, title="Transaction Amount by Year", color_discrete_sequence=['#8A2BE2'])
        st.plotly_chart(fig3, use_container_width=True)
        
    with col4:
        df_time_vol = load_data("SELECT Year, SUM(Count) as Total_Count FROM Aggregated_transaction GROUP BY Year ORDER BY Year")
        df_time_vol['Year'] = df_time_vol['Year'].astype(str)
        fig4 = px.area(df_time_vol, x='Year', y='Total_Count', title="Transaction Volume by Year", color_discrete_sequence=['#20B2AA'])
        st.plotly_chart(fig4, use_container_width=True)

# ==========================================
# PAGE 2: GEO-VISUALIZATIONS
# ==========================================
elif page == "🗺️ Geo-Visualizations":
    st.title("Geographical Analysis")
    
    # Add an interactive filter!
    selected_year = st.selectbox("Select Year to Filter Map Data:", ["All Years", "2018", "2019", "2020", "2021", "2022", "2023"])
    
    if selected_year == "All Years":
        query_map = "SELECT State, District, SUM(Amount) as Total_Amount FROM Map_transaction GROUP BY State, District ORDER BY Total_Amount DESC LIMIT 25"
    else:
        query_map = f"SELECT State, District, SUM(Amount) as Total_Amount FROM Map_transaction WHERE Year = {selected_year} GROUP BY State, District ORDER BY Total_Amount DESC LIMIT 25"
        
    st.subheader(f"Transaction Hotspots: Top 25 Districts ({selected_year})")
    df_map = load_data(query_map)
    fig5 = px.treemap(df_map, path=[px.Constant("India"), 'State', 'District'], values='Total_Amount', color='Total_Amount', color_continuous_scale='Viridis')
    fig5.update_traces(root_color="lightgrey")
    fig5.update_layout(margin=dict(t=20, l=20, r=20, b=20))
    st.plotly_chart(fig5, use_container_width=True)

    st.divider()
    st.subheader("District-Level Insurance Adoption")
    df_ins_dist = load_data("SELECT District, State, SUM(Count) as Total_Policies FROM Map_insurance GROUP BY District, State ORDER BY Total_Policies DESC LIMIT 15")
    df_ins_dist['District_State'] = df_ins_dist['District'] + " (" + df_ins_dist['State'] + ")"
    fig6 = px.bar(df_ins_dist, x='District_State', y='Total_Policies', color='Total_Policies', color_continuous_scale='YlGnBu')
    fig6.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig6, use_container_width=True)

# ==========================================
# PAGE 3: TOP INSIGHTS
# ==========================================
elif page == "🏆 Top Insights":
    st.title("State & Hyper-Local Rankings")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top States: Transaction Amount")
        df_state_trans = load_data("SELECT State, SUM(Amount) as Total_Amount FROM Aggregated_transaction GROUP BY State ORDER BY Total_Amount DESC LIMIT 15")
        fig7 = px.bar(df_state_trans, x='State', y='Total_Amount', color='Total_Amount', color_continuous_scale='Magma')
        fig7.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig7, use_container_width=True)

    with col2:
        st.subheader("Top States: Insurance Policies")
        df_state_ins = load_data("SELECT State, SUM(Count) as Total_Policies FROM Aggregated_insurance GROUP BY State ORDER BY Total_Policies DESC LIMIT 15")
        fig8 = px.bar(df_state_ins, x='Total_Policies', y='State', orientation='h', color='Total_Policies', color_continuous_scale=px.colors.sequential.Sunset)
        fig8.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig8, use_container_width=True)

    st.divider()
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Most Engaged States (App Opens)")
        df_opens = load_data("SELECT State, SUM(App_Opens) as Total_Opens FROM Map_user GROUP BY State ORDER BY Total_Opens DESC LIMIT 15")
        fig9 = px.scatter(df_opens, x='State', y='Total_Opens', size='Total_Opens', color='Total_Opens', color_continuous_scale='Plasma')
        fig9.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig9, use_container_width=True)

    with col4:
        st.subheader("Top Pincodes for Registrations")
        df_pins = load_data("SELECT State, Entity_Name as Pincode, SUM(Registered_Users) as Total_Registrations FROM Top_user WHERE Entity_Type = 'Pincodes' GROUP BY State, Pincode ORDER BY Total_Registrations DESC LIMIT 10")
        df_pins['Location'] = df_pins['Pincode'].astype(str) + " (" + df_pins['State'] + ")"
        fig10 = px.funnel(df_pins, x='Total_Registrations', y='Location', color='Location')
        fig10.update_layout(showlegend=False)
        st.plotly_chart(fig10, use_container_width=True)