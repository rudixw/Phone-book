import sqlite3                   
from tkinter import *            
from tkinter import messagebox




class DB:                        
    def __init__(self):           
        self.conn = sqlite3.connect("mybooks.db")  
        self.cur = self.conn.cursor()    
        self.cur.execute(             
            "CREATE TABLE IF NOT EXISTS buy (id INTEGER PRIMARY KEY, product TEXT, price TEXT, comment TEXT)") 
        self.conn.commit()  


    def __del__(self):        
        self.conn.close()   
   
    def view(self):        

        self.cur.execute("SELECT * FROM buy") 
        rows = self.cur.fetchall()  
        return rows


    def insert(self, product, price, comment):  
        self.cur.execute("INSERT INTO buy VALUES (NULL,?,?,?)", (product, price, comment,)) 
        self.conn.commit()
        


    def update(self, id, product, price):    
        self.cur.execute("UPDATE buy SET product=?, price=? WHERE id=?", (product, price, id,))
        self.conn.commit()


    def delete(self, id):                  
        self.cur.execute("DELETE FROM buy WHERE id=?", (id,))
        self.conn.commit()


    def search(self, product="", price=""):  
        self.cur.execute("SELECT * FROM buy WHERE product=?", (product,))
        rows = self.cur.fetchall()
        return rows


db = DB()  

def get_selected_row(event): 
   
    global selected_tuple
    index = list1.curselection()[0] 
    selected_tuple = list1.get(index) 
    e1.delete(0, END)                
    e1.insert(END, selected_tuple[1]) 
    e2.delete(0, END)
    e2.insert(END, selected_tuple[2]) 
    e3.delete(0, END)
    e3.insert(END, selected_tuple[3]) 

def view_command():         
    list1.delete(0, END)    
    for row in db.view():   
        list1.insert(END, row)  


def search_command():       
    list1.delete(0, END)   
    for row in db.search(product_text.get()):
        list1.insert(END, row) 

def add_command():         
    db.insert(product_text.get(), price_text.get(), comment_text.get()) 
    view_command()

def delete_command(): 
    db.delete(selected_tuple[0]) 
    view_command()


def update_command():

    db.update(selected_tuple[0], product_text.get(), price_text.get()) 
    view_command()

window = Tk() 

window.title("Телефонная книга") 
icon = PhotoImage(file = "dddd.png")
window.iconphoto(False, icon)

def on_closing(): 
    if messagebox.askokcancel("", "Закрыть программу?"): 
        window.destroy()
        

window.protocol("WM_DELETE_WINDOW", on_closing)  

l1 = Label(window, text="Имя") 
l1.grid(row=0, column=0) 

l2 = Label(window, text="Номер +993")
l2.grid(row=0, column=2)

l3 = Label(window, text="Адресс")
l3.grid(row=1, column=0)


product_text = StringVar()
e1 = Entry(window, textvariable=product_text)
e1.grid(row=0, column=1)

price_text = StringVar() 
e2 = Entry(window, textvariable=price_text)
e2.grid(row=0, column=3)

comment_text = StringVar() 
e3 = Entry(window, textvariable=comment_text)
e3.grid(row=1, column=1)


list1 = Listbox(window, height=25, width=65) 
list1.grid(row=2, column=0, rowspan=6, columnspan=2) 


sb1 = Scrollbar(window) 
sb1.grid(row=2, column=2, rowspan=6)


list1.configure(yscrollcommand=sb1.set) 
sb1.configure(command=list1.yview)


list1.bind('<<ListboxSelect>>', get_selected_row)


b1 = Button(window, text="Посмотреть все", width=12, command=view_command) 
b1.grid(row=2, column=3) 

b2 = Button(window, text="Поиск", width=12, command=search_command)
b2.grid(row=3, column=3)

b3 = Button(window, text="Добавить", width=12, command=add_command)
b3.grid(row=4, column=3)

b4 = Button(window, text="Обновить", width=12, command=update_command)
b4.grid(row=5, column=3)

b5 = Button(window, text="Удалить", width=12, command=delete_command)
b5.grid(row=6, column=3)

b6 = Button(window, text="Закрыть", width=12, command=on_closing)
b6.grid(row=7, column=3)

view_command()

window.mainloop() 