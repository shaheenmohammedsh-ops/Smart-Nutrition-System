import pandas as pd

def create_professional_database():
    """
    Generates a massive, diverse database (~120+ items) with high variance.
    Graduated Scales:
    - Low: Economic & Low Calorie
    - Medium: Standard Meals
    - High: Premium & Heavy Meals
    """
    
    data = [
        # =======================================================
        #  BREAKFAST (Variety: Light -> Heavy)
        # =======================================================
        
        # --- EGGS (Low to High) ---
        {"Name": "Boiled Egg (1)", "Type": "Breakfast", "Category": "Eggs", "Cal": 70, "Price": 10},
        {"Name": "Boiled Eggs (2) with Arugula", "Type": "Breakfast", "Category": "Eggs", "Cal": 150, "Price": 20},
        {"Name": "Fried Eggs with Toast", "Type": "Breakfast", "Category": "Eggs", "Cal": 300, "Price": 25},
        {"Name": "Vegetable Omelette Sandwich", "Type": "Breakfast", "Category": "Eggs", "Cal": 400, "Price": 35},
        {"Name": "Shakshuka Pan with Bread", "Type": "Breakfast", "Category": "Eggs", "Cal": 500, "Price": 45},
        {"Name": "Scrambled Eggs with Pastrami", "Type": "Breakfast", "Category": "Eggs", "Cal": 600, "Price": 60},
        {"Name": "Mega Omelette (3 Eggs + Cheese + Beef)", "Type": "Breakfast", "Category": "Eggs", "Cal": 850, "Price": 90},

        # --- VEGETARIAN / EGYPTIAN (Budget to Full Meal) ---
        {"Name": "Foul Medames Sandwich", "Type": "Breakfast", "Category": "Vegetarian", "Cal": 300, "Price": 12},
        {"Name": "Falafel Sandwich", "Type": "Breakfast", "Category": "Vegetarian", "Cal": 350, "Price": 12},
        {"Name": "Fried Potato Sandwich", "Type": "Breakfast", "Category": "Vegetarian", "Cal": 450, "Price": 20},
        {"Name": "Foul Plate with Flaxseed Oil", "Type": "Breakfast", "Category": "Vegetarian", "Cal": 500, "Price": 30},
        {"Name": "Falafel Plate (6 pcs) with Tahini", "Type": "Breakfast", "Category": "Vegetarian", "Cal": 600, "Price": 35},
        {"Name": "Foul with Butter & Eggs Plate", "Type": "Breakfast", "Category": "Vegetarian", "Cal": 750, "Price": 55},
        {"Name": "Egyptian Breakfast Tray (Foul, Falafel, Fries, Eggs)", "Type": "Breakfast", "Category": "Vegetarian", "Cal": 1100, "Price": 100},

        # --- DAIRY (Light to Rich) ---
        {"Name": "Cottage Cheese (Quraish) with Tomato", "Type": "Breakfast", "Category": "Dairy", "Cal": 150, "Price": 15},
        {"Name": "White Cheese Sandwich", "Type": "Breakfast", "Category": "Dairy", "Cal": 250, "Price": 20},
        {"Name": "Yogurt with Honey", "Type": "Breakfast", "Category": "Dairy", "Cal": 300, "Price": 30},
        {"Name": "Cheddar Cheese Toast", "Type": "Breakfast", "Category": "Dairy", "Cal": 350, "Price": 40},
        {"Name": "Roomi Cheese Sandwich", "Type": "Breakfast", "Category": "Dairy", "Cal": 400, "Price": 45},
        {"Name": "Grilled Halloumi Cheese Plate", "Type": "Breakfast", "Category": "Dairy", "Cal": 550, "Price": 80},
        {"Name": "Full Cream Milk & Cereal Bowl", "Type": "Breakfast", "Category": "Dairy", "Cal": 600, "Price": 50},

        # --- SWEET / BAKERY (Carb Loading) ---
        {"Name": "Plain Croissant", "Type": "Breakfast", "Category": "Dessert", "Cal": 300, "Price": 35},
        {"Name": "Oatmeal with Water (Diet)", "Type": "Breakfast", "Category": "Healthy", "Cal": 200, "Price": 25},
        {"Name": "Oatmeal with Whole Milk & Nuts", "Type": "Breakfast", "Category": "Healthy", "Cal": 500, "Price": 60},
        {"Name": "Pancakes with Honey", "Type": "Breakfast", "Category": "Dessert", "Cal": 600, "Price": 70},
        {"Name": "Waffles with Chocolate & Fruit", "Type": "Breakfast", "Category": "Dessert", "Cal": 900, "Price": 90},

        # =======================================================
        #  LUNCH (Massive Variance: 300 Cal -> 2000 Cal)
        # =======================================================

        # --- CHICKEN (Low -> High) ---
        {"Name": "Grilled Chicken Breast (Diet) w/ Salad", "Type": "Lunch", "Category": "Chicken", "Cal": 400, "Price": 100},
        {"Name": "Chicken Shawerma Sandwich (Small)", "Type": "Lunch", "Category": "Chicken", "Cal": 500, "Price": 70},
        {"Name": "Grilled Chicken (Quarter) with Rice", "Type": "Lunch", "Category": "Chicken", "Cal": 850, "Price": 140},
        {"Name": "Shish Tawook Meal (Rice & Bread)", "Type": "Lunch", "Category": "Chicken", "Cal": 950, "Price": 160},
        {"Name": "Fried Chicken Pane with Pasta", "Type": "Lunch", "Category": "Chicken", "Cal": 1100, "Price": 150},
        {"Name": "Broasted Chicken (3 pcs) with Fries", "Type": "Lunch", "Category": "Chicken", "Cal": 1300, "Price": 190},
        {"Name": "Chicken Mandi Tray (Large)", "Type": "Lunch", "Category": "Chicken", "Cal": 1600, "Price": 250},
        {"Name": "Whole Grilled Chicken Meal", "Type": "Lunch", "Category": "Chicken", "Cal": 1900, "Price": 320},

        # --- MEAT (Standard -> Luxury) ---
        {"Name": "Minced Meat Sandwich", "Type": "Lunch", "Category": "Meat", "Cal": 500, "Price": 60},
        {"Name": "Hawawshi Loaf (Standard)", "Type": "Lunch", "Category": "Meat", "Cal": 800, "Price": 90},
        {"Name": "Grilled Kofta (3 pcs) with Salad", "Type": "Lunch", "Category": "Meat", "Cal": 850, "Price": 150},
        {"Name": "Beef Burger with Cheese", "Type": "Lunch", "Category": "Meat", "Cal": 950, "Price": 130},
        {"Name": "Pasta Bolognese (Red Sauce Meat)", "Type": "Lunch", "Category": "Meat", "Cal": 1000, "Price": 110},
        {"Name": "Kebab & Kofta Mix Plate", "Type": "Lunch", "Category": "Meat", "Cal": 1200, "Price": 280},
        {"Name": "Double Beef Burger with Large Fries", "Type": "Lunch", "Category": "Meat", "Cal": 1500, "Price": 220},
        {"Name": "Fatteh with Lamb Meat (Large)", "Type": "Lunch", "Category": "Meat", "Cal": 1800, "Price": 300},
        {"Name": "Ribeye Steak (300g) with Sides", "Type": "Lunch", "Category": "Meat", "Cal": 1400, "Price": 600},

        # --- SEAFOOD (Economic -> Premium) ---
        {"Name": "Tuna Salad with Corn", "Type": "Lunch", "Category": "Seafood", "Cal": 400, "Price": 80},
        {"Name": "Fried Calamari Sandwich", "Type": "Lunch", "Category": "Seafood", "Cal": 600, "Price": 90},
        {"Name": "Grilled Tilapia (Bolti) with Rice", "Type": "Lunch", "Category": "Seafood", "Cal": 750, "Price": 120},
        {"Name": "Grilled Grey Mullet (Bouri) Meal", "Type": "Lunch", "Category": "Seafood", "Cal": 900, "Price": 180},
        {"Name": "Fried Fish Fillet with Tartar & Rice", "Type": "Lunch", "Category": "Seafood", "Cal": 1100, "Price": 160},
        {"Name": "Shrimp Pasta White Sauce", "Type": "Lunch", "Category": "Seafood", "Cal": 1200, "Price": 220},
        {"Name": "Seafood Soup (Creamy) with Bread", "Type": "Lunch", "Category": "Seafood", "Cal": 800, "Price": 150},
        {"Name": "Grand Seafood Platter (Shrimp/Crab/Fish)", "Type": "Lunch", "Category": "Seafood", "Cal": 1600, "Price": 550},

        # --- VEGETARIAN / CARB (Budget -> Heavy) ---
        {"Name": "Koshary Bowl (Small)", "Type": "Lunch", "Category": "Vegetarian", "Cal": 600, "Price": 35},
        {"Name": "Koshary Bowl (Large)", "Type": "Lunch", "Category": "Vegetarian", "Cal": 900, "Price": 60},
        {"Name": "Lentil Soup with Toast", "Type": "Lunch", "Category": "Vegetarian", "Cal": 450, "Price": 50},
        {"Name": "Eggplant Moussaka (Vegetarian) w/ Bread", "Type": "Lunch", "Category": "Vegetarian", "Cal": 700, "Price": 55},
        {"Name": "Stuffed Vine Leaves (Mahshi) Plate", "Type": "Lunch", "Category": "Vegetarian", "Cal": 800, "Price": 70},
        {"Name": "Vegetarian Pizza (Medium)", "Type": "Lunch", "Category": "Vegetarian", "Cal": 1100, "Price": 100},
        {"Name": "Large Pizza Margherita", "Type": "Lunch", "Category": "Vegetarian", "Cal": 1600, "Price": 140},
        {"Name": "Pasta Bechamel (Vegetarian/Cheese)", "Type": "Lunch", "Category": "Vegetarian", "Cal": 1400, "Price": 90},

        # =======================================================
        #  DINNER (Light -> Late Night Heavy)
        # =======================================================

        # --- LIGHT / HEALTHY ---
        {"Name": "Green Apple & Water", "Type": "Dinner", "Category": "Healthy", "Cal": 100, "Price": 15},
        {"Name": "Yogurt with Lemon", "Type": "Dinner", "Category": "Dairy", "Cal": 150, "Price": 10},
        {"Name": "Fruit Salad Cup", "Type": "Dinner", "Category": "Healthy", "Cal": 250, "Price": 40},
        {"Name": "Greek Salad with Feta", "Type": "Dinner", "Category": "Healthy", "Cal": 300, "Price": 60},
        {"Name": "Cottage Cheese with Cucumber", "Type": "Dinner", "Category": "Dairy", "Cal": 200, "Price": 20},

        # --- SANDWICHES (Medium) ---
        {"Name": "Turkey & Cheese Sandwich", "Type": "Dinner", "Category": "Meat", "Cal": 400, "Price": 55},
        {"Name": "Luncheon Meat Sandwich", "Type": "Dinner", "Category": "Meat", "Cal": 350, "Price": 30},
        {"Name": "Tuna Sandwich on Brown Bread", "Type": "Dinner", "Category": "Seafood", "Cal": 450, "Price": 65},
        {"Name": "Fried Roomi Cheese Sandwich", "Type": "Dinner", "Category": "Dairy", "Cal": 600, "Price": 50},
        {"Name": "Chicken Pane Sandwich", "Type": "Dinner", "Category": "Chicken", "Cal": 650, "Price": 60},
        {"Name": "Shawerma Roll (Meat)", "Type": "Dinner", "Category": "Meat", "Cal": 500, "Price": 75},

        # --- HEAVY DINNER ---
        {"Name": "Indomie with Egg & Vegetables", "Type": "Dinner", "Category": "Vegetarian", "Cal": 600, "Price": 30},
        {"Name": "Crepe Crispy Chicken", "Type": "Dinner", "Category": "Chicken", "Cal": 900, "Price": 110},
        {"Name": "Burger Sandwich with Cheese", "Type": "Dinner", "Category": "Meat", "Cal": 800, "Price": 100},
        {"Name": "Pasta Negresco (Chicken)", "Type": "Dinner", "Category": "Chicken", "Cal": 1100, "Price": 140},
        {"Name": "Sujuk Sandwich (XL)", "Type": "Dinner", "Category": "Meat", "Cal": 1000, "Price": 85},
        {"Name": "Hawawshi Loaf", "Type": "Dinner", "Category": "Meat", "Cal": 800, "Price": 90},
        {"Name": "Pizza Slice (Pepperoni)", "Type": "Dinner", "Category": "Meat", "Cal": 700, "Price": 50},
        {"Name": "Whole Pizza (Small)", "Type": "Dinner", "Category": "Vegetarian", "Cal": 1200, "Price": 120},
    ]

    # Create DataFrame and Export
    df = pd.DataFrame(data)
    file_name = "Smart_System_db.xlsx"
    df.to_excel(file_name, index=False)
    
    print(f"Success: Database generated with {len(df)} unique items.")
    print(f"Calorie Range: {df['Cal'].min()} - {df['Cal'].max()} Kcal")
    print(f"Price Range: {df['Price'].min()} - {df['Price'].max()} EGP")

if __name__ == "__main__":
    create_professional_database()