import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

sns.set(style='dark')

def hourly_usage_df(dataframe):
    hourly_usage_ = dataframe.groupby(by="hour").agg({"count_x": "sum"}).reset_index()
    hourly_usage_ = hourly_usage_.rename(columns={"count_x": "total_usage"})
    return hourly_usage_

def weathereffect_df(dataframe):
    weathereffect_ = dataframe.groupby(by="weather_x").agg({"count_x": "mean"}).reset_index()
    weathereffect_ = weathereffect_.rename(columns={"count_x": "average_usage"})
    return weathereffect_

all_df = pd.read_csv("all_data.csv")

# Streamlit Sidebar
with st.sidebar:
    st.title('Dashboard Analisis Peminjaman Sepeda 🚴‍♀️')
    st.subheader('Disusun oleh: Kharisma Ayuningtyas')
    st.markdown("Email: **kharisma.ayuningtyas@student.ppns.ac.id**")
    st.markdown("ID Dicoding: **kharisma_ayuningtyas**")
    
# Main Content
st.title('📊 Dashboard Peminjaman Sepeda:sparkles:')
st.markdown("""
Selamat datang di dashboard analisis data peminjaman sepeda!  
Berikut adalah berbagai wawasan yang telah disusun untuk menjawab pertanyaan bisnis terkait.
""")

hourly_usage = hourly_usage_df(all_df)
weathereffect = weathereffect_df (all_df)
#Pertanyaan 1

total_usage = hourly_usage['total_usage'].sum()
avg_usage = round(hourly_usage['total_usage'].mean(), 2)

st.subheader("Penggunaan Sepeda Berdasarkan Jam")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Penggunaan Sepeda", value=total_usage)

with col2:
    st.metric("Rata-Rata Penggunaan per Jam", value=avg_usage)

fig, ax = plt.subplots(figsize=(16, 8))

ax.plot(
    hourly_usage["hour"],
    hourly_usage["total_usage"],
    marker='o',
    linewidth=2,
    color="#90CAF9",
    label="Total Usage"
)

ax.set_title("Penggunaan Sepeda Berdasarkan Jam", fontsize=24, fontweight='bold')
ax.set_xlabel("Jam", fontsize=18, fontweight='bold')
ax.set_ylabel("Total Penggunaan Sepeda", fontsize=18, fontweight='bold')

ax.set_xticks(range(24))  
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=12)

ax.grid(axis='y', linestyle='--', linewidth=0.7)
ax.legend(fontsize=15)

st.pyplot(fig)


#Pertanyaan 2

colors = ['#90CAF9' if avg == weathereffect['average_usage'].max() else '#D3D3D3' for avg in weathereffect['average_usage']]

labels = ['Cerah', 'Mendung', 'Hujan ringan', 'Hujan deras']
weathereffect['labels'] = labels

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="average_usage", 
    y="labels", 
    data=weathereffect, 
    palette=colors, 
    ax=ax
)

ax.set_title("Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda", fontsize=20, fontweight='bold')
ax.set_xlabel("Rata-Rata Penyewaan Sepeda", fontsize=15)
ax.set_ylabel(None)

for index, row in weathereffect.iterrows():
    ax.text(row['average_usage'] + 5, index, f'{row["average_usage"]:.1f}', va='center', fontsize=12)

st.pyplot(fig)

st.caption('Copyright (c) Kharisma Ayuningtyas 2024')
