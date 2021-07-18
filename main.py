# Import modules
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import sqlite3

# Create root
root = ThemedTk(theme='breeze')
root.title("Bookkeeping")
root.geometry("1920x1080")

# Create database
conn = sqlite3.connect('Bookkeeping_Database.sqlite3')

# Create Tkinter Notebook
main_window = ttk.Notebook(root)
main_window.pack(fill="both", expand="yes")

class Customers:

    def __init__(self):
        """
        Creates the Tkinter Notebook tab, tab heading and customer database table
        """
        
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

        def customer_tab():
            # Create the tab
            self.tab = tk.Frame(main_window)
            self.tab.pack(fill="both")
        
            # Add the tab to the notebook and provide a heading
            main_window.add(self.tab, text="Customers")
        
        def customer_ribbon():
            """                 
            Creates the ribbon of fuctional buttons
            """
        
            # Make a frame for the button icons to sit
            customer_ribbon_frame = tk.Frame(self.tab)
            customer_ribbon_frame.pack(fill="x", padx=10, pady=10)

            # Assign an image to each button icon
            self.new_customer_icon = tk.PhotoImage(file="images/new_contact.png")
            self.delete_customer_icon = tk.PhotoImage(file="images/delete_contact.png")
            self.edit_customer_icon = tk.PhotoImage(file="images/edit_contact.png")

            # Add new contact button icon to the frame
            new_customer_contact_button = tk.Button(customer_ribbon_frame, image=self.new_customer_icon, command=self.new_customer)
            new_customer_contact_button.grid(padx=10, row=1, column=1)
            new_customer_contact_label = tk.Label(customer_ribbon_frame, text="Add New Customer")
            new_customer_contact_label.grid(padx=10, row=2, column=1)

            # Add edit contact button icon to the frame
            edit_customer_contact_button = tk.Button(customer_ribbon_frame, image=self.edit_customer_icon, command=self.edit_customer)
            edit_customer_contact_button.grid(padx=10, row=1, column=2)
            edit_customer_contact_label = tk.Label(customer_ribbon_frame, text="Edit Customer")
            edit_customer_contact_label.grid(padx=10, row=2, column=2)

            # Add delete contact button icon to the frame
            delete_customer_contact_button = tk.Button(customer_ribbon_frame, image=self.delete_customer_icon, command=self.delete_customer)
            delete_customer_contact_button.grid(padx=10, row=1, column=3)
            delete_customer_contact_label = tk.Label(customer_ribbon_frame, text="Delete Customer")
            delete_customer_contact_label.grid(padx=10, row=2, column=3)
            
        def customer_treeview():
            """
            Creates a Tkinter Treeview for cutomers
            """

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
        """
        Selects everything in the customer database table and displays it in Treeview
        """

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
                row[0], 
                row[2], 
                row[3], 
                row[4], 
                row[5], 
                row[6], 
                row[7], 
                row[8], 
                row[9], 
                row[10])
                )
            count+=1    

        # Close connection
        conn.commit()
        conn.close() 

    def new_customer(self):
        """
        Opens a new window with the entry boxes used to create a new contact
        """

        # Create a new window and make it sit on top all all other windows
        new_customer_window = tk.Toplevel()
        new_customer_window.title("Add New Contact")
        new_customer_window.attributes()

        # Create a frame in the new window    
        new_customer_window_frame = tk.Frame(new_customer_window)
        new_customer_window_frame.pack(fill="both", expand=1, pady=10)      

        # Add the entry boxes
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

        # Save contact
        new_customer_window_save_button = tk.Button(new_customer_window_frame, text="Save", command=lambda:[save_new_customer()])
        new_customer_window_save_button.grid(row=11, column=1, padx=10, pady=5)

        # Close window
        new_customer_window_close_button = tk.Button(new_customer_window_frame, text="Close", command=new_customer_window.destroy)
        new_customer_window_close_button.grid(row=11, column=2)

        def save_new_customer():
            """
            Takes the data from the entry boxes and adds it to the database table as a new contact
            """
            
            # Connect to database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()
            
            # Make sure the new contact has at least a name. If not, provide a popup window asking for a name.
            if len(new_name_entry.get()) == 0:
                fault_window = tk.Toplevel()
                fault_window.title("Error")
                fault_window.attributes()
                
                fault_window_frame = tk.Frame(fault_window)
                fault_window_frame.pack(fill="both", expand=1, pady=10)
                
                fault = tk.Label(fault_window_frame, text="A new customer must have a name")
                fault.pack(side="left", padx=10, pady=10)
                
                close_button = tk.Button(fault_window, text="Close", command=fault_window.destroy)
                close_button.pack(side="bottom", pady=10)
            
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

    def edit_customer (self):
        """
        Opens a new window with the entry boxes used to edit an existing contact
        """

        # Select the Customer to edit
        selected_customer = self.customer_treeview.focus()
        values_customer = self.customer_treeview.item(selected_customer, 'values') 

        # If a customer is selected then open edit window
        if values_customer:    

            # Create update window
            edit_customer_window = tk.Toplevel()
            edit_customer_window.title("Update Contact")
            edit_customer_window.attributes()

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

            # Save contact 
            close_button = tk.Button(edit_customer_window_frame, text="Save", command=lambda:[update_customer()])
            close_button.grid(row=11, column=1, padx=10, pady=5)

            # Close window
            close_button = tk.Button(edit_customer_window_frame, text="Cancel", command=edit_customer_window.destroy)
            close_button.grid(row=11, column=2)

        # If a customer isn't select tell the user to select one
        else:
            fault_window = tk.Toplevel()
            fault_window.title("Error")
            fault_window.attributes()
             
            fault_window_frame = tk.Frame(fault_window)
            fault_window_frame.pack(fill="both", expand=1, pady=10)
             
            fault = tk.Label(fault_window_frame, text="Please select a contact to edit")
            fault.pack(side="left", padx=10, pady=10)
             
            close_button = tk.Button(fault_window, text="Close", command=fault_window.destroy)
            close_button.pack(side="bottom", pady=10)

        def update_customer():
            """
            Take the data from the entry boxes and update the database of the row selected in the Treeview
            """
        
            # Connect to the database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Make sure the contact has at least a name. If not, show a pop-up window asking for a name
            if len(edit_name_entry.get()) == 0:
                fault_window = tk.Toplevel()
                fault_window.title("Error")
                fault_window.attributes()
                
                fault_window.frame = tk.Frame(fault_window)
                fault_window.frame.pack(fill="both", expand=1, pady=10)
                
                fault = tk.Label(fault_window.frame, text="A customer must have a name")
                fault.pack(side="left", padx=10, pady=10)
                
                close_button = tk.Button(fault_window, text="Close", command=fault_window.destroy)
                close_button.pack(side="bottom", pady=10)
            
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

    def delete_customer (self):
        """
        Delete the row selected in the Treeview from the database
        """

        # Connect to the database
        conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
        cur = conn.cursor()

        # Make the selected item in Treeview the focus and make it a variable called 'selected'
        # Pull the values in 'selected' from the 'values' part of the database
        selected = self.customer_treeview.focus()
        values = self.customer_treeview.item(selected, 'values') 
        
        # If a customer is selected then delete from the database
        if values:
            # Delete the database row(rowid) that has the same rowid as the one selected in the Treeview
            cur.execute("DELETE FROM Customers WHERE rowid = " + values[0])

        # If a customer isn't selected then tell the user to select one         
        else:
            fault_window = tk.Toplevel()
            fault_window.title("Error")
            fault_window.attributes('-topmost', 'true')
             
            fault_window_frame = tk.Frame(fault_window)
            fault_window_frame.pack(fill="both", expand=1, pady=10)
             
            fault_failed = tk.Label(fault_window_frame, text="Please select a contact to delete")
            fault_failed.pack(side="left", padx=10, pady=10)
             
            fault_close_button = tk.Button(fault_window, text="Close", command=fault_window.destroy)
            fault_close_button.pack(side="bottom", pady=10)
   
        # Close connection
        conn.commit()
        conn.close() 

        # Re-populate the Treeview
        self.populate_customer_tree()

class Vendors:

    def __init__(self):
        """
        Creates the Tkinter Notebook tab, tab heading and vendor database table
        """
        
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
            """                 
            Creates the ribbon of fuctional buttons
            """
        
            # Make a frame for the button icons to sit
            vendor_ribbon_frame = tk.Frame(self.tab)
            vendor_ribbon_frame.pack(fill="x", padx=10, pady=10)

            # Assign an image to each button icon
            self.new_vendor_icon = tk.PhotoImage(file="images/new_contact.png")
            self.delete_vendor_icon = tk.PhotoImage(file="images/delete_contact.png")
            self.edit_vendor_icon = tk.PhotoImage(file="images/edit_contact.png")

            # Add new contact button icon to the frame
            new_vendor_contact_button = tk.Button(vendor_ribbon_frame, image=self.new_vendor_icon, command=self.new_vendor)
            new_vendor_contact_button.grid(padx=10, row=1, column=1)
            new_vendor_contact_label = tk.Label(vendor_ribbon_frame, text="Add New Vendor")
            new_vendor_contact_label.grid(padx=10, row=2, column=1)

            # Add edit contact button icon to the frame
            edit_vendor_contact_button = tk.Button(vendor_ribbon_frame, image=self.edit_vendor_icon, command=self.edit_vendor)
            edit_vendor_contact_button.grid(padx=10, row=1, column=2)
            edit_vendor_contact_label = tk.Label(vendor_ribbon_frame, text="Edit Vendor")
            edit_vendor_contact_label.grid(padx=10, row=2, column=2)

            # Add delete contact button icon to the frame
            delete_vendor_contact_button = tk.Button(vendor_ribbon_frame, image=self.delete_vendor_icon, command=self.delete_vendor)
            delete_vendor_contact_button.grid(padx=10, row=1, column=3)
            delete_vendor_contact_label = tk.Label(vendor_ribbon_frame, text="Delete Vendor")
            delete_vendor_contact_label.grid(padx=10, row=2, column=3)
            
        def vendor_treeview():
            """
            Creates a Tkinter Treeview for cutomers
            """

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
        """
        Selects everything in the vendor database table and displays it in Treeview
        """

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
                row[0], 
                row[2], 
                row[3], 
                row[4], 
                row[5], 
                row[6], 
                row[7], 
                row[8], 
                row[9], 
                row[10])
                )
            count+=1    

        # Close connection
        conn.commit()
        conn.close() 

    def new_vendor(self):
        """
        Opens a new window with the entry boxes used to create a new contact
        """

        # Create a new window and make it sit on top all all other windows
        new_vendor_window = tk.Toplevel()
        new_vendor_window.title("Add New Contact")
        new_vendor_window.attributes()

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

        # Save contact
        new_vendor_window_save_button = tk.Button(new_vendor_window_frame, text="Save", command=lambda:[save_new_vendor()])
        new_vendor_window_save_button.grid(row=11, column=1, padx=10, pady=5)

        # Close window
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
                fault_window = tk.Toplevel()
                fault_window.title("Error")
                fault_window.attributes()
                
                fault_window_frame = tk.Frame(fault_window)
                fault_window_frame.pack(fill="both", expand=1, pady=10)
                
                fault = tk.Label(fault_window_frame, text="A new vendor must have a name")
                fault.pack(side="left", padx=10, pady=10)
                
                close_button = tk.Button(fault_window, text="Close", command=fault_window.destroy)
                close_button.pack(side="bottom", pady=10)
            
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

    def edit_vendor (self):
        """
        Opens a new window with the entry boxes used to edit an existing contact
        """

        # Select the vendor to edit
        selected_vendor = self.vendor_treeview.focus()
        values_vendor = self.vendor_treeview.item(selected_vendor, 'values') 

        # If a vendor is selected then open edit window
        if values_vendor:    

            # Create update window
            edit_vendor_window = tk.Toplevel()
            edit_vendor_window.title("Update Contact")
            edit_vendor_window.attributes()

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

            # Save contact 
            close_button = tk.Button(edit_vendor_window_frame, text="Save", command=lambda:[update_vendor()])
            close_button.grid(row=11, column=1, padx=10, pady=5)

            # Close window
            close_button = tk.Button(edit_vendor_window_frame, text="Cancel", command=edit_vendor_window.destroy)
            close_button.grid(row=11, column=2)

        # If a vendor isn't select tell the user to select one
        else:
            fault_window = tk.Toplevel()
            fault_window.title("Error")
            fault_window.attributes()
             
            fault_window_frame = tk.Frame(fault_window)
            fault_window_frame.pack(fill="both", expand=1, pady=10)
             
            fault = tk.Label(fault_window_frame, text="Please select a contact to edit")
            fault.pack(side="left", padx=10, pady=10)
             
            close_button = tk.Button(fault_window, text="Close", command=fault_window.destroy)
            close_button.pack(side="bottom", pady=10)

        def update_vendor():
            """
            Take the data from the entry boxes and update the database of the row selected in the Treeview
            """
        
            # Connect to the database
            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Make sure the contact has at least a name. If not, show a pop-up window asking for a name
            if len(edit_name_entry.get()) == 0:
                fault_window = tk.Toplevel()
                fault_window.title("Error")
                fault_window.attributes()
                
                fault_window.frame = tk.Frame(fault_window)
                fault_window.frame.pack(fill="both", expand=1, pady=10)
                
                fault = tk.Label(fault_window.frame, text="A vendor must have a name")
                fault.pack(side="left", padx=10, pady=10)
                
                close_button = tk.Button(fault_window, text="Close", command=fault_window.destroy)
                close_button.pack(side="bottom", pady=10)
            
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

    def delete_vendor (self):
        """
        Delete the row selected in the Treeview from the database
        """

        # Connect to the database
        conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
        cur = conn.cursor()

        # Make the selected item in Treeview the focus and make it a variable called 'selected'
        # Pull the values in 'selected' from the 'values' part of the database
        selected = self.vendor_treeview.focus()
        values = self.vendor_treeview.item(selected, 'values') 
        
        # If a vendor is selected then delete from the database
        if values:
            # Delete the database row(rowid) that has the same rowid as the one selected in the Treeview
            cur.execute("DELETE FROM vendors WHERE rowid = " + values[0])

        # If a vendor isn't selected then tell the user to select one         
        else:
            fault_window = tk.Toplevel()
            fault_window.title("Error")
            fault_window.attributes('-topmost', 'true')
             
            fault_window_frame = tk.Frame(fault_window)
            fault_window_frame.pack(fill="both", expand=1, pady=10)
             
            fault_failed = tk.Label(fault_window_frame, text="Please select a contact to delete")
            fault_failed.pack(side="left", padx=10, pady=10)
             
            fault_close_button = tk.Button(fault_window, text="Close", command=fault_window.destroy)
            fault_close_button.pack(side="bottom", pady=10)
   
        # Close connection
        conn.commit()
        conn.close() 

        # Re-populate the Treeview
        self.populate_vendor_tree()

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
            """ 
            Creates the ribbon and functional buttons
            """

            # Make a frame for the ribbon on the tab
            accounts_ribbon_frame = tk.Frame(self.tab)
            accounts_ribbon_frame.pack(fill="x", padx=10, pady=10)
        
            # Assign an image to each button icon
            self.new_account_icon = tk.PhotoImage(file="images/new_account.png")
            self.new_child_account_icon = tk.PhotoImage(file="images/new_child_account.png")
            self.delete_account_icon = tk.PhotoImage(file="images/delete_account.png")
            self.edit_account_icon = tk.PhotoImage(file="images/edit_account.png")

            # Add "new account" button icon to the frame and give it a command
            new_account_button = tk.Button(accounts_ribbon_frame, image=self.new_account_icon, command=self.new_parent_account)
            new_account_button.grid(padx=10, row=1, column=1)

            new_account_label = tk.Label(accounts_ribbon_frame, text="Add New Account")
            new_account_label.grid(padx=10, row=2, column=1)

            # Add " add child account" button icon to the frame and give it a command
            new_child_account_button = tk.Button(accounts_ribbon_frame, image=self.new_child_account_icon, command=self.child_account)
            new_child_account_button.grid(padx=10, row=1, column=2)

            new_child_account_label = tk.Label(accounts_ribbon_frame, text="Add Child Account")
            new_child_account_label.grid(padx=10, row=2, column=2)

            # Add "edit account" button icon to the frame and give it a command
            edit_account_button = tk.Button(accounts_ribbon_frame, image=self.edit_account_icon)
            edit_account_button.grid(padx=10, row=1, column=3)

            edit_account_label = tk.Label(accounts_ribbon_frame, text="Edit Account")
            edit_account_label.grid(padx=10, row=2, column=3)

            # Add "delete account" button icon to the frame and give it a command
            delete_account_button = tk.Button(accounts_ribbon_frame, image=self.delete_account_icon)
            delete_account_button.grid(padx=10, row=1, column=4)

            delete_account_label = tk.Label(accounts_ribbon_frame, text="Delete Account")
            delete_account_label.grid(padx=10, row=2, column=4)
            
        def accounts_treeview():
            """
            Creates a Treeview in the tab. Adds a scrollbar to the Treeview, columns, and column headings.
            """          

            # Create a frame for the Treeview
            self.accounts_treeview_frame = tk.Frame(self.tab)
            self.accounts_treeview_frame.pack(fill="both", padx=10, expand=1)

            # Create a scrollbar for the Treeview
            self.accounts_treeview_scroll = tk.Scrollbar(self.accounts_treeview_frame)
            self.accounts_treeview_scroll.pack(side="right", fill="y") 

            # Create the Treeview
            self.accounts_treeview = ttk.Treeview(self.accounts_treeview_frame, yscrollcommand=self.accounts_treeview_scroll.set, selectmode="extended") 
            self.accounts_treeview.pack(fill="both", expand="yes")        
            
            # Create the Treeview columns
            self.accounts_treeview['columns'] = ("ID", "Account Number", "Type", "Account Name", "Total", "Parent", "Child")
            
            # Create the Treeview column headings
            self.accounts_treeview.column("#0", minwidth=0, width=0, stretch="false")
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
            self.accounts_treeview.insert(parent='', index='end', iid=row[2], text='', values=(
                row[0], 
                row[2], 
                row[7],
                row[3], 
                row[4], 
                row[2], 
                row[6]
                ))
        
        # For each row in the child table, add the data to the Treeview columns
        for row in child_record:
            self.tab_tree.insert(parent=row[5], index='end', iid=row[2], text='', values=(
                row[0], 
                row[2], 
                row[7],
                row[3], 
                row[4], 
                row[5], 
                row[6]
                ))

        # Close connection
        conn.commit()
        conn.close() 

    def new_parent_account(self):

        """
        Opens a new window with the entry boxes used to create a new account
        """

        # Create window and add a frame
        new_account_window = tk.Toplevel()
        new_account_window.title("Add New Account")
        #new_account_window.attributes('-topmost', 'true')
            
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

            # Make sure the new account has a number. If not, provide a popup window asking for a number.    
            if len(new_account_number_entry.get()) == 0:
                fault_window = tk.Toplevel()
                fault_window.title("Error")
                fault_window.attributes('-topmost', 'true')
                
                fault_window.frame = tk.Frame(fault_window)
                fault_window.frame.pack(fill="both", expand=1, pady=10)
                
                fault = tk.Label(fault_window.frame, text="A new account must have an Account Number, Name and account type")
                fault.pack(side="left", padx=10, pady=10)
                
                close_button = tk.Button(fault_window, text="Close", command=fault_window.destroy)
                close_button.pack(side="bottom", pady=10)    

            # Make sure the new account has a name. If not, provide a popup window asking for a name.
            elif len(new_account_name_entry.get()) == 0:
                fault_window = tk.Toplevel()
                fault_window.title("Error")
                fault_window.attributes('-topmost', 'true')
                
                fault_window.frame = tk.Frame(fault_window)
                fault_window.frame.pack(fill="both", expand=1, pady=10)
                
                fault = tk.Label(fault_window.frame, text="A new account must have an Account Number, Name and account type")
                fault.pack(side="left", padx=10, pady=10)
                
                close_button = tk.Button(fault_window, text="Close", command=fault_window.destroy)
                close_button.pack(side="bottom", pady=10)      
            
            # Make sure the new account has an account type selected
            elif new_account_type_entry.get() != "Bank" and new_account_type_entry.get() != "Cash" and new_account_type_entry.get() != "Income" and new_account_type_entry.get() != "Expenses":
                fault_window = tk.Toplevel()
                fault_window.title("Error")
                fault_window.attributes('-topmost', 'true')
                
                fault_window.frame = tk.Frame(fault_window)
                fault_window.frame.pack(fill="both", expand=1, pady=10)
                
                fault = tk.Label(fault_window.frame, text="A new account must have an Account Number, Name and account type")
                fault.pack(side="left", padx=10, pady=10)
                
                close_button = tk.Button(fault_window, text="Close", command=fault_window.destroy)
                close_button.pack(side="bottom", pady=10)       

            # If the new account has a name and number insert into database...
            else:
                if len(new_account_number_entry.get() and new_account_name_entry.get()) != 0:
                    # Check to see if the account number is in use already. Attempt to make an account number list from the database using the account number in the entry box        
                    cur.execute("SELECT account_number FROM parent_accounts WHERE account_number = " + new_account_number_entry.get() + "")
                    parent_account_number_query = cur.fetchone()
                    cur.execute("SELECT account_number FROM child_accounts WHERE account_number = " + new_account_number_entry.get() + "")
                    child_account_number_query = cur.fetchone()

                    # If of the lists exist (True), ie account number is in the database tell the user the account number is in use.
                    if parent_account_number_query:
                        fault_window = tk.Toplevel()
                        fault_window.title("Error")
                        fault_window.attributes('-topmost', 'true')
                        
                        fault_window.frame = tk.Frame(fault_window)
                        fault_window.frame.pack(fill="both", expand=1, pady=10)
                        
                        fault = tk.Label(fault_window.frame, text="That account number is in use already")
                        fault.pack(side="left", padx=10, pady=10)
                        
                        close_button = tk.Button(fault_window, text="Close", command=fault_window.destroy)
                        close_button.pack(side="bottom", pady=10)    
                    
                    elif child_account_number_query:
                        fault_window = tk.Toplevel()
                        fault_window.title("Error")
                        fault_window.attributes('-topmost', 'true')
                        
                        fault_window.frame = tk.Frame(self.window)
                        fault_window.frame.pack(fill="both", expand=1, pady=10)
                        
                        fault = tk.Label(fault_window.frame, text="That account number is in use already")
                        fault.pack(side="left", padx=10, pady=10)
                        
                        close_button = tk.Button(fault_window, text="Close", command=fault_window.destroy)
                        close_button.pack(side="bottom", pady=10)         
                        
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

            # Re=populate the Treeview
            self.populate_accounts_tree()
        
    def new_child_account(self):
        """
        Opens a new window with the entry boxes used to create a new account
        """

        # Make the selected item in Treeview the focus and make it a variable called 'selected'
        # Pull the values in 'selected' from the 'values' part of the database
        self.selected = self.tab_tree.focus()
        self.selected_account = self.tab_tree.item(self.selected, 'values') 
        
        if self.selected_account:
            # Create window and add a frame
            self.child_account_window = Toplevel()
            self.child_account_window.title("Add Child Account")
            self.child_account_window.attributes('-topmost', 'true')
                
            self.child_account_window_frame = Frame(self.child_account_window)
            self.child_account_window_frame.pack(fill="both", expand=1, pady=10)      

            # Create the entry boxes
            self.child_account_id_label = Label(self.child_account_window_frame, text="ID")
            #self.child_account_id_label.grid(row=1, column=1, padx=10, pady=5)
            self.child_account_id_entry = Entry(self.child_account_window_frame, width=15)
            #self.child_account_id_entry.grid(row=1, column=2, padx=10, pady=5)
            
            self.child_account_number_label = Label(self.child_account_window_frame, text="Account Number")
            self.child_account_number_label.grid(row=2, column=1, padx=10, pady=5)
            self.child_account_number_entry = Entry(self.child_account_window_frame, width=15)
            self.child_account_number_entry.grid(row=2, column=2, padx=10, pady=5)

            self.child_account_name_label = Label(self.child_account_window_frame, text="Account Name")
            self.child_account_name_label.grid(row=3, column=1, padx=10, pady=5)
            self.child_account_name_entry = Entry(self.child_account_window_frame, width=15)
            self.child_account_name_entry.grid(row=3, column=2, padx=10, pady=5)    

            self.child_account_total_label = Label(self.child_account_window_frame, text="Total")
            #self.child_account_total_label.grid(row=4, column=1, padx=10, pady=5)
            self.child_account_total_entry = Entry(self.child_account_window_frame, width=15)
            #self.child_account_total_entry.grid(row=4, column=2, padx=10, pady=5)       

            self.child_parent_account_label = Label(self.child_account_window_frame, text="Parent")
            self.child_parent_account_label.grid(row=5, column=1, padx=10, pady=5)
            self.child_parent_account_entry = Entry(self.child_account_window_frame, width=15)
            self.child_parent_account_entry.grid(row=5, column=2, padx=10, pady=5)     

            self.child_child_account_status_label = Label(self.child_account_window_frame, text="Child Account?")
            #self.child_child_account_status_label.grid(row=6, column=1, padx=10, pady=5)
            self.child_child_account_status_entry = Entry(self.child_account_window_frame, width=15)
            #self.child_child_account_status_entry.grid(row=6, column=2, padx=10, pady=5)

            self.child_account_type_label = Label(self.child_account_window_frame, text="Type")
            self.child_account_type_label.grid(row=7, column=1, padx=10, pady=5)
            self.child_account_type_entry = Entry(self.child_account_window_frame, width=15)
            self.child_account_type_entry.grid(row=7, column=2, padx=10, pady=5)

            # Using the account number and account type of the selected account as the parent account number and account type, insert the account number and account type into the entry boxes
            self.child_parent_account_entry.insert(0, self.selected_account[1])
            self.child_account_type_entry.insert(0,self.selected_account[2])
            
            # Make account type and parent account number read-only
            self.child_account_type_entry.config(state='readonly')
            self.child_parent_account_entry.config(state='readonly')

            # Save contact and close window
            self.close_button = Button(self.child_account_window_frame, text="Save", command=lambda:[self.child_account(), self.child_account_window.destroy()])
            self.close_button.grid(row=8, column=1)

            # Close window
            self.close_button = Button(self.child_account_window_frame, text="Close", command=self.child_account_window.destroy)
            self.close_button.grid(row=8, column=2)    

        # If a parent account hasn't been selected tell the user to choose a parent account. 
        else:
            self.window = Toplevel()
            self.window.title("Error")
            self.window.attributes('-topmost', 'true')
            
            self.window_frame = Frame(self.window)
            self.window_frame.pack(fill="both", expand=1, pady=10)
            
            self.failed = Label(self.window_frame, text="Please select a parent account first")
            self.failed.pack(side=LEFT, padx=10, pady=10)
            
            self.close_button = Button(self.window, text="Close", command=self.window.destroy)
            self.close_button.pack(side=BOTTOM, pady=10)
        
        def child_account(self):
            """
            Creates a new account but as a child to an existing account
            """

            conn = sqlite3.connect('Bookkeeping_Database.sqlite3')
            cur = conn.cursor()

            # Pull the data from the entry boxes and store them in a list called 'inputted_data'. "YES" is to signal that it's a child account.
            inputted_data = [self.child_account_number_entry.get(), self.child_account_name_entry.get(), self.child_parent_account_entry.get(), "YES", self.child_account_type_entry.get()]

            # Make sure the new account has a number. If not, provide a popup window asking for a number. 
            if len(self.child_account_number_entry.get()) == 0:
                self.window = Toplevel()
                self.window.title("Error")
                self.window.attributes('-topmost', 'true')
                
                self.window.frame = Frame(self.window)
                self.window.frame.pack(fill="both", expand=1, pady=10)
                
                self.failed = Label(self.window.frame, text="A new " + self.button_info + " must have an Account Number and Name")
                self.failed.pack(side=LEFT, padx=10, pady=10)
                
                self.close_button = Button(self.window, text="Close", command=self.window.destroy)
                self.close_button.pack(side=BOTTOM, pady=10)    

            # Make sure the new account has a name. If not, provide a popup window asking for a name. 
            elif len(self.child_account_name_entry.get()) == 0:
                self.window = Toplevel()
                self.window.title("Error")
                self.window.attributes('-topmost', 'true')
                
                self.window.frame = Frame(self.window)
                self.window.frame.pack(fill="both", expand=1, pady=10)
                
                self.failed = Label(self.window.frame, text="A new " + self.button_info + " must have an Account Number and Name")
                self.failed.pack(side=LEFT, padx=10, pady=10)
                
                self.close_button = Button(self.window, text="Close", command=self.window.destroy)
                self.close_button.pack(side=BOTTOM, pady=10) 

            # Make sure the new account has a parent account number. If not, provide a pop-up window asking for a parent account to be selected. 
            elif len(self.child_parent_account_entry.get()) == 0:
                
                self.window = Toplevel()
                self.window.title("Error")
                self.window.attributes('-topmost', 'true')
                
                self.window.frame = Frame(self.window)
                self.window.frame.pack(fill="both", expand=1, pady=10)
                
                self.failed = Label(self.window.frame, text="Please select a parent account first")
                self.failed.pack(side=LEFT, padx=10, pady=10)
                
                self.close_button = Button(self.window, text="Close", command=self.window.destroy)
                self.close_button.pack(side=BOTTOM, pady=10)
            
            # If the parent account chosen is already a child account tell the user that a child account cannot be a parent account
            elif self.selected_account[5] == "YES":
                self.window = Toplevel()
                self.window.title("Error")
                self.window.attributes('-topmost', 'true')
                
                self.window.frame = Frame(self.window)
                self.window.frame.pack(fill="both", expand=1, pady=10)
                
                self.failed = Label(self.window.frame, text="You cannot have a child account of a child account")
                self.failed.pack(side=LEFT, padx=10, pady=10)
                
                self.close_button = Button(self.window, text="Close", command=self.window.destroy)
                self.close_button.pack(side=BOTTOM, pady=10)

            # If the new account has an account number, name and parent account then add to database
            elif len(self.child_account_number_entry.get() and self.child_account_name_entry.get() and self.child_parent_account_entry.get()) != 0: 

                # Check to see if the account number is in use already. Attempt to make an account number list from the database using the account number in the entry box        
                cur.execute("SELECT account_number FROM Accounts WHERE account_number = " + self.child_account_number_entry.get() + "")
                parent_account_number_query = cur.fetchone()
                cur.execute("SELECT account_number FROM Child_Accounts WHERE account_number = " + self.child_account_number_entry.get() + "")
                child_account_number_query = cur.fetchone()

                # If the list exists (True), ie account number is in the database tell the user the account number is in use.
                if parent_account_number_query:
                    self.window = Toplevel()
                    self.window.title("Error")
                    self.window.attributes('-topmost', 'true')
                    
                    self.window.frame = Frame(self.window)
                    self.window.frame.pack(fill="both", expand=1, pady=10)
                    
                    self.failed = Label(self.window.frame, text="That account number is already in use")
                    self.failed.pack(side=LEFT, padx=10, pady=10)
                    
                    self.close_button = Button(self.window, text="Close", command=self.window.destroy)
                    self.close_button.pack(side=BOTTOM, pady=10)  

                # If the list exists (True), ie account number is in the database tell the user the account number is in use.
                if child_account_number_query:
                    self.window = Toplevel()
                    self.window.title("Error")
                    self.window.attributes('-topmost', 'true')
                    
                    self.window.frame = Frame(self.window)
                    self.window.frame.pack(fill="both", expand=1, pady=10)
                    
                    self.failed = Label(self.window.frame, text="That account number is already in use")
                    self.failed.pack(side=LEFT, padx=10, pady=10)
                    
                    self.close_button = Button(self.window, text="Close", command=self.window.destroy)
                    self.close_button.pack(side=BOTTOM, pady=10)   

                # If the list doesn't exist (False), add the contents of the entry boxes to the database
                else:
                    # Add contents of entry boxes to the database
                    cur.execute("INSERT INTO Child_Accounts (account_number, account_name, total, parent, child, type) VALUES (?, ?, 0.00, ?, ?, ?)", inputted_data)

            # Close connection
            conn.commit()
            conn.close()    

            # Re-populate the Treeview      
            self.populate_accounts_tree()
            
Customers()
Vendors()
Chart_of_accounts()

root.mainloop()


################## Add child account #######################
################## Make class for fault window???? ########