import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


Aotizhongxin_df = pd.read_csv("dashboard/Aotizhongxin_df.csv")
Aotizhongxin_df.sort_values(by="timestamp", inplace=True)
Aotizhongxin_df.reset_index(inplace=True)
Aotizhongxin_df["timestamp"] = pd.to_datetime(
    Aotizhongxin_df["timestamp"], errors="coerce"
)

min_date = Aotizhongxin_df["timestamp"].min().date()
min_time = Aotizhongxin_df["timestamp"].min().time()
max_date = Aotizhongxin_df["timestamp"].max().date()
max_time = Aotizhongxin_df["timestamp"].max().time()

with st.sidebar:
    st.header("Filter Data")

    start_date, end_date = st.date_input(
        label="Rentang Tanggal",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

    # start_time = st.sidebar.time_input(
    #     "Pilih Jam Mulai", Aotizhongxin_df["timestamp"].min().time(), step=3600
    # )
    # end_time = st.sidebar.time_input(
    #     "Pilih Jam Akhir", Aotizhongxin_df["timestamp"].max().time(), step=3600
    # )


start_datetime = pd.to_datetime(f"{start_date} {min_time}")
end_datetime = pd.to_datetime(f"{end_date} {max_time}")

main_df = Aotizhongxin_df[
    Aotizhongxin_df["timestamp"].between(start_datetime, end_datetime)
]

pollutant_by_day = main_df.groupby("day").agg(
    {
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean",
    }
)

weather_by_day = main_df.groupby("day").agg(
    {
        "TEMP": "mean",
        "PRES": "mean",
        "DEWP": "mean",
        "RAIN": "mean",
        "WSPM": "mean",
    }
)

main_df_copy = main_df.copy()
main_df_copy["day_of_week"] = pd.Categorical(
    main_df_copy["day_of_week"],
    categories=[
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ],
    ordered=True,
)

avg_pollutant_by_year = main_df.groupby("year").agg(
    {
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean",
    }
)

avg_pollutant_by_month = main_df.groupby("month").agg(
    {
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean",
    }
)

avg_pollutant_by_day = main_df_copy.groupby("day_of_week").agg(
    {
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean",
    }
)

avg_pollutant_by_hour = main_df.groupby("hour").agg(
    {
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean",
    }
)


main_df = main_df.drop(
    columns=[
        "index",
        "No",
        "year",
        "month",
        "day",
        "hour",
        "wd",
        "station",
        "day_of_week",
    ]
)

st.header("Aotizhongxin Station Air Quality ⛅")

st.subheader("Summary")
st.write(f"Data polutan dan kondisi cuaca dari {start_date} hingga {end_date}:")
st.dataframe(weather_by_day, width=720)
st.dataframe(pollutant_by_day, width=720)

st.subheader("Tren Polusi PM2.5 dan PM10 dalam jam")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(
        avg_pollutant_by_hour.index,
        avg_pollutant_by_hour["PM2.5"],
        label="PM2.5",
        color="salmon",
        linewidth=8,
    )
    ax.set_title("PM2.5", loc="center", fontsize=50)
    ax.set_xlabel(None)
    ax.set_ylabel("Konsentrasi", fontsize=40)
    ax.tick_params(axis="x", labelsize=35)
    ax.tick_params(axis="y", labelsize=35)
    st.pyplot(fig)


with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(
        avg_pollutant_by_hour.index,
        avg_pollutant_by_hour["PM10"],
        label="PM10",
        color="skyblue",
        linewidth=8,
    )
    ax.set_title("PM10", loc="center", fontsize=50)
    ax.set_xlabel(None)
    ax.set_ylabel("Konsentrasi", fontsize=40)
    ax.tick_params(axis="x", labelsize=35)
    ax.tick_params(axis="y", labelsize=35)
    st.pyplot(fig)


st.subheader("Tren Polusi PM2.5 dan PM10 harian")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.bar(
        avg_pollutant_by_day.index,
        avg_pollutant_by_day["PM2.5"],
        label="PM2.5",
        color="salmon",
    )
    ax.set_title("PM2.5", loc="center", fontsize=50)
    ax.set_xlabel(None)
    ax.set_ylabel("Konsentrasi", fontsize=40)
    ax.tick_params(axis="x", labelsize=35, rotation=45)
    ax.tick_params(axis="y", labelsize=35)
    st.pyplot(fig)


with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.bar(
        avg_pollutant_by_day.index,
        avg_pollutant_by_day["PM10"],
        label="PM10",
        color="skyblue",
    )
    ax.set_title("PM10", loc="center", fontsize=50)
    ax.set_xlabel(None)
    ax.set_ylabel("Konsentrasi", fontsize=40)
    ax.tick_params(axis="x", labelsize=35, rotation=45)
    ax.tick_params(axis="y", labelsize=35)
    st.pyplot(fig)


if main_df["timestamp"].dt.month.nunique() > 1:
    st.subheader("Tren Polusi PM2.5 dan PM10 bulanan")

    avg_pollutant_by_month.rename(
        index={
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "Mei",
            6: "Jun",
            7: "Jul",
            8: "Agt",
            9: "Sep",
            10: "Okt",
            11: "Nov",
            12: "Des",
        },
        inplace=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(20, 10))
        sns.barplot(
            x=avg_pollutant_by_month.index,
            y=avg_pollutant_by_month["PM2.5"],
            ax=ax,
            color="salmon",
        )
        ax.set_title("PM2.5", loc="center", fontsize=50)
        ax.set_xlabel(None)
        ax.set_ylabel("Konsentrasi", fontsize=40)
        ax.tick_params(axis="x", labelsize=45, rotation=45)
        ax.tick_params(axis="y", labelsize=45)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(20, 10))
        sns.barplot(
            x=avg_pollutant_by_month.index,
            y=avg_pollutant_by_month["PM10"],
            ax=ax,
            color="skyblue",
        )
        ax.set_title("PM10", loc="center", fontsize=50)
        ax.set_xlabel(None)
        ax.set_ylabel("Konsentrasi", fontsize=40)
        ax.tick_params(axis="x", labelsize=45, rotation=45)
        ax.tick_params(axis="y", labelsize=45)
        st.pyplot(fig)


if main_df["timestamp"].dt.year.nunique() > 1:
    st.subheader("Tren Polusi PM2.5 dan PM10 tahunan")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(20, 10))
        sns.barplot(
            x=avg_pollutant_by_year.index,
            y=avg_pollutant_by_year["PM2.5"],
            ax=ax,
            color="salmon",
        )
        ax.set_title("PM2.5", loc="center", fontsize=50)
        ax.set_xlabel(None)
        ax.set_ylabel("Konsentrasi", fontsize=40)
        ax.tick_params(axis="x", labelsize=55)
        ax.tick_params(axis="y", labelsize=45)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(20, 10))
        sns.barplot(
            x=avg_pollutant_by_year.index,
            y=avg_pollutant_by_year["PM10"],
            ax=ax,
            color="skyblue",
        )
        ax.set_title("PM10", loc="center", fontsize=50)
        ax.set_xlabel(None)
        ax.set_ylabel("Konsentrasi", fontsize=40)
        ax.tick_params(axis="x", labelsize=55)
        ax.tick_params(axis="y", labelsize=45)
        st.pyplot(fig)


st.subheader("Hubungan Polutan dan Faktor Cuaca")

col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(25, 12))
    ax.scatter(
        main_df["TEMP"],
        main_df["PM2.5"],
        label="PM2.5",
        color="salmon",
    )
    ax.set_title("Korelasi Suhu (TEMP) dan PM2.5", loc="center", fontsize=50)
    ax.set_xlabel("Suhu (°C)", fontsize=40)
    ax.set_ylabel("PM2.5 (µgram/m3)", fontsize=40)
    ax.tick_params(axis="x", labelsize=35)
    ax.tick_params(axis="y", labelsize=35)
    st.pyplot(fig)


with col2:
    fig, ax = plt.subplots(figsize=(25, 12))
    ax.scatter(
        main_df["TEMP"],
        main_df["PM10"],
        color="skyblue",
    )
    ax.set_title("Korelasi Suhu (TEMP) dan PM10", loc="center", fontsize=50)
    ax.set_xlabel("Suhu (°C)", fontsize=40)
    ax.set_ylabel("PM10 (µgram/m3)", fontsize=40)
    ax.tick_params(axis="x", labelsize=35)
    ax.tick_params(axis="y", labelsize=35)
    st.pyplot(fig)


col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(25, 12))
    ax.scatter(
        main_df["WSPM"],
        main_df["PM2.5"],
        color="salmon",
    )
    ax.set_title("Korelasi Kecepatan Angin (WSPM) dan PM2.5", loc="center", fontsize=50)
    ax.set_xlabel("Kecepatan Angin (m/s)", fontsize=40)
    ax.set_ylabel("PM2.5 (µgram/m3)", fontsize=40)
    ax.tick_params(axis="x", labelsize=35)
    ax.tick_params(axis="y", labelsize=35)
    st.pyplot(fig)


with col2:
    fig, ax = plt.subplots(figsize=(25, 12))
    ax.scatter(
        main_df["WSPM"],
        main_df["PM10"],
        color="skyblue",
    )
    ax.set_title("Korelasi Kecepatan Angin (WSPM) dan PM10", loc="center", fontsize=50)
    ax.set_xlabel("Kecepatan Angin (m/s)", fontsize=40)
    ax.set_ylabel("PM10 (µgram/m3)", fontsize=40)
    ax.tick_params(axis="x", labelsize=3)
    ax.tick_params(axis="y", labelsize=35)
    st.pyplot(fig)


col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(25, 12))
    ax.scatter(
        main_df["PRES"],
        main_df["PM2.5"],
        color="salmon",
    )
    ax.set_title(
        "Korelasi antara Tekanan Udara (PRES) dan Konsentrasi PM2.5",
        loc="center",
        fontsize=50,
    )
    ax.set_xlabel("Tekanan Udara (hPa)", fontsize=40)
    ax.set_ylabel("PM2.5 (µgram/m3)", fontsize=40)
    ax.tick_params(axis="x", labelsize=35)
    ax.tick_params(axis="y", labelsize=35)
    st.pyplot(fig)


with col2:
    fig, ax = plt.subplots(figsize=(25, 12))
    ax.scatter(
        main_df["PRES"],
        main_df["PM10"],
        color="skyblue",
    )
    ax.set_title(
        "Korelasi antara Tekanan Udara (PRES) dan Konsentrasi PM10",
        loc="center",
        fontsize=50,
    )
    ax.set_xlabel("Tekanan Udara (hPa)", fontsize=40)
    ax.set_ylabel("PM10 (µgram/m3)", fontsize=40)
    ax.tick_params(axis="x", labelsize=3)
    ax.tick_params(axis="y", labelsize=35)
    st.pyplot(fig)


col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(25, 12))
    ax.scatter(
        main_df["DEWP"],
        main_df["PM2.5"],
        color="salmon",
    )
    ax.set_title(
        "Korelasi antara Titik Embun (DEWP) dan Konsentrasi PM2.5",
        loc="center",
        fontsize=50,
    )
    ax.set_xlabel("Titik Embun (°C)", fontsize=40)
    ax.set_ylabel("PM2.5 (µgram/m3)", fontsize=40)
    ax.tick_params(axis="x", labelsize=35)
    ax.tick_params(axis="y", labelsize=35)
    st.pyplot(fig)


with col2:
    fig, ax = plt.subplots(figsize=(25, 12))
    ax.scatter(
        main_df["DEWP"],
        main_df["PM10"],
        color="skyblue",
    )
    ax.set_title(
        "Korelasi antara Titik Embun (DEWP) dan Konsentrasi PM10",
        loc="center",
        fontsize=50,
    )
    ax.set_xlabel("Titik Embun (°C)", fontsize=40)
    ax.set_ylabel("PM10 (µgram/m3)", fontsize=40)
    ax.tick_params(axis="x", labelsize=35)
    ax.tick_params(axis="y", labelsize=35)
    st.pyplot(fig)


fig, ax = plt.subplots(figsize=(30, 15))
ax.scatter(main_df["TEMP"], main_df["O3"])
ax.set_title(
    "Korelasi antara Suhu (TEMP) dan Konsentrasi Ozon (O3)", loc="center", fontsize=35
)
ax.set_xlabel("Suhu (°C)", fontsize=30)
ax.set_ylabel("Ozon (O3)", fontsize=30)
ax.tick_params(axis="x", labelsize=25)
ax.tick_params(axis="y", labelsize=30)
st.pyplot(fig)


fig, ax = plt.subplots(figsize=(40, 20))
ax.scatter(main_df["WSPM"], main_df["NO2"])
ax.set_title(
    "Korelasi antara Kecepatan Angin (WSPM) dan Konsentrasi Nitrogen Dioksida (NO2)",
    loc="center",
    fontsize=50,
)
ax.set_xlabel("Kecepatan Angin (m/s)", fontsize=35)
ax.set_ylabel("Nitrogen Dioksida (NO2)", fontsize=35)
ax.tick_params(axis="x", labelsize=25)
ax.tick_params(axis="y", labelsize=30)
st.pyplot(fig)


st.sidebar.info("Air Quality Analysis Dashboard - Aotizhongxin Station")
st.caption("Copyright (c) Lukman Harahap")
