import pandas as pd

valid_meal_path = 'C:\\Users\\MichaelDixon\\OneDrive - Dufrain Consulting\\Documents\\Python Scripts\\ShoppingList\\Recipe_Master.xlsx'
column_name = 'Meal_Name'

# Read the Excel file
vm_data = pd.read_excel(valid_meal_path)
valid_meals = vm_data[column_name].unique().tolist()
print(valid_meals)