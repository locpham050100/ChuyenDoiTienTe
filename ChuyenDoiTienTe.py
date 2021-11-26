import requests
from tkinter import*
import tkinter as tk
from tkinter import ttk

# tao lop chuyen doi tien te
class RealTimeCurrencyConverter():

    def __init__(self, url):
            self.data = requests.get(url).json()
            self.currencies = self.data['rates']

    # phuong thuc doi
    def convert(self, from_currency, to_currency, amount):
        
        initial_amount = amount
        
        # dau tien chuyen doi thanh USD neu dau vao khong phai la USD
        # vi tien USD duoc chon lam chuan ti gia hoi doi
        if from_currency != 'USD': 
            amount = amount / self.currencies[from_currency]
        
        # gioi han co 4 chu so thap phan
        amount = round(amount * self.currencies[to_currency], 4)
        return amount 

# tao giao dien nguoi dung
class App(tk.Tk):

    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.currency_converter = converter 
        self.configure(background = 'pink')
        self.geometry("500x200")

        # label
        self.intro_label = Label(self, text = 'Chào bạn đến với Công Cụ Đổi Tiền', fg = 'blue', relief = tk.RAISED, borderwidth = 3)
        self.intro_label.config(font = ('Courier', 15, 'bold'))
        self.data_label = Label(self, text = f"1 USA Dollar equals = {self.currency_converter.convert('USD', 'VND', 1)} VND \n Ngày: {self.currency_converter.data['date']}", relief = tk.GROOVE, borderwidth = 5)
        self.intro_label.place(x = 50, y = 5)
        self.data_label.place(x = 170, y = 50)

        # o nhap
        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        # restrictNumberOnly ham se gioi han nguoi dung nhap so khong hop le
        # dinh nghia ham bang doan code duoi day
        self.amount_field = Entry(self, bd = 3, relief = tk.RIDGE, justify = tk.CENTER, validate = 'key', validatecommand = valid)
        self.converted_amount_field_label = Label(self, text = '', fg = 'black', bg = 'white', relief = tk.RIDGE, justify = tk.CENTER, width = 17, borderwidth = 3)

        # thanh cuon 
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("VND") # dat gia tri mac dinh
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("USD")

        font = ("Courier", 12, "bold")
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable = self.from_currency_variable, values = list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 12, justify = tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable = self.to_currency_variable, values=list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 12, justify = tk.CENTER)

        # dat vao giao dien
        self.from_currency_dropdown.place(x = 30, y = 120)
        self.amount_field.place(x = 36, y = 150)
        self.to_currency_dropdown.place(x = 340, y = 120)
        self.converted_amount_field_label.place(x = 346, y = 150)

        # nut chuyen doi
        self.convert_button = Button(self, text = "Chuyển Đổi", fg = "black", command = self.perform)
        self.convert_button.config(font = ('Courier', 10, 'bold'))
        self.convert_button.place(x = 225, y = 135)

    # phuong thuc lay dl nhap nguoi dung va chuyen thanh tien mong muon va hien thi tren hop nhap so
    def perform(self):
        amount = float(self.amount_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()

        converted_amount = self.currency_converter.convert(from_curr, to_curr, amount)
        converted_amount = round(converted_amount, 2)

        self.converted_amount_field_label.config(text = str(converted_amount))

    # ham gioi han ki tu nguoi dung nhap vao
    def restrictNumberOnly(self, action, string):
        regex = action.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return (string == "" or (string.count('.') <= 1 and result is not None ))

if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url)

    App(converter)
    mainloop()
    

























        