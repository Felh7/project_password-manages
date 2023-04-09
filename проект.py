import tkinter
from tkinter import *
from hashlib import md5

fl =False
flag = False
s = ["", "", ""]
obj=""
def button_click(): #функция для сохранения введенных значений входа
    linkvalue=link.get()
    loginvalue=login.get()
    pasvalue=password.get()
    colour_login = login['fg']
    colour_pas = password['fg']
    colour_link = link['fg']

    # проверяет чтобы ни одно поле не было пустым
    if colour_login != 'grey ' and colour_pas != 'grey' and colour_link != 'grey' and link.flag != False and login.flag != False and password.flag != False :
         if linkvalue != s[0] or loginvalue != s[1] or pasvalue != s[2]:
            with open("text.txt", 'a') as file: # запись в файл данных входа
                file.write(linkvalue + " " + loginvalue + ' ' + pasvalue + "\n")
                s.clear()
                s.append(linkvalue)
                s.append(loginvalue)
                s.append(pasvalue)
                window()

def show_click(): # функция для реализации кнопки сокрытия данных пароля в поле ввода пароля
    if password['fg'] != password.placeholder_colour:
        if password['show'] == '*':
            password['show'] = ''
            eye['text'] = 'hide'
        else:
            password['show'] = '*'
            eye['text'] = 'show'

class Entry_with_placeholder(Entry): #класс чтобы реализовать серые строки в невыбранном поле ввода
    def __init__(self, master = None, placeholder = None):
        super().__init__(master)
        self.flag = True
        if placeholder is not None:
            self.placeholder = placeholder
            self.placeholder_colour = 'grey'
            self.colour = self.placeholder_colour
            self.default_fg_color = self['fg']
            self.bind('<FocusIn>', self.focus_in)
            self.bind('<FocusOut>', self.focus_out)
            self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.colour
        self.flag = False

    def focus_in(self, *args):
        if self['fg'] == self.colour:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
            self.flag = False
    def focus_out(self, *args):
        if not self.get():
            self.put_placeholder()
        else:
            self.flag = True

def button_save(): #функция сохранения секретного слова
    a = en.get()
    b = en1.get()
    if a == b == "": #если поля пусты ничего не делает
        pass
    elif a == b: # записывает хеш секретного слова в файл
        with open("test.txt", "a") as f:
            global obj
            global flag
            flag = True
            obj = md5(a.encode()).hexdigest()
            f.write(obj)
            kill()
            window()

    else:
        wrong_window()

def button_aut(): #сравнение хеша в файле и хеша введенного пользователем слова
    obj2 = enter_sec.get() #полученное значение из поля ввода
    entered_hash = md5(obj2.encode()).hexdigest()
    if entered_hash == obj:
        global fl
        fl = True
        autentification.destroy()
    else:
        window_try_again()

class Entery_secretly(Entry_with_placeholder):
    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.colour
        self['show'] = ''
    def focus_in(self, *args):
        if self['fg'] == self.colour:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
            self.flag = False
            self['show'] = '*'

class window(): #класс окна оповещения об успехе
    def __init__(self):
        succes =Tk()
        succes.geometry('190x70+650+400')
        succes.title("succes")

        self.label = tkinter.Label(succes, text = "данные успешно сохранены")
        self.button = tkinter.Button(succes, text = "закрыть", command = succes.destroy)
        self.label.pack()
        self.button.pack()
        succes.mainloop()
def kill(): # уничтожает окна придумывания слова
    sec.destroy()

class wrong_window():
    def __init__(self):
        wrong = tkinter.Toplevel()
        wrong.title = ("wrong")
        self.label = Label(wrong, text  ="ошибка")
        self.label = tkinter.Label(wrong, text="значения не сходятся")
        self.button = tkinter.Button(wrong, text="закрыть", command=wrong.destroy)
        self.label.pack()
        self.button.pack()

class window_try_again():
    def __init__(self):
        try_more= tkinter.Toplevel()
        try_more.title("try again")

        self.label = Label(try_more, text = "Неверное секретное слово, попробуйте еще раз.")
        self.button = Button(try_more, text = "закрыть", command = try_more.destroy)

        self.label.pack()
        self.button.pack()


if __name__ == "__main__":
    with open("test.txt", "r") as file:
        target = file.readline()
        if target == "":  # если нет записи секретного слова
            sec = Tk()
            lb = Label(sec, text="придумайте секретное слово")
            en = Entry(sec)
            lb2 = Label(sec, text="повторите секретное слово")
            en1 = Entry(sec)

            bt = Button(sec, text="сохранить", command=button_save)

            lb.pack()
            en.pack()
            lb2.pack()
            en1.pack()
            bt.pack()
            sec.mainloop()
        else:
            obj = target
            flag = True
    if flag is True: # флаг чтобы окно аутентификации открылось только после ввода правильного слова на этапе придумываения секретного слова
        autentification = Tk()
        autentification.title("Bakérché")
        lb = Label(autentification, text = "введите секретное слово")
        bt_uat = Button(autentification, text = "ок", command=button_aut)
        enter_sec= Entery_secretly(autentification, "секретное слово")
        eye2 = Button(autentification, command = show_click)
        autentification.geometry('300x200+470+150')

        lb.pack()
        enter_sec.pack()
        bt_uat.pack()
        autentification.mainloop()

    if fl is True:
        root = Tk()
        root.title("Bakérché")
        root.geometry('300x200+470+150')

        link=Entry_with_placeholder(root, "адрес страницы")
        link['width'] = '20'
        login=Entry_with_placeholder(root, "логин")
        password=Entery_secretly(root, "пароль")
        eye = Button(height=1, width=1, text = "show", command = show_click)
        b=Button(root, width= 8,text="сохранить",command=button_click)
        link.grid( row = 1, column = 1 , padx=10)
        login.grid(row = 2, column = 1, padx=10)
        password.grid(row = 3, column = 1, padx=10)
        eye.grid(row = 3, column=2, padx=10)
        b.grid(row = 5, column = 1)

        root.mainloop()
