import openai
import fitz
import sys
from tkinter import Tk, filedialog, Label, Entry, Button, StringVar

# Define OpenAI API Key
openai.api_key = "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"

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
        f.write(f"{keyword_var.get()}\n")
        f.write(f"{density_var.get()}\n")
        f.write(f"{length_var.get()}\n")

    article_text = read_pdf(file_path)

    instructions = (f"You are tasked with rewriting an article following a specific structure and guidelines: "
                    f"You are a highly skilled technical writer with a strong background in science and technology. You possess a unique blend of technical knowledge, analytical thinking, and exceptional writing skills that enable you to create comprehensive and insightful scientific and technical articles. Your expertise lies in your ability to break down complex scientific and technical concepts into clear, understandable language. You have a deep understanding of various scientific and technical fields, and you are adept at conducting thorough research to ensure that your articles are accurate, up-to-date, and informative. Your writing style is marked by its clarity and precision. You understand that your readers may not always have a technical background, so you strive to make your articles as accessible as possible, without sacrificing depth or detail. You are skilled at explaining complex ideas in a way that is easy for anyone to understand, regardless of their level of technical knowledge. In addition to your technical expertise, you also have a keen eye for detail and a strong commitment to accuracy. You understand that in the world of science and technology, even the smallest details can be crucial, so you take great care to ensure that every fact you include in your articles is correct and up-to-date."
                    f"1. Include the keyword '{keyword}' with a density of {density}.Strictly enforce these requirements. "
                    f"2. The article should be approximately {length} words long.Strictly enforce this requirement. "
                    "3. A clear heading in big letters and bold type. "
                    "4. A table of contents. "
                    "5. Subheadings for each section. "
                    "6. Bullet points scattered throughout for dynamic feel. "
                    "7. Use the AIDA model for the introduction and conclusion sections. "
                    "8. Include FAQs at the end.")

    aida_messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": article_text}
    ]

    rewritten_article = chat_with_gpt3(aida_messages)

    with open('rewritten_article.md', 'w') as f:
        f.write(rewritten_article)

    print("Rewritten article has been saved to 'rewritten_article.md'.")

if __name__ == "__main__":
    root = Tk()

    # Add this line to set a callback for the window close event
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

    # Check whether the window was closed
    if window_closed:
        print("User closed the window. Exiting program.")
        sys.exit(0)