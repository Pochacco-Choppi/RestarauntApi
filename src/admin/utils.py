import pandas as pd

from src.config import EXCEL_FILE_PATH


def get_entitues_from_excel(excel_file_path: str = EXCEL_FILE_PATH) -> list:
    df = pd.read_excel(excel_file_path, header=None)

    df_json = []

    for index, row in df.iterrows():
        if not pd.isnull(row[0]):
            menu_id, menu_title, menu_desc = str(row[0]), str(row[1]), str(row[2])
            menu = {
                'title': menu_title,
                'description': menu_desc,
                'id': menu_id,
                'submenus': []
            }

            df_json.append(menu)

        elif not pd.isnull(row[1]):
            submenu_id, submenu_title, submenu_desc = str(row[1]), str(row[2]), str(row[3])
            submenu = {
                'title': submenu_title,
                'description': submenu_desc,
                'id': submenu_id,
                'menu_id': menu['id'],
                'dishes': []
            }

            menu['submenus'].append(submenu)  # type: ignore[attr-defined]

            continue

        elif all([not pd.isnull(row[i]) for i in range(2, 6)]):
            dish_id, dish_title, dish_desc, dish_price = str(row[2]), str(row[3]), str(row[4]), str(row[5])
            dish = {
                'title': dish_title,
                'description': dish_desc,
                'price': dish_price,
                'id': dish_id,
                'submenu_id': submenu['id']
            }

            submenu['dishes'].append(dish)  # type: ignore[attr-defined]

    return df_json
