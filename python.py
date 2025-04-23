import tkinter as tk
from tkinter import messagebox, font
from tkinter import ttk
from ttkthemes import ThemedTk  # Для использования тем
import random
import string
import pyperclip

# Глобальные настройки
BG_COLOR = "#2f2f2f"  # Основной фон (тёмно-серый)
TEXT_COLOR = "#cccccc"  # Цвет текста (светло-серый)
BUTTON_BG = "#4f4f4f"  # Фон кнопок
LISTBOX_BG = "#3f3f3f"  # Фон списка паролей
LISTBOX_SELECT_BG = "#4f4f4f"  # Цвет выделения в списке
FONT_FAMILY = "Segoe UI"  # Шрифт
FONT_SIZE = 12  # Размер шрифта

# Функция для генерации пароля
def generate_password():
    try:
        length = int(length_entry.get())
        if length <= 0:
            messagebox.showerror("Ошибка", "Длина пароля должна быть больше 0!")
            return
        
        # Генерация пароля
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        
        # Отображение пароля
        password_label.config(text=password)
        
        # Сохранение пароля в список
        previous_passwords.append(password)
        update_previous_passwords_list()
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное число для длины пароля!")

# Функция для копирования текущего пароля
def copy_current_password(event=None):
    password = password_label.cget("text")
    if password:
        try:
            pyperclip.copy(password)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось скопировать пароль: {e}")

# Функция для копирования пароля из списка
def copy_previous_password(event):
    try:
        selected_index = previous_passwords_listbox.curselection()
        if selected_index:
            password = previous_passwords_listbox.get(selected_index)
            pyperclip.copy(password)
            messagebox.showinfo("Успех", "Предыдущий пароль скопирован в буфер обмена!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось скопировать пароль: {e}")

# Функция для очистки списка паролей
def clear_previous_passwords():
    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить список паролей?"):
        previous_passwords.clear()
        update_previous_passwords_list()

# Функция для обновления списка паролей
def update_previous_passwords_list():
    previous_passwords_listbox.delete(0, tk.END)
    for pwd in previous_passwords:
        previous_passwords_listbox.insert(tk.END, pwd)

# Создание основного окна
try:
    root = ThemedTk(theme="equilux")  # Тема "equilux" — серая тема
except Exception as e:
    print(f"Ошибка при загрузке темы: {e}")
    root = tk.Tk()  # Если тема не загружается, используем стандартный Tkinter

root.title("Генератор паролей")
root.geometry("500x650")
root.resizable(False, False)
root.configure(bg=BG_COLOR)  # Устанавливаем фон окна

# Установка иконки (проверяем, существует ли файл)
try:
    root.iconbitmap("snow.ico")  # Путь к файлу иконки
except Exception as e:
    print(f"Иконка не загружена: {e}")

# Настройка стилей для ttk
style = ttk.Style()
style.theme_use("equilux")  # Принудительно используем тему equilux
style.configure("TFrame", background=BG_COLOR)  # Стиль для Frame
style.configure("TLabel", font=(FONT_FAMILY, FONT_SIZE), background=BG_COLOR, foreground=TEXT_COLOR)
style.configure("TButton", font=(FONT_FAMILY, FONT_SIZE), padding=5, background=BUTTON_BG, relief="flat", borderwidth=0)
style.configure("TEntry", font=(FONT_FAMILY, FONT_SIZE), fieldbackground=LISTBOX_BG, foreground=TEXT_COLOR, relief="flat", borderwidth=0)

# Список для хранения предыдущих паролей
previous_passwords = []

# Заголовок программы
header_label = ttk.Label(root, text="Генератор паролей", font=("Segoe UI", 16, "bold"), foreground="#cccccc")
header_label.pack(pady=10)

# Раздел для ввода длины пароля
length_frame = ttk.Frame(root, style="TFrame")  # Используем стиль TFrame
length_frame.pack(pady=10)

length_label = ttk.Label(length_frame, text="Длина пароля:")
length_label.pack(side=tk.LEFT, padx=5)

length_entry = ttk.Entry(length_frame, width=10, justify="center")
length_entry.pack(side=tk.LEFT, padx=5)

# Кнопка "Создать пароль"
generate_button = ttk.Button(root, text="Создать пароль", command=generate_password)
generate_button.pack(pady=10)

# Метка для отображения текущего пароля
password_label = ttk.Label(root, text="", font=("Segoe UI", 14), foreground="#cccccc", cursor="hand2")
password_label.pack(pady=10)

# Привязка события двойного клика для копирования текущего пароля
password_label.bind("<Double-Button-1>", copy_current_password)

# Раздел для предыдущих паролей
previous_passwords_frame = ttk.Frame(root, style="TFrame")  # Используем стиль TFrame
previous_passwords_frame.pack(pady=10, fill="x")

previous_passwords_label = ttk.Label(previous_passwords_frame, text="Предыдущие пароли:", font=("Segoe UI", 12, "bold"))
previous_passwords_label.pack(anchor="w")

# Список предыдущих паролей
previous_passwords_listbox = tk.Listbox(
    root,
    font=("Segoe UI", 12),
    width=40,
    height=10,
    bg=LISTBOX_BG,
    fg=TEXT_COLOR,
    selectbackground=LISTBOX_SELECT_BG,
    selectforeground=TEXT_COLOR,
    relief="flat",  # Убираем стандартную обводку
    highlightthickness=0  # Убираем выделение при фокусе
)
previous_passwords_listbox.pack()

# Привязка события двойного клика для копирования пароля из списка
previous_passwords_listbox.bind("<Double-Button-1>", copy_previous_password)

# Кнопка очистки списка паролей
clear_button = ttk.Button(
    root,
    text="❌ Очистить",
    width=15,
    command=clear_previous_passwords
)
clear_button.pack(pady=10)

# Запуск главного цикла
root.mainloop()