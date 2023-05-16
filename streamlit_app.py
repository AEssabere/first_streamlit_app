import streamlit
import pandas
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
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# display the dataframe on the app
streamlit.dataframe(my_fruit_list)


