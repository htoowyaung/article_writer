import openai
import sys
from fpdf import FPDF

# Define OpenAI API Key
# Read API key from a text file
with open('api_key.txt', 'r') as f:
    openai.api_key = f.read().strip()

def get_instructions_from_file(filename):
    with open(filename, 'r') as f:
        return f.read()

def chat_with_gpt3(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message['content']

def markdown_to_pdf(text, pdf_filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=1, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.cell(0, 10, line, ln=True)
    pdf.output(pdf_filename)

def main():
    print("Revising article.")
    keyword = sys.argv[1]
    density = sys.argv[2]
    length = sys.argv[3]
    
    # Read instructions from a file
    instructions_template = get_instructions_from_file('instructions2.txt')
    
    # Replace placeholders with actual variables
    instructions = instructions_template.format(keyword=keyword, density=density, length=length)
    
    with open('rewritten_article.md', 'r') as f:
        rewritten_article = f.read()
    
    with open('critique.md', 'r') as f:
        critique = f.read()

    combined_rewrite_messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": critique + "\n\n" + rewritten_article}
    ]

    revised_article = chat_with_gpt3(combined_rewrite_messages)
    
    with open('revised_article.md', 'w') as f:
        f.write(revised_article)

    print("Revised article has been saved to 'revised_article.md'.")
    with open('original_filename.txt', 'r') as f:
        original_filename = f.read().strip()
    
    revised_filename_md = f"{original_filename}_revised.md"
    revised_filename_pdf = f"{original_filename}_revised.pdf"

    with open(revised_filename_md, 'w') as f:
        f.write(revised_article)

    print(f"Revised article has been saved to '{revised_filename_md}'.")
    
    markdown_to_pdf(revised_article, revised_filename_pdf)
    print(f"Revised article has also been saved as '{revised_filename_pdf}'.")

if __name__ == "__main__":
    main()
