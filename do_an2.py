import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql


class DatabaseApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Database App")

        # Database connection fields
        self.db_name = tk.StringVar(value='dbtest')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='0')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='sinhvien')

        # Create the GUI elements
        self.create_widgets()
    
    
    def create_widgets(self):
         # Create Notebook widget
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        # Tab 1: Connection section
        connection_frame = tk.Frame(self.notebook, bg="#ADD8E6")
        self.notebook.add(connection_frame, text='Đăng Nhập')

        tk.Label(connection_frame, text="DB Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(connection_frame, text="User:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)
        tk.Label(connection_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.password, show="*").grid(row=2, column=1, padx=5, pady=5)
        tk.Label(connection_frame, text="Host:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.host).grid(row=3, column=1, padx=5, pady=5)
        tk.Label(connection_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.port).grid(row=4, column=1, padx=5, pady=5)
        tk.Button(connection_frame, text="Connect", command=self.connect_db).grid(row=5, columnspan=2, pady=10)

        # Tab 2: Query and Insert section
        query_frame = tk.Frame(self.notebook , bg="#ADD8E6")
        self.notebook.add(query_frame, text='Thông tin')

        insert_frame3 = tk.LabelFrame(query_frame, text='Load Data')
        insert_frame3.grid(row=1, column=0, columnspan=2, pady=10, sticky=tk.W)
        
        tk.Label(insert_frame3, text="Table Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(insert_frame3, textvariable=self.table_name).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(insert_frame3, text="Load Data", command=self.load_data).grid(row=1, column=0, pady=10)

        self.tree = ttk.Treeview(query_frame, columns=( 'stt','Ho ten','mssv'), show='headings', height=10)
        self.tree.column('stt', width=50, anchor='center')
        self.tree.column('mssv', width=140, anchor='w')
        self.tree.column('Ho ten', width=230, anchor='w')
        self.tree.heading('stt', text='stt')
        self.tree.heading('mssv', text='mssv')
        self.tree.heading('Ho ten', text='Ho ten')
        self.tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Tab 2: Insert section
        
        insert_frame1 = tk.LabelFrame(query_frame, text='Insert Data')
        insert_frame1.grid(row=4, column=0, columnspan=2, pady=10, sticky=tk.W)

        self.column1 = tk.StringVar()
        self.column2 = tk.StringVar()

        tk.Label(insert_frame1, text="Ho ten:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(insert_frame1, textvariable=self.column1).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(insert_frame1, text="mssv:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(insert_frame1, textvariable=self.column2).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(insert_frame1, text="Insert Data", command=self.insert_data).grid(row=2, column=0, padx=5, pady=5)


        # Search and Delete section
        insert_frame2 = tk.LabelFrame(query_frame, text='Search and Delete Data')
        insert_frame2.grid(row=5, column=0, columnspan=3, pady=10, sticky=tk.W)

        tk.Label(insert_frame2, text="MSSV:").grid(row=0, column=0, padx=5, pady=5)
        self.mssv_entry = tk.Entry(insert_frame2)
        self.mssv_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(insert_frame2, text="Search", command=self.search_data).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(insert_frame2, text="Delete", command=self.delete_data).grid(row=0, column=3, padx=5, pady=5)
        
        

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),   
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Connected to the database successfully!")
            self.notebook.select(1)
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to the database: {e}")

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            print("Query Results:", rows) 
            self.tree.delete(*self.tree.get_children()) 
    
            for idx, row in enumerate(rows, start=1):
                print("Row Data:", row) 
                self.tree.insert('', 'end', values=(idx, row[0], row[1])) 
    
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")

        
    def insert_data(self):
        try:
            insert_query = sql.SQL("INSERT INTO {} (hoten, mssv) VALUES (%s, %s)").format(sql.Identifier(self.table_name.get()))
            data_to_insert = (self.column1.get(), self.column2.get())
            self.cur.execute(insert_query, data_to_insert)
            self.conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")
    
    def search_data(self):
        try:
            search_query = sql.SQL("SELECT * FROM {} WHERE mssv = %s").format(sql.Identifier(self.table_name.get()))
            mssv_to_search = self.mssv_entry.get().strip()  
            self.cur.execute(search_query, (mssv_to_search,))
            rows = self.cur.fetchall()
            self.tree.delete(*self.tree.get_children()) 
    
            if rows:
                for idx, row in enumerate(rows, start=1):
                    self.tree.insert('', 'end', values=(idx, row[0], row[1]))  
            else:
                messagebox.showinfo("Info", "No records found for the given mssv.")
    
        except Exception as e:
            messagebox.showerror("Error", f"Error searching data: {e}")


    def delete_data(self):
        try:
            # Search for the mssv
            search_query = sql.SQL("SELECT * FROM {} WHERE mssv = %s").format(sql.Identifier(self.table_name.get()))
            mssv_to_search = self.mssv_entry.get()
            self.cur.execute(search_query, (mssv_to_search,))
            rows = self.cur.fetchall()

            if not rows:
                messagebox.showinfo("Info", "No records found to delete.")
                return

        # Delete the mssv
            delete_query = sql.SQL("DELETE FROM {} WHERE mssv = %s").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(delete_query, (mssv_to_search,))
            self.conn.commit()
    
            # Display the result
            self.tree.delete(*self.tree.get_children())
            messagebox.showinfo("Success", f"Record with mssv {mssv_to_search} deleted successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error deleting data: {e}")
if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()