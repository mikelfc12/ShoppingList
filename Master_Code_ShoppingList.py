import tkinter as tk
from tkinter import simpledialog
import pandas as pd
import numpy as np

#Valid Meal List
valid_meal_path = 'C:\\Users\\MichaelDixon\\OneDrive - Dufrain Consulting\\Documents\\Python Scripts\\ShoppingList\\Recipe_Master.xlsx'
column_name = 'Meal_Name'
vm_data = pd.read_excel(valid_meal_path)
valid_meals = vm_data[column_name].unique().tolist()
print(valid_meals)


def get_meals_with_servings():
    meals_with_servings = []
    while True:
        meal = simpledialog.askstring("Meal Input", "Enter a meal (or 'exit' to finish):")
        if not meal or meal.lower() == 'exit':
            break
        elif meal not in valid_meals:
            tk.messagebox.showerror("Error", "Invalid meal. Please enter a valid meal.")
        else:
            servings = simpledialog.askinteger("Servings Input", f"How many servings for {meal}?")
            meals_with_servings.append({'Meal': meal, 'Servings': servings})
            update_listbox(meals_with_servings)
    return meals_with_servings

def update_listbox(meals_list):
    listbox.delete(0, tk.END)  # Clear the listbox
    for meal in meals_list:
        listbox.insert(tk.END, f"{meal['Meal']} - {meal['Servings']} servings")

def delete_selected():
    selected_index = listbox.curselection()
    if selected_index:
        meals.pop(selected_index[0])
        update_listbox(meals)

def edit_selected():
    selected_index = listbox.curselection()
    if selected_index:
        meal_to_edit = meals[selected_index[0]]
        new_meal = simpledialog.askstring("Edit Meal", f"Edit the meal for {meal_to_edit['Meal']}:", initialvalue=meal_to_edit['Meal'])
        new_servings = simpledialog.askinteger("Edit Servings", f"Edit the servings for {meal_to_edit['Meal']}:", initialvalue=meal_to_edit['Servings'])
        meals[selected_index[0]] = {'Meal': new_meal, 'Servings': new_servings}
        update_listbox(meals)
        
        # Recalculate result_df after editing
        recalculate_result_df()

def submit_meals():
    global meals_df
    meals_data = meals  # Use the existing meals list

    # Update the DataFrame with the existing data
    if meals_data:
        meals_df = pd.DataFrame(meals_data)
        update_listbox(meals_data)
    
        # Recalculate result_df after submitting
        recalculate_result_df()
    root.destroy()

def recalculate_result_df():
    global result_df
    if meals_df is not None:
        result_df = perform_data_manipulation(meals_df)
        print("\nResult DataFrame after merging and manipulation:")
        print(result_df)

def perform_data_manipulation(Meals):
    # Additional manipulation steps
    #Recipes_path = 'https://github.com/mikelfc12/ShoppingList/raw/main/Recipe_Master.xlsx'
    Recipes_path = 'C:\\Users\\MichaelDixon\\OneDrive - Dufrain Consulting\\Documents\\Python Scripts\\ShoppingList\\Recipe_Master.xlsx'
    Recipes = pd.read_excel(Recipes_path)
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

    return Shopping_List_Sort

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Meal Input List")

    meals = []

    # Create a listbox to display entered meals
    listbox = tk.Listbox(root)
    listbox.pack(padx=50, pady=50)
    
    # Buttons for actions
    delete_button = tk.Button(root, text="Delete", command=delete_selected)
    delete_button.pack(side=tk.LEFT, padx=5)

    edit_button = tk.Button(root, text="Edit", command=edit_selected)
    edit_button.pack(side=tk.LEFT, padx=5)
    
    # Button to submit meals
    submit_button = tk.Button(root, text="Submit", command=submit_meals)
    submit_button.pack(pady=10)
    
    meals_df = None

    meals_data = get_meals_with_servings()
    meals.extend(meals_data)  # Add initial meals to the list

    # Create a DataFrame from the list of dictionaries
    Meals = pd.DataFrame(meals_data)

    # Print the DataFrame
    print("DataFrame:")
    print(Meals)

    # Perform merging and additional manipulation steps
    result_df = perform_data_manipulation(Meals)

    # Print the result DataFrame
    print("\nResult DataFrame after merging and manipulation:")
    print(result_df)

    root.mainloop()
        # After the Tkinter window is closed, you can perform further manipulation
    if meals_df is not None:
        recalculate_result_df()
    