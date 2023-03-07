import streamlit
import pandas
import requests

from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
#display the table 
fruits_to_show = my_fruit_list.loc[fruits_selected]


#CREATE THE REPEATABLE CODE BLOCK(CALLED A FUNTION)
def get_fruityvice_data(this_fruit_choice):
     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ this_fruit_choice)    
     fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
     return fruityvice_normalized
   
# Display the table on the page.
streamlit.dataframe(fruits_to_show)
streamlit.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
   else:
     back_from_funtion =get_fruityvice_data(fruit_choice)    
     streamlit.dataframe(back_from_funtion)
except URLError as e:
  streamlit.error()
  
#import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)

# write your own comment adjust the data? 
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - PUT INTO A FRAME?
#streamlit.dataframe(fruityvice_normalized)

import snowflake.connector
streamlit.header("The fruit load list contains:")
#Snowflake-related funtions
def get_fruit_load_list():
     with my_cnx.cursor() as my_cur:
          my_cur.execute("SELECT * from fruit_load_list")
          return  my_cur.fetchall()
#add a button to load the fruit list 
if streamlit.button('Get fruit_load_list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

#DON´T run anything past here while we have a trobleshoot
streamlit.stop()

fruit_choice = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', fruit_choice)
my_cur.excecute("insert into FRUIT_LOAD_LIST values('from streamlit')") 

