import sys
from languages import languages

class CodeAssistant:
    def __init__(self):
        self.language = None

    def set_language(self, language):
        self.language = language
        print(f"Language set to: {self.language}")

    def prompt_user(self):
        while True:
            user_input = input(f"[{self.language}] Enter your question (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                print("Exiting the assistant.")
                break
            self.handle_query(user_input)

    def handle_query(self, query):
        if self.language in languages:
            print(f"Handling {self.language} query: {query}")
        else:
            print(f"Language '{self.language}' is not supported.")
            print(f"Supported languages: {', '.join(languages)}")

if __name__ == '__main__':
    assistant = CodeAssistant()
    assistant.set_language()
    print(f"Language set to: {assistant.language}")

    assistant.prompt_user()
