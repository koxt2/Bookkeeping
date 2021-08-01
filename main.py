# Import modules
import tkinter as tk
from tkinter import ttk
#from tkinter.constants import DISABLED
from ttkthemes import ThemedTk
import sqlite3

# Create root
root = ThemedTk(theme='aqua, breeze')
root.title("Bookkeeping")
root.geometry("1920x1080")

# Create database
conn = sqlite3.connect('Bookkeeping_Database.sqlite3')

# Create Tkinter Notebook
main_window = ttk.Notebook(root)
main_window.pack(fill="both", expand="yes")

class Menu_bar:
    def __init__(self):
        # Create a menu in root called top_menu and configure root to use top_menu
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        self.file_menu()
        self.customer_menu()
        self.vendor_menu()
        self.chart_of_accounts_menu()

    def file_menu(self):
        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff="false")
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=root.quit)

    def customer_menu(self):
        # Create customers menu
        customers_menu = tk.Menu(self.menu_bar, tearoff="false")
        self.menu_bar.add_cascade(label="Customers", menu=customers_menu)

        # Add menu items
        customers_menu.add_command(label="New Customer", command=customers.new_customer)
        customers_menu.add_command(label="Edit Customer", command=customers.edit_customer, state="disabled")
        customers_menu.add_command(label="Delete Customer", command=customers.delete_customer, state="disabled")

        # Enable certain items when a customer is selected in the treeview
        def enable_buttons(event):
            selected_customer = customers.customer_treeview.focus()
            values_customer = customers.customer_treeview.item(selected_customer, 'values')
            
            if values_customer:
                customers_menu.entryconfig("Edit Customer", state="normal")
                customers_menu.entryconfig("Delete Customer", state="normal")
            else:
                pass
        
        customers.customer_treeview.bind("<ButtonRelease-1>", enable_buttons)
        #customers.customer_treeview.bind("<Control-n>", customers.new_customer)

    def vendor_menu(self):
        # Create vendors menu
        vendors_menu = tk.Menu(self.menu_bar, tearoff="false")
        self.menu_bar.add_cascade(label="Vendors", menu=vendors_menu)

        # Add vendors menu items
        vendors_menu.add_command(label="New Vendor", command=vendors.new_vendor)
        vendors_menu.add_command(label="Edit Vendor", command=vendors.edit_vendor, state="disabled")
        vendors_menu.add_command(label="Delete Vendor", command=vendors.delete_vendor, state="disabled")

        # Enable certain items when a vendor is selected in the treeview
        def enable_buttons(event):
            selected_vendor = vendors.vendor_treeview.focus()
            values_vendor = vendors.vendor_treeview.item(selected_vendor, 'values')
            
            if values_vendor:
                vendors_menu.entryconfig("Edit Vendor", state="normal")
                vendors_menu.entryconfig("Delete Vendor", state="normal")
            else:
                pass
        
        vendors.vendor_treeview.bind("<ButtonRelease-1>", enable_buttons)

    def chart_of_accounts_menu(self):
        # Create chart of accounts menu
        chart_of_accounts_menu = tk.Menu(self.menu_bar, tearoff="false")
        self.menu_bar.add_cascade(label="Chart of Accounts", menu=chart_of_accounts_menu)

        # Add menu items
        chart_of_accounts_menu.add_command(label="New Account", command=chart_of_accounts.new_parent_account)
        chart_of_accounts_menu.add_command(label="New Child Account", command=chart_of_accounts.new_child_account, state="disabled")
        chart_of_accounts_menu.add_command(label="Edit Account", command=chart_of_accounts.edit_account, state="disabled")
        chart_of_accounts_menu.add_command(label="Delete Account", command=chart_of_accounts.delete_account, state="disabled")

        # Enable certain items if an account is selected in the treeview
        def enable_buttons(event):
            selected_account = chart_of_accounts.accounts_treeview.focus()
            values_accounts = chart_of_accounts.accounts_treeview.item(selected_account, 'values')

            if values_accounts[6] == "YES":
                chart_of_accounts_menu.entryconfig("New Child Account", state="disabled")
                chart_of_accounts_menu.entryconfig("Edit Account", state="normal")
                chart_of_accounts_menu.entryconfig("Delete Account", state="normal")
            elif values_accounts[6] == "NO":
                chart_of_accounts_menu.entryconfig("New Child Account", state="normal")
                chart_of_accounts_menu.entryconfig("Edit Account", state="normal")
                chart_of_accounts_menu.entryconfig("Delete Account", state="normal")
            else:
                pass

        chart_of_accounts.accounts_treeview.bind("<ButtonRelease-1>", enable_buttons)

class Right_click:
    def __init__(self):
        self.right_click_customer()
        

    def right_click_customer(self):
        right_click_customer = tk.Menu(customers.customer_treeview, tearoff="false")
        
        right_click_customer.add_command(label="New Customer")
        right_click_customer.add_command(label="Edit Customer", command=customers.edit_customer, state="disabled")
        right_click_customer.add_command(label="Delete Customer", command=customers.delete_customer, state="disabled")

        def popup(event):
            print("rik")
            right_click_customer.tk_popup(event.x_root, event.y_root)
        
        customers.customer_treeview.bind("<ButtonRelease-1>", popup)

    
        

class Customers:

    def __init__(self):
        
        def customer_database_table():
            # Connect to the database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Create the database table
            cur.execute("""CREATE TABLE IF NOT EXISTS customers (   
                id INTEGER, 
                name TEXT, 
                company TEXT, 
                street TEXT, 
                town TEXT, 
                city TEXT, 
                county TEXT, 
                postcode TEXT, 
                email TEXT, 
                phone INTEGER
                )""") 

            # Close connection
            conn.commit()
            conn.close() 

        def customer_tab():
            # Create the tab
            self.tab = tk.Frame(main_window)
            self.tab.pack(fill="both")
        
            # Add the tab to the notebook and provide a heading
            main_window.add(self.tab, text="Customers")
        
        def customer_ribbon():       
            # Make a frame for the buttons
            customer_ribbon_frame = tk.Frame(self.tab)
            customer_ribbon_frame.pack(fill="x", padx=10, pady=10)

            # Assign an image to each button
            self.new_customer_icon = tk.PhotoImage(file="images/new_contact.png")
            self.delete_customer_icon = tk.PhotoImage(file="images/delete_contact.png")
            self.edit_customer_icon = tk.PhotoImage(file="images/edit_contact.png")

            # Add the new contact button to the frame
            new_customer_contact_button = tk.Button(customer_ribbon_frame, image=self.new_customer_icon, command=self.new_customer)
            new_customer_contact_button.grid(padx=10, row=1, column=1)
            new_customer_contact_label = tk.Label(customer_ribbon_frame, text="Add New Customer")
            new_customer_contact_label.grid(padx=10, row=2, column=1)

            # Add the edit contact button to the frame
            self.edit_customer_contact_button = tk.Button(customer_ribbon_frame, image=self.edit_customer_icon, command=self.edit_customer)
            self.edit_customer_contact_button.grid(padx=10, row=1, column=2)
            self.edit_customer_contact_label = tk.Label(customer_ribbon_frame, text="Edit Customer")
            self.edit_customer_contact_label.grid(padx=10, row=2, column=2)

            # Add the delete contact button to the frame
            delete_customer_contact_button = tk.Button(customer_ribbon_frame, image=self.delete_customer_icon, command=self.delete_customer)
            delete_customer_contact_button.grid(padx=10, row=1, column=3)
            delete_customer_contact_label = tk.Label(customer_ribbon_frame, text="Delete Customer")
            delete_customer_contact_label.grid(padx=10, row=2, column=3)

        def customer_treeview():
            # Create a frame for the customer treeview
            self.customer_treeview_frame = tk.Frame(self.tab)
            self.customer_treeview_frame.pack(fill="both", padx=10, pady=10, expand="yes")

            # Add a scrollbar to the frame
            self.customer_treeview_frame_scroll = tk.Scrollbar(self.customer_treeview_frame)
            self.customer_treeview_frame_scroll.pack(side="right", fill="y") 

            # Add a Treeview to the frame
            self.customer_treeview = ttk.Treeview(self.customer_treeview_frame, yscrollcommand=self.customer_treeview_frame_scroll.set, selectmode="extended")
            self.customer_treeview.pack(fill="both", expand="y")     

            # Create the columns in the customer treeview
            self.customer_treeview['columns'] = (
                "ID", 
                "Name", 
                "Company", 
                "Street", 
                "Town", 
                "City", 
                "County", 
                "Postcode", 
                "Email", 
                "Phone"
                )
            
            # Provide the headings for each column
            self.customer_treeview.column("#0", width=0, stretch="no")
            self.customer_treeview.heading("#0", text="")
            
            self.customer_treeview.column("ID", width=0, stretch="no")
            self.customer_treeview.heading("ID", text="ID")
            
            self.customer_treeview.column("Name", minwidth=25, width=50) 
            self.customer_treeview.heading("Name", text="Name")   
            
            self.customer_treeview.column("Company", minwidth=25, width=50) 
            self.customer_treeview.heading("Company", text="Company")   
            
            self.customer_treeview.column("Street", minwidth=25, width=50) 
            self.customer_treeview.heading("Street", text="Street")   
            
            self.customer_treeview.column("Town", minwidth=25, width=50) 
            self.customer_treeview.heading("Town", text="Town")   
            
            self.customer_treeview.column("City", minwidth=25, width=50) 
            self.customer_treeview.heading("City", text="City")   
            
            self.customer_treeview.column("County", minwidth=25, width=50) 
            self.customer_treeview.heading("County", text="County")   
            
            self.customer_treeview.column("Postcode", minwidth=25, width=50) 
            self.customer_treeview.heading("Postcode", text="Postcode")   
            
            self.customer_treeview.column("Email", minwidth=25, width=50) 
            self.customer_treeview.heading("Email", text="Email")   
            
            self.customer_treeview.column("Phone", minwidth=25, width=50) 
            self.customer_treeview.heading("Phone", text="Phone") 

        customer_database_table()
        customer_tab()
        customer_ribbon()
        customer_treeview()
        self.populate_customer_tree()
        
    def populate_customer_tree(self):  
        # Connect to the database
        conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
        cur = conn.cursor()

        # Clear the treeview
        for record in self.customer_treeview.get_children():
            self.customer_treeview.delete(record)

        # Select the rowid and everything in the table and fetch 
        cur.execute("SELECT rowid, * FROM Customers")
        customer_record = cur.fetchall()    

        # For each row in the table, add the data to the Treeview columns
        global count
        count = 0
        for row in customer_record:
            self.customer_treeview.insert(parent='', index='end', iid=count, text='', values=(  
                row[0], # row_id
                row[2], # name
                row[3], # company
                row[4], # street
                row[5], # town
                row[6], # city
                row[7], # county
                row[8], # postcode
                row[9], # email
                row[10] # phone
                ))

            count+=1    

        # Close connection
        conn.commit()
        conn.close() 

    def new_customer(self):
        # Create a new window and make it sit on top all all other windows
        new_customer_window = tk.Toplevel()
        new_customer_window.title("Add New Customer")
        new_customer_window.attributes('-topmost', 'True')

        # Create a frame in the new window    
        new_customer_window_frame = tk.Frame(new_customer_window)
        new_customer_window_frame.pack(fill="both", expand=1, pady=10)      

        # Add the entry boxes to the frame
        new_id_label = tk.Label(new_customer_window_frame, text="ID")
        #new_id_label.grid(row=1, column=1, padx=10, pady=5)
        new_id_entry = tk.Entry(new_customer_window_frame, width=15)
        #new_id_entry.grid(row=1, column=2, padx=10, pady=5)

        new_name_label = tk.Label(new_customer_window_frame, text="Name")
        new_name_label.grid(row=2, column=1, padx=10, pady=5)
        new_name_entry = tk.Entry(new_customer_window_frame, width=15)
        new_name_entry.grid(row=2, column=2, padx=10, pady=5)

        new_company_label = tk.Label(new_customer_window_frame, text="Company")
        new_company_label.grid(row=3, column=1, padx=10, pady=5)
        new_company_entry = tk.Entry(new_customer_window_frame, width=15)
        new_company_entry.grid(row=3, column=2, padx=10, pady=5)

        new_street_label = tk.Label(new_customer_window_frame, text="Street")
        new_street_label.grid(row=4, column=1, padx=10, pady=5)
        new_street_entry = tk.Entry(new_customer_window_frame, width=15)
        new_street_entry.grid(row=4, column=2, padx=10, pady=5)

        new_town_label = tk.Label(new_customer_window_frame, text="Town")
        new_town_label.grid(row=5, column=1, padx=10, pady=5)
        new_town_entry = tk.Entry(new_customer_window_frame, width=15)
        new_town_entry.grid(row=5, column=2, padx=10, pady=5)

        new_city_label = tk.Label(new_customer_window_frame, text="City")
        new_city_label.grid(row=6, column=1, padx=10, pady=5)
        new_city_entry = tk.Entry(new_customer_window_frame, width=15)
        new_city_entry.grid(row=6, column=2, padx=10, pady=5)

        new_county_label = tk.Label(new_customer_window_frame, text="County")
        new_county_label.grid(row=7, column=1, padx=10, pady=5)
        new_county_entry = tk.Entry(new_customer_window_frame, width=15)
        new_county_entry.grid(row=7, column=2, padx=10, pady=5)

        new_postcode_label = tk.Label(new_customer_window_frame, text="Postcode")
        new_postcode_label.grid(row=8, column=1, padx=10, pady=5)
        new_postcode_entry = tk.Entry(new_customer_window_frame, width=15)
        new_postcode_entry.grid(row=8, column=2, padx=10, pady=5)

        new_email_label = tk.Label(new_customer_window_frame, text="Email")
        new_email_label.grid(row=9, column=1, padx=10, pady=5)
        new_email_entry = tk.Entry(new_customer_window_frame, width=15)
        new_email_entry.grid(row=9, column=2, padx=10, pady=5)

        new_phone_label = tk.Label(new_customer_window_frame, text="Phone")
        new_phone_label.grid(row=10, column=1, padx=10, pady=5)
        new_phone_entry = tk.Entry(new_customer_window_frame, width=15)
        new_phone_entry.grid(row=10, column=2, padx=10, pady=5)

        # Save contact button
        new_customer_window_save_button = tk.Button(new_customer_window_frame, text="Save", command=lambda:[save_new_customer(), new_customer_window.destroy()])
        new_customer_window_save_button.grid(row=11, column=1, padx=10, pady=5)

        # Close window button
        new_customer_window_close_button = tk.Button(new_customer_window_frame, text="Close", command=new_customer_window.destroy)
        new_customer_window_close_button.grid(row=11, column=2)

        def save_new_customer():

            # Connect to database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()
            
            # Make sure the new contact has at least a name. If not, provide a popup window asking for a name.
            if len(new_name_entry.get()) == 0:
                Message("A new customer must have a name")
                            
            # Add the pulled data to the database.
            else:
                cur.execute("""INSERT INTO Customers (  
                    id, 
                    name, 
                    company, 
                    street, 
                    town, 
                    city, 
                    county, 
                    postcode, 
                    email, 
                    phone
                    ) 
                    
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", [
                    
                    new_id_entry.get(), 
                    new_name_entry.get(), 
                    new_company_entry.get(), 
                    new_street_entry.get(), 
                    new_town_entry.get(), 
                    new_city_entry.get(), 
                    new_county_entry.get(), 
                    new_postcode_entry.get(), 
                    new_email_entry.get(), 
                    new_phone_entry.get()
                    ])   
            
            # Close connection
            conn.commit()
            conn.close() 

            # Re-populate the Treeview
            self.populate_customer_tree()   

            # Re-generate menu
            Menu_bar()       

    def edit_customer (self):
        # Select the Customer to edit
        selected_customer = self.customer_treeview.focus()
        values_customer = self.customer_treeview.item(selected_customer, 'values') 

        # If a customer is selected then open edit window
        if values_customer:    

            # Create update window
            edit_customer_window = tk.Toplevel()
            edit_customer_window.title("Update Contact")
            edit_customer_window.attributes('-topmost', 'True')

            # Create frame in the window    
            edit_customer_window_frame = tk.Frame(edit_customer_window)
            edit_customer_window_frame.pack(fill="both", expand=1, pady=10)      

            # Add the entry boxes
            edit_id_label = tk.Label(edit_customer_window_frame, text="ID")
            #edit_id_label.grid(row=1, column=1, padx=10, pady=5)
            edit_id_entry = tk.Entry(edit_customer_window_frame, width=15)
            #edit_id_entry.grid(row=1, column=2, padx=10, pady=5)

            edit_name_label = tk.Label(edit_customer_window_frame, text="Name")
            edit_name_label.grid(row=2, column=1, padx=10, pady=5)
            edit_name_entry = tk.Entry(edit_customer_window_frame, width=15)
            edit_name_entry.grid(row=2, column=2, padx=10, pady=5)

            edit_company_label = tk.Label(edit_customer_window_frame, text="Company")
            edit_company_label.grid(row=3, column=1, padx=10, pady=5)
            edit_company_entry = tk.Entry(edit_customer_window_frame, width=15)
            edit_company_entry.grid(row=3, column=2, padx=10, pady=5)

            edit_street_label = tk.Label(edit_customer_window_frame, text="Street")
            edit_street_label.grid(row=4, column=1, padx=10, pady=5)
            edit_street_entry = tk.Entry(edit_customer_window_frame, width=15)
            edit_street_entry.grid(row=4, column=2, padx=10, pady=5)

            edit_town_label = tk.Label(edit_customer_window_frame, text="Town")
            edit_town_label.grid(row=5, column=1, padx=10, pady=5)
            edit_town_entry = tk.Entry(edit_customer_window_frame, width=15)
            edit_town_entry.grid(row=5, column=2, padx=10, pady=5)

            edit_city_label = tk.Label(edit_customer_window_frame, text="City")
            edit_city_label.grid(row=6, column=1, padx=10, pady=5)
            edit_city_entry = tk.Entry(edit_customer_window_frame, width=15)
            edit_city_entry.grid(row=6, column=2, padx=10, pady=5)

            edit_county_label = tk.Label(edit_customer_window_frame, text="County")
            edit_county_label.grid(row=7, column=1, padx=10, pady=5)
            edit_county_entry = tk.Entry(edit_customer_window_frame, width=15)
            edit_county_entry.grid(row=7, column=2, padx=10, pady=5)

            edit_postcode_label = tk.Label(edit_customer_window_frame, text="Postcode")
            edit_postcode_label.grid(row=8, column=1, padx=10, pady=5)
            edit_postcode_entry = tk.Entry(edit_customer_window_frame, width=15)
            edit_postcode_entry.grid(row=8, column=2, padx=10, pady=5)

            edit_email_label = tk.Label(edit_customer_window_frame, text="Email")
            edit_email_label.grid(row=9, column=1, padx=10, pady=5)
            edit_email_entry = tk.Entry(edit_customer_window_frame, width=15)
            edit_email_entry.grid(row=9, column=2, padx=10, pady=5)

            edit_phone_label = tk.Label(edit_customer_window_frame, text="Phone")
            edit_phone_label.grid(row=10, column=1, padx=10, pady=5)
            edit_phone_entry = tk.Entry(edit_customer_window_frame, width=15)
            edit_phone_entry.grid(row=10, column=2, padx=10, pady=5)
            
            # Insert the pulled values from the database into the entry boxes
            edit_id_entry.insert(0, values_customer[0])
            edit_name_entry.insert(0, values_customer[1])
            edit_company_entry.insert(0, values_customer[2])
            edit_street_entry.insert(0, values_customer[3])
            edit_town_entry.insert(0, values_customer[4])
            edit_city_entry.insert(0, values_customer[5])
            edit_county_entry.insert(0, values_customer[6])
            edit_postcode_entry.insert(0, values_customer[7])
            edit_email_entry.insert(0, values_customer[8])
            edit_phone_entry.insert(0, values_customer[9])

            # Save contact button
            close_button = tk.Button(edit_customer_window_frame, text="Save", command=lambda:[update_customer()])
            close_button.grid(row=11, column=1, padx=10, pady=5)

            # Close window button
            close_button = tk.Button(edit_customer_window_frame, text="Cancel", command=edit_customer_window.destroy)
            close_button.grid(row=11, column=2)

        # If a customer isn't select tell the user to select one
        else:
            Message("Please select a contact to edit")

        def update_customer():
            # Connect to the database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Make sure the contact has a name. If not, show a pop-up window asking for a name
            if len(edit_name_entry.get()) == 0:
                Message("A customer must have a name")
            
            # If the contact has a name then update the database
            else:
                cur.execute("""UPDATE Customers SET 
                    name = :name, 
                    company = :company, 
                    street = :street, 
                    town = :town, 
                    city = :city, 
                    county = :county, 
                    postcode = :postcode, 
                    email = :email, 
                    phone = :phone 
                    
                    WHERE oid = :oid""",
                    
                    {
                    'name' : edit_name_entry.get(),
                    'company' : edit_company_entry.get(),
                    'street' : edit_street_entry.get(),
                    'town' : edit_town_entry.get(),
                    'city'  : edit_city_entry.get(),
                    'county' : edit_county_entry.get(),
                    'postcode' : edit_postcode_entry.get(),
                    'email' : edit_email_entry.get(),
                    'phone' : edit_phone_entry.get(),
                    'oid' : edit_id_entry.get(),
                    })

                # Close the window
                edit_customer_window.destroy()

            # Close connection
            conn.commit()
            conn.close() 

            # Re-populate the Treeview
            self.populate_customer_tree()

            # Re-generate menu
            Menu_bar()

    def delete_customer (self):
        # Connect to the database
        conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
        cur = conn.cursor()

        # Select the customer to delete
        selected_customer = self.customer_treeview.focus()
        values_customer = self.customer_treeview.item(selected_customer, 'values') 
        
        # If a customer is selected then delete from the database
        if values_customer:
            cur.execute("DELETE FROM Customers WHERE rowid = " + values_customer[0]) # row_id

        # If a customer isn't selected then tell the user to select one         
        else:
            Message("Please select a customer to delete")
   
        # Close connection
        conn.commit()
        conn.close() 

        # Re-populate the Treeview
        self.populate_customer_tree()

        # Re-generate menu
        Menu_bar()

class Vendors:

    def __init__(self):

        def vendor_database_table():
            
            # Connect to the database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Create the database table
            cur.execute("""CREATE TABLE IF NOT EXISTS vendors (   
                id INTEGER, 
                name TEXT, 
                company TEXT, 
                street TEXT, 
                town TEXT, 
                city TEXT, 
                county TEXT, 
                postcode TEXT, 
                email TEXT, 
                phone INTEGER
                )""") 

        def vendor_tab():
            # Create the tab
            self.tab = tk.Frame(main_window)
            self.tab.pack(fill="both")
        
            # Add the tab to the notebook and provide a heading
            main_window.add(self.tab, text="Vendors")
        
        def vendor_ribbon():
            # Make a frame for the buttons
            vendor_ribbon_frame = tk.Frame(self.tab)
            vendor_ribbon_frame.pack(fill="x", padx=10, pady=10)

            # Assign an image to each button
            self.new_vendor_icon = tk.PhotoImage(file="images/new_contact.png")
            self.delete_vendor_icon = tk.PhotoImage(file="images/delete_contact.png")
            self.edit_vendor_icon = tk.PhotoImage(file="images/edit_contact.png")

            # Add new contact button to the frame
            new_vendor_button = tk.Button(vendor_ribbon_frame, image=self.new_vendor_icon, command=self.new_vendor)
            new_vendor_button.grid(padx=10, row=1, column=1)
            new_vendor_label = tk.Label(vendor_ribbon_frame, text="Add New Vendor")
            new_vendor_label.grid(padx=10, row=2, column=1)

            # Add edit contact button to the frame
            edit_vendor_button = tk.Button(vendor_ribbon_frame, image=self.edit_vendor_icon, command=self.edit_vendor)
            edit_vendor_button.grid(padx=10, row=1, column=2)
            edit_vendor_label = tk.Label(vendor_ribbon_frame, text="Edit Vendor")
            edit_vendor_label.grid(padx=10, row=2, column=2)

            # Add delete contact button to the frame
            delete_vendor_button = tk.Button(vendor_ribbon_frame, image=self.delete_vendor_icon, command=self.delete_vendor)
            delete_vendor_button.grid(padx=10, row=1, column=3)
            delete_vendor_label = tk.Label(vendor_ribbon_frame, text="Delete Vendor")
            delete_vendor_label.grid(padx=10, row=2, column=3)
            
        def vendor_treeview():
            # Create a frame for the vendor treeview
            self.vendor_treeview_frame = tk.Frame(self.tab)
            self.vendor_treeview_frame.pack(fill="both", padx=10, pady=10, expand="yes")

            # Add a scrollbar to the frame
            self.vendor_treeview_frame_scroll = tk.Scrollbar(self.vendor_treeview_frame)
            self.vendor_treeview_frame_scroll.pack(side="right", fill="y") 

            # Add a Treeview to the frame
            self.vendor_treeview = ttk.Treeview(self.vendor_treeview_frame, yscrollcommand=self.vendor_treeview_frame_scroll.set, selectmode="extended")
            self.vendor_treeview.pack(fill="both", expand="yes")     

            # Create the columns in the vendor treeview
            self.vendor_treeview['columns'] = (
                "ID", 
                "Name", 
                "Company", 
                "Street", 
                "Town", 
                "City", 
                "County", 
                "Postcode", 
                "Email", 
                "Phone"
                )
            
            # Provide the headings for each column
            self.vendor_treeview.column("#0", width=0, stretch="no")
            self.vendor_treeview.heading("#0", text="")
            
            self.vendor_treeview.column("ID", width=0, stretch="no")
            self.vendor_treeview.heading("ID", text="ID")
            
            self.vendor_treeview.column("Name", minwidth=25, width=50) 
            self.vendor_treeview.heading("Name", text="Name")   
            
            self.vendor_treeview.column("Company", minwidth=25, width=50) 
            self.vendor_treeview.heading("Company", text="Company")   
            
            self.vendor_treeview.column("Street", minwidth=25, width=50) 
            self.vendor_treeview.heading("Street", text="Street")   
            
            self.vendor_treeview.column("Town", minwidth=25, width=50) 
            self.vendor_treeview.heading("Town", text="Town")   
            
            self.vendor_treeview.column("City", minwidth=25, width=50) 
            self.vendor_treeview.heading("City", text="City")   
            
            self.vendor_treeview.column("County", minwidth=25, width=50) 
            self.vendor_treeview.heading("County", text="County")   
            
            self.vendor_treeview.column("Postcode", minwidth=25, width=50) 
            self.vendor_treeview.heading("Postcode", text="Postcode")   
            
            self.vendor_treeview.column("Email", minwidth=25, width=50) 
            self.vendor_treeview.heading("Email", text="Email")   
            
            self.vendor_treeview.column("Phone", minwidth=25, width=50) 
            self.vendor_treeview.heading("Phone", text="Phone")  
        
        vendor_database_table()
        vendor_tab()
        vendor_ribbon()
        vendor_treeview()
        self.populate_vendor_tree()
        
    def populate_vendor_tree(self):  
        # Connect to the database
        conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
        cur = conn.cursor()

        # Clear the treeview
        for record in self.vendor_treeview.get_children():
            self.vendor_treeview.delete(record)

        # Select the rowid and everything in the table and fetch 
        cur.execute("SELECT rowid, * FROM vendors")
        vendor_record = cur.fetchall()    

        # For each row in the table, add the data to the Treeview columns
        global count
        count = 0
        for row in vendor_record:
            self.vendor_treeview.insert(parent='', index='end', iid=count, text='', values=(  
                row[0], # row_id
                row[2], # name
                row[3], # company
                row[4], # street
                row[5], # town
                row[6], # city
                row[7], # county
                row[8], # postcode
                row[9], # email
                row[10] # phone
                ))

            count+=1    

        # Close connection
        conn.commit()
        conn.close() 

    def new_vendor(self):
        # Create a new window and make it sit on top all all other windows
        new_vendor_window = tk.Toplevel()
        new_vendor_window.title("Add New Contact")
        new_vendor_window.attributes('-topmost', 'True')

        # Create a frame in the new window    
        new_vendor_window_frame = tk.Frame(new_vendor_window)
        new_vendor_window_frame.pack(fill="both", expand=1, pady=10)      

        # Add the entry boxes
        new_id_label = tk.Label(new_vendor_window_frame, text="ID")
        #new_id_label.grid(row=1, column=1, padx=10, pady=5)
        new_id_entry = tk.Entry(new_vendor_window_frame, width=15)
        #new_id_entry.grid(row=1, column=2, padx=10, pady=5)

        new_name_label = tk.Label(new_vendor_window_frame, text="Name")
        new_name_label.grid(row=2, column=1, padx=10, pady=5)
        new_name_entry = tk.Entry(new_vendor_window_frame, width=15)
        new_name_entry.grid(row=2, column=2, padx=10, pady=5)

        new_company_label = tk.Label(new_vendor_window_frame, text="Company")
        new_company_label.grid(row=3, column=1, padx=10, pady=5)
        new_company_entry = tk.Entry(new_vendor_window_frame, width=15)
        new_company_entry.grid(row=3, column=2, padx=10, pady=5)

        new_street_label = tk.Label(new_vendor_window_frame, text="Street")
        new_street_label.grid(row=4, column=1, padx=10, pady=5)
        new_street_entry = tk.Entry(new_vendor_window_frame, width=15)
        new_street_entry.grid(row=4, column=2, padx=10, pady=5)

        new_town_label = tk.Label(new_vendor_window_frame, text="Town")
        new_town_label.grid(row=5, column=1, padx=10, pady=5)
        new_town_entry = tk.Entry(new_vendor_window_frame, width=15)
        new_town_entry.grid(row=5, column=2, padx=10, pady=5)

        new_city_label = tk.Label(new_vendor_window_frame, text="City")
        new_city_label.grid(row=6, column=1, padx=10, pady=5)
        new_city_entry = tk.Entry(new_vendor_window_frame, width=15)
        new_city_entry.grid(row=6, column=2, padx=10, pady=5)

        new_county_label = tk.Label(new_vendor_window_frame, text="County")
        new_county_label.grid(row=7, column=1, padx=10, pady=5)
        new_county_entry = tk.Entry(new_vendor_window_frame, width=15)
        new_county_entry.grid(row=7, column=2, padx=10, pady=5)

        new_postcode_label = tk.Label(new_vendor_window_frame, text="Postcode")
        new_postcode_label.grid(row=8, column=1, padx=10, pady=5)
        new_postcode_entry = tk.Entry(new_vendor_window_frame, width=15)
        new_postcode_entry.grid(row=8, column=2, padx=10, pady=5)

        new_email_label = tk.Label(new_vendor_window_frame, text="Email")
        new_email_label.grid(row=9, column=1, padx=10, pady=5)
        new_email_entry = tk.Entry(new_vendor_window_frame, width=15)
        new_email_entry.grid(row=9, column=2, padx=10, pady=5)

        new_phone_label = tk.Label(new_vendor_window_frame, text="Phone")
        new_phone_label.grid(row=10, column=1, padx=10, pady=5)
        new_phone_entry = tk.Entry(new_vendor_window_frame, width=15)
        new_phone_entry.grid(row=10, column=2, padx=10, pady=5)

        # Save contact button
        new_vendor_window_save_button = tk.Button(new_vendor_window_frame, text="Save", command=lambda:[save_new_vendor()])
        new_vendor_window_save_button.grid(row=11, column=1, padx=10, pady=5)

        # Close window button
        new_vendor_window_close_button = tk.Button(new_vendor_window_frame, text="Cancel", command=new_vendor_window.destroy)
        new_vendor_window_close_button.grid(row=11, column=2)

        def save_new_vendor():
            """
            Takes the data from the entry boxes and adds it to the database table as a new contact
            """
            
            # Connect to database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()
            
            # Make sure the new contact has at least a name. If not, provide a popup window asking for a name.
            if len(new_name_entry.get()) == 0:
                Message("A new vendor must have a name")
            
            # Add the pulled data to the database.
            else:
                cur.execute("""INSERT INTO vendors (  
                    id, 
                    name, 
                    company, 
                    street, 
                    town, 
                    city, 
                    county, 
                    postcode, 
                    email, 
                    phone
                    ) 
                    
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", [
                    
                    new_id_entry.get(), 
                    new_name_entry.get(), 
                    new_company_entry.get(), 
                    new_street_entry.get(), 
                    new_town_entry.get(), 
                    new_city_entry.get(), 
                    new_county_entry.get(), 
                    new_postcode_entry.get(), 
                    new_email_entry.get(), 
                    new_phone_entry.get()
                    ])   
            
            # Close connection
            conn.commit()
            conn.close() 

            # Re-populate the Treeview
            self.populate_vendor_tree()

            # Re-generate menu
            Menu_bar()    

    def edit_vendor (self):
        # Select the vendor to edit
        selected_vendor = self.vendor_treeview.focus()
        values_vendor = self.vendor_treeview.item(selected_vendor, 'values') 

        # If a vendor is selected then open edit window
        if values_vendor:    

            # Create update window
            edit_vendor_window = tk.Toplevel()
            edit_vendor_window.title("Update Contact")
            edit_vendor_window.attributes('-topmost', 'True')

            # Create frame in the window    
            edit_vendor_window_frame = tk.Frame(edit_vendor_window)
            edit_vendor_window_frame.pack(fill="both", expand=1, pady=10)      

            # Add the entry boxes
            edit_id_label = tk.Label(edit_vendor_window_frame, text="ID")
            #edit_id_label.grid(row=1, column=1, padx=10, pady=5)
            edit_id_entry = tk.Entry(edit_vendor_window_frame, width=15)
            #edit_id_entry.grid(row=1, column=2, padx=10, pady=5)

            edit_name_label = tk.Label(edit_vendor_window_frame, text="Name")
            edit_name_label.grid(row=2, column=1, padx=10, pady=5)
            edit_name_entry = tk.Entry(edit_vendor_window_frame, width=15)
            edit_name_entry.grid(row=2, column=2, padx=10, pady=5)

            edit_company_label = tk.Label(edit_vendor_window_frame, text="Company")
            edit_company_label.grid(row=3, column=1, padx=10, pady=5)
            edit_company_entry = tk.Entry(edit_vendor_window_frame, width=15)
            edit_company_entry.grid(row=3, column=2, padx=10, pady=5)

            edit_street_label = tk.Label(edit_vendor_window_frame, text="Street")
            edit_street_label.grid(row=4, column=1, padx=10, pady=5)
            edit_street_entry = tk.Entry(edit_vendor_window_frame, width=15)
            edit_street_entry.grid(row=4, column=2, padx=10, pady=5)

            edit_town_label = tk.Label(edit_vendor_window_frame, text="Town")
            edit_town_label.grid(row=5, column=1, padx=10, pady=5)
            edit_town_entry = tk.Entry(edit_vendor_window_frame, width=15)
            edit_town_entry.grid(row=5, column=2, padx=10, pady=5)

            edit_city_label = tk.Label(edit_vendor_window_frame, text="City")
            edit_city_label.grid(row=6, column=1, padx=10, pady=5)
            edit_city_entry = tk.Entry(edit_vendor_window_frame, width=15)
            edit_city_entry.grid(row=6, column=2, padx=10, pady=5)

            edit_county_label = tk.Label(edit_vendor_window_frame, text="County")
            edit_county_label.grid(row=7, column=1, padx=10, pady=5)
            edit_county_entry = tk.Entry(edit_vendor_window_frame, width=15)
            edit_county_entry.grid(row=7, column=2, padx=10, pady=5)

            edit_postcode_label = tk.Label(edit_vendor_window_frame, text="Postcode")
            edit_postcode_label.grid(row=8, column=1, padx=10, pady=5)
            edit_postcode_entry = tk.Entry(edit_vendor_window_frame, width=15)
            edit_postcode_entry.grid(row=8, column=2, padx=10, pady=5)

            edit_email_label = tk.Label(edit_vendor_window_frame, text="Email")
            edit_email_label.grid(row=9, column=1, padx=10, pady=5)
            edit_email_entry = tk.Entry(edit_vendor_window_frame, width=15)
            edit_email_entry.grid(row=9, column=2, padx=10, pady=5)

            edit_phone_label = tk.Label(edit_vendor_window_frame, text="Phone")
            edit_phone_label.grid(row=10, column=1, padx=10, pady=5)
            edit_phone_entry = tk.Entry(edit_vendor_window_frame, width=15)
            edit_phone_entry.grid(row=10, column=2, padx=10, pady=5)
            
            # Insert the pulled values from the database into the entry boxes
            edit_id_entry.insert(0, values_vendor[0])
            edit_name_entry.insert(0, values_vendor[1])
            edit_company_entry.insert(0, values_vendor[2])
            edit_street_entry.insert(0, values_vendor[3])
            edit_town_entry.insert(0, values_vendor[4])
            edit_city_entry.insert(0, values_vendor[5])
            edit_county_entry.insert(0, values_vendor[6])
            edit_postcode_entry.insert(0, values_vendor[7])
            edit_email_entry.insert(0, values_vendor[8])
            edit_phone_entry.insert(0, values_vendor[9])

            # Save contact button
            close_button = tk.Button(edit_vendor_window_frame, text="Save", command=lambda:[update_vendor()])
            close_button.grid(row=11, column=1, padx=10, pady=5)

            # Close window button
            close_button = tk.Button(edit_vendor_window_frame, text="Cancel", command=edit_vendor_window.destroy)
            close_button.grid(row=11, column=2)

        # If a vendor isn't select tell the user to select one
        else:
            Message("Please select a vendor to edit")

        def update_vendor():
            """
            Take the data from the entry boxes and update the database of the row selected in the Treeview
            """
        
            # Connect to the database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Make sure the contact has at least a name. If not, show a pop-up window asking for a name
            if len(edit_name_entry.get()) == 0:
                Message("A vendor must have a name")
            
            # If the contact has a name then update the database
            else:
                cur.execute("""UPDATE vendors SET 
                    name = :name, 
                    company = :company, 
                    street = :street, 
                    town = :town, 
                    city = :city, 
                    county = :county, 
                    postcode = :postcode, 
                    email = :email, 
                    phone = :phone 
                    
                    WHERE oid = :oid""",
                    
                    {
                    'name' : edit_name_entry.get(),
                    'company' : edit_company_entry.get(),
                    'street' : edit_street_entry.get(),
                    'town' : edit_town_entry.get(),
                    'city'  : edit_city_entry.get(),
                    'county' : edit_county_entry.get(),
                    'postcode' : edit_postcode_entry.get(),
                    'email' : edit_email_entry.get(),
                    'phone' : edit_phone_entry.get(),
                    'oid' : edit_id_entry.get(),
                    })

                # Close the window
                edit_vendor_window.destroy()

            # Close connection
            conn.commit()
            conn.close() 

            # Re-populate the Treeview
            self.populate_vendor_tree()

            # Re-generate menu
            Menu_bar()    

    def delete_vendor (self):
        # Connect to the database
        conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
        cur = conn.cursor()

        # Select a vendor to delete
        selected_vendor = self.vendor_treeview.focus()
        values_vendor = self.vendor_treeview.item(selected_vendor, 'values') 
        
        # If a vendor is selected then delete from the database
        if values_vendor:
            cur.execute("DELETE FROM vendors WHERE rowid = " + values_vendor[0]) # row_id

        # If a vendor isn't selected then tell the user to select one         
        else:
            Message("Please select a contact to delete")
   
        # Close connection
        conn.commit()
        conn.close() 

        # Re-populate the Treeview
        self.populate_vendor_tree()

        # Re-generate menu
        Menu_bar()    

class Chart_of_accounts:
    
    def __init__(self):

        def accounts_database_table():
            # Connect to database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Create the database table
            cur.execute("""CREATE TABLE IF NOT EXISTS parent_accounts (
                id INTEGER, 
                account_number INTEGER, 
                account_name TEXT, 
                total FLOAT, 
                parent INTEGER, 
                child TEXT,
                type TEXT
                )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS child_accounts (
                id INTEGER, 
                account_number INTEGER, 
                account_name TEXT, 
                total FLOAT, 
                parent INTEGER, 
                child TEXT,
                type TEXT
                )""")

        def accounts_tab():
            # Create the tab
            self.tab = tk.Frame(main_window)
            self.tab.pack(fill="both", expand="yes")

            # Add the tab to the notebook and provide a heading
            main_window.add(self.tab, text="Chart of Accounts")
        
        def accounts_ribbon():
            # Make a frame for the ribbon
            accounts_ribbon_frame = tk.Frame(self.tab)
            accounts_ribbon_frame.pack(side="top", fill="x", padx=10, pady=10)
        
            # Assign an image to each button
            self.new_account_icon = tk.PhotoImage(file="images/new_account.png")
            self.new_child_account_icon = tk.PhotoImage(file="images/new_child_account.png")
            self.delete_account_icon = tk.PhotoImage(file="images/delete_account.png")
            self.edit_account_icon = tk.PhotoImage(file="images/edit_account.png")

            # Add "new account" button to the frame and give it a command
            new_account_button = tk.Button(accounts_ribbon_frame, image=self.new_account_icon, command=self.new_parent_account)
            new_account_button.grid(padx=10, row=1, column=1)

            new_account_label = tk.Label(accounts_ribbon_frame, text="Add New Account")
            new_account_label.grid(padx=10, row=2, column=1)

            # Add "add child account" button to the frame and give it a command  
            new_child_account_button = tk.Button(accounts_ribbon_frame, image=self.new_child_account_icon, command=self.new_child_account)
            new_child_account_button.grid(padx=10, row=1, column=2)
            new_child_account_label = tk.Label(accounts_ribbon_frame, text="Add Child Account")
            new_child_account_label.grid(padx=10, row=2, column=2)

            # Add "edit account" button to the frame and give it a command
            edit_account_button = tk.Button(accounts_ribbon_frame, image=self.edit_account_icon, command=self.edit_account)
            edit_account_button.grid(padx=10, row=1, column=3)

            edit_account_label = tk.Label(accounts_ribbon_frame, text="Edit Account")
            edit_account_label.grid(padx=10, row=2, column=3)

            # Add "delete account" button to the frame and give it a command
            delete_account_button = tk.Button(accounts_ribbon_frame, image=self.delete_account_icon, command=self.delete_account)
            delete_account_button.grid(padx=10, row=1, column=4)

            delete_account_label = tk.Label(accounts_ribbon_frame, text="Delete Account")
            delete_account_label.grid(padx=10, row=2, column=4)
            
        def accounts_treeview():
            # Create a frame for the Treeview
            self.accounts_treeview_frame = tk.Frame(self.tab)
            self.accounts_treeview_frame.pack(side="bottom", fill="both", padx=10, expand=1)

            # Create a scrollbar for the Treeview
            self.accounts_treeview_scroll = tk.Scrollbar(self.accounts_treeview_frame)
            self.accounts_treeview_scroll.pack(side="right", fill="y") 

            # Create the Treeview
            self.accounts_treeview = ttk.Treeview(self.accounts_treeview_frame, yscrollcommand=self.accounts_treeview_scroll.set, selectmode="extended") 
            self.accounts_treeview.pack(fill="both", expand="yes")        
            
            # Create the Treeview columns
            self.accounts_treeview['columns'] = ("ID", "Account Number", "Type", "Account Name", "Total", "Parent", "Child")
            
            # Create the Treeview column headings
            self.accounts_treeview.column("#0", minwidth=20, width=20, stretch="false")
            self.accounts_treeview.heading("#0", text="")

            self.accounts_treeview.column("ID", width=0, stretch="false") 
            self.accounts_treeview.heading("ID", text="ID")  
            
            self.accounts_treeview.column("Account Number", minwidth=100, width=100, stretch="false")
            self.accounts_treeview.heading("Account Number", text="Account Number")
            
            self.accounts_treeview.column("Type", minwidth=100, width=100, stretch="false")            
            self.accounts_treeview.heading("Type", text="Type")
            
            self.accounts_treeview.column("Account Name", minwidth=200, width=200, stretch="true")
            self.accounts_treeview.heading("Account Name", text="Account Name") 
            
            self.accounts_treeview.column("Total", minwidth=250, width=250, stretch="false")            
            self.accounts_treeview.heading("Total", text="Total")          
            
            self.accounts_treeview.column("Parent", width=0, stretch="false")          
            self.accounts_treeview.heading("Parent", text="Parent")    
            
            self.accounts_treeview.column("Child", width=0, stretch="false")           
            self.accounts_treeview.heading("Child", text="Child") 
        
        accounts_database_table()
        accounts_tab()
        accounts_ribbon()
        accounts_treeview()
        self.populate_accounts_tree()
             
    def populate_accounts_tree(self): 
        # Connect to database
        conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
        cur = conn.cursor()

        # Clear the treeview
        for record in self.accounts_treeview.get_children():
            self.accounts_treeview.delete(record)

        # Select the rowid and everything in the parent account table
        cur.execute("SELECT rowid, * FROM parent_accounts")
        parent_record = cur.fetchall()  
        
        # Select the rowid and everything in the child account table
        cur.execute("SELECT rowid, * FROM child_accounts")
        child_record = cur.fetchall()
        
        # For each row in the parent table, add the data to the Treeview columns
        for row in parent_record:
            self.accounts_treeview.insert(parent='', index='end', iid=row[2], text='', values=( # account_number
                row[0], # row_id
                row[2], # account_number
                row[7], # type
                row[3], # account_name
                row[4], # total
                row[2], # account_number
                row[6]  # child (yes/no)
                ))
        
        # For each row in the child table, add the data to the Treeview columns
        for row in child_record:
            self.accounts_treeview.insert(parent=row[5], index='end', iid=row[2], text='', values=( # parent - account_number
                row[0], # row_id
                row[2], # account_number
                row[7], # type
                row[3], # account_name
                row[4], # total
                row[5], # parent
                row[6]  # child (yes/no)
                ))

        # Close connection
        conn.commit()
        conn.close() 

    def new_parent_account(self):
        # Create window and add a frame
        new_account_window = tk.Toplevel()
        new_account_window.title("Add New Account")
        new_account_window.attributes('-topmost', 'True')
            
        new_account_window_frame = tk.Frame(new_account_window)
        new_account_window_frame.pack(fill="both", expand=1, pady=10)      

        # Create the entry boxes
        new_account_id_label = tk.Label(new_account_window_frame, text="ID")
        #new_account_id_label.grid(row=1, column=1, padx=10, pady=5)
        new_account_id_entry = tk.Entry(new_account_window_frame, width=15)
        #new_account_id_entry.grid(row=1, column=2, padx=10, pady=5)
        
        new_account_number_label = tk.Label(new_account_window_frame, text="Account Number")
        new_account_number_label.grid(row=2, column=1, padx=10, pady=5)
        new_account_number_entry = tk.Entry(new_account_window_frame, width=15)
        new_account_number_entry.grid(row=2, column=2, padx=10, pady=5)

        new_account_name_label = tk.Label(new_account_window_frame, text="Account Name")
        new_account_name_label.grid(row=3, column=1, padx=10, pady=5)
        new_account_name_entry = tk.Entry(new_account_window_frame, width=15)
        new_account_name_entry.grid(row=3, column=2, padx=10, pady=5)    

        new_account_total_label = tk.Label(new_account_window_frame, text="Total")
        #new_account_total_label.grid(row=4, column=1, padx=10, pady=5)
        new_account_total_entry = tk.Entry(new_account_window_frame, width=15)
        #new_account_total_entry.grid(row=4, column=2, padx=10, pady=5)       

        new_parent_account_label = tk.Label(new_account_window_frame, text="Parent")
        #new_parent_account_label.grid(row=5, column=1, padx=10, pady=5)
        new_parent_account_entry = tk.Entry(new_account_window_frame, width=15)
        #new_parent_account_entry.grid(row=5, column=2, padx=10, pady=5)     

        new_child_account_status_label = tk.Label(new_account_window_frame, text="Child Account?")
        #new_child_account_status_label.grid(row=6, column=1, padx=10, pady=5)
        new_child_account_status_entry = tk.Entry(new_account_window_frame, width=10)
        #new_child_account_status_entry.grid(row=6, column=2, padx=10, pady=5)

        new_account_type_label = tk.Label(new_account_window_frame, text="Type")
        new_account_type_label.grid(row=7, column=1, padx=10, pady=5)
        new_account_type_entry = ttk.Combobox(new_account_window_frame, values=["Bank", "Cash", "Income", "Expenses"], width=15)
        new_account_type_entry.set("Choose account type")
        new_account_type_entry.grid(row=7, column=2, padx=10, pady=5)

        # Save contact button
        close_button = tk.Button(new_account_window_frame, text="Save", command=lambda:[save_new_account()])
        close_button.grid(row=8, column=1)

        # Close window button
        self.close_button = tk.Button(new_account_window_frame, text="Close", command=new_account_window.destroy)
        self.close_button.grid(row=8, column=2)

        def save_new_account():   
            """
            Take the data from the enrty boxes in new_account_window and add to the database table as a new account
            """        

            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Pull the data from the entry boxes and store them in a list called 'inputted_data'. "NO" is to signal that this is not a child account.
            inputted_data = [new_account_number_entry.get(), new_account_name_entry.get(), "NO", new_account_type_entry.get()]

            # Make sure the new account has a number, andme and type. If not, provide a popup window asking for a number.    
            if len(new_account_number_entry.get()) == 0 or len(new_account_name_entry.get()) == 0 or (new_account_type_entry.get() != "Bank" and new_account_type_entry.get() != "Cash" and new_account_type_entry.get() != "Income" and new_account_type_entry.get() != "Expenses"):
                Message("A new account must have an Account Number, Name and account type")  

            # If the new account has a name, number and type insert into database...
            else:
                if len(new_account_number_entry.get() and new_account_name_entry.get()) != 0:
                    # Check to see if the account number is in use already. Attempt to make an account number list from the database using the account number in the entry box        
                    cur.execute("SELECT account_number FROM parent_accounts WHERE account_number = " + new_account_number_entry.get() + "")
                    parent_account_number_query = cur.fetchone()
                    cur.execute("SELECT account_number FROM child_accounts WHERE account_number = " + new_account_number_entry.get() + "")
                    child_account_number_query = cur.fetchone()

                    # If either of the lists exist (True), ie account number is in the database tell the user the account number is in use.
                    if parent_account_number_query or child_account_number_query:
                        Message("That account number is in use already")  

                    # If false, (account number in entry box isn't in database) insert entry box data into database
                    else:
                        # Insert entry box data into database and close connection.
                        cur.execute("""INSERT INTO parent_accounts (
                            account_number, 
                            account_name, 
                            total,
                            child, 
                            type
                            ) 
                            
                            VALUES 
                            
                            (?, ?, 0.00, ?, ?)""", inputted_data) 

            # Close connection
            conn.commit()
            conn.close() 

            # Repopulate the Treeview
            self.populate_accounts_tree()

            # Regenerate Menu bar
            Menu_bar()
        
    def new_child_account(self):
        # Select a parent account to create a child from...
        selected_account = self.accounts_treeview.focus()
        values_account = self.accounts_treeview.item(selected_account, 'values') 
        
        # If a parent account is selected open a window to enter the child account details into
        if values_account:
            # Create window and add a frame
            child_account_window = tk.Toplevel()
            child_account_window.title("Add Child Account")
            child_account_window.attributes('-topmost', 'True')
                
            child_account_window_frame = tk.Frame(child_account_window)
            child_account_window_frame.pack(fill="both", expand=1, pady=10)      

            # Create the entry boxes
            child_account_id_label = tk.Label(child_account_window_frame, text="ID")
            #child_account_id_label.grid(row=1, column=1, padx=10, pady=5)
            child_account_id_entry = tk.Entry(child_account_window_frame, width=15)
            #child_account_id_entry.grid(row=1, column=2, padx=10, pady=5)
            
            child_account_number_label = tk.Label(child_account_window_frame, text="Account Number")
            child_account_number_label.grid(row=2, column=1, padx=10, pady=5)
            child_account_number_entry = tk.Entry(child_account_window_frame, width=15)
            child_account_number_entry.grid(row=2, column=2, padx=10, pady=5)

            child_account_name_label = tk.Label(child_account_window_frame, text="Account Name")
            child_account_name_label.grid(row=3, column=1, padx=10, pady=5)
            child_account_name_entry = tk.Entry(child_account_window_frame, width=15)
            child_account_name_entry.grid(row=3, column=2, padx=10, pady=5)    

            child_account_total_label = tk.Label(child_account_window_frame, text="Total")
            #child_account_total_label.grid(row=4, column=1, padx=10, pady=5)
            child_account_total_entry = tk.Entry(child_account_window_frame, width=15)
            #child_account_total_entry.grid(row=4, column=2, padx=10, pady=5)       

            parent_account_number_label = tk.Label(child_account_window_frame, text="Parent")
            parent_account_number_label.grid(row=5, column=1, padx=10, pady=5)
            parent_account_number_entry = tk.Entry(child_account_window_frame, width=15)
            parent_account_number_entry.grid(row=5, column=2, padx=10, pady=5) 
            parent_account_number_entry.insert(0, values_account[1])  
            parent_account_number_entry.config(state='readonly')  

            child_account_status_label = tk.Label(child_account_window_frame, text="Child Account?")
            #child_account_status_label.grid(row=6, column=1, padx=10, pady=5)
            child_account_status_entry = tk.Entry(child_account_window_frame, width=15)
            #child_account_status_entry.grid(row=6, column=2, padx=10, pady=5)

            child_account_type_label = tk.Label(child_account_window_frame, text="Type")
            child_account_type_label.grid(row=7, column=1, padx=10, pady=5)
            child_account_type_entry = tk.Entry(child_account_window_frame, width=15)
            child_account_type_entry.grid(row=7, column=2, padx=10, pady=5)
            child_account_type_entry.insert(0, values_account[2])
            child_account_type_entry.config(state='readonly')

            # Save contact and close window
            save_button = tk.Button(child_account_window_frame, text="Save", command=lambda:[save_child_account(), child_account_window.destroy()])
            save_button.grid(row=8, column=1)

            # Close window
            close_button = tk.Button(child_account_window_frame, text="Close", command=child_account_window.destroy)
            close_button.grid(row=8, column=2)    

        # If a parent account hasn't been selected tell the user to choose a parent account. 
        else:
            Message("Please select a parent account first")
        
        def save_child_account():
            # Connect to the database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Pull the data from the entry boxes and store them in a list called 'inputted_data'. "YES" is to signal that it's a child account.
            inputted_data = [child_account_number_entry.get(), child_account_name_entry.get(), parent_account_number_entry.get(), "YES", child_account_type_entry.get()]

            # Make sure the new account has a number and name. If not, provide a popup window asking for a number and name. 
            if len(child_account_number_entry.get()) == 0 or len(child_account_name_entry.get()) == 0:
                Message("A new child account must have an Account Number and Name")    

            # If the new account has an account number, name and parent account then add to database
            elif len(child_account_number_entry.get() and child_account_name_entry.get()) != 0: 

                # Check to see if the account number is in use already. Attempt to make an account number list from the database using the account number in the entry box        
                cur.execute("SELECT account_number FROM parent_accounts WHERE account_number = " + child_account_number_entry.get() + "")
                parent_account_number_query = cur.fetchone()
                cur.execute("SELECT account_number FROM child_accounts WHERE account_number = " + child_account_number_entry.get() + "")
                child_account_number_query = cur.fetchone()

                # If the list exists (True), ie account number is in the database tell the user the account number is in use.
                if parent_account_number_query or child_account_number_query:
                    Message("That account number is already in use")

                # If the list doesn't exist (False), add the contents of the entry boxes to the database
                else:
                    # Add contents of entry boxes to the database
                    cur.execute("INSERT INTO child_accounts (account_number, account_name, total, parent, child, type) VALUES (?, ?, 0.00, ?, ?, ?)", inputted_data)

            # Close connection
            conn.commit()
            conn.close()    

            # Re-populate the Treeview      
            self.populate_accounts_tree()

            # Regenerate Menu bar
            Menu_bar()
    
    def edit_account(self):
        # Select an account to edit
        selected_account = self.accounts_treeview.focus()
        values_account = self.accounts_treeview.item(selected_account, 'values') 

        # If an account is selected open the new window and fill the entry boxes with the existing data
        if values_account:
            # Create window and add a frame
            edit_account_window = tk.Toplevel()
            edit_account_window.title("Edit Account")
            edit_account_window.attributes('-topmost', 'True')
                
            edit_account_window_frame = tk.Frame(edit_account_window)
            edit_account_window_frame.pack(fill="both", expand=1, pady=10)      

            # Create the entry boxes
            edit_account_id_label = tk.Label(edit_account_window_frame, text="ID")
            #edit_account_id_label.grid(row=1, column=1, padx=10, pady=5)
            edit_account_id_entry = tk.Entry(edit_account_window_frame, width=15)
            #edit_account_id_entry.grid(row=1, column=2, padx=10, pady=5)
            
            edit_account_number_label = tk.Label(edit_account_window_frame, text="Account Number")
            edit_account_number_label.grid(row=2, column=1, padx=10, pady=5)
            edit_account_number_entry = tk.Entry(edit_account_window_frame, width=15)
            edit_account_number_entry.grid(row=2, column=2, padx=10, pady=5)

            edit_account_name_label = tk.Label(edit_account_window_frame, text="Account Name")
            edit_account_name_label.grid(row=3, column=1, padx=10, pady=5)
            edit_account_name_entry = tk.Entry(edit_account_window_frame, width=15)
            edit_account_name_entry.grid(row=3, column=2, padx=10, pady=5)    

            edit_account_total_label = tk.Label(edit_account_window_frame, text="Total")
            #edit_account_total_label.grid(row=4, column=1, padx=10, pady=5)
            edit_account_total_entry = tk.Entry(edit_account_window_frame, width=15)
            #edit_account_total_entry.grid(row=4, column=2, padx=10, pady=5)       

            edit_parent_account_label = tk.Label(edit_account_window_frame, text="Parent")
            edit_parent_account_label.grid(row=5, column=1, padx=10, pady=5)
            edit_parent_account_entry = tk.Entry(edit_account_window_frame, width=15)
            edit_parent_account_entry.grid(row=5, column=2, padx=10, pady=5)     

            edit_child_account_status_label = tk.Label(edit_account_window_frame, text="Child Account?")
            #edit_child_account_status_label.grid(row=6, column=1, padx=10, pady=5)
            edit_child_account_status_entry = tk.Entry(edit_account_window_frame, width=15)
            #edit_child_account_status_entry.grid(row=6, column=2, padx=10, pady=5)

            edit_account_type_label = tk.Label(edit_account_window_frame, text="Type")
            edit_account_type_label.grid(row=7, column=1, padx=10, pady=5)
            edit_account_type_entry = tk.Entry(edit_account_window_frame, width=15)
            edit_account_type_entry.grid(row=7, column=2, padx=10, pady=5)

            # Insert the pulled values from the database into the entry boxes
            edit_account_id_entry.insert(0, values_account[0])
            edit_account_number_entry.insert(0,values_account[1])
            edit_account_name_entry.insert(0, values_account[3])
            edit_account_total_entry.insert(0, values_account[4])
            edit_parent_account_entry.insert(0, values_account[5])
            edit_child_account_status_entry.insert(0, values_account[6])
            edit_account_type_entry.insert(0, values_account[2])

            # Make parent account number and account type readonly
            edit_account_number_entry.config(state='readonly')
            edit_parent_account_entry.config(state='readonly')
            edit_account_type_entry.config(state='readonly')

            # Update account button
            save_button = tk.Button(edit_account_window_frame, text="Save", command=lambda:[save_account_edit(), edit_account_window.destroy()])
            save_button.grid(row=8, column=1)

            # Close window button
            close_button = tk.Button(edit_account_window_frame, text="Close", command=edit_account_window.destroy)
            close_button.grid(row=8, column=2)

        # If an account in the Treeview isn't selected tell the user to select and account
        else:
            Message("Please select an account to edit")
    
        def save_account_edit():
            #Connect to the database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Make sure the account has a name, if not show a popup window telling customer to set a name
            if len(edit_account_name_entry.get()) == 0:
                Message("An account must have a name and number")
            
            # If the account that is being enetered is not a child account insert the data from the entry boxes into the Accounts table
            elif values_account[6] == "NO":
                # Update the parent account
                cur.execute("""UPDATE parent_accounts SET 
                    account_name = :account_name 
                    
                    WHERE 
                    oid = :oid""", 
                    {
                    'account_name' : edit_account_name_entry.get(), 
                    'oid' : edit_account_id_entry.get()
                    })
            
            # If the account that is being enetered is a child account insert the data from the entry boxes into the Child_accounts tabel
            else:
                # Update the child account database
                cur.execute("""UPDATE child_accounts SET 
                account_number = :account_number, 
                account_name = :account_name 
                
                WHERE 
                
                oid = :oid""", 
                {
                'account_number' : edit_account_number_entry.get(), 
                'account_name' : edit_account_name_entry.get(), 
                'oid' : edit_account_id_entry.get()
                })

            # Close connection
            conn.commit()
            conn.close() 

            # Re-populate the Treeview               
            self.populate_accounts_tree()

            # Regenerate Menu bar
            Menu_bar()

    def delete_account(self):
        # Connect to the database
        conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
        cur = conn.cursor()

        # Select an account to delete
        selected_account = self.accounts_treeview.focus()
        values_account = self.accounts_treeview.item(selected_account, 'values') 
        
        # If an account has been selected in Treeview
        if values_account:
            # If the account that is being deleted is a child account...
            if values_account[6] == "YES":
                # Select rowid and everything in the Child_accounts table. 
                cur.execute("SELECT rowid, * FROM child_accounts")

                # Delete the database row(rowid) that has the same rowid as the one selected in the Treeview         
                cur.execute("DELETE FROM child_accounts WHERE rowid = " + str(values_account[0])) 
            # If the account that is being deleted is not a child account...
            elif values_account[6] == "NO":
                # Does the account number exist in the Child_accounts table named as a parent account (ie, does the account to be deleted have child accounts?)
                cur.execute("SELECT parent FROM child_accounts WHERE parent = " + values_account[1] + "")
                parent_to_child_query = cur.fetchone()

                #If true, show a popup window telling user to delete all child accoutns first
                if parent_to_child_query:
                    Message("Please delete all child accounts first")
                
                # If the account doesn't have children delete from database
                else:
                    # Select rowid and everything in table, fetch and save as 'record'
                    cur.execute("SELECT rowid, * FROM parent_accounts")
                    
                    # Delete the row whchi has the rowid from the entry box    
                    cur.execute("DELETE FROM parent_accounts WHERE rowid = " + str(values_account[0])) 

        else:
            Message("Please select an account to delete")
    
        # Close connection
        conn.commit()
        conn.close() 

        # Re-populate the Treeview
        self.populate_accounts_tree()

        # Regenerate Menu bar
        Menu_bar()

class Settings:

    def __init__(self):

        def settings_database_table():
            # Connect to the database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Create database table
            cur.execute('''CREATE TABLE IF NOT EXISTS settings (   
            company TEXT, 
            street TEXT, 
            town TEXT, 
            city TEXT, 
            county TEXT, 
            postcode TEXT, 
            email TEXT, 
            phone INTEGER
            )''')

            # Close connection
            conn.commit()
            conn.close() 

        def settings_tab():
            # Create the settings tab
            self.settings_tab = tk.Frame(main_window)
            self.settings_tab.pack(fill="both")

            # Add the tab to the Notebook
            main_window.add(self.settings_tab, text="Settings")         
        
        settings_database_table()
        settings_tab()
        self.business_address()

    def business_address(self):
        # Create the frame for the business address form
        business_address_frame = tk.LabelFrame(self.settings_tab, text="Business Address")
        business_address_frame.pack(fill="x", padx=10, pady=10)

        # Add the entry boxes
        company_label = tk.Label(business_address_frame, text="Company")
        company_label.grid(row=1, column=1, padx=10, pady=5)
        company_entry = tk.Entry(business_address_frame, width=15)
        company_entry.grid(row=1, column=2, padx=10, pady=5)
        
        street_label = tk.Label(business_address_frame, text="Street")
        street_label.grid(row=2, column=1, padx=10, pady=5)
        street_entry = tk.Entry(business_address_frame, width=15)
        street_entry.grid(row=2, column=2, padx=10, pady=5)
    
        town_label = tk.Label(business_address_frame, text="Town")
        town_label.grid(row=3, column=1, padx=10, pady=5)
        town_entry = tk.Entry(business_address_frame, width=15)
        town_entry.grid(row=3, column=2, padx=10, pady=5)
        
        city_label = tk.Label(business_address_frame, text="City")
        city_label.grid(row=4, column=1, padx=10, pady=5)
        city_entry = tk.Entry(business_address_frame, width=15)
        city_entry.grid(row=4, column=2, padx=10, pady=5)
        
        county_label = tk.Label(business_address_frame, text="County")
        county_label.grid(row=5, column=1, padx=10, pady=5)
        county_entry = tk.Entry(business_address_frame, width=15)
        county_entry.grid(row=5, column=2, padx=10, pady=5)
        
        postcode_label = tk.Label(business_address_frame, text="Postcode")
        postcode_label.grid(row=6, column=1, padx=10, pady=5)
        postcode_entry = tk.Entry(business_address_frame, width=15)
        postcode_entry.grid(row=6, column=2, padx=10, pady=5)
        
        email_label = tk.Label(business_address_frame, text="Email")
        email_label.grid(row=7, column=1, padx=10, pady=5)
        email_entry = tk.Entry(business_address_frame, width=15)
        email_entry.grid(row=7, column=2, padx=10, pady=5)
        
        phone_label = tk.Label(business_address_frame, text="Phone")
        phone_label.grid(row=8, column=1, padx=10, pady=5)
        phone_entry = tk.Entry(business_address_frame, width=15)
        phone_entry.grid(row=8, column=2, padx=10, pady=5)

        def populate_business_address():
            # Connect to the database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Clear the business address entry boxes 
            company_entry.delete(0, 'end')
            street_entry.delete(0, 'end')
            town_entry.delete(0, 'end')
            city_entry.delete(0, 'end')
            county_entry.delete(0, 'end')
            postcode_entry.delete(0, 'end')
            email_entry.delete(0, 'end')
            phone_entry.delete(0, 'end')

            # Create the business address table
            cur.execute('''CREATE TABLE IF NOT EXISTS business_address (   
            company TEXT, 
            street TEXT, 
            town TEXT, 
            city TEXT, 
            county TEXT, 
            postcode TEXT, 
            email TEXT, 
            phone INTEGER
            )''')

            # Select everything from the business address table
            cur.execute("SELECT * FROM business_address WHERE rowid = 1")
            values_business_address = cur.fetchall()  

            # Insert the data from the table into the business address entry boxes
            for record in values_business_address:
                company_entry.insert(0, record[0])  # company
                street_entry.insert(0, record[1])   # street
                town_entry.insert(0, record[2])     # town
                city_entry.insert(0, record[3])     # city
                county_entry.insert(0, record[4])   # county
                postcode_entry.insert(0, record[5]) # postcode
                email_entry.insert(0, record[6])    # email
                phone_entry.insert(0, record[7])    # phone
            
            # If there are data for the business address in the database create a button named update
            if values_business_address:
                update_business_address_button = tk.Button(business_address_frame, text="Update", command=lambda:[update_business_address()])
                update_business_address_button.grid(row=9, column=1, padx=10, pady=5)
            
            # If the table is empty then create a button named save
            else:
                save_business_address_button = tk.Button(business_address_frame, text="Save", command=lambda:[save_business_address(), populate_business_address()])
                save_business_address_button.grid(row=9, column=1, padx=10, pady=5)

            # Close connection
            conn.commit()
            conn.close() 

        def save_business_address():
                # Connect to the database
                conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
                cur = conn.cursor()

                # Get the data from the entry boxes
                inputted_data= [
                company_entry.get(), 
                street_entry.get(), 
                town_entry.get(), 
                city_entry.get(), 
                county_entry.get(), 
                postcode_entry.get(), 
                email_entry.get(), 
                phone_entry.get()
                ]

                # If a business name hasn't been entered pop up a window asking for a name 
                if len(company_entry.get()) == 0:
                    Message("Please enter at least a name")

                # Save the data from the entry boxes in the database
                else:
                    # Add data to the database
                    cur.execute('''INSERT INTO business_address (  
                        company, 
                        street, 
                        town, 
                        city, 
                        county, 
                        postcode, 
                        email, 
                        phone
                        ) 

                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
                        ,inputted_data)

                    # Display a message window telling the user the business address is saved
                    Message("Business address saved")

                # Close connection
                conn.commit()
                conn.close() 

        def update_business_address():
            # Connect to the database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # If a business name hasn't been entered pop up a window asking for a name
            if len(company_entry.get()) == 0:
                Message("Please enter at least a name")

            # If a business address name has been entered then save the data from the entry boxes in the database
            else:
                cur.execute("""UPDATE business_address SET 
                    company = :company, 
                    street = :street, 
                    town = :town, 
                    city = :city, 
                    county = :county, 
                    postcode = :postcode, 
                    email = :email, 
                    phone = :phone 

                    WHERE oid = :oid""",
                    {
                    'company' : company_entry.get(),
                    'street' : street_entry.get(),
                    'town' : town_entry.get(),
                    'city'  : city_entry.get(),
                    'county' : county_entry.get(),
                    'postcode' : postcode_entry.get(),
                    'email' : email_entry.get(),
                    'phone' : phone_entry.get(),
                    'oid' : 1
                    })

                # Display a message window telling the user the business address is updated
                Message("Business address updated")

            # Close connection
            conn.commit()
            conn.close() 
        
        populate_business_address()
        
class Message:

    def __init__(self, message):
        # Create a window
        message_window = tk.Toplevel()
        message_window.title("Message")
        message_window.attributes('-topmost', 'True')
        
        # Create a frame in the window
        message_window_frame = tk.Frame(message_window)
        message_window_frame.pack(fill="both", expand=1, pady=10)
        
        # Add a message to the frame
        message = tk.Label(message_window_frame, text=message)
        message.pack(side="left", padx=10, pady=10)
        
        # Create a close button
        close_button = tk.Button(message_window, text="Close", command=message_window.destroy)
        close_button.pack(side="bottom", pady=10)


customers = Customers()
vendors = Vendors()
chart_of_accounts = Chart_of_accounts()
Settings()
menu_bar = Menu_bar()
right_click = Right_click()

root.mainloop()
