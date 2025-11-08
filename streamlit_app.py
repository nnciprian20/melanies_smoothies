# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!"""
)

name_on_order = st.text_input("Name on Smoothie:")
st.write('The name on your smoothie will be: ' + name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list = st.multiselect(
    'Chose up to 5 ingredients: ', my_dataframe, max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    for fruit_choosen in ingredients_list:
        ingredients_string += (fruit_choosen + ' ')
        st.subheader(fruit_choosen + ' Nutritional Information ')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_choosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = """INSERT INTO SMOOTHIES.PUBLIC.ORDERS(ingredients, name_on_order) 
                        VALUES('""" + ingredients_string + """', '""" + name_on_order + """')"""

    time_to_insert = st.button('Submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered, '+ name_on_order +'!', icon = '✅')




