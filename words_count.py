import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
import re

def select_file():
    filepath = filedialog.askopenfilename()
    print("Selected:", filepath)
    extension = os.path.splitext(filepath)[1]
    if extension == ".txt":
        continue_with_column2(filepath, extension)
        column_entry.config(state="disabled")
    elif extension in [".csv", ".xlsx"]:
        continue_with_column(filepath, extension)
    else:
        messagebox.showerror("Error", "The file must be a .txt , .csv or excel file")
        

def continue_with_column(filepath, extension):
    column_entry.config(state="normal")
    confirm_button.config(command=lambda: filter_text(filepath, extension))
    
def continue_with_column2(filepath, extension):
    confirm_button.config(command=lambda: filter_text(filepath, extension))


def filter_text(filepath, extension):
    column = column_entry.get()
    if not column_entry2.get().strip():
        messagebox.showerror("Error", "You have to enter a integer number")
    if extension == ".txt":
        text=open(filepath, 'r', encoding='utf-8').read()
    elif extension == ".csv":
        if not column.strip():
            messagebox.showerror("Error", "You have to enter a valid column name")
        data=pd.read_csv(filepath)
        text=""
        if column not in data.columns:
            messagebox.showerror("Error", "The column name is not in the dataset")
        for i in data[column]:
            i=str(i)
            text=text+i
    elif extension == ".xlsx":
        if not column.strip():
            messagebox.showerror("Error", "You have to enter a valid column name")
        data=pd.read_excel(filepath)
        text=""
        if column not in data.columns:
            messagebox.showerror("Error", "The column name is not in the dataset")
        for i in data[column]:
            i=str(i)
            text=text+i
    
    number_words = int(column_entry2.get())
    
    word_count(text,number_words) 
    
    
def word_count(text,number_words):
    text=re.sub(r"[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]", " ", text)
    text_language=language_var.get()
    words = nltk.word_tokenize(text, language=text_language)

    stop_words = set(stopwords.words(text_language))

    words = [word for word in words if (word.lower() not in stop_words) and (len(word) > 2)]

    fdist = FreqDist(words)
    
    top_words = fdist.most_common(number_words)

    
    words = [word for word, freq in top_words][::-1]  
    freqs = [freq for word, freq in top_words][::-1]

    
    plt.figure(figsize=(10,5))
    plt.barh(range(len(words)), freqs, color='salmon', edgecolor='black', linewidth=1)
    plt.yticks(range(len(words)), words)
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.gca().set_facecolor('aliceblue')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()
    
    
root = tk.Tk()
root.geometry("300x300")
root.title("Select a .txt , .csv or excel file to analize")

background_image = tk.PhotoImage(file = "background_image.png")
background_label = tk.Label(root, image = background_image)
background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

language_var = tk.StringVar(value="English")
language_dropdown = tk.OptionMenu(root, language_var, "Portuguese", "Spanish", "English")
language_dropdown.config(fg="white", bd=0)
language_dropdown.pack(pady=10)

language_dropdown.config(bg="#2196f3", activebackground="#1976d2", bd=0)

file_button = tk.Button(root, text="Select file", command=select_file, bg="#2196f3", activebackground="#1976d2", fg="white", bd=0, padx=5, pady=5, width=10 ,height=1)
file_button.pack(pady=5)

column_label = tk.Label(root, text="Enter column name:",bg="#2196f3", activebackground="#1976d2", fg="white", padx=5, pady=5)
column_label.pack(pady=5)

column_entry = tk.Entry(root, state="disabled")
column_entry.pack(pady=5)

column_label_2 = tk.Label(root, text="Top N repeated words:",bg="#2196f3", activebackground="#1976d2", fg="white", padx=5, pady=5)
column_label_2.pack(pady=5)

column_entry2 = tk.Entry(root, state="normal")
column_entry2.pack(side="top")

confirm_button = tk.Button(root, text="Confirm", state="normal", bg="#2196f3", activebackground="#1976d2", fg="white", bd=0, padx=5, pady=5)
confirm_button.pack(pady=5)


root.mainloop()

