import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title("My Mom's New Healthy Dinner")
streamlit.header('Breakfast Favorites')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
streamlit.text('Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
streamlit.text('Pick some fruits:')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

def get_fruit_load_list(my_cnx):
  with my_cnx.cursor() as my_cur:
    my_cur.execute('select * from fruit_load_list')
    return my_cur.fetchall()

if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row = get_fruit_load_list(my_cnx)
  streamlit.dataframe(my_data_row)
  
#my_cur = my_cnx.cursor()
#my_cur.execute('select * from fruit_load_list')
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchall()
#streamlit.text("The fruit load list contains:")
#streamlit.text("Hello from Snowflake:")
#streamlit.dataframe(my_data_row)

#streamlit.write('What fruit would you like to add?')
fruit_choice1 = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', fruit_choice1)

streamlit.header("Build Your Own Fruit Smoothie")
my_cur.execute("select * from fruit_load_list")
fruits_selected = streamlit.multiselect("Pick some fruits:", initcap(my_cur.fetchall()))
my_cur.execute("select * from fruityvice where name in fruits_selected")
my_data_row = my_cur.fetchall()
streamlit.dataframe(my_data_row)


