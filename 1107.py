import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# 頁面設定
# -------------------------------
st.set_page_config(page_title="臺南市智慧管理科技執法設備分析", layout="wide")

# -------------------------------
# 主標題
# -------------------------------
st.title("🚦 臺南市智慧管理科技執法設備分析")
st.markdown("探索各行政區的科技執法設備分布、速限與拍攝行向。")

# -------------------------------
# 讀取 CSV
# -------------------------------
df = pd.read_csv("tainan_smart_enforcement.csv", encoding="utf-8-sig")
df.columns = df.columns.str.strip()

# -------------------------------
# 篩選功能
# -------------------------------
with st.sidebar:
    st.header("📍 篩選條件")
    districts = df['行政區'].dropna().unique()
    selected_district = st.selectbox("選擇行政區", sorted(districts))

    stations = df[df['行政區'] == selected_district]['轄區分局'].dropna().unique()
    selected_station = st.selectbox("選擇轄區分局", sorted(stations))

# -------------------------------
# 篩選後的資料
# -------------------------------
filtered_df = df[(df['行政區'] == selected_district) & (df['轄區分局'] == selected_station)]

# -------------------------------
# 統計摘要
# -------------------------------
st.markdown("---")
st.subheader(f"📊 {selected_district} - {selected_station} 設備概況")

col1, col2, col3 = st.columns(3)
col1.metric("設備總數", len(filtered_df))
col2.metric("速限種類", filtered_df['速限'].nunique())
col3.metric("拍攝行向種類", filtered_df['拍攝行向'].nunique())

# -------------------------------
# 原始資料（可收合）
# -------------------------------
with st.expander("📄 查看原始資料"):
    st.dataframe(filtered_df, use_container_width=True)

# -------------------------------
# 圖表排版
# -------------------------------
col_a, col_b = st.columns(2)

# 速限統計
with col_a:
    st.subheader("🏎️ 各速限設備數量")
    if '速限' in filtered_df.columns:
        speed_count = filtered_df['速限'].value_counts().reset_index()
        speed_count.columns = ['速限', '數量']
        fig_speed = px.bar(
            speed_count,
            x='速限',
            y='數量',
            text='數量',
            title="速限分布",
            color='速限',
            color_discrete_sequence=px.colors.sequential.Blues
        )
        st.plotly_chart(fig_speed, use_container_width=True)
    else:
        st.warning("⚠️ 找不到「速限」欄位")

# 拍攝行向統計
with col_b:
    st.subheader("📸 拍攝行向比例")
    if '拍攝行向' in filtered_df.columns:
        direction_count = filtered_df['拍攝行向'].value_counts().reset_index()
        direction_count.columns = ['拍攝行向', '數量']
        fig_dir = px.pie(
            direction_count,
            names='拍攝行向',
            values='數量',
            title="拍攝行向統計",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_dir, use_container_width=True)
    else:
        st.warning("⚠️ 找不到「拍攝行向」欄位")

# -------------------------------
# 備註
# -------------------------------
st.markdown("---")
st.caption("📍 資料來源：臺南市政府開放資料 | 製作：Streamlit + Plotly Dashboard")
