# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie ")
st.write(
  """Choose the fruits you want in your custom Smoothie!"""
)

name_on_order = st.text_input("Name on Smoothie:")
st.write('The name on your smoothie will be: ' + name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Chose up to 5 ingredients: ', my_dataframe, max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    for x in ingredients_list:
        ingredients_string += (x + ' ')

    my_insert_stmt = """INSERT INTO SMOOTHIES.PUBLIC.ORDERS(ingredients, name_on_order) 
                        VALUES('""" + ingredients_string + """', '""" + name_on_order + """')"""

    time_to_insert = st.button('Submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered, '+ name_on_order +'!', icon = '✅')
    
