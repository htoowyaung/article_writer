from flask import Flask, request, send_file, render_template
import os

app = Flask(__name__)

def rewrite_article(uploaded_file, keyword, density, length):
    # Your code to rewrite the article
    # For demonstration purposes, let's assume it generates a PDF and returns its path
    pdf_path = "rewritten_article.pdf"
    return pdf_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            uploaded_file = request.files['file']
            keyword = request.form['keyword']
            density = request.form['density']
            length = request.form['length']

            if uploaded_file.filename != '':
                pdf_path = rewrite_article(uploaded_file, keyword, density, length)

                if os.path.exists(pdf_path):
                    return send_file(pdf_path, as_attachment=True)
                else:
                    return "PDF file could not be found", 404

        except Exception as e:
            return f"An error occurred: {str(e)}", 500

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
