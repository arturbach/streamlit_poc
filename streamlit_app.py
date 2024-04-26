  # Import python packages
import streamlit as st
###from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
    
)

from snowflake.snowpark.functions import col





##session = get_active_session()
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
name_on_order = st.text_input(
           "Please Enter Name of Smothie","Default name is... "
          
        )
   
st.write("You entered: ", name_on_order) 

ingredients_list  = st.multiselect(
    "Choose up to 5 ingredients:",
     my_dataframe ,
    max_selections=5
) 

if ingredients_list :
  ## st.write('You selected:',ingredients_list  )
  ## st.text(ingredients_list)

   ingredients_string =''   
    
   for fruit_chosen in ingredients_list:
       ingredients_string += fruit_chosen + ' '
   st.write('You selected:',ingredients_string  )
   my_insert_stmt = """ insert into smoothies.public.orders(ingredients , name_on_order)
            values ('""" + ingredients_string + """' , '""" + name_on_order + """')"""
  
   ###st.write(my_insert_stmt)
   if st.button('Submit Order'):
      session.sql(my_insert_stmt).collect()
      st.success('Your Smoothie is ordered!', icon="✅")   
   
import requests
fruityvice_responce = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_responce.json())
