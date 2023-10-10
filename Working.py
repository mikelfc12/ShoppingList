import tkinter as tk
import numpy as np
from tkinter import ttk
from tkinter import simpledialog
import pandas as pd

class MealInputApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meal Input List")

        self.meals = []

        # Load valid meals from Excel file
        self.valid_meals = self.load_valid_meals()

        # Create a combo box for meal selection
        self.meal_var = tk.StringVar()
        self.meal_combo = ttk.Combobox(self.root, textvariable=self.meal_var)
        self.meal_combo['values'] = self.valid_meals
        self.meal_combo.set("Select a meal")

        # Create an entry for servings input
        self.servings_var = tk.StringVar()
        self.servings_entry = tk.Entry(self.root, textvariable=self.servings_var)

        # Create a list box to display selected meals
        self.meals_listbox = tk.Listbox(self.root)

        # Buttons for actions
        self.delete_button = tk.Button(self.root, text="Delete", command=self.on_delete_button)
        self.edit_button = tk.Button(self.root, text="Edit", command=self.on_edit_button)
        self.submit_button = tk.Button(self.root, text="Submit", command=self.on_submit_button)
        self.create_list_button = tk.Button(self.root, text="Create List", command=self.on_create_list_button)

        # Layout
        self.meal_combo.pack(pady=10)
        self.servings_entry.pack(pady=10)
        self.delete_button.pack(pady=10)
        self.edit_button.pack(pady=10)
        self.submit_button.pack(pady=10)
        self.create_list_button.pack(pady=10)
        self.meals_listbox.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def on_delete_button(self):
        selected_index = self.meals_listbox.curselection()
        if selected_index:
            self.meals.pop(selected_index[0])
            self.update_meals_listbox()

    def on_edit_button(self):
        selected_index = self.meals_listbox.curselection()
        if selected_index:
            meal_to_edit = self.meals[selected_index[0]]
            new_meal = simpledialog.askstring("Edit Meal", f"Edit the meal for {meal_to_edit['Meal']}:", initialvalue=meal_to_edit['Meal'])
            new_servings = simpledialog.askinteger("Edit Servings", f"Edit the servings for {meal_to_edit['Meal']}:", initialvalue=meal_to_edit['Servings'])
            self.meals[selected_index[0]] = {'Meal': new_meal, 'Servings': new_servings}
            self.update_meals_listbox()

    def on_submit_button(self):
        meal = self.meal_var.get()
        servings = self.servings_var.get()

        if meal and servings:
            self.meals.append({'Meal': meal, 'Servings': servings})
            self.update_meals_listbox()

    def on_create_list_button(self):
        if self.meals:
            result_df = self.perform_data_manipulation()
            print("\nResult DataFrame after merging and manipulation:")
            print(result_df)
            # You can further process or display the result as needed

    def update_meals_listbox(self):
        self.meals_listbox.delete(0, tk.END)
        for meal in self.meals:
            self.meals_listbox.insert(tk.END, f"{meal['Meal']} - {meal['Servings']} servings")

    def load_valid_meals(self):
        # Replace 'your_file.xlsx' with the actual path to your Excel file
        valid_meal_path = 'C:\\Users\\MichaelDixon\\OneDrive - Dufrain Consulting\\Documents\\Python Scripts\\ShoppingList\\Recipe_Master.xlsx'
        df = pd.read_excel(valid_meal_path)
        return df['Meal_Name'].unique().tolist()  # Assuming 'Meal' is the column with valid meals

    def perform_data_manipulation(self):
        # Placeholder for your data manipulation steps
        # You can replace this with your actual data processing logic
        columns = ['Meal', 'Servings']
        meals_df = pd.DataFrame(self.meals, columns=columns)
        Recipes_path = 'C:\\Users\\MichaelDixon\\OneDrive - Dufrain Consulting\\Documents\\Python Scripts\\ShoppingList\\Recipe_Master.xlsx'
        Recipes = pd.read_excel(Recipes_path)
        
        # Merge with Recipes DataFrame
        Shopping_List_Merge = pd.merge(Recipes, meals_df, left_on='Meal_Name', right_on='Meal', how='inner', suffixes=('_R', '_M'))
        ######   CREATE COLUMNS   ######
        #Shopping_List_Merge['Quantity_Required'] = Shopping_List_Merge['Quantity'] / Shopping_List_Merge['Servings_R'] *  Shopping_List_Merge['Servings_M'] 

        # Convert 'Servings_M' column to numeric, coercing errors to NaN
        Shopping_List_Merge['Servings_M'] = pd.to_numeric(Shopping_List_Merge['Servings_M'], errors='coerce')

        # Fill NaN values with a default value (e.g., 0)
        Shopping_List_Merge['Servings_M'].fillna(0, inplace=True)

        # Convert the column to integers
        Shopping_List_Merge['Servings_M'] = Shopping_List_Merge['Servings_M'].astype(int)

        # Now you can perform the division
        Shopping_List_Merge['Quantity_Required'] = (Shopping_List_Merge['Quantity'] / Shopping_List_Merge['Servings_R'] * Shopping_List_Merge['Servings_M'])
    
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

        Shopping_List=Shopping_List_Sort
        
        return Shopping_List


if __name__ == '__main__':
    root = tk.Tk()
    app = MealInputApp(root)
    root.mainloop()
    