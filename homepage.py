import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_icon= "📚",
                   page_title = "streamlit homepage")


data_base = pd.read_csv("https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv")
data_base["continent"] = data_base["continent"].apply(lambda x: x[:-1].strip())


data_reduct = data_base[["mpg", "cylinders", "cubicinches", "hp", "weightlbs", "time-to-60"]]

with st.sidebar:
    st.title("faites vos choix")
    region = st.selectbox("régions", ["All", "US", "Japon", "Europe"])
    if region == "US":
        data = data_base[data_base["continent"] == "US"]
    elif region == "Japon":
        data = data_base[data_base["continent"] == "Japan"]
    elif region == "Europe":
        data = data_base[data_base["continent"] == "Europe"]
    elif region == "All":
        data = data_base
    
    puissance_min = data["cubicinches"].min()
    puissance_max = data["cubicinches"].max() 

    min_puissance, max_puissance = st.slider("puissance", min_value=puissance_min, max_value=puissance_max, value=(puissance_min, puissance_max))


data = data[data["cubicinches"].between(min_puissance, max_puissance)]


fig, ax = plt.subplots(2,2, figsize=(18, 18))
ax[0,0].set_title("heatmap de corrélation")
sns.heatmap(data_reduct.corr(), annot=True, cmap='coolwarm', ax=ax[0,0])
ax[0,1].set_title("evolution des mpg par année")
sns.lineplot(data=data, y="mpg", x="year", hue= "continent", ax=ax[0,1])
ax[1,0].set_title("nuage de point des 0 à 100 par années")
sns.scatterplot(data=data, x="year", y="time-to-60",hue= "continent", ax=ax[1,0])
ax[1,1].set_title("distribution des cylindrées")
sns.violinplot(data=data, x="cubicinches", ax=ax[1,1])
        
st.sidebar.write("nombre de références : ", len(data))
st.pyplot(fig)

# st.pyplot(sns.pairplot(data, hue = "continent"))

if st.sidebar.button(label="reset_all") :
    data = data_base

