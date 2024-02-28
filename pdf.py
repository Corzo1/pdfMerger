import os
import tkinter as tk
from tkinter import Label
from tkinter import filedialog
from tkinter import Toplevel
import tkinter.ttk as ttk
import fitz

def find_pdf_files(folder_path, pdf_files_list):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files_list.append(os.path.join(root, file))

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        pdf_files_list.clear()
        find_pdf_files(folder_path, pdf_files_list)
        update_listbox()

def remove_selected():
    selected_indices = listbox.curselection()
    for index in selected_indices:
        listbox.delete(index)
        pdf_files_list.pop(index)

def update_listbox():
    listbox.delete(0, tk.END)
    for pdf_file in pdf_files_list:
        listbox.insert(tk.END, pdf_file)
    max_name_length = max(len(pdf_file) for pdf_file in pdf_files_list)
        
        # Set the width of the listbox to the maximum length + some padding
    listbox.config(width=max_name_length + 10)
def merge_pdfs():
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if not output_path:
        return

    # Initialize progress bar
    progress_window = Toplevel(root)
    progress_window.title("Merging PDFs...")
    progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(padx=20, pady=10)

    pdf_merger = fitz.open()

    total_pages = sum(len(fitz.open(pdf_file)) for pdf_file in pdf_files_list)

    current_progress = 0
    for pdf_file in pdf_files_list:
        with fitz.open(pdf_file) as pdf_document:
            pdf_merger.insert_pdf(pdf_document)
            current_progress += len(pdf_document)
            progress_bar["value"] = current_progress
            progress_window.update()

    pdf_merger.save(output_path)
    pdf_merger.close()
    
    progress_window.destroy()

    top = Toplevel(root)
    top.title("Outcome")

    outcome_text = f"PDF files merged successfully into '{output_path}'."
    label = Label(top, text=outcome_text, font=("Arial 14"))
    label.pack(pady=20)

    # Calculate the width based on the length of the outcome text
    text_length = len(outcome_text)
    font_width = label.winfo_reqwidth()
    padding = 10
    window_width = font_width + 2 * padding

    # Set the top window to be resizable and set its width
    top.resizable(False, False)
    top.geometry(f"{window_width}x75")
if __name__ == "__main__":
    root = tk.Tk()
    root.title("PDF File Search")
    pdf_files_list = []

    browse_button = tk.Button(root, text="Browse Folder", command=browse_folder)
    browse_button.pack(pady=10)

    listbox = tk.Listbox(root, selectmode=tk.SINGLE)
    listbox.pack(fill=tk.BOTH, expand=True)

    remove_button = tk.Button(root, text="Remove Selected", command=remove_selected)
    remove_button.pack(pady=5)

    merge_button = tk.Button(root, text="Merge PDFs", command=merge_pdfs)
    merge_button.pack(pady=5)

    root.mainloop()
