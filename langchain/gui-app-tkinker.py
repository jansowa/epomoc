import tkinter as tk
import pandas as pd
from pathlib import Path
from tkinter import ttk, messagebox
from epomoc_retriever import retrieve_documents

# Utwórz DataFrame, jeśli nie istnieje, z załadowaniem istniejących danych jeśli plik już istnieje
file_path = Path('prompts.csv')
if file_path.exists():
    df = pd.read_csv(file_path)
else:
    df = pd.DataFrame(columns=['Query', 'Documents', 'Line', 'Program', 'UserFeedback'])

def retrieve(event=None):
    query = entry.get()
    line = line_combobox.get()
    program = program_combobox.get()
    documents = retrieve_documents(query)
    display_query_result(query, line, program, documents)
    entry.delete(0, tk.END)
    # Zapisz zapytanie i odpowiedź bez oceny użytkownika
    save_feedback(query, documents, line, program, None)

def display_query_result(query, line, program, documents):
    index = len(df)
    result_text = f"Pytanie: {query}\nLinia: {line}\nProgram: {program}\n{documents}\n"
    text_area.insert(tk.END, result_text)
    feedback_frame = tk.Frame(text_area)
    positive_button = tk.Button(feedback_frame, text="+", command=lambda: update_feedback(index, 'Positive'))
    negative_button = tk.Button(feedback_frame, text="-", command=lambda: update_feedback(index, 'Negative'))
    positive_button.pack(side=tk.LEFT)
    negative_button.pack(side=tk.LEFT)
    text_area.window_create(tk.END, window=feedback_frame)
    text_area.insert(tk.END, "\n\n")
    text_area.see(tk.END)

def save_feedback(query, documents, line, program, feedback):
    global df
    new_data = pd.DataFrame({'Query': [query], 'Documents': [documents], 'Line': [line], 'Program': [program], 'UserFeedback': [feedback]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(file_path, index=False)

def update_feedback(index, feedback):
    # Aktualizacja istniejącego rekordu z nową oceną
    global df
    df.at[index, 'UserFeedback'] = feedback
    df.to_csv(file_path, index=False)

root = tk.Tk()
root.title("RAG Query Interface")

line_combobox = ttk.Combobox(root, values=["GT", "nexo"], state="readonly")
line_combobox.set("Wybierz linię")
line_combobox.pack(side=tk.TOP, fill=tk.X)

program_combobox = ttk.Combobox(root, values=["Subiekt", "Subiekt 123", "Gratyfikant", "Rachmistrz", "Rewizor"], state="readonly")
program_combobox.set("Wybierz program")
program_combobox.pack(side=tk.TOP, fill=tk.X)

text_area = tk.Text(root, height=15)
text_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

entry = tk.Entry(root, width=50)
entry.pack(side=tk.BOTTOM, fill=tk.X)
entry.bind("<Return>", retrieve)

search_button = tk.Button(root, text="Wyślij", command=retrieve)
search_button.pack(side=tk.BOTTOM)

root.mainloop()