  # Import python packages
import streamlit as st
import requests
import pandas  

from snowflake.snowpark.functions import col

###from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
    
)


name_on_order = st.text_input(
           "Please Enter Name of Smothie","Default name is... "
          
        )
st.write("You entered: ", name_on_order) 


##session = get_active_session()
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME') ,col('search_on'))
pd_df =my_dataframe.to_pandas()
st.dataframe(pd_df)
###st.stop()

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
       st.subheader(fruit_chosen+ ' Nutrition infotmation') 
       search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
       st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
       fruityvice_responce = requests.get("https://fruityvice.com/api/fruit/" + search_on)
       fv_df = st.dataframe(data=fruityvice_responce.json(), use_container_width=True)
       st.write("https://fruityvice.com/api/fruit/" + fruit_chosen)
       st.write('You selected:',ingredients_string  )
       my_insert_stmt = """ insert into smoothies.public.orders(ingredients , name_on_order)
            values ('""" + ingredients_string + """' , '""" + name_on_order + """')"""
  
   ###st.write(my_insert_stmt)
   if st.button('Submit Order'):
      session.sql(my_insert_stmt).collect()
      st.success('Your Smoothie is ordered!', icon="✅")   
   

