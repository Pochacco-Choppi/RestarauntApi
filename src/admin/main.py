import os

import pandas as pd

excel_file_path = 'src/admin/Menu.xlsx'
df = pd.read_excel(excel_file_path, header=None)

# Loop through the rows and process the data
for index, row in df.iterrows():
    if not pd.isnull(row[0]):
        menu_id, menu_name, menu_desc = row[0], row[1], row[2]

        print("!MENU!", menu_id, menu_name, menu_desc)

    elif not pd.isnull(row[1]):
        submenu_id, submenu_name, submenu_desc = row[1], row[2], row[3]

        print("!    SUBMENU!", menu_id, submenu_id, submenu_name, submenu_desc)

    elif not pd.isnull(row[2]):
        dish_id, dish_name, dish_desc, dish_price = row[2], row[3], row[4], row[5]
        print("!        DISH!", submenu_id, dish_id, dish_name, dish_desc, dish_price)



        
    #     # Process the dish information here (e.g., print, store in a data structure, etc.)
    #     print("Menu:", menu_name, "| Submenu:", submenu_name, "| Dish:", dish_name, "| Price:", dish_price)
