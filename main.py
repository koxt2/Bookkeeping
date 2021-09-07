# Import modules
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
import sqlite3
import tkcalendar as tkcal

# Create root
root = ThemedTk(theme='plastik')
root.title("Bookkeeping")
root.geometry("1920x1080")

# Create Tkinter Notebook
main_window = ttk.Notebook(root)
main_window.pack(fill="both", expand="yes")

# Create database
conn = sqlite3.connect('Bookkeeping_Database.sqlite3')

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

        # File menu items
        file_menu.add_command(label="Exit", command=root.quit)

    def customer_menu(self):
        # Create customers menu
        customers_menu = tk.Menu(self.menu_bar, tearoff="false")
        self.menu_bar.add_cascade(label="Customers", menu=customers_menu)

        # Customer menu items
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
        
        # Bind left clicking on a customer to enabling certain menu items
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
        vendors_menu.add_command(label="New Vendor Invoice", command=vendors.new_vendor_invoice, state="disabled")
        vendors_menu.add_command(label="Invoice History", command=vendors.invoice_history, state="disabled")

        # Enable certain items when a vendor is selected in the treeview
        def enable_buttons(event):
            selected_vendor = vendors.vendor_treeview.focus()
            values_vendor = vendors.vendor_treeview.item(selected_vendor, 'values')
            
            if values_vendor:
                vendors_menu.entryconfig("Edit Vendor", state="normal")
                vendors_menu.entryconfig("Delete Vendor", state="normal")
                vendors_menu.entryconfig("New Vendor Invoice", state="normal")
                vendors_menu.entryconfig("Invoice History", state="normal")
            else:
                pass
        
        # Bind left clicking on a vendor to enabling certain menu items
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

            if values_accounts:
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

            cur.execute("""CREATE TABLE IF NOT EXISTS customer_invoices (   
                id INTEGER,
                invoice_number TEXT,
                customer_rowid INTEGER, 
                date INTEGER, 
                description TEXT, 
                quantity FLOAT, 
                unit_price FLOAT, 
                total FLOAT,
                account TEXT
                )""")

            # Close connection
            conn.commit()
            conn.close() 

        def customer_tab():
            # Create the tab
            self.tab = ttk.Frame(main_window)
            self.tab.pack(fill="both")
        
            # Add the tab to the notebook and provide a heading
            main_window.add(self.tab, text="Customers")
        
        def customer_ribbon():       
            # Make a frame for the buttons
            customer_ribbon_frame = ttk.Frame(self.tab)
            customer_ribbon_frame.pack(fill="x", padx=10, pady=10)

            # Assign an image to each button
            self.new_customer_icon = tk.PhotoImage(file="images/new_contact.png")
            self.delete_customer_icon = tk.PhotoImage(file="images/delete_contact.png")
            self.edit_customer_icon = tk.PhotoImage(file="images/edit_contact.png")
            self.customer_invoice_icon = tk.PhotoImage(file="images/invoice.png")

            # Add the new contact button to the frame
            new_customer_contact_button = ttk.Button(customer_ribbon_frame, image=self.new_customer_icon, command=self.new_customer)
            new_customer_contact_button.grid(padx=10, row=1, column=1)
            new_customer_contact_label = ttk.Label(customer_ribbon_frame, text="Add New Customer")
            new_customer_contact_label.grid(padx=10, row=2, column=1)

            # Add the edit contact button to the frame
            self.edit_customer_contact_button = ttk.Button(customer_ribbon_frame, image=self.edit_customer_icon, command=self.edit_customer)
            self.edit_customer_contact_button.grid(padx=10, row=1, column=2)
            self.edit_customer_contact_label = ttk.Label(customer_ribbon_frame, text="Edit Customer")
            self.edit_customer_contact_label.grid(padx=10, row=2, column=2)

            # Add the delete contact button to the frame
            delete_customer_contact_button = ttk.Button(customer_ribbon_frame, image=self.delete_customer_icon, command=self.delete_customer)
            delete_customer_contact_button.grid(padx=10, row=1, column=3)
            delete_customer_contact_label = ttk.Label(customer_ribbon_frame, text="Delete Customer")
            delete_customer_contact_label.grid(padx=10, row=2, column=3)

            # Add invoice button icon to the frame
            new_customer_invoice_button = ttk.Button(customer_ribbon_frame, image=self.customer_invoice_icon, command=self.new_customer_invoice)
            new_customer_invoice_button.grid(padx=10, row=1, column=4)
            new_customer_invoice_label = ttk.Label(customer_ribbon_frame, text="Add Customer Invoice")
            new_customer_invoice_label.grid(padx=10, row=2, column=4)

        def customer_treeview():

            def right_click_customer(event):
                # Create a toggle to determine if a customer is selected
                selected_customer = customers.customer_treeview.focus()
                values_customer = customers.customer_treeview.item(selected_customer, 'values')

                # Create the menu
                right_click_customer = tk.Menu(customers.customer_treeview, tearoff="false")

                # Create the menu items
                right_click_customer.add_command(label="New Customer", command=customers.new_customer)
                right_click_customer.add_command(label="Edit Customer", command=customers.edit_customer, state="disabled")
                right_click_customer.add_command(label="Delete Customer", command=customers.delete_customer, state="disabled")                  

                # If a customer is selected change the state of menu items
                if values_customer:
                    right_click_customer.entryconfig("Edit Customer", state="normal")
                    right_click_customer.entryconfig("Delete Customer", state="normal")
                else:
                    pass

                # Pop-up the menu 
                right_click_customer.tk_popup(event.x_root, event.y_root)

            # Create a frame for the customer treeview
            self.customer_treeview_frame = ttk.Frame(self.tab)
            self.customer_treeview_frame.pack(fill="both", padx=10, pady=10, expand="yes")

            # Add a scrollbar to the frame
            self.customer_treeview_frame_scroll = ttk.Scrollbar(self.customer_treeview_frame)
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

            self.customer_treeview.bind("<Control-Button-1>", right_click_customer)
            self.customer_treeview.bind("<ButtonRelease-3>", right_click_customer)

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
        new_customer_window_frame = ttk.Frame(new_customer_window)
        new_customer_window_frame.pack(fill="both", expand=1)      

        # Add the entry boxes to the frame
        new_id_label = ttk.Label(new_customer_window_frame, text="ID")
        #new_id_label.grid(row=1, column=1, padx=10, pady=5)
        new_id_entry = ttk.Entry(new_customer_window_frame, width=15, background="white")
        #new_id_entry.grid(row=1, column=2, padx=10, pady=5)

        new_name_label = ttk.Label(new_customer_window_frame, text="Name")
        new_name_label.grid(row=2, column=1, padx=10, pady=5)
        new_name_entry = ttk.Entry(new_customer_window_frame, width=15, background="white")
        new_name_entry.grid(row=2, column=2, padx=10, pady=5)

        new_company_label = ttk.Label(new_customer_window_frame, text="Company")
        new_company_label.grid(row=3, column=1, padx=10, pady=5)
        new_company_entry = ttk.Entry(new_customer_window_frame, width=15, background="white")
        new_company_entry.grid(row=3, column=2, padx=10, pady=5)

        new_street_label = ttk.Label(new_customer_window_frame, text="Street")
        new_street_label.grid(row=4, column=1, padx=10, pady=5)
        new_street_entry = ttk.Entry(new_customer_window_frame, width=15, background="white")
        new_street_entry.grid(row=4, column=2, padx=10, pady=5)

        new_town_label = ttk.Label(new_customer_window_frame, text="Town")
        new_town_label.grid(row=5, column=1, padx=10, pady=5)
        new_town_entry = ttk.Entry(new_customer_window_frame, width=15, background="white")
        new_town_entry.grid(row=5, column=2, padx=10, pady=5)

        new_city_label = ttk.Label(new_customer_window_frame, text="City")
        new_city_label.grid(row=6, column=1, padx=10, pady=5)
        new_city_entry = ttk.Entry(new_customer_window_frame, width=15, background="white")
        new_city_entry.grid(row=6, column=2, padx=10, pady=5)

        new_county_label = ttk.Label(new_customer_window_frame, text="County")
        new_county_label.grid(row=7, column=1, padx=10, pady=5)
        new_county_entry = ttk.Entry(new_customer_window_frame, width=15, background="white")
        new_county_entry.grid(row=7, column=2, padx=10, pady=5)

        new_postcode_label = ttk.Label(new_customer_window_frame, text="Postcode")
        new_postcode_label.grid(row=8, column=1, padx=10, pady=5)
        new_postcode_entry = ttk.Entry(new_customer_window_frame, width=15, background="white")
        new_postcode_entry.grid(row=8, column=2, padx=10, pady=5)

        new_email_label = ttk.Label(new_customer_window_frame, text="Email")
        new_email_label.grid(row=9, column=1, padx=10, pady=5)
        new_email_entry = ttk.Entry(new_customer_window_frame, width=15, background="white")
        new_email_entry.grid(row=9, column=2, padx=10, pady=5)

        new_phone_label = ttk.Label(new_customer_window_frame, text="Phone")
        new_phone_label.grid(row=10, column=1, padx=10, pady=5)
        new_phone_entry = ttk.Entry(new_customer_window_frame, width=15, background="white")
        new_phone_entry.grid(row=10, column=2, padx=10, pady=5)

        # Save contact button
        new_customer_window_save_button = ttk.Button(new_customer_window_frame, text="Save", command=lambda:[save_new_customer(), new_customer_window.destroy()])
        new_customer_window_save_button.grid(row=11, column=1, padx=10, pady=5)

        # Close window button
        new_customer_window_close_button = ttk.Button(new_customer_window_frame, text="Close", command=new_customer_window.destroy)
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

            # Regenerate menu
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
            edit_customer_window_frame = ttk.Frame(edit_customer_window)
            edit_customer_window_frame.pack(fill="both", expand=1, pady=10)      

            # Add the entry boxes
            edit_id_label = ttk.Label(edit_customer_window_frame, text="ID")
            #edit_id_label.grid(row=1, column=1, padx=10, pady=5)
            edit_id_entry = ttk.Entry(edit_customer_window_frame, width=15, background="white")
            #edit_id_entry.grid(row=1, column=2, padx=10, pady=5)

            edit_name_label = ttk.Label(edit_customer_window_frame, text="Name")
            edit_name_label.grid(row=2, column=1, padx=10, pady=5)
            edit_name_entry = ttk.Entry(edit_customer_window_frame, width=15, background="white")
            edit_name_entry.grid(row=2, column=2, padx=10, pady=5)

            edit_company_label = ttk.Label(edit_customer_window_frame, text="Company")
            edit_company_label.grid(row=3, column=1, padx=10, pady=5)
            edit_company_entry = ttk.Entry(edit_customer_window_frame, width=15, background="white")
            edit_company_entry.grid(row=3, column=2, padx=10, pady=5)

            edit_street_label = ttk.Label(edit_customer_window_frame, text="Street")
            edit_street_label.grid(row=4, column=1, padx=10, pady=5)
            edit_street_entry = ttk.Entry(edit_customer_window_frame, width=15, background="white")
            edit_street_entry.grid(row=4, column=2, padx=10, pady=5)

            edit_town_label = ttk.Label(edit_customer_window_frame, text="Town")
            edit_town_label.grid(row=5, column=1, padx=10, pady=5)
            edit_town_entry = ttk.Entry(edit_customer_window_frame, width=15, background="white")
            edit_town_entry.grid(row=5, column=2, padx=10, pady=5)

            edit_city_label = ttk.Label(edit_customer_window_frame, text="City")
            edit_city_label.grid(row=6, column=1, padx=10, pady=5)
            edit_city_entry = ttk.Entry(edit_customer_window_frame, width=15, background="white")
            edit_city_entry.grid(row=6, column=2, padx=10, pady=5)

            edit_county_label = ttk.Label(edit_customer_window_frame, text="County")
            edit_county_label.grid(row=7, column=1, padx=10, pady=5)
            edit_county_entry = ttk.Entry(edit_customer_window_frame, width=15, background="white")
            edit_county_entry.grid(row=7, column=2, padx=10, pady=5)

            edit_postcode_label = ttk.Label(edit_customer_window_frame, text="Postcode")
            edit_postcode_label.grid(row=8, column=1, padx=10, pady=5)
            edit_postcode_entry = ttk.Entry(edit_customer_window_frame, width=15, background="white")
            edit_postcode_entry.grid(row=8, column=2, padx=10, pady=5)

            edit_email_label = ttk.Label(edit_customer_window_frame, text="Email")
            edit_email_label.grid(row=9, column=1, padx=10, pady=5)
            edit_email_entry = ttk.Entry(edit_customer_window_frame, width=15, background="white")
            edit_email_entry.grid(row=9, column=2, padx=10, pady=5)

            edit_phone_label = ttk.Label(edit_customer_window_frame, text="Phone")
            edit_phone_label.grid(row=10, column=1, padx=10, pady=5)
            edit_phone_entry = ttk.Entry(edit_customer_window_frame, width=15, background="white")
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
            close_button = ttk.Button(edit_customer_window_frame, text="Save", command=lambda:[update_customer()])
            close_button.grid(row=11, column=1, padx=10, pady=5)

            # Close window button
            close_button = ttk.Button(edit_customer_window_frame, text="Cancel", command=edit_customer_window.destroy)
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

            # Regenerate menu and right click
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

        # Regenerate menu
        Menu_bar()

    
    def new_customer_invoice(self):
        # Connect to database
        conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
        cur = conn.cursor()

        # Select a vendor
        selected_customer = self.customer_treeview.focus()
        values_customer = self.customer_treeview.item(selected_customer, 'values') 

        # If a customer is selected open a window with a form to enter invoice details into
        if values_customer:
            # Create the window
            customer_invoice_window = tk.Toplevel()
            customer_invoice_window.title("Add Customer Invoice")
            customer_invoice_window.geometry("1024x800")
            #customer_invoice_window.attributes('-topmost', 'true') 
            
            # Add the vendor address, date and invoice number to the invoice
            # Create a frame in the window for the supplier address
            customer_address_frame = ttk.Frame(customer_invoice_window)
            customer_address_frame.pack(fill="both", padx=10, pady=15)  

            # Add the supplier address to the invoice
            customer_name_label = ttk.Label(customer_address_frame, text=values_customer[1])
            customer_name_label.grid(sticky="w", row=1, column=1, padx=10)

            customer_company_label = ttk.Label(customer_address_frame, text=values_customer[2])
            customer_company_label.grid(sticky="w", row=2, column=1, padx=10)
    
            customer_street_label = ttk.Label(customer_address_frame, text=values_customer[3])
            customer_street_label.grid(sticky="w", row=3, column=1, padx=10)
    
            customer_town_label = ttk.Label(customer_address_frame, text=values_customer[4])
            customer_town_label.grid(sticky="w", row=4, column=1, padx=10)
    
            customer_city_label = ttk.Label(customer_address_frame, text=values_customer[5])
            customer_city_label.grid(sticky="w", row=5, column=1, padx=10)
    
            customer_county_label = ttk.Label(customer_address_frame, text=values_customer[6])
            customer_county_label.grid(sticky="w", row=6, column=1, padx=10)
    
            customer_postcode_label = ttk.Label(customer_address_frame, text=values_customer[7])
            customer_postcode_label.grid(sticky="w", row=7, column=1, padx=10)

            # Add the date to the invoice
            date_frame = ttk.Frame(customer_invoice_window)
            date_frame.pack(fill="both", padx=10, pady=15) 

            date_label = ttk.Label(date_frame, text="Date")
            date_label.grid(sticky="w", row=8, column=1, padx=10)
            cal = tkcal.DateEntry(date_frame, showweeknumbers=False, date_pattern='yyyy-mm-dd')
            cal.grid(sticky="w", row=9, column=1, padx=10)

            cal._top_cal.overrideredirect(False)

            # Add the invoice number
            invoice_number_frame = ttk.Frame(customer_invoice_window)
            invoice_number_frame.pack(fill="both", padx=10, pady=15) 

            customer_invoice_number_label = ttk.Label(invoice_number_frame, text="Invoice number")
            customer_invoice_number_label.grid(sticky="w", row=9, column=1, padx=10)
            customer_invoice_number_entry = ttk.Entry(invoice_number_frame, width=15, background="white")
            customer_invoice_number_entry.grid(sticky="w", row=10, column=1, padx=10, pady=2)

            # Add the Treeview to the invoice
            # Create a frame for the Treeview widget
            customer_invoice_treeview_frame = ttk.Frame(customer_invoice_window)
            customer_invoice_treeview_frame.pack(fill="both", expand=1, padx=10)

            # Add a scrollbar to the frame
            customer_invoice_treeview_scroll = ttk.Scrollbar(customer_invoice_treeview_frame)
            customer_invoice_treeview_scroll.pack(side="right", fill="y") 

            # Add the Treeview to the frame
            customer_invoice_treeview = ttk.Treeview(customer_invoice_treeview_frame, yscrollcommand=customer_invoice_treeview_scroll.set, selectmode="extended") 
            customer_invoice_treeview.pack(fill="both", expand="yes")  

            # Add the invoice total box            
            invoice_total_box_entry = ttk.Entry(customer_invoice_treeview_frame, width=15)
            invoice_total_box_entry.pack(side="right", padx=10, pady=5)
            invoice_total_box_entry.configure(state="readonly")
            invoice_total_box_label = ttk.Label(customer_invoice_treeview_frame, text="Total")
            invoice_total_box_label.pack(side="right", padx=0, pady=5)

            # Create the columns in the Treeview
            customer_invoice_treeview['columns'] = (
            "id",
            "Description", 
            "Account",
            "Quantity", 
            "Unit Price", 
            "Sub Total"
            )

            # Provide the headings for each column
            customer_invoice_treeview.column("#0", width=0, stretch="no")
            customer_invoice_treeview.heading("#0", text="")
            
            customer_invoice_treeview.column("id", width=0, stretch="no")
            customer_invoice_treeview.heading("id", text="id")

            customer_invoice_treeview.column("Description", minwidth=500) 
            customer_invoice_treeview.heading("Description", text="Description")   

            customer_invoice_treeview.column("Account", minwidth=100) 
            customer_invoice_treeview.heading("Account", text="Account") 
            
            customer_invoice_treeview.column("Quantity", minwidth=100) 
            customer_invoice_treeview.heading("Quantity", text="Quantity")   
            
            customer_invoice_treeview.column("Unit Price", minwidth=100) 
            customer_invoice_treeview.heading("Unit Price", text="Unit Price")   
            
            customer_invoice_treeview.column("Sub Total", minwidth=100) 
            customer_invoice_treeview.heading("Sub Total", text="Sub Total")
        
            # Add the invoice entry boxes and functional buttons to window
            # Create frame for the entry boxes and functional buttons
            customer_invoice_entry_frame = ttk.LabelFrame(customer_invoice_window, text="Add item to invoice")
            customer_invoice_entry_frame.pack(fill="both", padx=10, pady=10, expand=1)
            
            # Add the entry boxes
            # Create a list of the all the accounts for the account type Expenses
            cur.execute("SELECT account_name FROM child_accounts WHERE type = 'Sales'")
            accounts = cur.fetchall()
           
            expense_accounts = []
            for account in accounts:
                for record in account:
                    expense_accounts.append(record)

            invoice_item_id_label = ttk.Label(customer_invoice_entry_frame, text="id")
            #invoice_item_id_label.grid(row=1, column=1, padx=10)
            invoice_item_id_entry = ttk.Entry(customer_invoice_entry_frame, width=15)
            #invoice_item_id_entry.grid(row=2, column=1, padx=10)

            invoice_item_description_label = ttk.Label(customer_invoice_entry_frame, text="Description")
            invoice_item_description_label.grid(row=1, column=2, padx=10)
            invoice_item_description_entry = ttk.Entry(customer_invoice_entry_frame, width=15, background="white")
            invoice_item_description_entry.grid(row=2, column=2, padx=10)

            invoice_item_quantity_label = ttk.Label(customer_invoice_entry_frame, text="Quantity")
            invoice_item_quantity_label.grid(row=1, column=3, padx=10)
            invoice_item_quantity_entry = ttk.Entry(customer_invoice_entry_frame, width=15, background="white")
            invoice_item_quantity_entry.grid(row=2, column=3, padx=10)
            
            invoice_item_unit_price_label = ttk.Label(customer_invoice_entry_frame, text="Unit Price")
            invoice_item_unit_price_label.grid(row=1, column=4, padx=10)
            invoice_item_unit_price_entry = ttk.Entry(customer_invoice_entry_frame, width=15, background="white")
            invoice_item_unit_price_entry.grid(row=2, column=4, padx=10)

            invoice_item_account = ttk.Label(customer_invoice_entry_frame, text="Sales Account")
            invoice_item_account.grid(row=1, column=5, padx=10)
            invoice_item_account_combo = ttk.Combobox(customer_invoice_entry_frame, value=expense_accounts, width=15, background="white")
            invoice_item_account_combo.grid(row=2, column=5, padx=10)
            
            # Add the functional buttons
            self.add_to_invoice_button = ttk.Button(customer_invoice_entry_frame, text="Add to invoice", command=lambda:[add_invoice_item()])
            self.add_to_invoice_button.grid(row=3, column=2, padx=10) 
            
            self.edit_button = ttk.Button(customer_invoice_entry_frame, text="Edit selected item")
            self.edit_button.grid(row=3, column=3, padx=10) 
            
            self.delete_button = ttk.Button(customer_invoice_entry_frame, text="Delete item", command=lambda:[delete_invoice_item()])
            self.delete_button.grid(row=3, column=4, padx=10)

        else:
            Message("Please select a customer first")
        
        def add_invoice_item():
            # Connect to database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Make a list of all the invoice numbers in use already
            cur.execute("SELECT invoice_number FROM customer_invoices WHERE customer_rowid = " + values_customer[0])
            records = cur.fetchall()

            customer_invoices = []
            for record in records:
                for invoice in record:
                    customer_invoices.append(invoice)

            # Make a list of all the vendors entered into the ledger
            cur.execute("SELECT description FROM ledger WHERE customer_rowid = " + values_customer[0])
            records = cur.fetchall()   

            customer = []
            for record in records:
                for invoice in record:
                    customer.append(invoice)
            
            # Make a list of all the accounts entered into the ledger
            cur.execute("SELECT account FROM ledger WHERE customer_rowid = " + values_customer[0])
            records = cur.fetchall()

            ledger_accounts = []
            for record in records:
                for invoice in record:
                    ledger_accounts.append(invoice)

            # Check the invoice has an invoice number. If not tell the user to set one
            if len(customer_invoice_number_entry.get()) == 0:
                Message("Please set an invoice number")

            else:
                # Work out the sub_total of the item being added (quantity*unit price)
                sub_total = round(float(invoice_item_quantity_entry.get()) * float(invoice_item_unit_price_entry.get()),2)

                # Add the item to the invoice database
                cur.execute("""INSERT INTO customer_invoices (
                    id,
                    invoice_number,
                    customer_rowid, 
                    date, 
                    description, 
                    quantity, 
                    unit_price, 
                    total,
                    account
                    ) 

                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", [

                    invoice_item_id_entry.get(),
                    customer_invoice_number_entry.get(),
                    values_customer[0],
                    cal.get(),
                    invoice_item_description_entry.get(), 
                    invoice_item_quantity_entry.get(), 
                    invoice_item_unit_price_entry.get(), 
                    sub_total,
                    invoice_item_account_combo.get()
                    ])     

                # Add the item value to the child account database
                cur.execute('UPDATE child_accounts SET total = total+? WHERE account_name=?',(sub_total, invoice_item_account_combo.get(),))

                # Add the item value to the parent account database
                cur.execute('SELECT parent FROM child_accounts WHERE account_name=?', (invoice_item_account_combo.get(),))
                parent_account = cur.fetchall()
                cur.execute('UPDATE parent_accounts SET total = total+? WHERE account_number=?', (sub_total, parent_account[0][0]),)
                
                # Add the invoice item value to the Accounts Payable database
                cur.execute('UPDATE parent_accounts SET total = total+? WHERE account_name=?', (sub_total, 'Accounts Receivable (Debtors)'))

                # Add the invoice to the ledger
                # Add up all the items in an invoice to give a total invoice figure
                cur.execute("SELECT SUM(total) FROM customer_invoices WHERE invoice_number = " + customer_invoice_number_entry.get() + " AND customer_rowid = " + values_customer[0])
                self.figure = cur.fetchall()
                for figure in self.figure:
                    for value in figure:
                        total_figure = value
                
                if values_customer[1] in customer and customer_invoice_number_entry.get() in customer_invoices and invoice_item_account_combo.get() in ledger_accounts:
                    # Update accounts payable in ledger
                    cur.execute("""UPDATE ledger SET
                        customer_rowid = :customer_rowid, 
                        date = :date,
                        description = :description,
                        account = :account,
                        invoice_number = :invoice_number, 
                        
                        debit = :debit

                        WHERE invoice_number = :invoice_number AND customer_rowid = :customer_rowid AND account = :account""", 

                        {
                        'customer_rowid' :values_customer[0], 
                        'date' :cal.get(),
                        'description' :values_customer[1],
                        'account' :'Accounts Receivable (Debtors)',
                        'invoice_number' :customer_invoice_number_entry.get(),
                        
                        'debit' :total_figure
                        })

                    # Update child account in ledger
                    cur.execute("""UPDATE ledger SET
                        customer_rowid = :customer_rowid, 
                        date = :date,
                        description = :description,
                        account = :account,
                        invoice_number = :invoice_number, 
                        credit = credit+:credit 
                        

                        WHERE invoice_number = :invoice_number AND customer_rowid = :customer_rowid AND account = :account""", 

                        {
                        'customer_rowid' :values_customer[0], 
                        'date' :cal.get(),
                        'description' :values_customer[1],
                        'account' :invoice_item_account_combo.get(),
                        'invoice_number' :customer_invoice_number_entry.get(),
                        'credit' :sub_total
                        
                        })

                elif values_customer[1] in customer and customer_invoice_number_entry.get() in customer_invoices:
                    cur.execute("""UPDATE ledger SET
                        customer_rowid = :customer_rowid, 
                        date = :date,
                        description = :description,
                        account = :account,
                        invoice_number = :invoice_number, 
                        
                        debit = :debit

                        WHERE invoice_number = :invoice_number AND customer_rowid = :customer_rowid AND account = :account""", 

                        {
                        'customer_rowid' :values_customer[0], 
                        'date' :cal.get(),
                        'description' :values_customer[1],
                        'account' :'Accounts Receivable (Debtors)',
                        'invoice_number' :customer_invoice_number_entry.get(),
                        
                        'debit' :total_figure
                        })

                    cur.execute("""INSERT INTO ledger (
                            customer_rowid, 
                            date,
                            description,
                            account,
                            invoice_number, 
                            debit,
                            credit                            
                            )

                            VALUES (?, ?, ?, ?, ?, ?, ?)""",[

                            values_customer[0], 
                            cal.get(),
                            values_customer[1],
                            invoice_item_account_combo.get(),
                            customer_invoice_number_entry.get(),
                            '',
                            sub_total
                            ])
                    
                else:      
                    # Add Accounts Payable to ledger          
                    cur.execute("""INSERT INTO ledger (
                            customer_rowid, 
                            date,
                            description,
                            account,
                            invoice_number,  
                            debit,
                            credit
                            )

                            VALUES (?, ?, ?, ?, ?, ?, ?)""",[

                            values_customer[0], 
                            cal.get(),
                            values_customer[1],
                            'Accounts Receivable (Debtors)',
                            customer_invoice_number_entry.get(),
                            total_figure,
                            ''                            
                            ])

                    # Add child account to ledger
                    cur.execute("""INSERT INTO ledger (
                            customer_rowid, 
                            date,
                            description,
                            account,
                            invoice_number, 
                            debit,
                            credit                          
                            )

                            VALUES (?, ?, ?, ?, ?, ?, ?)""",[

                            values_customer[0], 
                            cal.get(),
                            values_customer[1],
                            invoice_item_account_combo.get(),
                            customer_invoice_number_entry.get(),
                            '',
                            sub_total
                            ])
                           
                # Re-populate the invoice treeview
                # Clear the entry boxes
                invoice_item_id_entry.delete(0,'end')
                invoice_item_description_entry.delete(0,'end')
                invoice_item_quantity_entry.delete(0,'end')
                invoice_item_unit_price_entry.delete(0,'end')
                invoice_item_account_combo.delete(0,'end')

                # Clear the treeview and total box
                for record in customer_invoice_treeview.get_children():
                    customer_invoice_treeview.delete(record)
                invoice_total_box_entry.delete(0,'end')

                # Get data from the database that has the same invoice number as the one given in the invoice
                cur.execute("SELECT rowid, * FROM customer_invoices WHERE invoice_number = " + customer_invoice_number_entry.get() + " AND customer_rowid = " + values_customer[0])
                record = cur.fetchall()    

                cur.execute("SELECT SUM(total) FROM customer_invoices WHERE invoice_number = " + customer_invoice_number_entry.get() + " AND customer_rowid = " + values_customer[0])
                self.figure = cur.fetchall()
                for figure in self.figure:
                    for value in figure:
                        total_figure = value 
                
                # Add the fetched data to the treeview and total box
                global count
                self.count = 0

                for row in record:
                    customer_invoice_treeview.insert(parent='', index='end', iid=self.count, text='', values=(row[0], row[5], row[9], row[6], row[7], row[8]))
                    self.count+=1   
                invoice_total_box_entry.configure(state="normal") 
                invoice_total_box_entry.delete(0,'end')    
                invoice_total_box_entry.insert(0, total_figure)
                invoice_total_box_entry.configure(state="readonly")
            


            # Close connection
            conn.commit()
            conn.close() 

            # Lock the date
            cal.grid_forget()
            date_entry = ttk.Entry(date_frame)
            date_entry.grid(sticky="w", row=9, column=1, padx=10)
            date_entry.insert(0, cal.get())
            date_entry.configure(state="readonly")

            # Lock the invoice number
            customer_invoice_number_entry.grid_forget()
            invoice_number = ttk.Entry(invoice_number_frame, width=15, background="white")
            invoice_number.grid(sticky="w", row=10, column=1, padx=10, pady=2)
            invoice_number.insert(0, customer_invoice_number_entry.get())
            invoice_number.configure(state="readonly")

            # Re-populate the Chart of Accounts Treeview      
            chart_of_accounts.populate_accounts_tree()

            # Re-populate ledger
            ledger.populate_ledger_tree()

        def delete_invoice_item():

            # Connect to the database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Make the selected item in Treeview the focus and make it a variable called 'selected'
            # Pull the values in 'selected' from the 'values' part of the database
            selected_item = customer_invoice_treeview.focus()
            invoice_item = customer_invoice_treeview.item(selected_item, 'values')
            
            # If an item is selected then delete it from the database
            if invoice_item:
                # Select the rowid and data from the database table and fetch everything
                cur.execute("SELECT rowid, * FROM customer_invoices")
                record = cur.fetchall()       

                # Work out the sub_total of the item being deleted (quantity*unit price)
                sub_total = invoice_item[5]
                
                # Delete the database row(rowid) that has the same rowid as the one selected in the Treeview
                cur.execute("DELETE FROM customer_invoices WHERE rowid = " + invoice_item[0])

                # Delete the item value from the parent account database
                cur.execute('UPDATE parent_accounts SET total=total-? WHERE account_name=?',(sub_total, "Accounts Receivable (Debtors)"))

                cur.execute("SELECT parent FROM child_accounts WHERE account_name=?", (invoice_item[2],))
                parent_account = cur.fetchall()
                cur.execute('UPDATE parent_accounts SET total=total-? WHERE account_number=?', (sub_total, parent_account[0][0]))
                
                # Delete the item value from the child account database
                cur.execute('UPDATE child_accounts SET total=total-? WHERE account_name=?',(sub_total, invoice_item[2]))

                # Delete the item value from the ledger
                cur.execute('UPDATE ledger SET debit=debit-? WHERE customer_rowid=? AND invoice_number=? AND account =?', (sub_total, values_customer[0], customer_invoice_number_entry.get(), "Accounts Receivable (Debtors)"))
                cur.execute('UPDATE ledger SET credit=credit-? WHERE customer_rowid=? AND invoice_number=? AND account =?', (sub_total, values_customer[0], customer_invoice_number_entry.get(), invoice_item[2]))

                # Re-populate the invoice treeview
                # Clear the treeview and total box
                for record in customer_invoice_treeview.get_children():
                    customer_invoice_treeview.delete(record)
                
                # Get data from the database that has the same invoice number as the one given in the invoice
                cur.execute("SELECT rowid, * FROM customer_invoices WHERE invoice_number = " + customer_invoice_number_entry.get() + " AND customer_rowid = " + values_customer[0])
                record = cur.fetchall()  

                # Add up all the items in an invoice to give a total invoice figure
                cur.execute("SELECT SUM(total) FROM customer_invoices WHERE invoice_number = " + customer_invoice_number_entry.get() + " AND customer_rowid = " + values_customer[0])
                self.figure = cur.fetchall()
                for figure in self.figure:
                    for value in figure:
                        total_figure = value 
                
                # Add the fetched data to the treeview and total box
                global count
                count = 0

                for row in record:
                    customer_invoice_treeview.insert(parent='', index='end', iid=count, text='', values=(row[0], row[5], row[9], row[6], row[7], row[8]))
                    count+=1        

                invoice_total_box_entry.configure(state="normal") 
                invoice_total_box_entry.delete(0,'end')
                invoice_total_box_entry.insert(0, total_figure)
                invoice_total_box_entry.configure(state="readonly") 
            
            else:
                Message("Please choose an item to delete")
            
            conn.commit()
            conn.close()

            # Re-populate the Chart of Accounts Treeview      
            chart_of_accounts.populate_accounts_tree()

            # Re-populate ledger treeview
            ledger.populate_ledger_tree()

class Vendors:

    def __init__(self):

        def vendor_database_table():
            
            # Connect to the database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Create the database tables
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

            cur.execute("""CREATE TABLE IF NOT EXISTS vendor_invoices (   
                id INTEGER,
                invoice_number TEXT,
                vendor_rowid INTEGER, 
                date INTEGER, 
                description TEXT, 
                quantity FLOAT, 
                unit_price FLOAT, 
                total FLOAT,
                account TEXT
                )""")
        
            # Close connection
            conn.commit()
            conn.close() 

        def vendor_tab():
            # Create the tab
            self.tab = ttk.Frame(main_window)
            self.tab.pack(fill="both")
        
            # Add the tab to the notebook and provide a heading
            main_window.add(self.tab, text="Vendors")
        
        def vendor_ribbon():
            # Make a frame for the buttons
            vendor_ribbon_frame = ttk.Frame(self.tab)
            vendor_ribbon_frame.pack(fill="x", padx=10, pady=10)

            # Assign an image to each button
            self.new_vendor_icon = tk.PhotoImage(file="images/new_contact.png")
            self.delete_vendor_icon = tk.PhotoImage(file="images/delete_contact.png")
            self.edit_vendor_icon = tk.PhotoImage(file="images/edit_contact.png")
            self.vendor_invoice_icon = tk.PhotoImage(file="images/invoice.png")
            self.vendor_invoice_history_icon = tk.PhotoImage(file="images/invoice_history.png")

            # Add new contact button to the frame
            new_vendor_button = ttk.Button(vendor_ribbon_frame, image=self.new_vendor_icon, command=self.new_vendor)
            new_vendor_button.grid(padx=10, row=1, column=1)
            new_vendor_label = ttk.Label(vendor_ribbon_frame, text="Add New Vendor")
            new_vendor_label.grid(padx=10, row=2, column=1)

            # Add edit contact button to the frame
            edit_vendor_button = ttk.Button(vendor_ribbon_frame, image=self.edit_vendor_icon, command=self.edit_vendor)
            edit_vendor_button.grid(padx=10, row=1, column=2)
            edit_vendor_label = ttk.Label(vendor_ribbon_frame, text="Edit Vendor")
            edit_vendor_label.grid(padx=10, row=2, column=2)

            # Add delete contact button to the frame
            delete_vendor_button = ttk.Button(vendor_ribbon_frame, image=self.delete_vendor_icon, command=self.delete_vendor)
            delete_vendor_button.grid(padx=10, row=1, column=3)
            delete_vendor_label = ttk.Label(vendor_ribbon_frame, text="Delete Vendor")
            delete_vendor_label.grid(padx=10, row=2, column=3)

            # Add invoice button icon to the frame
            new_vendor_invoice_button = ttk.Button(vendor_ribbon_frame, image=self.vendor_invoice_icon, command=self.new_vendor_invoice)
            new_vendor_invoice_button.grid(padx=10, row=1, column=4)
            new_vendor_invoice_label = ttk.Label(vendor_ribbon_frame, text="Add Vendor Invoice")
            new_vendor_invoice_label.grid(padx=10, row=2, column=4)

            # View invoices icon
            vendor_invoice_history_button = ttk.Button(vendor_ribbon_frame, image=self.vendor_invoice_history_icon, command=self.invoice_history)
            vendor_invoice_history_button.grid(padx=10, row=1, column=5)
            vendor_invoice_history_button.bind("<ButtonRelease-1>", self.invoice_history)
            vendor_invoice_history_label = ttk.Label(vendor_ribbon_frame, text="Invoice History")
            vendor_invoice_history_label.grid(padx=10, row=2, column=5)
            
        def vendor_treeview():
            
            def vendor_double_clicked(event):
                # Call the method
                vendors.invoice_history()

            def right_click_vendor(event):
                # Create a toggle to determine if a vendor is selected
                selected_vendor = vendors.vendor_treeview.focus()
                values_vendor = vendors.vendor_treeview.item(selected_vendor, 'values')

                # Create the menu
                right_click_vendor = tk.Menu(vendors.vendor_treeview, tearoff="false")

                # Create the menu items
                right_click_vendor.add_command(label="New Vendor", command=vendors.new_vendor, state="normal")
                right_click_vendor.add_command(label="Edit Vendor", command=vendors.edit_vendor, state="disabled")
                right_click_vendor.add_command(label="Delete Vendor", command=vendors.delete_vendor, state="disabled")
                right_click_vendor.add_separator()
                right_click_vendor.add_command(label="New Vendor Invoice", command=vendors.new_vendor_invoice, state="disabled")
                right_click_vendor.add_command(label="Invoice History", command=vendors.invoice_history, state="disabled")

                # If a vendor is selected change the state of menu items
                if values_vendor:
                    right_click_vendor.entryconfig("Edit Vendor", state="normal")
                    right_click_vendor.entryconfig("Delete Vendor", state="normal")
                    right_click_vendor.entryconfig("New Vendor Invoice", state="normal")
                    right_click_vendor.entryconfig("Invoice History", state="normal")
                else:
                    pass
                
                # Pop-up the menu 
                right_click_vendor.tk_popup(event.x_root, event.y_root)

            # Create a frame for the vendor treeview
            self.vendor_treeview_frame = ttk.Frame(self.tab)
            self.vendor_treeview_frame.pack(fill="both", padx=10, pady=10, expand="yes")

            # Add a scrollbar to the frame
            self.vendor_treeview_frame_scroll = ttk.Scrollbar(self.vendor_treeview_frame)
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
        
            # Bind a double click
            self.vendor_treeview.bind("<Double-Button-1>", vendor_double_clicked)  

            # Bind a right click
            self.vendor_treeview.bind("<Control-Button-1>", right_click_vendor)
            self.vendor_treeview.bind("<ButtonRelease-3>", right_click_vendor)
        
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
        new_vendor_window_frame = ttk.Frame(new_vendor_window)
        new_vendor_window_frame.pack(fill="both", expand=1, pady=10)      

        # Add the entry boxes
        new_id_label = ttk.Label(new_vendor_window_frame, text="ID")
        #new_id_label.grid(row=1, column=1, padx=10, pady=5)
        new_id_entry = ttk.Entry(new_vendor_window_frame, width=15, background="white")
        #new_id_entry.grid(row=1, column=2, padx=10, pady=5)

        new_name_label = ttk.Label(new_vendor_window_frame, text="Name")
        new_name_label.grid(row=2, column=1, padx=10, pady=5)
        new_name_entry = ttk.Entry(new_vendor_window_frame, width=15, background="white")
        new_name_entry.grid(row=2, column=2, padx=10, pady=5)

        new_company_label = ttk.Label(new_vendor_window_frame, text="Company")
        new_company_label.grid(row=3, column=1, padx=10, pady=5)
        new_company_entry = ttk.Entry(new_vendor_window_frame, width=15, background="white")
        new_company_entry.grid(row=3, column=2, padx=10, pady=5)

        new_street_label = ttk.Label(new_vendor_window_frame, text="Street")
        new_street_label.grid(row=4, column=1, padx=10, pady=5)
        new_street_entry = ttk.Entry(new_vendor_window_frame, width=15, background="white")
        new_street_entry.grid(row=4, column=2, padx=10, pady=5)

        new_town_label = ttk.Label(new_vendor_window_frame, text="Town")
        new_town_label.grid(row=5, column=1, padx=10, pady=5)
        new_town_entry = ttk.Entry(new_vendor_window_frame, width=15, background="white")
        new_town_entry.grid(row=5, column=2, padx=10, pady=5)

        new_city_label = ttk.Label(new_vendor_window_frame, text="City")
        new_city_label.grid(row=6, column=1, padx=10, pady=5)
        new_city_entry = ttk.Entry(new_vendor_window_frame, width=15, background="white")
        new_city_entry.grid(row=6, column=2, padx=10, pady=5)

        new_county_label = ttk.Label(new_vendor_window_frame, text="County")
        new_county_label.grid(row=7, column=1, padx=10, pady=5)
        new_county_entry = ttk.Entry(new_vendor_window_frame, width=15, background="white")
        new_county_entry.grid(row=7, column=2, padx=10, pady=5)

        new_postcode_label = ttk.Label(new_vendor_window_frame, text="Postcode")
        new_postcode_label.grid(row=8, column=1, padx=10, pady=5)
        new_postcode_entry = ttk.Entry(new_vendor_window_frame, width=15, background="white")
        new_postcode_entry.grid(row=8, column=2, padx=10, pady=5)

        new_email_label = ttk.Label(new_vendor_window_frame, text="Email")
        new_email_label.grid(row=9, column=1, padx=10, pady=5)
        new_email_entry = ttk.Entry(new_vendor_window_frame, width=15, background="white")
        new_email_entry.grid(row=9, column=2, padx=10, pady=5)

        new_phone_label = ttk.Label(new_vendor_window_frame, text="Phone")
        new_phone_label.grid(row=10, column=1, padx=10, pady=5)
        new_phone_entry = ttk.Entry(new_vendor_window_frame, width=15, background="white")
        new_phone_entry.grid(row=10, column=2, padx=10, pady=5)

        # Save contact button
        new_vendor_window_save_button = ttk.Button(new_vendor_window_frame, text="Save", command=lambda:[save_new_vendor(), new_vendor_window.destroy()])
        new_vendor_window_save_button.grid(row=11, column=1, padx=10, pady=5)

        # Close window button
        new_vendor_window_close_button = ttk.Button(new_vendor_window_frame, text="Cancel", command=new_vendor_window.destroy)
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

            # Regenerate menu
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
            edit_vendor_window_frame = ttk.Frame(edit_vendor_window)
            edit_vendor_window_frame.pack(fill="both", expand=1, pady=10)      

            # Add the entry boxes
            edit_id_label = ttk.Label(edit_vendor_window_frame, text="ID")
            #edit_id_label.grid(row=1, column=1, padx=10, pady=5)
            edit_id_entry = ttk.Entry(edit_vendor_window_frame, width=15, background="white")
            #edit_id_entry.grid(row=1, column=2, padx=10, pady=5)

            edit_name_label = ttk.Label(edit_vendor_window_frame, text="Name")
            edit_name_label.grid(row=2, column=1, padx=10, pady=5)
            edit_name_entry = ttk.Entry(edit_vendor_window_frame, width=15, background="white")
            edit_name_entry.grid(row=2, column=2, padx=10, pady=5)

            edit_company_label = ttk.Label(edit_vendor_window_frame, text="Company")
            edit_company_label.grid(row=3, column=1, padx=10, pady=5)
            edit_company_entry = ttk.Entry(edit_vendor_window_frame, width=15, background="white")
            edit_company_entry.grid(row=3, column=2, padx=10, pady=5)

            edit_street_label = ttk.Label(edit_vendor_window_frame, text="Street")
            edit_street_label.grid(row=4, column=1, padx=10, pady=5)
            edit_street_entry = ttk.Entry(edit_vendor_window_frame, width=15, background="white")
            edit_street_entry.grid(row=4, column=2, padx=10, pady=5)

            edit_town_label = ttk.Label(edit_vendor_window_frame, text="Town")
            edit_town_label.grid(row=5, column=1, padx=10, pady=5)
            edit_town_entry = ttk.Entry(edit_vendor_window_frame, width=15, background="white")
            edit_town_entry.grid(row=5, column=2, padx=10, pady=5)

            edit_city_label = ttk.Label(edit_vendor_window_frame, text="City")
            edit_city_label.grid(row=6, column=1, padx=10, pady=5)
            edit_city_entry = ttk.Entry(edit_vendor_window_frame, width=15, background="white")
            edit_city_entry.grid(row=6, column=2, padx=10, pady=5)

            edit_county_label = ttk.Label(edit_vendor_window_frame, text="County")
            edit_county_label.grid(row=7, column=1, padx=10, pady=5)
            edit_county_entry = ttk.Entry(edit_vendor_window_frame, width=15, background="white")
            edit_county_entry.grid(row=7, column=2, padx=10, pady=5)

            edit_postcode_label = ttk.Label(edit_vendor_window_frame, text="Postcode")
            edit_postcode_label.grid(row=8, column=1, padx=10, pady=5)
            edit_postcode_entry = ttk.Entry(edit_vendor_window_frame, width=15, background="white")
            edit_postcode_entry.grid(row=8, column=2, padx=10, pady=5)

            edit_email_label = ttk.Label(edit_vendor_window_frame, text="Email")
            edit_email_label.grid(row=9, column=1, padx=10, pady=5)
            edit_email_entry = ttk.Entry(edit_vendor_window_frame, width=15, background="white")
            edit_email_entry.grid(row=9, column=2, padx=10, pady=5)

            edit_phone_label = ttk.Label(edit_vendor_window_frame, text="Phone")
            edit_phone_label.grid(row=10, column=1, padx=10, pady=5)
            edit_phone_entry = ttk.Entry(edit_vendor_window_frame, width=15, background="white")
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
            close_button = ttk.Button(edit_vendor_window_frame, text="Save", command=lambda:[update_vendor()])
            close_button.grid(row=11, column=1, padx=10, pady=5)

            # Close window button
            close_button = ttk.Button(edit_vendor_window_frame, text="Cancel", command=edit_vendor_window.destroy)
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

            # Regenerate menu
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

        # Regenerate menu
        Menu_bar()    

    
    def new_vendor_invoice(self):
        # Connect to database
        conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
        cur = conn.cursor()

        # Select a vendor
        selected_vendor = self.vendor_treeview.focus()
        values_vendor = self.vendor_treeview.item(selected_vendor, 'values') 
    
        # If a vendor is selected open a window with a form to enter invoice details into
        if values_vendor: 
            # Create the window
            vendor_invoice_window = tk.Toplevel()
            vendor_invoice_window.title("Add Vendor Invoice")
            vendor_invoice_window.geometry("1024x800")
            #vendor_invoice_window.attributes('-topmost', 'true') 
            
            # Add the vendor address, date and invoice number to the invoice
            # Create a frame in the window for the supplier address
            vendor_address_frame = ttk.Frame(vendor_invoice_window)
            vendor_address_frame.pack(fill="both", padx=10, pady=15)  

            # Add the supplier address to the invoice
            vendor_name_label = ttk.Label(vendor_address_frame, text=values_vendor[1])
            vendor_name_label.grid(sticky="w", row=1, column=1, padx=10)

            vendor_company_label = ttk.Label(vendor_address_frame, text=values_vendor[2])
            vendor_company_label.grid(sticky="w", row=2, column=1, padx=10)
    
            vendor_street_label = ttk.Label(vendor_address_frame, text=values_vendor[3])
            vendor_street_label.grid(sticky="w", row=3, column=1, padx=10)
    
            vendor_town_label = ttk.Label(vendor_address_frame, text=values_vendor[4])
            vendor_town_label.grid(sticky="w", row=4, column=1, padx=10)
    
            vendor_city_label = ttk.Label(vendor_address_frame, text=values_vendor[5])
            vendor_city_label.grid(sticky="w", row=5, column=1, padx=10)
    
            vendor_county_label = ttk.Label(vendor_address_frame, text=values_vendor[6])
            vendor_county_label.grid(sticky="w", row=6, column=1, padx=10)
    
            vendor_postcode_label = ttk.Label(vendor_address_frame, text=values_vendor[7])
            vendor_postcode_label.grid(sticky="w", row=7, column=1, padx=10)

            # Add the date to the invoice
            date_frame = ttk.Frame(vendor_invoice_window)
            date_frame.pack(fill="both", padx=10, pady=15) 

            date_label = ttk.Label(date_frame, text="Date")
            date_label.grid(sticky="w", row=8, column=1, padx=10)
            cal = tkcal.DateEntry(date_frame, showweeknumbers=False, date_pattern='yyyy-mm-dd')
            cal.grid(sticky="w", row=9, column=1, padx=10)

            cal._top_cal.overrideredirect(False)

            # Add the invoice number
            invoice_number_frame = ttk.Frame(vendor_invoice_window)
            invoice_number_frame.pack(fill="both", padx=10, pady=15) 

            vendor_invoice_number_label = ttk.Label(invoice_number_frame, text="Invoice number")
            vendor_invoice_number_label.grid(sticky="w", row=9, column=1, padx=10)
            vendor_invoice_number_entry = ttk.Entry(invoice_number_frame, width=15, background="white")
            vendor_invoice_number_entry.grid(sticky="w", row=10, column=1, padx=10, pady=2)

            # Add the Treeview to the invoice
            # Create a frame for the Treeview widget
            vendor_invoice_treeview_frame = ttk.Frame(vendor_invoice_window)
            vendor_invoice_treeview_frame.pack(fill="both", expand=1, padx=10)

            # Add a scrollbar to the frame
            vendor_invoice_treeview_scroll = ttk.Scrollbar(vendor_invoice_treeview_frame)
            vendor_invoice_treeview_scroll.pack(side="right", fill="y") 

            # Add the Treeview to the frame
            vendor_invoice_treeview = ttk.Treeview(vendor_invoice_treeview_frame, yscrollcommand=vendor_invoice_treeview_scroll.set, selectmode="extended") 
            vendor_invoice_treeview.pack(fill="both", expand="yes")  

            # Add the invoice total box            
            invoice_total_box_entry = ttk.Entry(vendor_invoice_treeview_frame, width=15)
            invoice_total_box_entry.pack(side="right", padx=10, pady=5)
            invoice_total_box_entry.configure(state="readonly")
            invoice_total_box_label = ttk.Label(vendor_invoice_treeview_frame, text="Total")
            invoice_total_box_label.pack(side="right", padx=0, pady=5)

            # Create the columns in the Treeview
            vendor_invoice_treeview['columns'] = (
            "id",
            "Description", 
            "Account",
            "Quantity", 
            "Unit Price", 
            "Sub Total"
            )

            # Provide the headings for each column
            vendor_invoice_treeview.column("#0", width=0, stretch="no")
            vendor_invoice_treeview.heading("#0", text="")
            
            vendor_invoice_treeview.column("id", width=0, stretch="no")
            vendor_invoice_treeview.heading("id", text="id")

            vendor_invoice_treeview.column("Description", minwidth=500) 
            vendor_invoice_treeview.heading("Description", text="Description")   

            vendor_invoice_treeview.column("Account", minwidth=100) 
            vendor_invoice_treeview.heading("Account", text="Account") 
            
            vendor_invoice_treeview.column("Quantity", minwidth=100) 
            vendor_invoice_treeview.heading("Quantity", text="Quantity")   
            
            vendor_invoice_treeview.column("Unit Price", minwidth=100) 
            vendor_invoice_treeview.heading("Unit Price", text="Unit Price")   
            
            vendor_invoice_treeview.column("Sub Total", minwidth=100) 
            vendor_invoice_treeview.heading("Sub Total", text="Sub Total")

            # Add the invoice entry boxes and functional buttons to window
            # Create frame for the entry boxes and functional buttons
            vendor_invoice_entry_frame = ttk.LabelFrame(vendor_invoice_window, text="Add item to invoice")
            vendor_invoice_entry_frame.pack(fill="both", padx=10, pady=10, expand=1)
            
            # Add the entry boxes
            # Create a list of the all the accounts for the account type Expenses
            cur.execute("SELECT account_name FROM child_accounts WHERE type = 'Expense'")
            accounts = cur.fetchall()
           
            expense_accounts = []
            for account in accounts:
                for record in account:
                    expense_accounts.append(record)

            invoice_item_id_label = ttk.Label(vendor_invoice_entry_frame, text="id")
            #invoice_item_id_label.grid(row=1, column=1, padx=10)
            invoice_item_id_entry = ttk.Entry(vendor_invoice_entry_frame, width=15)
            #invoice_item_id_entry.grid(row=2, column=1, padx=10)

            invoice_item_description_label = ttk.Label(vendor_invoice_entry_frame, text="Description")
            invoice_item_description_label.grid(row=1, column=2, padx=10)
            invoice_item_description_entry = ttk.Entry(vendor_invoice_entry_frame, width=15, background="white")
            invoice_item_description_entry.grid(row=2, column=2, padx=10)

            invoice_item_quantity_label = ttk.Label(vendor_invoice_entry_frame, text="Quantity")
            invoice_item_quantity_label.grid(row=1, column=3, padx=10)
            invoice_item_quantity_entry = ttk.Entry(vendor_invoice_entry_frame, width=15, background="white")
            invoice_item_quantity_entry.grid(row=2, column=3, padx=10)
            
            invoice_item_unit_price_label = ttk.Label(vendor_invoice_entry_frame, text="Unit Price")
            invoice_item_unit_price_label.grid(row=1, column=4, padx=10)
            invoice_item_unit_price_entry = ttk.Entry(vendor_invoice_entry_frame, width=15, background="white")
            invoice_item_unit_price_entry.grid(row=2, column=4, padx=10)

            invoice_item_account = ttk.Label(vendor_invoice_entry_frame, text="Expense Account")
            invoice_item_account.grid(row=1, column=5, padx=10)
            invoice_item_account_combo = ttk.Combobox(vendor_invoice_entry_frame, value=expense_accounts, width=15, background="white")
            invoice_item_account_combo.grid(row=2, column=5, padx=10)
            
            # Add the functional buttons
            self.add_to_invoice_button = ttk.Button(vendor_invoice_entry_frame, text="Add to invoice", command=lambda:[add_invoice_item()])
            self.add_to_invoice_button.grid(row=3, column=2, padx=10) 
            
            self.edit_button = ttk.Button(vendor_invoice_entry_frame, text="Edit selected item")
            self.edit_button.grid(row=3, column=3, padx=10) 
            
            self.delete_button = ttk.Button(vendor_invoice_entry_frame, text="Delete item", command=lambda:[delete_invoice_item()])
            self.delete_button.grid(row=3, column=4, padx=10)
            
        else:
            Message("Please select a supplier first")
        
        # Close connection
        conn.commit()
        conn.close() 

        def add_invoice_item():
            # Connect to database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Make a list of all the invoice numbers in use already
            cur.execute("SELECT invoice_number FROM vendor_invoices WHERE vendor_rowid = " + values_vendor[0])
            records = cur.fetchall()

            vendor_invoices = []
            for record in records:
                for invoice in record:
                    vendor_invoices.append(invoice)

            # Make a list of all the vendors entered into the ledger
            cur.execute("SELECT description FROM ledger WHERE vendor_rowid = " + values_vendor[0])
            records = cur.fetchall()   

            vendor = []
            for record in records:
                for invoice in record:
                    vendor.append(invoice)
            
            # Make a list of all the accounts entered into the ledger
            cur.execute("SELECT account FROM ledger WHERE vendor_rowid = " + values_vendor[0])
            records = cur.fetchall()

            ledger_accounts = []
            for record in records:
                for invoice in record:
                    ledger_accounts.append(invoice)

            # Check the invoice has an invoice number. If not tell the user to set one
            if len(vendor_invoice_number_entry.get()) == 0:
                Message("Please set an invoice number")

            # Check the invoice number isn't being used already
            # elif vendor_invoice_number_entry.get() in vendor_invoices:
            #    Message("""That invoice number is already in use. 
            #        Please choose a different number""")
                
            # If the invoice has an invoice number add to the database
            else:
                # Work out the sub_total of the item being added (quantity*unit price)
                sub_total = round(float(invoice_item_quantity_entry.get()) * float(invoice_item_unit_price_entry.get()),2)

                # Add the item to the invoice database
                cur.execute("""INSERT INTO vendor_invoices (
                    id,
                    invoice_number,
                    vendor_rowid, 
                    date, 
                    description, 
                    quantity, 
                    unit_price, 
                    total,
                    account
                    ) 

                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", [

                    invoice_item_id_entry.get(),
                    vendor_invoice_number_entry.get(),
                    values_vendor[0],
                    cal.get(),
                    invoice_item_description_entry.get(), 
                    invoice_item_quantity_entry.get(), 
                    invoice_item_unit_price_entry.get(), 
                    sub_total,
                    invoice_item_account_combo.get()
                    ])     

                # Add the item value to the child account database
                cur.execute('UPDATE child_accounts SET total = total+? WHERE account_name=?',(sub_total, invoice_item_account_combo.get(),))

                # Add the item value to the parent account database
                cur.execute('SELECT parent FROM child_accounts WHERE account_name=?', (invoice_item_account_combo.get(),))
                parent_account = cur.fetchall()
                cur.execute('UPDATE parent_accounts SET total = total+? WHERE account_number=?', (sub_total, parent_account[0][0]),)
                
                # Add the invoice item value to the Accounts Payable database
                cur.execute('UPDATE parent_accounts SET total = total+? WHERE account_name=?', (sub_total, 'Accounts Payable (Creditors)'))

                # Add the invoice to the ledger
                # Add up all the items in an invoice to give a total invoice figure
                cur.execute("SELECT SUM(total) FROM vendor_invoices WHERE invoice_number = " + vendor_invoice_number_entry.get() + " AND vendor_rowid = " + values_vendor[0])
                self.figure = cur.fetchall()
                for figure in self.figure:
                    for value in figure:
                        total_figure = value
                
                if values_vendor[1] in vendor and vendor_invoice_number_entry.get() in vendor_invoices and invoice_item_account_combo.get() in ledger_accounts:
                    # Update accounts payable in ledger
                    cur.execute("""UPDATE ledger SET
                        vendor_rowid = :vendor_rowid, 
                        date = :date,
                        description = :description,
                        account = :account,
                        invoice_number = :invoice_number, 
                        
                        credit = :credit

                        WHERE invoice_number = :invoice_number AND vendor_rowid = :vendor_rowid AND account = :account""", 

                        {
                        'vendor_rowid' :values_vendor[0], 
                        'date' :cal.get(),
                        'description' :values_vendor[1],
                        'account' :'Accounts Payable (Creditors)',
                        'invoice_number' :vendor_invoice_number_entry.get(),
                        
                        'credit' :total_figure
                        })

                    # Update child account in ledger
                    cur.execute("""UPDATE ledger SET
                        vendor_rowid = :vendor_rowid, 
                        date = :date,
                        description = :description,
                        account = :account,
                        invoice_number = :invoice_number, 
                        debit = debit+:debit 
                        

                        WHERE invoice_number = :invoice_number AND vendor_rowid = :vendor_rowid AND account = :account""", 

                        {
                        'vendor_rowid' :values_vendor[0], 
                        'date' :cal.get(),
                        'description' :values_vendor[1],
                        'account' :invoice_item_account_combo.get(),
                        'invoice_number' :vendor_invoice_number_entry.get(),
                        'debit' :sub_total
                        
                        })

                elif values_vendor[1] in vendor and vendor_invoice_number_entry.get() in vendor_invoices:
                    cur.execute("""UPDATE ledger SET
                        vendor_rowid = :vendor_rowid, 
                        date = :date,
                        description = :description,
                        account = :account,
                        invoice_number = :invoice_number, 
                        
                        credit = :credit

                        WHERE invoice_number = :invoice_number AND vendor_rowid = :vendor_rowid AND account = :account""", 

                        {
                        'vendor_rowid' :values_vendor[0], 
                        'date' :cal.get(),
                        'description' :values_vendor[1],
                        'account' :'Accounts Payable (Creditors)',
                        'invoice_number' :vendor_invoice_number_entry.get(),
                        
                        'credit' :total_figure
                        })

                    cur.execute("""INSERT INTO ledger (
                            vendor_rowid, 
                            date,
                            description,
                            account,
                            invoice_number, 
                            debit,
                            credit                            
                            )

                            VALUES (?, ?, ?, ?, ?, ?, ?)""",[

                            values_vendor[0], 
                            cal.get(),
                            values_vendor[1],
                            invoice_item_account_combo.get(),
                            vendor_invoice_number_entry.get(),
                            sub_total,
                            ''
                            ])
                    
                else:      
                    # Add Accounts Payable to ledger          
                    cur.execute("""INSERT INTO ledger (
                            vendor_rowid, 
                            date,
                            description,
                            account,
                            invoice_number,  
                            debit,
                            credit
                            )

                            VALUES (?, ?, ?, ?, ?, ?, ?)""",[

                            values_vendor[0], 
                            cal.get(),
                            values_vendor[1],
                            'Accounts Payable (Creditors)',
                            vendor_invoice_number_entry.get(),
                            '',
                            total_figure
                            ])

                    # Add child account to ledger
                    cur.execute("""INSERT INTO ledger (
                            vendor_rowid, 
                            date,
                            description,
                            account,
                            invoice_number, 
                            debit,
                            credit                          
                            )

                            VALUES (?, ?, ?, ?, ?, ?, ?)""",[

                            values_vendor[0], 
                            cal.get(),
                            values_vendor[1],
                            invoice_item_account_combo.get(),
                            vendor_invoice_number_entry.get(),
                            sub_total,
                            ''
                            ])
                           
                # Re-populate the invoice treeview
                # Clear the entry boxes
                invoice_item_id_entry.delete(0,'end')
                invoice_item_description_entry.delete(0,'end')
                invoice_item_quantity_entry.delete(0,'end')
                invoice_item_unit_price_entry.delete(0,'end')
                invoice_item_account_combo.delete(0,'end')

                # Clear the treeview and total box
                for record in vendor_invoice_treeview.get_children():
                    vendor_invoice_treeview.delete(record)
                invoice_total_box_entry.delete(0,'end')

                # Get data from the database that has the same invoice number as the one given in the invoice
                cur.execute("SELECT rowid, * FROM vendor_invoices WHERE invoice_number = " + vendor_invoice_number_entry.get() + " AND vendor_rowid = " + values_vendor[0])
                record = cur.fetchall()    

                cur.execute("SELECT SUM(total) FROM vendor_invoices WHERE invoice_number = " + vendor_invoice_number_entry.get() + " AND vendor_rowid = " + values_vendor[0])
                self.figure = cur.fetchall()
                for figure in self.figure:
                    for value in figure:
                        total_figure = value 
                
                # Add the fetched data to the treeview and total box
                global count
                self.count = 0

                for row in record:
                    vendor_invoice_treeview.insert(parent='', index='end', iid=self.count, text='', values=(row[0], row[5], row[9], row[6], row[7], row[8]))
                    self.count+=1   
                invoice_total_box_entry.configure(state="normal") 
                invoice_total_box_entry.delete(0,'end')    
                invoice_total_box_entry.insert(0, total_figure)
                invoice_total_box_entry.configure(state="readonly")
            
            # Disconnect from the database
            conn.commit()
            conn.close() 

            # Lock the date
            cal.grid_forget()
            date_entry = ttk.Entry(date_frame)
            date_entry.grid(sticky="w", row=9, column=1, padx=10)
            date_entry.insert(0, cal.get())
            date_entry.configure(state="readonly")

            # Lock the invoice number
            vendor_invoice_number_entry.grid_forget()
            invoice_number = ttk.Entry(invoice_number_frame, width=15, background="white")
            invoice_number.grid(sticky="w", row=10, column=1, padx=10, pady=2)
            invoice_number.insert(0, vendor_invoice_number_entry.get())
            invoice_number.configure(state="readonly")

            # Re-populate the Chart of Accounts Treeview      
            chart_of_accounts.populate_accounts_tree()

            # Re-populate ledger
            ledger.populate_ledger_tree()

        def delete_invoice_item():

            # Connect to the database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Make the selected item in Treeview the focus and make it a variable called 'selected'
            # Pull the values in 'selected' from the 'values' part of the database
            selected_item = vendor_invoice_treeview.focus()
            invoice_item = vendor_invoice_treeview.item(selected_item, 'values')
            
            # If an item is selected then delete it from the database
            if invoice_item:
                # Select the rowid and data from the database table and fetch everything
                cur.execute("SELECT rowid, * FROM vendor_invoices")
                record = cur.fetchall()       

                # Work out the sub_total of the item being deleted (quantity*unit price)
                sub_total = invoice_item[5]
                
                # Delete the database row(rowid) that has the same rowid as the one selected in the Treeview
                cur.execute("DELETE FROM vendor_invoices WHERE rowid = " + invoice_item[0])

                # Delete the item value from the parent account database
                cur.execute('UPDATE parent_accounts SET total=total-? WHERE account_name=?',(sub_total, "Accounts Payable (Creditors)"))

                cur.execute("SELECT parent FROM child_accounts WHERE account_name=?", (invoice_item[2],))
                parent_account = cur.fetchall()
                cur.execute('UPDATE parent_accounts SET total=total-? WHERE account_number=?', (sub_total, parent_account[0][0]))
                
                # Delete the item value from the child account database
                cur.execute('UPDATE child_accounts SET total=total-? WHERE account_name=?',(sub_total, invoice_item[2]))

                # Delete the item value from the ledger
                cur.execute('UPDATE ledger SET credit=credit-? WHERE vendor_rowid=? AND invoice_number=? AND account =?', (sub_total, values_vendor[0], vendor_invoice_number_entry.get(), "Accounts Payable (Creditors)"))
                cur.execute('UPDATE ledger SET debit=debit-? WHERE vendor_rowid=? AND invoice_number=? AND account =?', (sub_total, values_vendor[0], vendor_invoice_number_entry.get(), invoice_item[2]))

                # Re-populate the invoice treeview
                # Clear the treeview and total box
                for record in vendor_invoice_treeview.get_children():
                    vendor_invoice_treeview.delete(record)
                
                # Get data from the database that has the same invoice number as the one given in the invoice
                cur.execute("SELECT rowid, * FROM vendor_invoices WHERE invoice_number = " + vendor_invoice_number_entry.get() + " AND vendor_rowid = " + values_vendor[0])
                record = cur.fetchall()  

                # Add up all the items in an invoice to give a total invoice figure
                cur.execute("SELECT SUM(total) FROM vendor_invoices WHERE invoice_number = " + vendor_invoice_number_entry.get() + " AND vendor_rowid = " + values_vendor[0])
                self.figure = cur.fetchall()
                for figure in self.figure:
                    for value in figure:
                        total_figure = value 
                
                # Add the fetched data to the treeview and total box
                global count
                count = 0

                for row in record:
                    vendor_invoice_treeview.insert(parent='', index='end', iid=count, text='', values=(row[0], row[5], row[9], row[6], row[7], row[8]))
                    count+=1        

                invoice_total_box_entry.configure(state="normal") 
                invoice_total_box_entry.delete(0,'end')
                invoice_total_box_entry.insert(0, total_figure)
                invoice_total_box_entry.configure(state="readonly") 
            
            else:
                Message("Please choose an item to delete")
            
            conn.commit()
            conn.close()

            # Re-populate the Chart of Accounts Treeview      
            chart_of_accounts.populate_accounts_tree()

            # Re-populate ledger treeview
            ledger.populate_ledger_tree()

    def invoice_history(self):
        
        def invoice_clicked(event):
            # Call the method
            self.view_invoice()

        # Connect to the database
        conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
        cur = conn.cursor()

        # Select a vendor
        vendor_selected = self.vendor_treeview.focus()
        vendor_values = self.vendor_treeview.item(vendor_selected, 'values') 

        # If a supplier is selected open a window with a form to enter details into
        if vendor_values: 
            # Create the window
            vendor_invoice_history_window = tk.Toplevel()
            vendor_invoice_history_window.title("Invoice History")
            vendor_invoice_history_window.geometry("1024x640")
            vendor_invoice_history_window.attributes('-topmost', 'true') 
            
            # Create a frame in the window for the supplier address
            vendor_address_frame = ttk.Frame(vendor_invoice_history_window)
            vendor_address_frame.pack(fill="both")  

            # Add the supplier address to the invoice
            vendor_name_label = ttk.Label(vendor_address_frame, text=vendor_values[1])
            vendor_name_label.grid(sticky="w", row=1, column=1, padx=10)
            
            vendor_company_label = ttk.Label(vendor_address_frame, text=vendor_values[2])
            vendor_company_label.grid(sticky="w", row=2, column=1, padx=10)
            
            vendor_street_label = ttk.Label(vendor_address_frame, text=vendor_values[3])
            vendor_street_label.grid(sticky="w", row=3, column=1, padx=10)
            
            vendor_town_label = ttk.Label(vendor_address_frame, text=vendor_values[4])
            vendor_town_label.grid(sticky="w", row=4, column=1, padx=10)
            vendor_city_label = ttk.Label(vendor_address_frame, text=vendor_values[5])
            
            vendor_city_label.grid(sticky="w", row=5, column=1, padx=10)
            vendor_county_label = ttk.Label(vendor_address_frame, text=vendor_values[6])
            vendor_county_label.grid(sticky="w", row=6, column=1, padx=10)
            
            vendor_postcode_label = ttk.Label(vendor_address_frame, text=vendor_values[7])
            vendor_postcode_label.grid(sticky="w", row=7, column=1, padx=10)

            # Create a frame for the ribbon
            vendor_invoice_history_ribbon_frame = ttk.Frame(vendor_invoice_history_window)
            vendor_invoice_history_ribbon_frame.pack(fill="both")

            # Add functional buttons to ribbon
            # Add invoice button icon to the frame
            self.view_invoice_icon = tk.PhotoImage(file="images/invoice.png")    
            view_invoice_button = ttk.Button(vendor_invoice_history_ribbon_frame, image=self.view_invoice_icon, command=self.view_invoice)
            view_invoice_button.grid(padx=10, pady=0, row=1, column=1)
            view_invoice_label = ttk.Label(vendor_invoice_history_ribbon_frame, text="View Invoice")
            view_invoice_label.grid(padx=10, pady=0, row=2, column=1)
                    
            # Create a frame for the Treeview widget
            invoice_history_treeview_frame = ttk.Frame(vendor_invoice_history_window)
            invoice_history_treeview_frame.pack(fill="both", expand=1)

            # Add a scrollbar to the frame
            invoice_history_treeview_scroll = ttk.Scrollbar(invoice_history_treeview_frame)
            invoice_history_treeview_scroll.pack(side="right", fill="y") 

            # Add the Treeview to the frame
            self.vendor_invoice_history_tree = ttk.Treeview(invoice_history_treeview_frame, yscrollcommand=invoice_history_treeview_scroll.set, selectmode="extended") 
            self.vendor_invoice_history_tree.pack(fill="both", expand="y")  

            # Create the columns in the Treeview
            self.vendor_invoice_history_tree['columns'] = (
            "ID",
            "Date", 
            "Invoice Number", 
            "Total"
            )

            # Provide the headings for each column
            self.vendor_invoice_history_tree.column("#0", width=0, stretch="no")
            self.vendor_invoice_history_tree.heading("#0", text="")
            
            self.vendor_invoice_history_tree.column("ID", width=0, stretch="no")
            self.vendor_invoice_history_tree.heading("ID", text="ID")
            
            self.vendor_invoice_history_tree.column("Date") 
            self.vendor_invoice_history_tree.heading("Date", text="Date")  
            
            self.vendor_invoice_history_tree.column("Invoice Number") 
            self.vendor_invoice_history_tree.heading("Invoice Number", text="Invoice Number")  
            
            self.vendor_invoice_history_tree.column("Total") 
            self.vendor_invoice_history_tree.heading("Total", text="Total")  

            # Add the data to the treeview
            # Fetch data from database
            cur.execute("SELECT rowid, *, SUM(total) FROM vendor_invoices WHERE vendor_rowid = " + vendor_values[0] + " GROUP BY invoice_number")
            record = cur.fetchall()   
            
            # Add the fetched data to the treeview
            global count
            count = 0

            for row in record:
                self.vendor_invoice_history_tree.insert(parent='', index='end', iid=count, text='', values=(row[1], row[4], row[2], row[10]))
                count+=1        
        
        # If a supplier isn't selected tell the user to select a supplier
        else:
            Message("Please select a supplier first")

        self.vendor_invoice_history_tree.bind("<Double-Button-1>", invoice_clicked)
        
        # Disconnect from the database
        conn.commit()
        conn.close()
    
    def view_invoice(self):
        # Connect to the database
        conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
        cur = conn.cursor()

        # Select vendor
        selected_vendor = self.vendor_treeview.focus()
        values_vendor = self.vendor_treeview.item(selected_vendor, 'values') 

        # Select an invoice
        selected_invoice = self.vendor_invoice_history_tree.focus()
        values_invoice = self.vendor_invoice_history_tree.item(selected_invoice, 'values') 

        # If an invoice is selected then open a window showing the invoice details
        if values_invoice:
            # Create the window
            vendor_invoice_window = tk.Toplevel()
            vendor_invoice_window.title("Invoice")
            vendor_invoice_window.geometry("1024x600")
            vendor_invoice_window.attributes('-topmost', 'true') 

            # Create a frame in the window for the supplier address
            vendor_address_frame = ttk.Frame(vendor_invoice_window)
            vendor_address_frame.pack(fill="both", padx=10, pady=5)  

            # Add the supplier address to the invoice
            vendor_name_label = ttk.Label(vendor_address_frame, text=values_vendor[1])
            vendor_name_label.grid(sticky="w", row=1, column=1, padx=10)

            vendor_company_label = ttk.Label(vendor_address_frame, text=values_vendor[2])
            vendor_company_label.grid(sticky="w", row=2, column=1, padx=10)
    
            vendor_street_label = ttk.Label(vendor_address_frame, text=values_vendor[3])
            vendor_street_label.grid(sticky="w", row=3, column=1, padx=10)
    
            vendor_town_label = ttk.Label(vendor_address_frame, text=values_vendor[4])
            vendor_town_label.grid(sticky="w", row=4, column=1, padx=10)
    
            vendor_city_label = ttk.Label(vendor_address_frame, text=values_vendor[5])
            vendor_city_label.grid(sticky="w", row=5, column=1, padx=10)
    
            vendor_county_label = ttk.Label(vendor_address_frame, text=values_vendor[6])
            vendor_county_label.grid(sticky="w", row=6, column=1, padx=10)
    
            vendor_postcode_label = ttk.Label(vendor_address_frame, text=values_vendor[7])
            vendor_postcode_label.grid(sticky="w", row=7, column=1, padx=10)

            # Add the date
            date_frame = ttk.Frame(vendor_invoice_window)
            date_frame.pack(fill="both", padx=10, pady=15) 

            date_label = ttk.Label(date_frame, text="Date")
            date_label.grid(sticky="w", row=8, column=1, padx=10, pady=0)
            date = ttk.Entry(date_frame)
            date.insert(0, values_invoice[1])
            date.configure(state="readonly")
            date.grid(sticky="w", row=9, column=1, padx=10)

            # Add the invoice number
            invoice_number_frame = ttk.Frame(vendor_invoice_window)
            invoice_number_frame.pack(fill="both", padx=10, pady=15)

            vendor_invoice_number_label = ttk.Label(invoice_number_frame, text="Invoice number")
            vendor_invoice_number_label.grid(sticky="w", row=9, column=1, padx=10)
            vendor_invoice_number_entry = ttk.Entry(invoice_number_frame, width=15, background="white")
            vendor_invoice_number_entry.insert(0, values_invoice[2])
            vendor_invoice_number_entry.configure(state="readonly")
            vendor_invoice_number_entry.grid(sticky="w", row=10, column=1, padx=10, pady=0)

            # Add the Treeview to the invoice
            # Create a frame for the Treeview widget
            vendor_invoice_treeview_frame = ttk.Frame(vendor_invoice_window)
            vendor_invoice_treeview_frame.pack(fill="both", expand=1, padx=10)

            # Add a scrollbar to the frame
            vendor_invoice_treeview_scroll = ttk.Scrollbar(vendor_invoice_treeview_frame)
            vendor_invoice_treeview_scroll.pack(side="right", fill="y") 

            # Add the Treeview to the frame
            vendor_invoice_treeview = ttk.Treeview(vendor_invoice_treeview_frame, yscrollcommand=vendor_invoice_treeview_scroll.set, selectmode="extended") 
            vendor_invoice_treeview.pack(fill="both", expand="yes")  

            # Add the invoice total box            
            invoice_total_box_entry = ttk.Entry(vendor_invoice_treeview_frame, width=15, state="readonly")
            invoice_total_box_entry.pack(side="right", padx=10, pady=10)
            invoice_total_box_label = ttk.Label(vendor_invoice_treeview_frame, text="Total")
            invoice_total_box_label.pack(side="right", padx=0, pady=10)

            # Create the columns in the Treeview
            vendor_invoice_treeview['columns'] = (
            "id",
            "Description", 
            "Account",
            "Quantity", 
            "Unit Price", 
            "Sub Total"
            )

            # Provide the headings for each column
            vendor_invoice_treeview.column("#0", width=0, stretch="no")
            vendor_invoice_treeview.heading("#0", text="")
            
            vendor_invoice_treeview.column("id", width=0, stretch="no")
            vendor_invoice_treeview.heading("id", text="id")

            vendor_invoice_treeview.column("Description", minwidth=500) 
            vendor_invoice_treeview.heading("Description", text="Description")   

            vendor_invoice_treeview.column("Account", minwidth=100) 
            vendor_invoice_treeview.heading("Account", text="Account") 
            
            vendor_invoice_treeview.column("Quantity", minwidth=100) 
            vendor_invoice_treeview.heading("Quantity", text="Quantity")   
            
            vendor_invoice_treeview.column("Unit Price", minwidth=100) 
            vendor_invoice_treeview.heading("Unit Price", text="Unit Price")   
            
            vendor_invoice_treeview.column("Sub Total", minwidth=100) 
            vendor_invoice_treeview.heading("Sub Total", text="Sub Total")

            # Populate the treeview
            # Get data from the database that has the same invoice number as the one given in the invoice
            cur.execute("SELECT rowid, * FROM vendor_invoices WHERE invoice_number = " + vendor_invoice_number_entry.get() + " AND vendor_rowid = " + values_vendor[0])
            record = cur.fetchall()  

            # Calculate the total 
            cur.execute("SELECT SUM(total) FROM vendor_invoices WHERE invoice_number = " + vendor_invoice_number_entry.get() + " AND vendor_rowid = " + values_vendor[0])
            self.figure = cur.fetchall()
            for figure in self.figure:
                for value in figure:
                    total_figure = value 

            # Add the fetched data to the treeview and total box
            global count
            self.count = 0

            for row in record:
                vendor_invoice_treeview.insert(parent='', index='end', iid=self.count, text='', values=(row[0], row[5], row[9], row[6], row[7], row[8]))
                self.count+=1   

            invoice_total_box_entry.configure(state="normal")     
            invoice_total_box_entry.insert(0, total_figure)
            invoice_total_box_entry.configure(state="readonly")

        else:
            pass
  
        # Disconnect from the database
        conn.commit()
        conn.close() 

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

            cur.execute("SELECT * FROM parent_accounts WHERE account_name = 'Current Accounts'")
            initial = cur.fetchall()
            if initial:
                pass
            else:
                cur.execute("INSERT INTO parent_accounts (account_number, account_name, total, child, type) VALUES (?, ?, ?, ?, ?)", (1000, 'Current Accounts', 0.00, "NO", 'Asset'))
                cur.execute("INSERT INTO parent_accounts (account_number, account_name, total, child, type) VALUES (?, ?, ?, ?, ?)", (1100, 'Accounts Receivable (Debtors)', 0.00, "NO", 'Asset'))
                cur.execute("INSERT INTO parent_accounts (account_number, account_name, total, child, type) VALUES (?, ?, ?, ?, ?)", (2000, 'Accounts Payable (Creditors)', 0.00, "NO", 'Liability'))
                cur.execute("INSERT INTO parent_accounts (account_number, account_name, total, child, type) VALUES (?, ?, ?, ?, ?)", (4000, 'Income', 0.00, "NO", 'Sales'))
                cur.execute("INSERT INTO parent_accounts (account_number, account_name, total, child, type) VALUES (?, ?, ?, ?, ?)", (5000, 'Expenses', 0.00, "NO", 'Expense'))
                conn.commit()

            
            cur.execute("SELECT * FROM parent_accounts WHERE account_name = 'Income'")
            income = cur.fetchall()
            if income:
                pass
            else:
                cur.execute("INSERT INTO parent_accounts (account_number, account_name, total, type) VALUES (?, ?, ?, ?)", (1100, 'Accounts Receivable (Debtors)', 0.00, 'Asset'))
                cur.execute("INSERT INTO parent_accounts (account_number, account_name, total, type) VALUES (?, ?, ?, ?)", (2000, 'Accounts Payable (Creditors)', 0.00, 'Liability'))
                conn.commit()

        def accounts_tab():
            # Create the tab
            self.tab = ttk.Frame(main_window)
            self.tab.pack(fill="both", expand="yes")

            # Add the tab to the notebook and provide a heading
            main_window.add(self.tab, text="Chart of Accounts")
        
        def accounts_ribbon():
            # Make a frame for the ribbon
            accounts_ribbon_frame = ttk.Frame(self.tab)
            accounts_ribbon_frame.pack(side="top", fill="x", padx=10, pady=10)
        
            # Assign an image to each button
            self.new_account_icon = tk.PhotoImage(file="images/new_account.png")
            self.new_child_account_icon = tk.PhotoImage(file="images/new_child_account.png")
            self.delete_account_icon = tk.PhotoImage(file="images/delete_account.png")
            self.edit_account_icon = tk.PhotoImage(file="images/edit_account.png")

            # Add "new account" button to the frame and give it a command
            new_account_button = ttk.Button(accounts_ribbon_frame, image=self.new_account_icon, command=self.new_parent_account)
            new_account_button.grid(padx=10, row=1, column=1)

            new_account_label = ttk.Label(accounts_ribbon_frame, text="Add New Account")
            new_account_label.grid(padx=10, row=2, column=1)

            # Add "add child account" button to the frame and give it a command  
            new_child_account_button = ttk.Button(accounts_ribbon_frame, image=self.new_child_account_icon, command=self.new_child_account)
            new_child_account_button.grid(padx=10, row=1, column=2)
            new_child_account_label = ttk.Label(accounts_ribbon_frame, text="Add Child Account")
            new_child_account_label.grid(padx=10, row=2, column=2)

            # Add "edit account" button to the frame and give it a command
            edit_account_button = ttk.Button(accounts_ribbon_frame, image=self.edit_account_icon, command=self.edit_account)
            edit_account_button.grid(padx=10, row=1, column=3)

            edit_account_label = ttk.Label(accounts_ribbon_frame, text="Edit Account")
            edit_account_label.grid(padx=10, row=2, column=3)

            # Add "delete account" button to the frame and give it a command
            delete_account_button = ttk.Button(accounts_ribbon_frame, image=self.delete_account_icon, command=self.delete_account)
            delete_account_button.grid(padx=10, row=1, column=4)

            delete_account_label = ttk.Label(accounts_ribbon_frame, text="Delete Account")
            delete_account_label.grid(padx=10, row=2, column=4)
            
        def accounts_treeview():

            def right_click_accounts(event):
                # Create a toggle to determine if a vendor is selected
                selected_account = chart_of_accounts.accounts_treeview.focus()
                values_accounts = chart_of_accounts.accounts_treeview.item(selected_account, 'values')

                # Create the menu
                right_click_accounts = tk.Menu(chart_of_accounts.accounts_treeview, tearoff="false")

                # Add menu items
                right_click_accounts.add_command(label="New Account", command=chart_of_accounts.new_parent_account)
                right_click_accounts.add_command(label="New Child Account", command=chart_of_accounts.new_child_account, state="disabled")
                right_click_accounts.add_command(label="Edit Account", command=chart_of_accounts.edit_account, state="disabled")
                right_click_accounts.add_command(label="Delete Account", command=chart_of_accounts.delete_account, state="disabled")

                # If an account is selected change the state of menu items
                if values_accounts:
                    if values_accounts[6] == "YES":
                        right_click_accounts.entryconfig("New Child Account", state="disabled")
                        right_click_accounts.entryconfig("Edit Account", state="normal")
                        right_click_accounts.entryconfig("Delete Account", state="normal")

                    elif values_accounts[6] == "NO":
                        right_click_accounts.entryconfig("New Child Account", state="normal")
                        right_click_accounts.entryconfig("Edit Account", state="normal")
                        right_click_accounts.entryconfig("Delete Account", state="normal")
                else:
                    pass
                
                # Pop-up the menu 
                right_click_accounts.tk_popup(event.x_root, event.y_root)

                
            # Create a frame for the Treeview
            self.accounts_treeview_frame = ttk.Frame(self.tab)
            self.accounts_treeview_frame.pack(side="bottom", fill="both", padx=10, expand=1)

            # Create a scrollbar for the Treeview
            self.accounts_treeview_scroll = ttk.Scrollbar(self.accounts_treeview_frame)
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
            
            self.accounts_treeview.column("Account Name", minwidth=200, width=200, stretch="false")
            self.accounts_treeview.heading("Account Name", text="Account Name") 
            
            self.accounts_treeview.column("Total", minwidth=250, width=250, stretch="false")            
            self.accounts_treeview.heading("Total", text="Total")          
            
            self.accounts_treeview.column("Parent", width=0, stretch="false")          
            self.accounts_treeview.heading("Parent", text="Parent")    
            
            self.accounts_treeview.column("Child", width=0, stretch="false")           
            self.accounts_treeview.heading("Child", text="Child") 

            self.accounts_treeview.bind("<ButtonRelease-3>", right_click_accounts)
        
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
        new_account_window.attributes('-topmost')
            
        new_account_window_frame = ttk.Frame(new_account_window)
        new_account_window_frame.pack(fill="both", expand=1, pady=10)      

        # Create the entry boxes
        new_account_id_label = ttk.Label(new_account_window_frame, text="ID")
        #new_account_id_label.grid(row=1, column=1, padx=10, pady=5)
        new_account_id_entry = ttk.Entry(new_account_window_frame, width=15)
        #new_account_id_entry.grid(row=1, column=2, padx=10, pady=5)
        
        new_account_number_label = ttk.Label(new_account_window_frame, text="Account Number")
        new_account_number_label.grid(row=2, column=1, padx=10, pady=5)
        new_account_number_entry = ttk.Entry(new_account_window_frame, width=15)
        new_account_number_entry.grid(row=2, column=2, padx=10, pady=5)

        new_account_name_label = ttk.Label(new_account_window_frame, text="Account Name")
        new_account_name_label.grid(row=3, column=1, padx=10, pady=5)
        new_account_name_entry = ttk.Entry(new_account_window_frame, width=15)
        new_account_name_entry.grid(row=3, column=2, padx=10, pady=5)    

        new_account_total_label = ttk.Label(new_account_window_frame, text="Total")
        #new_account_total_label.grid(row=4, column=1, padx=10, pady=5)
        new_account_total_entry = ttk.Entry(new_account_window_frame, width=15)
        #new_account_total_entry.grid(row=4, column=2, padx=10, pady=5)       

        new_parent_account_label = ttk.Label(new_account_window_frame, text="Parent")
        #new_parent_account_label.grid(row=5, column=1, padx=10, pady=5)
        new_parent_account_entry = ttk.Entry(new_account_window_frame, width=15)
        #new_parent_account_entry.grid(row=5, column=2, padx=10, pady=5)     

        new_child_account_status_label = ttk.Label(new_account_window_frame, text="Child Account?")
        #new_child_account_status_label.grid(row=6, column=1, padx=10, pady=5)
        new_child_account_status_entry = ttk.Entry(new_account_window_frame, width=10)
        #new_child_account_status_entry.grid(row=6, column=2, padx=10, pady=5)

        account_type = ["Asset", "Liability", "Capital", "Sales", "Expense"]
        new_account_type_label = ttk.Label(new_account_window_frame, text="Type")
        new_account_type_label.grid(row=7, column=1, padx=10, pady=5)
        new_account_type_entry = ttk.Combobox(new_account_window_frame, values=account_type, width=15)
        new_account_type_entry.set("Choose account type")
        new_account_type_entry.grid(row=7, column=2, padx=10, pady=5)

        # Save contact button
        close_button = ttk.Button(new_account_window_frame, text="Save", command=lambda:[save_new_account(), new_account_window.destroy()])
        close_button.grid(row=8, column=1)

        # Close window button
        self.close_button = ttk.Button(new_account_window_frame, text="Close", command=new_account_window.destroy)
        self.close_button.grid(row=8, column=2)

        def save_new_account():   
            """
            Take the data from the enrty boxes in new_account_window and add to the database table as a new account
            """        

            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Pull the data from the entry boxes and store them in a list called 'inputted_data'. "NO" is to signal that this is not a child account.
            inputted_data = [new_account_number_entry.get(), (new_account_name_entry.get()).title(), "NO", new_account_type_entry.get()]

            # Make sure the new account has a number, and and type. If not, provide a popup window asking for a number.    
            if len(new_account_number_entry.get()) == 0 or len(new_account_name_entry.get()) == 0 or new_account_type_entry.get() not in account_type:
                Message("A new account must have an Account Number, Name and account type")  

            # If the new account has a name, number and type insert into database...
            else:
                if len(new_account_number_entry.get() and new_account_name_entry.get()) != 0:
                    # Check to see if the account number is in use already. Attempt to make an account number list from the database using the account number in the entry box        
                    cur.execute("SELECT account_number FROM parent_accounts WHERE account_number = " + new_account_number_entry.get() + "")
                    parent_account_number_query = cur.fetchone()
                    cur.execute("SELECT account_number FROM child_accounts WHERE account_number = " + new_account_number_entry.get() + "")
                    child_account_number_query = cur.fetchone()

                    # Check to see if the account name is in use
                    cur.execute("SELECT account_name FROM parent_accounts")
                    account_name = cur.fetchall()  

                    account_names = []
                    for account in account_name:
                        for record in account:
                            account_names.append(record)
                    


                    # If either of the lists exist (True), ie account number is in the database tell the user the account number is in use.
                    if parent_account_number_query or child_account_number_query:
                        Message("That account number is in use already")  
                    
                    elif (new_account_name_entry.get()).title() in account_names:
                        Message("That account name is already in use")
                    
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
                
            child_account_window_frame = ttk.Frame(child_account_window)
            child_account_window_frame.pack(fill="both", expand=1, pady=10)      

            # Create the entry boxes
            child_account_id_label = ttk.Label(child_account_window_frame, text="ID")
            #child_account_id_label.grid(row=1, column=1, padx=10, pady=5)
            child_account_id_entry = ttk.Entry(child_account_window_frame, width=15)
            #child_account_id_entry.grid(row=1, column=2, padx=10, pady=5)
            
            child_account_number_label = ttk.Label(child_account_window_frame, text="Account Number")
            child_account_number_label.grid(row=2, column=1, padx=10, pady=5)
            child_account_number_entry = ttk.Entry(child_account_window_frame, width=15)
            child_account_number_entry.grid(row=2, column=2, padx=10, pady=5)

            child_account_name_label = ttk.Label(child_account_window_frame, text="Account Name")
            child_account_name_label.grid(row=3, column=1, padx=10, pady=5)
            child_account_name_entry = ttk.Entry(child_account_window_frame, width=15)
            child_account_name_entry.grid(row=3, column=2, padx=10, pady=5)    

            child_account_total_label = ttk.Label(child_account_window_frame, text="Total")
            #child_account_total_label.grid(row=4, column=1, padx=10, pady=5)
            child_account_total_entry = ttk.Entry(child_account_window_frame, width=15)
            #child_account_total_entry.grid(row=4, column=2, padx=10, pady=5)       

            parent_account_number_label = ttk.Label(child_account_window_frame, text="Parent")
            parent_account_number_label.grid(row=5, column=1, padx=10, pady=5)
            parent_account_number_entry = ttk.Entry(child_account_window_frame, width=15)
            parent_account_number_entry.grid(row=5, column=2, padx=10, pady=5) 
            parent_account_number_entry.insert(0, values_account[1])  
            parent_account_number_entry.config(state='readonly')  

            child_account_status_label = ttk.Label(child_account_window_frame, text="Child Account?")
            #child_account_status_label.grid(row=6, column=1, padx=10, pady=5)
            child_account_status_entry = ttk.Entry(child_account_window_frame, width=15)
            #child_account_status_entry.grid(row=6, column=2, padx=10, pady=5)

            child_account_type_label = ttk.Label(child_account_window_frame, text="Type")
            child_account_type_label.grid(row=7, column=1, padx=10, pady=5)
            child_account_type_entry = ttk.Entry(child_account_window_frame, width=15)
            child_account_type_entry.grid(row=7, column=2, padx=10, pady=5)
            child_account_type_entry.insert(0, values_account[2])
            child_account_type_entry.config(state='readonly')

            # Save contact and close window
            save_button = ttk.Button(child_account_window_frame, text="Save", command=lambda:[save_child_account(), child_account_window.destroy()])
            save_button.grid(row=8, column=1)

            # Close window
            close_button = ttk.Button(child_account_window_frame, text="Close", command=child_account_window.destroy)
            close_button.grid(row=8, column=2)    

        # If a parent account hasn't been selected tell the user to choose a parent account. 
        else:
            Message("Please select a parent account first")
        
        def save_child_account():
            # Connect to the database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Pull the data from the entry boxes and store them in a list called 'inputted_data'. "YES" is to signal that it's a child account.
            inputted_data = [child_account_number_entry.get(), (child_account_name_entry.get()).title(), parent_account_number_entry.get(), "YES", child_account_type_entry.get()]

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

                # Check to see if the account name is in use
                cur.execute("SELECT account_name FROM child_accounts")
                account_name = cur.fetchall()  

                account_names = []
                for account in account_name:
                    for record in account:
                        account_names.append(record)

                # If the list exists (True), ie account number is in the database tell the user the account number is in use.
                if parent_account_number_query or child_account_number_query:
                    Message("That account number is already in use")
                
                elif (child_account_name_entry.get()).title() in account_names:
                    Message("That account name is already in use")

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
                
            edit_account_window_frame = ttk.Frame(edit_account_window)
            edit_account_window_frame.pack(fill="both", expand=1, pady=10)      

            # Create the entry boxes
            edit_account_id_label = ttk.Label(edit_account_window_frame, text="ID")
            #edit_account_id_label.grid(row=1, column=1, padx=10, pady=5)
            edit_account_id_entry = ttk.Entry(edit_account_window_frame, width=15)
            #edit_account_id_entry.grid(row=1, column=2, padx=10, pady=5)
            
            edit_account_number_label = ttk.Label(edit_account_window_frame, text="Account Number")
            edit_account_number_label.grid(row=2, column=1, padx=10, pady=5)
            edit_account_number_entry = ttk.Entry(edit_account_window_frame, width=15)
            edit_account_number_entry.grid(row=2, column=2, padx=10, pady=5)

            edit_account_name_label = ttk.Label(edit_account_window_frame, text="Account Name")
            edit_account_name_label.grid(row=3, column=1, padx=10, pady=5)
            edit_account_name_entry = ttk.Entry(edit_account_window_frame, width=15)
            edit_account_name_entry.grid(row=3, column=2, padx=10, pady=5)    

            edit_account_total_label = ttk.Label(edit_account_window_frame, text="Total")
            #edit_account_total_label.grid(row=4, column=1, padx=10, pady=5)
            edit_account_total_entry = ttk.Entry(edit_account_window_frame, width=15)
            #edit_account_total_entry.grid(row=4, column=2, padx=10, pady=5)       

            edit_parent_account_label = ttk.Label(edit_account_window_frame, text="Parent")
            edit_parent_account_label.grid(row=5, column=1, padx=10, pady=5)
            edit_parent_account_entry = ttk.Entry(edit_account_window_frame, width=15)
            edit_parent_account_entry.grid(row=5, column=2, padx=10, pady=5)     

            edit_child_account_status_label = ttk.Label(edit_account_window_frame, text="Child Account?")
            #edit_child_account_status_label.grid(row=6, column=1, padx=10, pady=5)
            edit_child_account_status_entry = ttk.Entry(edit_account_window_frame, width=15)
            #edit_child_account_status_entry.grid(row=6, column=2, padx=10, pady=5)

            edit_account_type_label = ttk.Label(edit_account_window_frame, text="Type")
            edit_account_type_label.grid(row=7, column=1, padx=10, pady=5)
            edit_account_type_entry = ttk.Entry(edit_account_window_frame, width=15)
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
            save_button = ttk.Button(edit_account_window_frame, text="Save", command=lambda:[save_account_edit(), edit_account_window.destroy()])
            save_button.grid(row=8, column=1)

            # Close window button
            close_button = ttk.Button(edit_account_window_frame, text="Close", command=edit_account_window.destroy)
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
                'account_name' : (edit_account_name_entry.get()).title(), 
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
                #cur.execute("SELECT rowid, * FROM child_accounts")

                if values_account[4] != 0:
                    Message("This account has transactions linked to it so it cannot be deleted")
                
                else:
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

class Ledger:
    
    def __init__(self):
        def ledger_database_table():
            # Connect to the database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Create database table
            cur.execute("""CREATE TABLE IF NOT EXISTS ledger (
                id INTEGER,
                vendor_rowid INTEGER,
                date INTEGER, 
                description TEXT,
                account TEXT,
                invoice_number INTEGER, 
                debit FLOAT, 
                credit FLOAT,
                customer_rowid INTEGER
                )""")
            
            # Close connection
            conn.commit()
            conn.close() 
        
        def ledger_tab():
            # Create the tab
            self.tab = ttk.Frame(main_window)
            self.tab.pack(fill="both", expand="yes")

            # Add the tab to the notebook and provide a heading
            main_window.add(self.tab, text="Ledger")

        def ledger_treeview():
            # Create a frame for the Treeview
            self.ledger_treeview_frame = ttk.Frame(self.tab)
            self.ledger_treeview_frame.pack(side="bottom", fill="both", padx=10, expand=1)

            # Create a scrollbar for the Treeview
            self.ledger_treeview_scroll = ttk.Scrollbar(self.ledger_treeview_frame)
            self.ledger_treeview_scroll.pack(side="right", fill="y") 

            # Create the Treeview
            self.ledger_treeview = ttk.Treeview(self.ledger_treeview_frame, yscrollcommand=self.ledger_treeview_scroll.set, selectmode="extended") 
            self.ledger_treeview.pack(fill="both", expand="yes")        
            
            # Create the Treeview columns
            self.ledger_treeview['columns'] = ("ID", "Vendor_rowid", "Date", "Invoice_number", "Description", "Account",  "Debit", "Credit")
            
            # Create the Treeview column headings
            self.ledger_treeview.column("#0", width=0, stretch="false")
            self.ledger_treeview.heading("#0", text="")

            self.ledger_treeview.column("ID", width=0, stretch="false") 
            self.ledger_treeview.heading("ID", text="ID")  
            
            self.ledger_treeview.column("Vendor_rowid", width=0, stretch="false")
            self.ledger_treeview.heading("Vendor_rowid", text="Vendor rowid")
            
            self.ledger_treeview.column("Date", minwidth=100, width=100, stretch="false")            
            self.ledger_treeview.heading("Date", text="Date")

            self.ledger_treeview.column("Invoice_number", minwidth=100, width=100, stretch="false")            
            self.ledger_treeview.heading("Invoice_number", text="Invoice Number")       

            self.ledger_treeview.column("Description", minwidth=100, width=100, stretch="false")           
            self.ledger_treeview.heading("Description", text="Description")
            
            self.ledger_treeview.column("Account", minwidth=200, width=200, stretch="false")
            self.ledger_treeview.heading("Account", text="Account") 
            
            self.ledger_treeview.column("Invoice_number", minwidth=100, width=100, stretch="false")            
            self.ledger_treeview.heading("Invoice_number", text="Invoice Number")          
            
            self.ledger_treeview.column("Debit", minwidth=100, width=100, stretch="false")          
            self.ledger_treeview.heading("Debit", text="Debit")    
            
            self.ledger_treeview.column("Credit", minwidth=100, width=100, stretch="false")           
            self.ledger_treeview.heading("Credit", text="Credit")

            # Ledger total box
            # Create frame
            ledger_total_frame = ttk.Frame(self.ledger_treeview_frame)
            ledger_total_frame.pack(fill="both", padx=390, pady=10)

            # Create the boxes
            debit_total_label = ttk.Label(ledger_total_frame, text="Debit Total")
            debit_total_label.grid(row=1, column=1, padx=10)
            self.debit_total_entry = ttk.Entry(ledger_total_frame, width=12)
            self.debit_total_entry.grid(row=1, column=2)
            #self.debit_total_entry.insert(0, "debit total")
            #self.debit_total_entry.configure(state="readonly")

            credit_total_label = ttk.Label(ledger_total_frame, text="Credit Total")
            credit_total_label.grid(row=2, column=1, padx=10)
            self.credit_total_entry = ttk.Entry(ledger_total_frame, width=12)
            self.credit_total_entry.grid(row=2, column=3)
            self.credit_total_entry.insert(0, "credit total")
            self.credit_total_entry.configure(state="readonly")            

        ledger_database_table()
        ledger_tab()
        ledger_treeview()
        self.populate_ledger_tree()

    def populate_ledger_tree(self):  
        # Connect to the database
        conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
        cur = conn.cursor()

        # Clear the treeview
        for record in self.ledger_treeview.get_children():
            self.ledger_treeview.delete(record)

        # Select the rowid and everything in the table and fetch 
        cur.execute("SELECT rowid, * FROM ledger")
        ledger_record = cur.fetchall()    

        # For each row in the table, add the data to the Treeview columns
        global count
        count = 0
        for row in ledger_record:
            self.ledger_treeview.insert(parent='', index='end', iid=count, text='', values=(  
                row[0], # row_id
                row[2], # vendor_rowid
                row[3], # date
                row[6], # invoice_number
                row[4], # description
                row[5], # account
                row[7], # debit
                row[8], # credit
                ))

            count+=1    
        
        # Add the debit and credit total to the window
        cur.execute("SELECT SUM(debit) FROM ledger")
        debit_total = cur.fetchone()
        self.debit_total_entry.configure(state="normal")
        self.debit_total_entry.delete(0, "end")
        self.debit_total_entry.insert(0, debit_total)
        self.debit_total_entry.configure(state="readonly")

        cur.execute("SELECT SUM(credit) FROM ledger")
        credit_total = cur.fetchone()
        self.credit_total_entry.configure(state="normal")
        self.credit_total_entry.delete(0, "end")
        self.credit_total_entry.insert(0, credit_total)
        self.credit_total_entry.configure(state="readonly")

        # Close connection
        conn.commit()
        conn.close()

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
            self.settings_tab = ttk.Frame(main_window)
            self.settings_tab.pack(fill="both")

            # Add the tab to the Notebook
            main_window.add(self.settings_tab, text="Settings")         
        
        settings_database_table()
        settings_tab()
        self.business_address()

    def business_address(self):
        # Create the frame for the business address form
        business_address_frame = ttk.LabelFrame(self.settings_tab, text="Business Address")
        business_address_frame.pack(fill="x", padx=10, pady=10)

        # Add the entry boxes
        company_label = ttk.Label(business_address_frame, text="Company")
        company_label.grid(row=1, column=1, padx=10, pady=5)
        company_entry = ttk.Entry(business_address_frame, width=15, background="white")
        company_entry.grid(row=1, column=2, padx=10, pady=5)
        
        street_label = ttk.Label(business_address_frame, text="Street")
        street_label.grid(row=2, column=1, padx=10, pady=5)
        street_entry = ttk.Entry(business_address_frame, width=15, background="white")
        street_entry.grid(row=2, column=2, padx=10, pady=5)
    
        town_label = ttk.Label(business_address_frame, text="Town")
        town_label.grid(row=3, column=1, padx=10, pady=5)
        town_entry = ttk.Entry(business_address_frame, width=15, background="white")
        town_entry.grid(row=3, column=2, padx=10, pady=5)
        
        city_label = ttk.Label(business_address_frame, text="City")
        city_label.grid(row=4, column=1, padx=10, pady=5)
        city_entry = ttk.Entry(business_address_frame, width=15, background="white")
        city_entry.grid(row=4, column=2, padx=10, pady=5)
        
        county_label = ttk.Label(business_address_frame, text="County")
        county_label.grid(row=5, column=1, padx=10, pady=5)
        county_entry = ttk.Entry(business_address_frame, width=15, background="white")
        county_entry.grid(row=5, column=2, padx=10, pady=5)
        
        postcode_label = ttk.Label(business_address_frame, text="Postcode")
        postcode_label.grid(row=6, column=1, padx=10, pady=5)
        postcode_entry = ttk.Entry(business_address_frame, width=15, background="white")
        postcode_entry.grid(row=6, column=2, padx=10, pady=5)
        
        email_label = ttk.Label(business_address_frame, text="Email")
        email_label.grid(row=7, column=1, padx=10, pady=5)
        email_entry = ttk.Entry(business_address_frame, width=15, background="white")
        email_entry.grid(row=7, column=2, padx=10, pady=5)
        
        phone_label = ttk.Label(business_address_frame, text="Phone")
        phone_label.grid(row=8, column=1, padx=10, pady=5)
        phone_entry = ttk.Entry(business_address_frame, width=15, background="white")
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

            # Select everything from the business address table
            cur.execute("SELECT * FROM settings WHERE rowid = 1")
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
                update_business_address_button = ttk.Button(business_address_frame, text="Update", command=lambda:[update_business_address()])
                update_business_address_button.grid(row=9, column=1, padx=10, pady=5)
            
            # If the table is empty then create a button named save
            else:
                save_business_address_button = ttk.Button(business_address_frame, text="Save", command=lambda:[save_business_address(), populate_business_address()])
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
                    cur.execute('''INSERT INTO settings (  
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
                cur.execute("""UPDATE settings SET 
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
        messagebox.showerror('error', message)
        # Create a window
        #message_window = tk.Toplevel()
        #message_window.title("Message")
        #message_window.attributes('-topmost', 'True')
        
        # Create a frame in the window
        #message_window_frame = ttk.Frame(message_window)
        #message_window_frame.pack(fill="both", expand=1, pady=10)
        
        # Add a message to the frame
        #message = ttk.Label(message_window_frame, text=message)
        #message.pack(side="left", padx=10, pady=10)
        
        # Create a close button
        #close_button = ttk.Button(message_window, text="Close", command=message_window.destroy)
        #close_button.pack(side="bottom", pady=10)


customers = Customers()
vendors = Vendors()
chart_of_accounts = Chart_of_accounts()
ledger = Ledger()
settings = Settings()
menu_bar = Menu_bar()

root.mainloop()

#### Add edit invoice feature ####
#### Update right click options ####
#### Update ribbons ####

#### Process payment ####


#### Import csv ####

