import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title("My parents' healthy diet !!")

streamlit.header("Header : ")
streamlit.text("breakfast Menu : ")
streamlit.text("Foood ! ")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# read csv from the stage 
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# change index number to fruit names 
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

# pick rows of fruits_selected
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the dataframe on the app
streamlit.dataframe(fruits_to_show)

# display the header 
streamlit.header("Fruityvice Fruit Advice!")

# create a function to get fruit data
def get_fruityvice_data(this_fruit_choice):
  
    # fruityvice api's get request
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    
    # display fruity vice api response
    # normalize the json response
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    
    return fruityvice_normalized
  
try: 
  # user pick fruit
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice : 
    streamlit.error("Please select a fruit to get information.")
  else:
    streamlit.write('The user entered ', fruit_choice)
    
    # show data normalized as a dataframe
    streamlit.dataframe(get_fruityvice_data(fruit_choice))

except URLError as e:
  streamlit.error()
  

streamlit.header(" View our fruit list ")

# function to get data from snowflake
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM pc_rivery_db.public.fruit_load_list")
    return  my_cur.fetchall()
  
# add a button to load a fruit
if streamlit.button('Get fruit load list'):
  # snowflake connection
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  
  # close snowflake connection
  my_cnx.close()
  
  # display fruit list as a dataframe
  streamlit.dataframe(my_data_rows)
  
# function to insert data into snowflake's database table
def insert_fruit_load_list(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO pc_rivery_db.public.fruit_load_list values ('" + new_fruit + "')")
    return  "thanks for adding" + new_fruit

streamlit.header(" Add your favorites ")
  
# user chooses fruit to add
add_fruit = streamlit.text_input('What fruit would you like to add ?')

if streamlit.button('add fruit to the list'):
  # snowflake connection
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  
  # insert the new fruit chosen by the user
  streamlit.text(insert_fruit_load_list(add_fruit))
  
  # close snowflake connection
  my_cnx.close()
  


