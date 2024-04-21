import tkinter as tk
import pandas as pd
import re
import webbrowser
from pathlib import Path
from tkinter import ttk
from epomoc_retriever import retrieve_documents
from tkinter.font import Font

# Create dataframe or load the existing one
file_path = Path('prompts.csv')
if file_path.exists():
    df = pd.read_csv(file_path)
else:
    df = pd.DataFrame(columns=['Query', 'Documents', 'Line', 'Program', 'UserFeedback'])


def open_url(url):
    webbrowser.open(url, new=2)  # Open link in new tab


def format_links(start, end):
    content = text_area.get(start, end)
    for match in re.finditer(r'https?://\S+', content):
        start_index = f"{start}+{match.start()}c"
        end_index = f"{start}+{match.end()}c"
        text_area.tag_add("hyperlink", start_index, end_index)
        text_area.tag_bind("hyperlink", "<Button-1>", lambda e, url=match.group(): open_url(url))


def retrieve(event=None):
    query = entry.get()
    line = line_combobox.get()
    program = program_combobox.get()
    documents = retrieve_documents(query)
    display_query_result(query, line, program, documents)
    entry.delete(0, tk.END)
    save_feedback(query, documents, line, program, None)


def display_query_result(query, line, program, documents):
    index = len(df)
    # result_text = f"Pytanie: {query}\nLinia: {line}\nProgram: {program}\n{documents}\n"
    query_text = f"Pytanie: {query}\n"
    details_text = f"Linia: {line}\nProgram: {program}\n{documents}\n"
    start = text_area.index(tk.END)
    text_area.insert(tk.END, query_text, 'query')
    text_area.insert(tk.END, details_text)
    end = text_area.index(tk.END)
    format_links(start, end)
    feedback_frame = tk.Frame(text_area)
    positive_button = tk.Button(feedback_frame, text="+", command=lambda: update_feedback(index, 'Positive'), font=default_font)
    negative_button = tk.Button(feedback_frame, text="-", command=lambda: update_feedback(index, 'Negative'), font=default_font)
    positive_button.pack(side=tk.LEFT)
    negative_button.pack(side=tk.LEFT)
    text_area.window_create(tk.END, window=feedback_frame)
    text_area.insert(tk.END, "\n\n")
    text_area.see(tk.END)


def save_feedback(query, documents, line, program, feedback):
    global df
    new_data = pd.DataFrame(
        {'Query': [query], 'Documents': [documents], 'Line': [line], 'Program': [program], 'UserFeedback': [feedback]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(file_path, index=False)


def update_feedback(index, feedback):
    global df
    df.at[index, 'UserFeedback'] = feedback
    df.to_csv(file_path, index=False)


root = tk.Tk()
root.title("RAG Query Interface")

default_font_size = 20
default_font = Font(family="helvetica", size=default_font_size)

line_combobox = ttk.Combobox(root, values=["GT", "nexo"], state="readonly", font=default_font)
line_combobox.set("Wybierz linię")
line_combobox.pack(side=tk.TOP, fill=tk.X)

program_combobox = ttk.Combobox(root, values=["Subiekt", "Subiekt 123", "Gratyfikant", "Rachmistrz", "Rewizor"],
                                state="readonly", font=default_font)
program_combobox.set("Wybierz program")
program_combobox.pack(side=tk.TOP, fill=tk.X)

text_area = tk.Text(root, height=15, font=default_font)
text_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
text_area.tag_configure("hyperlink", foreground="blue", underline=True)
text_area.tag_configure("query", font=('helvetica', default_font_size, 'bold'))


entry = tk.Entry(root, width=50)
entry.pack(side=tk.BOTTOM, fill=tk.X)
entry.bind("<Return>", retrieve)

search_button = tk.Button(root, text="Wyślij", command=retrieve, font=default_font)
search_button.pack(side=tk.BOTTOM)

root.mainloop()
