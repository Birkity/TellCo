import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import euclidean_distances
import numpy as np

# Database connection
conn = st.connection("telecom")
df = conn.query("SELECT * FROM xdr_data")

# Streamlit App Title
st.title("Telecom Customer Satisfaction Analysis")

# Show initial dataset
st.subheader("Initial Data")
st.write(df.head())

# ---- Data Cleaning ----
st.subheader("Handle Missing Values")
missing_column = st.selectbox("Choose a column to fill missing values", df.columns[df.isnull().any()])
fill_method = st.radio("Fill method", ["Fill with Mean", "Fill with Median", "Drop Rows"])

if st.button("Apply Fill"):
    if fill_method == "Fill with Mean":
        df[missing_column] = df[missing_column].fillna(df[missing_column].mean())
    elif fill_method == "Fill with Median":
        df[missing_column] = df[missing_column].fillna(df[missing_column].median())
    else:
        df = df.dropna(subset=[missing_column])
    st.success(f"{missing_column} cleaned successfully")

# ---- Descriptive Statistics ----
st.subheader("Descriptive Statistics")
st.write(df.describe())


# ---- Comparison: Handset Type vs Total DL (Bytes) ----
df_clean = df.dropna(subset=["Handset Type", "Total DL (Bytes)"])
st.subheader("Comparison: Handset Type vs. Total DL (Bytes)")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x="Handset Type", y="Total DL (Bytes)", data=df_clean, ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)

# ---- Aggregation for Satisfaction Analysis ----
st.subheader("Aggregating Data for Satisfaction Analysis")
df_cleaned = df.copy()

# Handling missing values for satisfaction-related metrics
df_cleaned['TCP DL Retrans. Vol (Bytes)'].fillna(df_cleaned['TCP DL Retrans. Vol (Bytes)'].mean(), inplace=True)
df_cleaned['TCP UL Retrans. Vol (Bytes)'].fillna(df_cleaned['TCP UL Retrans. Vol (Bytes)'].mean(), inplace=True)
df_cleaned['Avg RTT DL (ms)'].fillna(df_cleaned['Avg RTT DL (ms)'].mean(), inplace=True)
df_cleaned['Avg RTT UL (ms)'].fillna(df_cleaned['Avg RTT UL (ms)'].mean(), inplace=True)
df_cleaned['Avg Bearer TP DL (kbps)'].fillna(df_cleaned['Avg Bearer TP DL (kbps)'].mean(), inplace=True)
df_cleaned['Avg Bearer TP UL (kbps)'].fillna(df_cleaned['Avg Bearer TP UL (kbps)'].mean(), inplace=True)
df_cleaned['Handset Type'].fillna(df_cleaned['Handset Type'].mode()[0], inplace=True)

# Aggregating per customer (MSISDN/Number)
customer_agg = df_cleaned.groupby('MSISDN/Number').agg({
    'TCP DL Retrans. Vol (Bytes)': 'mean',
    'TCP UL Retrans. Vol (Bytes)': 'mean',
    'Avg RTT DL (ms)': 'mean',
    'Avg RTT UL (ms)': 'mean',
    'Avg Bearer TP DL (kbps)': 'mean',
    'Avg Bearer TP UL (kbps)': 'mean',
    'Handset Type': 'first'
}).reset_index()

# Calculate additional metrics for engagement and experience scores
customer_agg['Avg TCP Retransmission'] = (customer_agg['TCP DL Retrans. Vol (Bytes)'] + customer_agg['TCP UL Retrans. Vol (Bytes)']) / 2
customer_agg['Avg RTT'] = (customer_agg['Avg RTT DL (ms)'] + customer_agg['Avg RTT UL (ms)']) / 2
customer_agg['Avg Throughput'] = (customer_agg['Avg Bearer TP DL (kbps)'] + customer_agg['Avg Bearer TP UL (kbps)']) / 2

st.write(customer_agg.head())

# Task 4.1 - Engagement and Experience Score Calculation
st.subheader("Task 4.1: Engagement and Experience Score")

# Standardizing and calculating Euclidean distance for engagement and experience score
scaler = StandardScaler()
engagement_features = customer_agg[['Avg Throughput']]
experience_features = customer_agg[['Avg RTT', 'Avg TCP Retransmission']]

engagement_scaled = scaler.fit_transform(engagement_features)
experience_scaled = scaler.fit_transform(experience_features)

# Clustering to determine less engaged and worst experience clusters
kmeans_engagement = KMeans(n_clusters=2, random_state=42)
customer_agg['Engagement Cluster'] = kmeans_engagement.fit_predict(engagement_scaled)
kmeans_experience = KMeans(n_clusters=2, random_state=42)
customer_agg['Experience Cluster'] = kmeans_experience.fit_predict(experience_scaled)

# Assigning scores based on distance from clusters
engagement_centers = kmeans_engagement.cluster_centers_
experience_centers = kmeans_experience.cluster_centers_

customer_agg['Engagement Score'] = euclidean_distances(engagement_scaled, engagement_centers[0].reshape(1, -1)).flatten()
customer_agg['Experience Score'] = euclidean_distances(experience_scaled, experience_centers[0].reshape(1, -1)).flatten()

st.write(customer_agg[['MSISDN/Number', 'Engagement Score', 'Experience Score']].head())

# Task 4.2 - Satisfaction Score Calculation
st.subheader("Task 4.2: Satisfaction Score")

# Satisfaction Score Calculation (mean of engagement and experience score)
customer_agg['Satisfaction Score'] = (customer_agg['Engagement Score'] + customer_agg['Experience Score']) / 2

# Display top 10 satisfied customers
top_10_satisfied = customer_agg.nlargest(10, 'Satisfaction Score')
st.write(top_10_satisfied[['MSISDN/Number', 'Satisfaction Score']])

# Task 4.3 - Visualizing Satisfaction Score
st.subheader("Satisfaction Score Distribution")

fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(customer_agg['Satisfaction Score'], bins=20, kde=True, ax=ax)
ax.set_title('Satisfaction Score Distribution')
st.pyplot(fig)

# Task 4.4 - K-means Clustering of Engagement & Experience
st.subheader("Task 4.4: K-Means Clustering")

kmeans_satisfaction = KMeans(n_clusters=2, random_state=42)
customer_agg['Satisfaction Cluster'] = kmeans_satisfaction.fit_predict(customer_agg[['Engagement Score', 'Experience Score']])

fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='Engagement Score', y='Experience Score', hue='Satisfaction Cluster', data=customer_agg, palette='coolwarm', ax=ax)
ax.set_title('Engagement vs Experience Clusters')
st.pyplot(fig)

# Task 4.5 - Aggregating Satisfaction Scores by Cluster
cluster_agg = customer_agg.groupby('Satisfaction Cluster')[['Satisfaction Score', 'Experience Score']].mean().reset_index()
st.write(cluster_agg)
