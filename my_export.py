import mysql.connector
import pandas as pd
import streamlit as st
import pandas as pd
#import streamlit_pandas as sp
#import matplotlib.pyplot as plt 
#from streamlit_webrtc import webrtc_streamer
conn = mysql.connector.connect(

    host="localhost",

    user="root",

    port="3306",

    password="mysqldatabase24",

    database="redbus"

)

table_name='bus_details2'
database="redbus"
cursor = conn.cursor()

writer = cursor 

query = "SELECT * FROM bus_details2"

query2 = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = '{database}' ORDER BY ORDINAL_POSITION"

writer.execute(query)

view = cursor.fetchall()

data=pd.DataFrame(view)

writer.execute(query2)
s=cursor.fetchall() 
data=pd.DataFrame(view)
flat_list = [item[0] for item in s]
#flat_list_1=['s_no','route-collected','name','type','arrival_time','departure_time','duration','price','seats_available','rating']
data.columns=flat_list
data=data.set_index('s_no')
#data['price'] = pd.to_numeric(data['price'], errors='coerce')
#data['price']=data['price'].fillna(0)
#data['price']=data['price'].astype('int64')




st.set_page_config(
    page_title="Red-Bus Details",
    page_icon="png-transparent-redbus-in-india-ticket-discounts-and-allowances-bus-text-logo-india.png",  
    layout="wide",  
    initial_sidebar_state="expanded"  
)
 

price_min=int(data['price'].min())
price_max=int(data['price'].max())
rating_min = float(data['rating'].min())
rating_max = float(data['rating'].max())
tab1,tab2,tab3=st.tabs(["Rating","Price","Route"])
with tab1:
    rating = st.slider('rating for 2nd', float(rating_min), float(rating_max ), (rating_min, rating_max))
with tab2:
    price=st.slider('pricefor2nd',price_min,price_max,(price_min, price_max))
x=data['route'].drop_duplicates()
with tab3:
    route_collected=st.selectbox('routefor2nd',x)
#filtered_df = data[(data['price'] >= price[0]) & (data['price'] <= price[1] ) & data["rating"]<=rating[0] & data['rating']>=rating[1]]
filtered_df = data[
    (data['price'] >= price[0]) & 
    (data['price'] <= price[1]) & 
    (data['rating'] >= rating[0]) & 
    (data['rating'] <= rating[1]) &
    (data['route']==route_collected)
]


st.title(':red[_*By streamlit*_]:bus:')
st.write(filtered_df) 
#x=data['route'].drop_duplicates()
#route_collected=st.selectbox('route',x)
#filter1=data[data['route']==route_collected] 
#st.write(filter1)
#plt.barh(data['route'],data['seats_available'])
#st.pyplot(plt)

query = f"SELECT * FROM bus_details2 WHERE price BETWEEN {price[0]} AND {price[1]} AND rating BETWEEN {rating[0]} AND {rating[1]} AND route='{route_collected}'"

writer.execute(query)
view2=cursor.fetchall()
query2 = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = '{database}' ORDER BY ORDINAL_POSITION"
writer.execute(query2)
s=cursor.fetchall() 
a=pd.DataFrame(view2)
try:
    flat_list = [item[0] for item in s]
    a.columns=flat_list
    a=a.set_index('s_no')
    st.title(':red[_*By Database*_]:bus:')

    st.write(a)
except:
    st.error(':red[NO :bus: Found]!!!')    

