import openai
import sys
from fpdf import FPDF
openai.api_key = "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"

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

    with open('rewritten_article.md', 'r') as f:
        rewritten_article = f.read()

    with open('critique.md', 'r') as f:
        critique = f.read()

    instructions = (f"Revise the article based on the following critique and recommendations."
                    f"You are a highly skilled technical writer with a strong background in science and technology. You possess a unique blend of technical knowledge, analytical thinking, and exceptional writing skills that enable you to create comprehensive and insightful scientific and technical articles. Your expertise lies in your ability to break down complex scientific and technical concepts into clear, understandable language. You have a deep understanding of various scientific and technical fields, and you are adept at conducting thorough research to ensure that your articles are accurate, up-to-date, and informative. Your writing style is marked by its clarity and precision. You understand that your readers may not always have a technical background, so you strive to make your articles as accessible as possible, without sacrificing depth or detail. You are skilled at explaining complex ideas in a way that is easy for anyone to understand, regardless of their level of technical knowledge. In addition to your technical expertise, you also have a keen eye for detail and a strong commitment to accuracy. You understand that in the world of science and technology, even the smallest details can be crucial, so you take great care to ensure that every fact you include in your articles is correct and up-to-date."
                    f"Also, make sure to include the keyword '{keyword}' with a density of {density}%, and aim for approximately {length} words.Strictly enforce these requirements. "
                    "Ensure to follow this structure: "
                    "1. A clear heading in big letters and bold type. "
                    "2. A table of contents. "
                    "3. Subheadings for each section. "
                    "4. Bullet points scattered throughout for dynamic feel. "
                    "5. Use the AIDA model for the introduction and conclusion sections. "
                    "6. Include FAQs at the end.")

    combined_rewrite_messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": critique + "\n\n" + rewritten_article}
    ]

    revised_article = chat_with_gpt3(combined_rewrite_messages)
    
    with open('revised_article.md', 'w') as f:
        f.write(revised_article)

    print("Revised article has been saved to 'revised_article.md'.")
    # Read the original PDF filename from a text file
    with open('original_filename.txt', 'r') as f:
        original_filename = f.read().strip()

    # Create a filename for the revised article based on the original PDF filename
    revised_filename = f"{original_filename}_revised.md"

    # Save the revised article
    with open(revised_filename, 'w') as f:
        f.write(revised_article)

    print(f"Revised article has been saved to '{revised_filename}'.")

    # Read the original PDF filename from a text file
    with open('original_filename.txt', 'r') as f:
        original_filename = f.read().strip()

    # Create a filename for the revised article based on the original PDF filename
    revised_filename_md = f"{original_filename}_revised.md"
    revised_filename_pdf = f"{original_filename}_revised.pdf"

    # Save the revised article
    with open(revised_filename_md, 'w') as f:
        f.write(revised_article)

    print(f"Revised article has been saved to '{revised_filename_md}'.")

    # Convert the revised Markdown file to PDF
    markdown_to_pdf(revised_article, revised_filename_pdf)
    print(f"Revised article has also been saved as '{revised_filename_pdf}'.")


if __name__ == "__main__":
    main()
