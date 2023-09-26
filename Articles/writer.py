import openai
import fitz
import sys
from tkinter import Tk, filedialog, Label, Entry, Button, StringVar

# Define OpenAI API Key
# Read API key from a text file
with open('api_key.txt', 'r') as f:
    openai.api_key = f.read().strip()

def read_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf_document:
        num_pages = pdf_document.page_count
        for page_num in range(num_pages):
            page = pdf_document.load_page(page_num)
            text += page.get_text("text")
    return text

def chat_with_gpt3(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message['content']

window_closed = False

def on_closing():
    global window_closed
    window_closed = True
    root.destroy()

def get_instructions_from_file(filename):
    with open(filename, 'r') as f:
        return f.read()

def rewrite_article(file_path, keyword, density, length):
    if not file_path:
        print("No PDF file selected. Exiting.")
        return
    
    # Save original PDF filename to a text file
    original_filename = file_path.split("/")[-1].replace(".pdf", "")
    with open('original_filename.txt', 'w') as f:
        f.write(original_filename)

    root.destroy()
    print("Rewriting article.")

    with open('variables.txt', 'w') as f:
        f.write(f"{keyword}\n")
        f.write(f"{density}\n")
        f.write(f"{length}\n")

    article_text = read_pdf(file_path)
    instructions = get_instructions_from_file('instructions.txt')

    aida_messages = [
        {"role": "system", "content": instructions.format(keyword=keyword, density=density, length=length)},
        {"role": "user", "content": article_text}
    ]

    rewritten_article = chat_with_gpt3(aida_messages)

    with open('rewritten_article.md', 'w') as f:
        f.write(rewritten_article)

    print("Rewritten article has been saved to 'rewritten_article.md'.")

if __name__ == "__main__":
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)

    file_path_var = StringVar()
    keyword_var = StringVar()
    density_var = StringVar()
    length_var = StringVar()

    Label(root, text="PDF File Path:").pack()
    Entry(root, textvariable=file_path_var).pack()
    Button(root, text="Select PDF", command=lambda: file_path_var.set(filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF files", "*.pdf")]))).pack()

    Label(root, text="Keyword:").pack()
    Entry(root, textvariable=keyword_var).pack()

    Label(root, text="Keyword Density:").pack()
    Entry(root, textvariable=density_var).pack()

    Label(root, text="Article Length (words):").pack()
    Entry(root, textvariable=length_var).pack()

    Button(root, text="Rewrite Article", command=lambda: rewrite_article(file_path_var.get(), keyword_var.get(), density_var.get(), length_var.get())).pack()

    root.geometry("300x500")
    root.mainloop()

    if window_closed:
        print("User closed the window. Exiting program.")
        sys.exit(0)
