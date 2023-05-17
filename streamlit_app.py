import streamlit
import pandas
import requests
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

# user pick fruit
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

# fruityvice api's get request
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

# display fruity vice api response
# normalize the json response
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# show data normalized as a dataframe
streamlit.dataframe(fruityvice_normalized)



