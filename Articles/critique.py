import openai
import sys

# Read API key from a text file
with open('api_key.txt', 'r') as f:
    openai.api_key = f.read().strip()

def get_instructions_from_file(filename):
    with open(filename, 'r') as f:
        return f.read().strip()

def chat_with_gpt3(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message['content']

def main():
    print("Critiquing rewritten article for recommendations.")

    # Read rewritten article
    with open('rewritten_article.md', 'r') as f:
        rewritten_article = f.read()

    # Read instructions for the critique from a text file
    instructions = get_instructions_from_file('instructions3.txt')

    critique_messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": rewritten_article}
    ]

    critique = chat_with_gpt3(critique_messages)

    # Save the critique to a file
    with open('critique.md', 'w') as f:
        f.write(critique)

    print("Rewritten article has been critiqued for recommendations.")

if __name__ == "__main__":
    main()
