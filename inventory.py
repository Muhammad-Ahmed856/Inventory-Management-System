import json
import os
import getpass
from datetime import datetime

def clear_screen():
    """Clear terminal screen in a cross-platform way."""
    try:
        # For Windows
        if os.name == 'nt':
            os.system('cls')
        # For macOS and Linux
        else:
            os.system('clear')
    except Exception:
        # Fallback: print some newlines if clearing fails
        print('\n' * 50)

class UserManager:
    def __init__(self, users_file="users.json"):
        self.users_file = users_file
        self.users = self.load_users()
        self.current_user = None
    
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as file:
                    return json.load(file)
            except (json.JSONDecodeError, Exception):
                return self.create_default_users()
        return self.create_default_users()
    
    def create_default_users(self):
        """Create default users if no user file exists"""
        default_users = {
            "admin": {
                "password": "admin123",
                "role": "admin",
                "full_name": "System Administrator"
            },
            "manager": {
                "password": "manager123",
                "role": "manager",
                "full_name": "Inventory Manager"
            },
            "staff": {
                "password": "staff123",
                "role": "staff",
                "full_name": "Store Staff"
            }
        }
        self.save_users(default_users)
        return default_users
    
    def save_users(self, users_data=None):
        """Save users to JSON file"""
        try:
            with open(self.users_file, 'w') as file:
                json.dump(users_data or self.users, file, indent=4)
            return True
        except Exception:
            return False
    
    def login(self, username, password):
        """Authenticate user"""
        if username in self.users and self.users[username]["password"] == password:
            self.current_user = {
                "username": username,
                "role": self.users[username]["role"],
                "full_name": self.users[username]["full_name"]
            }
            return True
        return False
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def get_current_user(self):
        """Get current logged in user info"""
        return self.current_user
    
    def has_permission(self, required_role):
        """Check if current user has required permission"""
        if not self.current_user:
            return False
        
        role_hierarchy = {"staff": 1, "manager": 2, "admin": 3}
        current_role_level = role_hierarchy.get(self.current_user["role"], 0)
        required_role_level = role_hierarchy.get(required_role, 0)
        
        return current_role_level >= required_role_level
    
    def change_password(self, username, new_password):
        """Change user password"""
        if username in self.users:
            self.users[username]["password"] = new_password
            return self.save_users()
        return False
    
    def get_users_by_role(self, role):
        """Get all users for a specific role"""
        role_users = []
        for username, user_data in self.users.items():
            if user_data["role"] == role:
                role_users.append({
                    "username": username,
                    "full_name": user_data["full_name"]
                })
        return role_users

class InventoryManagementSystem:
    def __init__(self, data_file="inventory_data.json"):
        self.data_file = data_file
        self.inventory = self.load_data()
        self.user_manager = UserManager()
    
    def press_enter_to_continue(self):
        """Utility function to wait for user to press Enter"""
        input("\nPress Enter to continue...")
    
    def load_data(self):
        """Load inventory data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                    # Convert categories list back to set
                    if "categories" in data and isinstance(data["categories"], list):
                        data["categories"] = set(data["categories"])
                    return data
            except (json.JSONDecodeError, Exception):
                return {"products": {}, "categories": set(), "transactions": []}
        return {"products": {}, "categories": set(), "transactions": []}
    
    def save_data(self):
        """Save inventory data to JSON file"""
        try:
            with open(self.data_file, 'w') as file:
                # Convert set to list for JSON serialization
                data_to_save = self.inventory.copy()
                data_to_save["categories"] = list(data_to_save["categories"])
                json.dump(data_to_save, file, indent=4)
            return True
        except Exception:
            return False
    
    def display_welcome_screen(self):
        """Display welcome screen with main options"""
        while True:
            clear_screen()
            print("\n" + "="*60)
            print("🌟 WELCOME TO INVENTORY MANAGEMENT SYSTEM 🌟")
            print("="*60)
            print("1. Login")
            print("2. Exit")
            print("-"*60)
            
            choice = input("Enter your choice (1-2): ").strip()
            
            if choice == '1':
                clear_screen()
                self.display_role_selection()
            elif choice == '2':
                print("\nThank you for using Inventory Management System! Goodbye! 👋")
                break
            else:
                print("❌ Invalid choice! Please enter 1 or 2.")
                self.press_enter_to_continue()
    
    def display_role_selection(self):
        """Display role selection screen"""
        while True:
            clear_screen()
            print("\n" + "="*50)
            print("👥 SELECT LOGIN TYPE")
            print("="*50)
            print("1. Login as Admin")
            print("2. Login as Manager") 
            print("3. Login as Staff")
            print("4. Back to Main Menu")
            print("-"*50)
            
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                if self.login_for_role("admin"):
                    self.show_main_menu()
                    break
            elif choice == '2':
                if self.login_for_role("manager"):
                    self.show_main_menu()
                    break
            elif choice == '3':
                if self.login_for_role("staff"):
                    self.show_main_menu()
                    break
            elif choice == '4':
                break
            else:
                print("❌ Invalid choice! Please enter a number between 1-4.")
                self.press_enter_to_continue()
    
    def login_for_role(self, role):
        """Handle login for specific role"""
        clear_screen()
        print(f"\n" + "="*40)
        print(f"🔐 LOGIN AS {role.upper()}")
        print("="*40)
        
        # Show available users for this role
        role_users = self.user_manager.get_users_by_role(role)
        if not role_users:
            print(f"❌ No {role} users found!")
            self.press_enter_to_continue()
            return False
        
        print(f"Available {role}s:")
        for user in role_users:
            print(f"  👤 {user['username']} - {user['full_name']}")
        print("-"*40)
        
        attempts = 0
        max_attempts = 3
        
        while attempts < max_attempts:
            username = input("Username: ").strip()
            password = getpass.getpass("Password: ")
            
            # Check if the username belongs to the selected role
            if username not in [user["username"] for user in role_users]:
                print(f"❌ {username} is not a {role} user!")
                attempts += 1
                continue
            
            if self.user_manager.login(username, password):
                current_user = self.user_manager.get_current_user()
                print(f"\n🎉 Welcome, {current_user['full_name']} ({current_user['role'].upper()})!")
                self.press_enter_to_continue()
                return True
            else:
                attempts += 1
                remaining_attempts = max_attempts - attempts
                if remaining_attempts > 0:
                    print(f"❌ Invalid password! {remaining_attempts} attempts remaining.")
                else:
                    print("❌ Too many failed login attempts. Please try again.")
                    self.press_enter_to_continue()
        
        return False
    
    def show_main_menu(self):
        """Display main menu after successful login"""
        while True:
            current_user = self.user_manager.get_current_user()
            clear_screen()
            user_display = f" ({current_user['username']} - {current_user['role']})" if current_user else ""
            
            print("\n" + "="*60)
            print(f"📦 INVENTORY MANAGEMENT SYSTEM{user_display}")
            print("="*60)
            
            # Display menu options based on user role
            role = current_user["role"]
            
            print("1.  View All Products")
            print("2.  Search Product")
            print("3.  View Product Details")
            print("4.  View Low Stock Products")
            
            if role in ["manager", "admin"]:
                print("5.  Add New Product")
                print("6.  View Transactions")
                print("7.  View Categories")
                print("8.  Inventory Value Report")
            
            if role == "admin":
                print("9.  Delete Product")
            
            print("10. Update Product Quantity")
            print("11. User Information")
            print("12. Change Password")
            print("13. Logout")
            print("-"*60)
            
            choice = input("Enter your choice: ").strip()
            
            # Staff permissions
            if choice == '1':
                self.display_all_products()
            elif choice == '2':
                self.search_product_menu()
            elif choice == '3':
                self.view_product_details_menu()
            elif choice == '4':
                self.display_low_stock()
            elif choice == '10':
                self.update_quantity_menu()
            elif choice == '11':
                self.display_user_info()
            elif choice == '12':
                self.change_user_password()
            elif choice == '13':
                if self.logout_menu():
                    break
            
            # Manager and Admin permissions
            elif choice == '5' and role in ["manager", "admin"]:
                self.add_product_menu()
            elif choice == '6' and role in ["manager", "admin"]:
                self.view_transactions_menu()
            elif choice == '7' and role in ["manager", "admin"]:
                self.display_categories()
            elif choice == '8' and role in ["manager", "admin"]:
                self.show_inventory_value_report()
            
            # Admin only permissions
            elif choice == '9' and role == "admin":
                self.delete_product_menu()
            
            else:
                print("❌ Invalid choice or insufficient permissions!")
            
            self.press_enter_to_continue()
    
    def display_product_selector(self, action="select"):
        """Display a paginated list of products for selection"""
        if not self.inventory["products"]:
            print("📭 No products in inventory!")
            return None
        
        products = list(self.inventory["products"].items())
        page_size = 10
        current_page = 0
        total_pages = (len(products) + page_size - 1) // page_size
        
        while True:
            clear_screen()
            print(f"\n" + "="*80)
            print(f"📋 SELECT PRODUCT TO {action.upper()} (Page {current_page + 1}/{total_pages})")
            print("="*80)
            print(f"{'#':<3} {'ID':<10} {'Name':<20} {'Category':<15} {'Price':<10} {'Quantity':<10} {'Status':<10}")
            print("="*80)
            
            start_idx = current_page * page_size
            end_idx = min(start_idx + page_size, len(products))
            
            for i in range(start_idx, end_idx):
                product_id, product = products[i]
                price = float(product.get("price", 0))
                quantity = int(product.get("quantity", 0))
                reorder_level = int(product.get("reorder_level", 0))
                status = "LOW STOCK" if quantity <= reorder_level else "OK"
                status_icon = "⚠️" if status == "LOW STOCK" else "✅"
                
                print(f"{i+1:<3} {product_id:<10} {product.get('name', 'N/A')[:20]:<20} "
                      f"{product.get('category', 'N/A')[:15]:<15} ${price:<9.2f} "
                      f"{quantity:<10} {status_icon} {status:<8}")
            
            print("="*80)
            print("\nNavigation:")
            print("• Enter product NUMBER (1, 2, 3...) to select")
            print("• Enter product ID directly")
            if current_page > 0:
                print("• 'P' for Previous page")
            if current_page < total_pages - 1:
                print("• 'N' for Next page")
            print("• 'S' to Search products")
            print("• 'B' to Go back")
            print("-"*40)
            
            user_input = input("Enter your choice: ").strip().upper()
            
            if user_input == 'B':
                return None
            elif user_input == 'P' and current_page > 0:
                current_page -= 1
            elif user_input == 'N' and current_page < total_pages - 1:
                current_page += 1
            elif user_input == 'S':
                search_term = input("Enter search term: ").strip()
                results = self.search_product(search_term)
                if results:
                    print(f"\n🔍 Search Results ({len(results)} found):")
                    print("-"*70)
                    for product_id, product in results:
                        print(f"ID: {product_id} | {product['name']} | ${product['price']} | Qty: {product['quantity']}")
                    print("-"*70)
                    self.press_enter_to_continue()
            else:
                # Check if input is a number (selection)
                if user_input.isdigit():
                    selection = int(user_input) - 1
                    if 0 <= selection < len(products):
                        return products[selection][0]  # Return product ID
                    else:
                        print("❌ Invalid selection number!")
                        self.press_enter_to_continue()
                else:
                    # Check if input is a direct product ID
                    if user_input in self.inventory["products"]:
                        return user_input
                    else:
                        print("❌ Product ID not found!")
                        self.press_enter_to_continue()
    
    def add_product_menu(self):
        """Menu for adding new product"""
        clear_screen()
        print("\n" + "="*20)
        print("➕ ADD NEW PRODUCT")
        print("="*20)
        product_id = input("Enter Product ID: ").strip()
        
        # Check if product ID already exists
        if product_id in self.inventory["products"]:
            print(f"❌ Product with ID '{product_id}' already exists!")
            print(f"📋 Existing product: {self.inventory['products'][product_id]['name']}")
            overwrite = input("Do you want to overwrite? (y/n): ").strip().lower()
            if overwrite != 'y':
                return
        
        name = input("Enter Product Name: ").strip()
        category = input("Enter Category: ").strip()
        
        try:
            price = float(input("Enter Price: "))
            quantity = int(input("Enter Quantity: "))
            reorder_level = int(input("Enter Reorder Level (default 5): ") or "5")
            self.add_product(product_id, name, category, price, quantity, reorder_level)
        except ValueError:
            print("❌ Invalid input! Please enter valid numbers for price and quantity.")
    
    def update_quantity_menu(self):
        """Menu for updating product quantity"""
        clear_screen()
        print("\n" + "="*25)
        print("📊 UPDATE PRODUCT QUANTITY")
        print("="*25)
        
        # Show product selector
        product_id = self.display_product_selector("UPDATE")
        if not product_id:
            return
        
        product = self.inventory["products"][product_id]
        print(f"\n📋 Selected Product: {product['name']} (ID: {product_id})")
        print(f"📦 Current Quantity: {product['quantity']}")
        print(f"💰 Price: ${product['price']}")
        print("-"*40)
        
        try:
            quantity_change = int(input("Enter quantity change (+ for add, - for deduct): "))
            reason = input("Enter reason for update: ").strip()
            self.update_product_quantity(product_id, quantity_change, reason)
        except ValueError:
            print("❌ Invalid input! Please enter a valid number for quantity.")
    
    def delete_product_menu(self):
        """Menu for deleting product"""
        clear_screen()
        print("\n" + "="*15)
        print("🗑️  DELETE PRODUCT")
        print("="*15)
        
        # Show product selector
        product_id = self.display_product_selector("DELETE")
        if not product_id:
            return
        
        product = self.inventory["products"][product_id]
        print(f"\n⚠️  PRODUCT TO DELETE:")
        print(f"🆔 ID: {product_id}")
        print(f"📛 Name: {product['name']}")
        print(f"📂 Category: {product['category']}")
        print(f"💰 Price: ${product['price']}")
        print(f"📦 Quantity: {product['quantity']}")
        print(f"📅 Added: {product['date_added']}")
        print("-"*40)
        
        confirm = input("❌ ARE YOU SURE YOU WANT TO DELETE THIS PRODUCT? (type 'DELETE' to confirm): ").strip().upper()
        if confirm == 'DELETE':
            self.delete_product(product_id)
        else:
            print("✅ Deletion cancelled.")
    
    def search_product_menu(self):
        """Menu for searching products"""
        clear_screen()
        print("\n" + "="*15)
        print("🔍 SEARCH PRODUCT")
        print("="*15)
        search_term = input("Enter product ID, name, or category to search: ").strip()
        results = self.search_product(search_term)
        
        if results:
            print(f"\n✅ Found {len(results)} product(s):")
            print("-"*80)
            print(f"{'ID':<10} {'Name':<20} {'Category':<15} {'Price':<10} {'Quantity':<10}")
            print("-"*80)
            for product_id, product in results:
                print(f"{product_id:<10} {product['name']:<20} {product['category']:<15} "
                      f"${product['price']:<9.2f} {product['quantity']:<10}")
        else:
            print("❌ No products found!")
    
    def view_product_details_menu(self):
        """Menu for viewing product details"""
        clear_screen()
        print("\n" + "="*20)
        print("📋 VIEW PRODUCT DETAILS")
        print("="*20)
        
        # Show product selector
        product_id = self.display_product_selector("VIEW DETAILS")
        if product_id:
            self.display_product_details(product_id)
    
    def view_transactions_menu(self):
        """Menu for viewing transactions"""
        try:
            limit = int(input("Enter number of transactions to display (default 10): ") or "10")
            clear_screen()
            self.display_transactions(limit)
        except ValueError:
            print("❌ Invalid input! Displaying last 10 transactions.")
            clear_screen()
            self.display_transactions()
    
    def show_inventory_value_report(self):
        """Display detailed inventory value report"""
        clear_screen()
        if not self.inventory["products"]:
            print("📭 No products in inventory!")
            return
        
        total_value = 0
        low_stock_value = 0
        out_of_stock_value = 0
        category_values = {}
        
        print("\n" + "="*80)
        print("💰 INVENTORY VALUE REPORT")
        print("="*80)
        
        # Calculate values
        for product_id, product in self.inventory["products"].items():
            product_value = product["price"] * product["quantity"]
            total_value += product_value
            
            # Categorize by stock status
            if product["quantity"] == 0:
                out_of_stock_value += product_value
            elif product["quantity"] <= product["reorder_level"]:
                low_stock_value += product_value
            
            # Calculate category-wise values
            category = product["category"]
            if category not in category_values:
                category_values[category] = 0
            category_values[category] += product_value
        
        # Display summary
        print(f"\n📊 INVENTORY SUMMARY:")
        print(f"   Total Products: {len(self.inventory['products'])}")
        print(f"   Total Categories: {len(self.inventory['categories'])}")
        print(f"   Total Inventory Value: ${total_value:,.2f}")
        
        # Display stock status breakdown
        print(f"\n📦 STOCK STATUS BREAKDOWN:")
        healthy_stock_value = total_value - low_stock_value - out_of_stock_value
        print(f"   ✅ Healthy Stock Value: ${healthy_stock_value:,.2f}")
        print(f"   ⚠️  Low Stock Value: ${low_stock_value:,.2f}")
        print(f"   ❌ Out of Stock Value: ${out_of_stock_value:,.2f}")
        
        # Display category-wise breakdown
        print(f"\n📂 CATEGORY-WISE BREAKDOWN:")
        for category, value in sorted(category_values.items(), key=lambda x: x[1], reverse=True):
            percentage = (value / total_value * 100) if total_value > 0 else 0
            print(f"   • {category}: ${value:,.2f} ({percentage:.1f}%)")
        
        # Display top 5 most valuable products
        print(f"\n🏆 TOP 5 MOST VALUABLE PRODUCTS:")
        sorted_products = sorted(
            self.inventory["products"].items(),
            key=lambda x: x[1]["price"] * x[1]["quantity"],
            reverse=True
        )[:5]
        
        for i, (product_id, product) in enumerate(sorted_products, 1):
            product_value = product["price"] * product["quantity"]
            status = "LOW STOCK" if product["quantity"] <= product["reorder_level"] else "OK"
            status_icon = "⚠️" if status == "LOW STOCK" else "✅"
            print(f"   {i}. {product['name']} (ID: {product_id}): ${product_value:,.2f} {status_icon}")
        
        print("="*80)
    
    def get_inventory_value(self):
        """Calculate total inventory value - used internally"""
        total_value = 0
        for product in self.inventory["products"].values():
            # Ensure both price and quantity are valid numbers
            try:
                price = float(product["price"])
                quantity = int(product["quantity"])
                total_value += price * quantity
            except (ValueError, KeyError):
                print(f"⚠️  Warning: Invalid data for product {product.get('name', 'Unknown')}")
                continue
        return total_value
    
    def logout_menu(self):
        """Handle logout"""
        confirm = input("Are you sure you want to logout? (y/n): ").strip().lower()
        if confirm == 'y':
            current_user = self.user_manager.get_current_user()
            self.user_manager.logout()
            print(f"👋 Goodbye, {current_user['full_name']}! You have been logged out.")
            self.press_enter_to_continue()
            return True
        return False

    # Core inventory management methods
    def add_product(self, product_id, name, category, price, quantity, reorder_level=5):
        """Add a new product to inventory"""
        if not self.user_manager.has_permission("manager"):
            print("❌ Permission denied! Manager role required to add products.")
            return False
        
        if product_id in self.inventory["products"]:
            print(f"⚠️  Overwriting existing product: {product_id}")
        
        self.inventory["products"][product_id] = {
            "name": name,
            "category": category,
            "price": float(price),
            "quantity": int(quantity),
            "reorder_level": int(reorder_level),
            "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "added_by": self.user_manager.get_current_user()["username"]
        }
        
        self.inventory["categories"].add(category)
        self.add_transaction("ADD", product_id, quantity, f"Added product: {name}")
        
        if self.save_data():
            print(f"✅ Product '{name}' added successfully!")
            return True
        else:
            print("❌ Error saving data!")
            return False
    
    def update_product_quantity(self, product_id, quantity_change, reason=""):
        """Update product quantity (positive for addition, negative for deduction)"""
        if not self.user_manager.has_permission("staff"):
            print("❌ Permission denied! Staff role required to update quantities.")
            return False
        
        if product_id not in self.inventory["products"]:
            print(f"❌ Product with ID {product_id} not found!")
            return False
        
        product = self.inventory["products"][product_id]
        new_quantity = product["quantity"] + quantity_change
        
        if new_quantity < 0:
            print(f"❌ Cannot update quantity! Available: {product['quantity']}, Requested: {-quantity_change}")
            return False
        
        product["quantity"] = new_quantity
        product["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        product["updated_by"] = self.user_manager.get_current_user()["username"]
        
        transaction_type = "RESTOCK" if quantity_change > 0 else "SALE"
        
        self.add_transaction(transaction_type, product_id, abs(quantity_change), reason)
        
        if self.save_data():
            action = "added" if quantity_change > 0 else "deducted"
            print(f"✅ Quantity {action} successfully! New quantity: {new_quantity}")
            
            # Check reorder level
            if new_quantity <= product["reorder_level"]:
                print(f"⚠️  LOW STOCK ALERT: {product['name']} needs restocking! (Current: {new_quantity})")
            
            return True
        else:
            print("❌ Error saving data!")
            return False
    
    def delete_product(self, product_id):
        """Remove a product from inventory"""
        if not self.user_manager.has_permission("admin"):
            print("❌ Permission denied! Admin role required to delete products.")
            return False
        
        if product_id not in self.inventory["products"]:
            print(f"❌ Product with ID {product_id} not found!")
            return False
        
        product_name = self.inventory["products"][product_id]["name"]
        del self.inventory["products"][product_id]
        
        self.add_transaction("DELETE", product_id, 0, f"Deleted product: {product_name}")
        
        if self.save_data():
            print(f"✅ Product '{product_name}' deleted successfully!")
            return True
        else:
            print("❌ Error saving data!")
            return False
    
    def search_product(self, search_term):
        """Search products by ID or name"""
        results = []
        search_term = search_term.lower()
        
        for product_id, product in self.inventory["products"].items():
            if (search_term in product_id.lower() or 
                search_term in product["name"].lower() or
                search_term in product["category"].lower()):
                results.append((product_id, product))
        
        return results
    
    def display_all_products(self):
        """Display all products in inventory"""
        clear_screen()
        if not self.inventory["products"]:
            print("📭 No products in inventory!")
            return
        
        print("\n" + "="*100)
        print("📦 ALL PRODUCTS")
        print("="*100)
        print(f"{'ID':<10} {'Name':<20} {'Category':<15} {'Price':<10} {'Quantity':<10} {'Value':<12} {'Status':<10}")
        print("="*100)
        
        for product_id, product in self.inventory["products"].items():
            # Use safe getters and defaults to avoid KeyError or type errors
            price = float(product.get("price", 0))
            quantity = int(product.get("quantity", 0))
            reorder_level = int(product.get("reorder_level", 0))
            product_value = price * quantity
            status = "LOW STOCK" if quantity <= reorder_level else "OK"
            status_icon = "⚠️" if status == "LOW STOCK" else "✅"
            name = product.get('name', 'N/A')[:20]
            category = product.get('category', 'N/A')[:15]
            print(f"{product_id:<10} {name:<20} {category:<15} "
                  f"${price:<9.2f} {quantity:<10} "
                  f"${product_value:<11.2f} {status_icon} {status:<8}")
        print("="*100)
    
    def display_low_stock(self):
        """Display products with low stock"""
        clear_screen()
        low_stock_products = []
        
        for product_id, product in self.inventory["products"].items():
            if product["quantity"] <= product["reorder_level"]:
                low_stock_products.append((product_id, product))
        
        if not low_stock_products:
            print("✅ No low stock products!")
            return
        
        print("\n" + "="*90)
        print("⚠️  LOW STOCK PRODUCTS")
        print("="*90)
        print(f"{'ID':<10} {'Name':<20} {'Category':<15} {'Price':<10} {'Quantity':<10} {'Value':<12} {'Reorder Level':<15}")
        print("="*90)
        
        for product_id, product in low_stock_products:
            price = float(product.get("price", 0))
            quantity = int(product.get("quantity", 0))
            reorder_level = int(product.get("reorder_level", 0))
            product_value = price * quantity
            name = product.get('name', 'N/A')[:20]
            category = product.get('category', 'N/A')[:15]
            print(f"{product_id:<10} {name:<20} {category:<15} "
                  f"${price:<9.2f} {quantity:<10} "
                  f"${product_value:<11.2f} {reorder_level:<15}")
        print("="*90)
    
    def add_transaction(self, transaction_type, product_id, quantity, notes=""):
        """Record a transaction"""
        current_user = self.user_manager.get_current_user()
        transaction = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": transaction_type,
            "product_id": product_id,
            "quantity": quantity,
            "notes": notes,
            "user": current_user["username"] if current_user else "system"
        }
        self.inventory["transactions"].append(transaction)
    
    def display_transactions(self, limit=10):
        """Display recent transactions"""
        if not self.user_manager.has_permission("manager"):
            print("❌ Permission denied! Manager role required to view transactions.")
            return
        
        transactions = self.inventory["transactions"][-limit:]
        
        if not transactions:
            print("📭 No transactions found!")
            return
        
        print("\n" + "="*120)
        print("📋 RECENT TRANSACTIONS")
        print("="*120)
        print(f"{'Timestamp':<20} {'Type':<10} {'Product ID':<12} {'Quantity':<10} {'User':<10} {'Notes':<40}")
        print("="*120)
        
        for transaction in reversed(transactions):
            timestamp = transaction.get('timestamp', '')
            ttype = transaction.get('type', '')
            pid = transaction.get('product_id', '')
            qty = transaction.get('quantity', '')
            user = transaction.get('user', '')
            notes = transaction.get('notes', '')
            print(f"{timestamp:<20} {ttype:<10} {pid:<12} {qty:<10} {user:<10} {notes:<40}")
        print("="*120)
    
    def display_categories(self):
        """Display all product categories"""
        clear_screen()
        categories = self.inventory["categories"]
        if not categories:
            print("📭 No categories found!")
            return
        
        print("\n📂 Product Categories:")
        print("-" * 20)
        for category in sorted(categories):
            print(f"• {category}")
    
    def display_product_details(self, product_id):
        """Display detailed information about a specific product"""
        clear_screen()
        if product_id not in self.inventory["products"]:
            print(f"❌ Product with ID {product_id} not found!")
            return

        product = self.inventory["products"][product_id]
        price = float(product.get("price", 0))
        quantity = int(product.get("quantity", 0))
        product_value = price * quantity

        print("\n" + "="*50)
        print("📋 PRODUCT DETAILS")
        print("="*50)
        print(f"🆔 ID: {product_id}")
        print(f"📛 Name: {product.get('name', 'N/A')}")
        print(f"📂 Category: {product.get('category', 'N/A')}")
        print(f"💰 Price: ${price:.2f}")
        print(f"📦 Quantity: {quantity}")
        print(f"💵 Total Value: ${product_value:.2f}")
        print(f"📊 Reorder Level: {product.get('reorder_level', 'N/A')}")
        print(f"📅 Date Added: {product.get('date_added', 'N/A')}")
        print(f"👤 Added By: {product.get('added_by', 'N/A')}")
        if 'last_updated' in product:
            print(f"🔄 Last Updated: {product.get('last_updated')}")
            print(f"👤 Updated By: {product.get('updated_by', 'N/A')}")
        status = "LOW STOCK" if quantity <= int(product.get('reorder_level', 0)) else "OK"
        status_icon = "⚠️" if status == "LOW STOCK" else "✅"
        print(f"📊 Status: {status_icon} {status}")
        print("="*50)
    
    def display_user_info(self):
        """Display current user information"""
        clear_screen()
        current_user = self.user_manager.get_current_user()
        if current_user:
            print("\n" + "="*30)
            print("👤 USER INFORMATION")
            print("="*30)
            print(f"📛 Username: {current_user['username']}")
            print(f"👤 Full Name: {current_user['full_name']}")
            print(f"🎯 Role: {current_user['role']}")
            print("="*30)
        else:
            print("❌ No user logged in!")
    
    def change_user_password(self):
        """Allow user to change their password"""
        clear_screen()
        current_user = self.user_manager.get_current_user()
        if not current_user:
            print("❌ No user logged in!")
            return False
        
        print(f"\n🔐 Change Password for {current_user['username']}")
        print("-" * 30)
        
        current_password = getpass.getpass("Current Password: ")
        if not self.user_manager.login(current_user['username'], current_password):
            print("❌ Current password is incorrect!")
            return False
        
        new_password = getpass.getpass("New Password: ")
        confirm_password = getpass.getpass("Confirm New Password: ")
        
        if new_password != confirm_password:
            print("❌ Passwords do not match!")
            return False
        
        if len(new_password) < 4:
            print("❌ Password must be at least 4 characters long!")
            return False
        
        if self.user_manager.change_password(current_user['username'], new_password):
            print("✅ Password changed successfully!")
            return True
        else:
            print("❌ Error changing password!")
            return False

def main():
    system = InventoryManagementSystem()
    system.display_welcome_screen()

if __name__ == "__main__":
    main()
