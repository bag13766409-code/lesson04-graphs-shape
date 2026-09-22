import streamlit as st
import pandas as pd
import plotly.express as px

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

st.set_page_config(
page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
page_icon="🎬",
layout="wide",
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write(
"1년간 박스오피스 10위권에 든 영화 가운데 해당 기간에 개봉한 "
"216편의 데이터를 살펴봅니다."
)

@st.cache_data
def load_data():
df = pd.read_csv(DATA_URL)

```
# 여러 장르가 |로 연결된 경우 첫 번째 장르만 사용
df["genre"] = (
    df["genre"]
    .fillna("알 수 없음")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

return df
```

df = load_data()

# ---------------------------------------------------------

# 1. 장르별 영화 편수

# ---------------------------------------------------------

st.subheader("1. 장르별 영화 편수")

genre_counts = (
df["genre"]
.value_counts()
.rename_axis("장르")
.reset_index(name="편수")
)

fig = px.pie(
genre_counts,
names="장르",
values="편수",
hole=0.5,
title="장르별 영화 편수",
)

fig.update_traces(
textinfo="percent",
hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
)

fig.update_layout(
legend_title="장르",
margin=dict(t=60, b=20, l=20, r=20),
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**이 그래프로 알 수 있는 것**")

st.text_area(
"한 문장으로 정리해 보세요.",
placeholder="예: 어떤 장르의 영화가 가장 많이 포함되어 있는지 알 수 있다.",
label_visibility="collapsed",
key="genre_insight",
)

st.divider()

st.caption(f"데이터 출처: KOBIS 영화 데이터 · 총 {len(df):,}편")
