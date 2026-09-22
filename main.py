import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ------------------------------------------------------------
# 기본 설정
# ------------------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide",
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption(
    "최근 1년간 박스오피스 10위권에 든 영화 중, 해당 기간에 개봉한 216편의 데이터를 살펴봅니다."
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일: 여덟 자리 숫자(YYYYMMDD) -> datetime
    df["openDt"] = pd.to_datetime(df["openDt"], format="%Y%m%d", errors="coerce")

    # 장르: 세로막대(|)로 여러 개 적힌 경우 첫 번째 장르만 사용
    df["genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0].strip())

    return df


df = load_data()

with st.expander("📄 원본 데이터 미리보기"):
    st.dataframe(df, use_container_width=True)

st.divider()

# ------------------------------------------------------------
# 1. 장르별 영화 편수 - 도넛 그래프
# ------------------------------------------------------------
st.header("1️⃣ 장르별 영화 편수")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig_genre = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.5,
)
fig_genre.update_traces(
    textinfo="label+percent",
    hovertemplate="%{label}<br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
)
fig_genre.update_layout(
    legend_title_text="장르",
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_genre, use_container_width=True, key="genre_donut_chart")

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info("여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어 주세요.")

st.divider()

# ------------------------------------------------------------
# 2. 장르 안 영화별 총 관객 - 트리맵
# ------------------------------------------------------------
st.header("2️⃣ 장르별 영화 총 관객 트리맵")

fig_treemap = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
)
fig_treemap.update_traces(
    hovertemplate="영화명: %{label}<br>총 관객: %{value:,}명<extra></extra>",
)
fig_treemap.update_layout(
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_treemap, use_container_width=True, key="genre_treemap_chart")

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info("여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어 주세요.")

st.divider()

# ------------------------------------------------------------
# 3. 총 관객 히스토그램
# ------------------------------------------------------------
st.header("3️⃣ 총 관객 분포")

n_bins = 20

fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=n_bins,
)
fig_hist.update_traces(
    hovertemplate="구간: %{x}<br>영화 편수: %{y}편<extra></extra>",
)
fig_hist.update_layout(
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수",
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_hist, use_container_width=True, key="total_audi_histogram")

# 가장 영화가 몰린 구간 계산
counts, bin_edges = np.histogram(df["total_audi"].dropna(), bins=n_bins)
max_bin_idx = counts.argmax()
bin_start = bin_edges[max_bin_idx]
bin_end = bin_edges[max_bin_idx + 1]

# 총 관객이 가장 많은 영화 계산
top_movie = df.loc[df["total_audi"].idxmax()]

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info(
    f"대부분의 영화는 총 관객 **{bin_start:,.0f}명 ~ {bin_end:,.0f}명** 구간에 몰려 있으며 "
    f"({counts[max_bin_idx]}편), 총 관객이 가장 많은 영화는 "
    f"**'{top_movie['movieNm']}'**(총 {top_movie['total_audi']:,.0f}명)입니다."
)

st.divider()

# ------------------------------------------------------------
# 4. 개봉일 스크린수 vs 총 관객 - 산점도
# ------------------------------------------------------------
st.header("4️⃣ 개봉일 스크린수와 총 관객의 관계")

fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
)
fig_scatter.update_traces(
    hovertemplate="%{hovertext}<br>개봉일 스크린수: %{x:,}개<br>총 관객: %{y:,}명<extra></extra>",
)
fig_scatter.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객 수",
    legend_title_text="장르",
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_scatter, use_container_width=True, key="scrn_vs_audi_scatter")

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info("여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어 주세요.")

st.divider()
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ------------------------------------------------------------
# 기본 설정
# ------------------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide",
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption(
    "최근 1년간 박스오피스 10위권에 든 영화 중, 해당 기간에 개봉한 216편의 데이터를 살펴봅니다."
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일: 여덟 자리 숫자(YYYYMMDD) -> datetime
    df["openDt"] = pd.to_datetime(df["openDt"], format="%Y%m%d", errors="coerce")

    # 장르: 세로막대(|)로 여러 개 적힌 경우 첫 번째 장르만 사용
    df["genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0].strip())

    return df


df = load_data()

with st.expander("📄 원본 데이터 미리보기"):
    st.dataframe(df, use_container_width=True)

st.divider()

# ------------------------------------------------------------
# 1. 장르별 영화 편수 - 도넛 그래프
# ------------------------------------------------------------
st.header("1️⃣ 장르별 영화 편수")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig_genre = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.5,
)
fig_genre.update_traces(
    textinfo="label+percent",
    hovertemplate="%{label}<br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
)
fig_genre.update_layout(
    legend_title_text="장르",
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_genre, use_container_width=True, key="genre_donut_chart")

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info("여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어 주세요.")

st.divider()

# ------------------------------------------------------------
# 2. 장르 안 영화별 총 관객 - 트리맵
# ------------------------------------------------------------
st.header("2️⃣ 장르별 영화 총 관객 트리맵")

fig_treemap = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
)
fig_treemap.update_traces(
    hovertemplate="영화명: %{label}<br>총 관객: %{value:,}명<extra></extra>",
)
fig_treemap.update_layout(
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_treemap, use_container_width=True, key="genre_treemap_chart")

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info("여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어 주세요.")

st.divider()

# ------------------------------------------------------------
# 3. 총 관객 히스토그램
# ------------------------------------------------------------
st.header("3️⃣ 총 관객 분포")

n_bins = 20

fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=n_bins,
)
fig_hist.update_traces(
    hovertemplate="구간: %{x}<br>영화 편수: %{y}편<extra></extra>",
)
fig_hist.update_layout(
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수",
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_hist, use_container_width=True, key="total_audi_histogram")

# 가장 영화가 몰린 구간 계산
counts, bin_edges = np.histogram(df["total_audi"].dropna(), bins=n_bins)
max_bin_idx = counts.argmax()
bin_start = bin_edges[max_bin_idx]
bin_end = bin_edges[max_bin_idx + 1]

# 총 관객이 가장 많은 영화 계산
top_movie = df.loc[df["total_audi"].idxmax()]

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info(
    f"대부분의 영화는 총 관객 **{bin_start:,.0f}명 ~ {bin_end:,.0f}명** 구간에 몰려 있으며 "
    f"({counts[max_bin_idx]}편), 총 관객이 가장 많은 영화는 "
    f"**'{top_movie['movieNm']}'**(총 {top_movie['total_audi']:,.0f}명)입니다."
)

st.divider()

# ------------------------------------------------------------
# 4. 개봉일 스크린수 vs 총 관객 - 산점도
# ------------------------------------------------------------
st.header("4️⃣ 개봉일 스크린수와 총 관객의 관계")

fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
)
fig_scatter.update_traces(
    hovertemplate="%{hovertext}<br>개봉일 스크린수: %{x:,}개<br>총 관객: %{y:,}명<extra></extra>",
)
fig_scatter.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객 수",
    legend_title_text="장르",
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_scatter, use_container_width=True, key="scrn_vs_audi_scatter")

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info("여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어 주세요.")

st.divider()
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ------------------------------------------------------------
# 기본 설정
# ------------------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide",
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption(
    "최근 1년간 박스오피스 10위권에 든 영화 중, 해당 기간에 개봉한 216편의 데이터를 살펴봅니다."
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일: 여덟 자리 숫자(YYYYMMDD) -> datetime
    df["openDt"] = pd.to_datetime(df["openDt"], format="%Y%m%d", errors="coerce")

    # 장르: 세로막대(|)로 여러 개 적힌 경우 첫 번째 장르만 사용
    df["genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0].strip())

    return df


df = load_data()

with st.expander("📄 원본 데이터 미리보기"):
    st.dataframe(df, use_container_width=True)

st.divider()

# ------------------------------------------------------------
# 1. 장르별 영화 편수 - 도넛 그래프
# ------------------------------------------------------------
st.header("1️⃣ 장르별 영화 편수")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig_genre = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.5,
)
fig_genre.update_traces(
    textinfo="label+percent",
    hovertemplate="%{label}<br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
)
fig_genre.update_layout(
    legend_title_text="장르",
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_genre, use_container_width=True, key="genre_donut_chart")

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info("여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어 주세요.")

st.divider()

# ------------------------------------------------------------
# 2. 장르 안 영화별 총 관객 - 트리맵
# ------------------------------------------------------------
st.header("2️⃣ 장르별 영화 총 관객 트리맵")

fig_treemap = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
)
fig_treemap.update_traces(
    hovertemplate="영화명: %{label}<br>총 관객: %{value:,}명<extra></extra>",
)
fig_treemap.update_layout(
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_treemap, use_container_width=True, key="genre_treemap_chart")

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info("여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어 주세요.")

st.divider()

# ------------------------------------------------------------
# 3. 총 관객 히스토그램
# ------------------------------------------------------------
st.header("3️⃣ 총 관객 분포")

n_bins = 20

fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=n_bins,
)
fig_hist.update_traces(
    hovertemplate="구간: %{x}<br>영화 편수: %{y}편<extra></extra>",
)
fig_hist.update_layout(
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수",
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_hist, use_container_width=True, key="total_audi_histogram")

# 가장 영화가 몰린 구간 계산
counts, bin_edges = np.histogram(df["total_audi"].dropna(), bins=n_bins)
max_bin_idx = counts.argmax()
bin_start = bin_edges[max_bin_idx]
bin_end = bin_edges[max_bin_idx + 1]

# 총 관객이 가장 많은 영화 계산
top_movie = df.loc[df["total_audi"].idxmax()]

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info(
    f"대부분의 영화는 총 관객 **{bin_start:,.0f}명 ~ {bin_end:,.0f}명** 구간에 몰려 있으며 "
    f"({counts[max_bin_idx]}편), 총 관객이 가장 많은 영화는 "
    f"**'{top_movie['movieNm']}'**(총 {top_movie['total_audi']:,.0f}명)입니다."
)

st.divider()

# ------------------------------------------------------------
# 4. 개봉일 스크린수 vs 총 관객 - 산점도
# ------------------------------------------------------------
st.header("4️⃣ 개봉일 스크린수와 총 관객의 관계")

fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
)
fig_scatter.update_traces(
    hovertemplate="%{hovertext}<br>개봉일 스크린수: %{x:,}개<br>총 관객: %{y:,}명<extra></extra>",
)
fig_scatter.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객 수",
    legend_title_text="장르",
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_scatter, use_container_width=True, key="scrn_vs_audi_scatter")

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info("여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어 주세요.")

st.divider()
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ------------------------------------------------------------
# 기본 설정
# ------------------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide",
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption(
    "최근 1년간 박스오피스 10위권에 든 영화 중, 해당 기간에 개봉한 216편의 데이터를 살펴봅니다."
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일: 여덟 자리 숫자(YYYYMMDD) -> datetime
    df["openDt"] = pd.to_datetime(df["openDt"], format="%Y%m%d", errors="coerce")

    # 장르: 세로막대(|)로 여러 개 적힌 경우 첫 번째 장르만 사용
    df["genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0].strip())

    return df


df = load_data()

with st.expander("📄 원본 데이터 미리보기"):
    st.dataframe(df, use_container_width=True)

st.divider()

# ------------------------------------------------------------
# 1. 장르별 영화 편수 - 도넛 그래프
# ------------------------------------------------------------
st.header("1️⃣ 장르별 영화 편수")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig_genre = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.5,
)
fig_genre.update_traces(
    textinfo="label+percent",
    hovertemplate="%{label}<br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
)
fig_genre.update_layout(
    legend_title_text="장르",
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_genre, use_container_width=True, key="genre_donut_chart")

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info("여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어 주세요.")

st.divider()

# ------------------------------------------------------------
# 2. 장르 안 영화별 총 관객 - 트리맵
# ------------------------------------------------------------
st.header("2️⃣ 장르별 영화 총 관객 트리맵")

fig_treemap = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
)
fig_treemap.update_traces(
    hovertemplate="영화명: %{label}<br>총 관객: %{value:,}명<extra></extra>",
)
fig_treemap.update_layout(
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_treemap, use_container_width=True, key="genre_treemap_chart")

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info("여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어 주세요.")

st.divider()

# ------------------------------------------------------------
# 3. 총 관객 히스토그램
# ------------------------------------------------------------
st.header("3️⃣ 총 관객 분포")

n_bins = 20

fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=n_bins,
)
fig_hist.update_traces(
    hovertemplate="구간: %{x}<br>영화 편수: %{y}편<extra></extra>",
)
fig_hist.update_layout(
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수",
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_hist, use_container_width=True, key="total_audi_histogram")

# 가장 영화가 몰린 구간 계산
counts, bin_edges = np.histogram(df["total_audi"].dropna(), bins=n_bins)
max_bin_idx = counts.argmax()
bin_start = bin_edges[max_bin_idx]
bin_end = bin_edges[max_bin_idx + 1]

# 총 관객이 가장 많은 영화 계산
top_movie = df.loc[df["total_audi"].idxmax()]

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info(
    f"대부분의 영화는 총 관객 **{bin_start:,.0f}명 ~ {bin_end:,.0f}명** 구간에 몰려 있으며 "
    f"({counts[max_bin_idx]}편), 총 관객이 가장 많은 영화는 "
    f"**'{top_movie['movieNm']}'**(총 {top_movie['total_audi']:,.0f}명)입니다."
)

st.divider()

# ------------------------------------------------------------
# 4. 개봉일 스크린수 vs 총 관객 - 산점도
# ------------------------------------------------------------
st.header("4️⃣ 개봉일 스크린수와 총 관객의 관계")

fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
)
fig_scatter.update_traces(
    hovertemplate="%{hovertext}<br>개봉일 스크린수: %{x:,}개<br>총 관객: %{y:,}명<extra></extra>",
)
fig_scatter.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객 수",
    legend_title_text="장르",
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_scatter, use_container_width=True, key="scrn_vs_audi_scatter")

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info("여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어 주세요.")

st.divider()
