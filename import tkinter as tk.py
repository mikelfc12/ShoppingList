import tkinter as tk
from tkinter import simpledialog
import pandas as pd
import numpy as np

Recipes_path = 'C:\\Users\\MichaelDixon\\OneDrive - Dufrain Consulting\\Documents\\Python Scripts\\ShoppingList\\Recipe_Master.xlsx'
Meals_path = 'C:\\Users\\MichaelDixon\\OneDrive - Dufrain Consulting\\Documents\\Python Scripts\\ShoppingList\\Weekly_Meals.xlsx'
Recipes = pd.read_excel(Recipes_path)
Meals = pd.read_excel(Meals_path)

Shopping_List_Merge = pd.merge(Recipes, Meals, left_on='Meal_Name', right_on='Meal', how='inner', suffixes=('_R', '_M'))

######   CREATE COLUMNS   ######
Shopping_List_Merge['Quantity_Required'] = Shopping_List_Merge['Quantity'] / Shopping_List_Merge['Servings_R'] *  Shopping_List_Merge['Servings_M'] 

######   KEEP COLUMNS   ######
columns_to_keep = ['Ingredients', 'Food_Group', 'Quantity_Required']
Shopping_List_Keep = Shopping_List_Merge.filter(columns_to_keep)

######   MATHS COLUMNS   ######
Shopping_List_Sum = Shopping_List_Keep.groupby(['Ingredients', 'Food_Group'])['Quantity_Required'].sum().reset_index()
Shopping_List_Sum['Quantity_Required_Rounded'] = np.ceil(Shopping_List_Sum['Quantity_Required']).astype(int)

######   RENAME COLUMNS   ######
Shopping_List_Rename = Shopping_List_Sum.rename(columns={'Quantity_Required_Rounded': 'Quantity'})

######   REORDER COLUMNS   ######
Shopping_List_ReOrder = pd.DataFrame(Shopping_List_Rename, columns=['Ingredients', 'Quantity', 'Food_Group'])

######   SORT COLUMNS   ######
custom_order = ['Fruit', 'Veg', 'Meat', 'Dairy', 'Bread', 'Pasta', 'Jar', 'Condiment']
# Create a mapping dictionary for unique values and their corresponding custom order
category_mapping = {category: i for i, category in enumerate(custom_order)}
# Use the mapping to create a new 'Category_Order' column
Shopping_List_ReOrder['Category_Order'] = Shopping_List_ReOrder['Food_Group'].map(category_mapping)
# Sort the DataFrame by the new 'Category_Order' column
Shopping_List_Sort = Shopping_List_ReOrder.sort_values(by='Category_Order')
# Drop the temporary 'Category_Order' column if you don't need it
Shopping_List_Sort.drop(columns='Category_Order', inplace=True)


result_df=Shopping_List_Sort
print(result_df)