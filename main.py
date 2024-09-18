from datetime import datetime
import sys
import os
import webbrowser
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QTextEdit
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
import pyttsx3
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Set up Google Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')
# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

# Get todays weekday and set the header accordingly (either morning or evening)
def get_greeting():
    now = datetime.now()
    hour = now.hour
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    else:
        return "Evening"

Now = get_greeting()
class DeveloperJarvis(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('JARVIS Developer Assistant')
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #f5f7fb;")  # Light background similar to the provided UI

        # Main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Header Section
        self.header = QLabel(f"Good {Now}, Tumelo! Welcome Back.")
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("font-size: 26px; font-weight: bold; color: #333; margin: 20px;")
        main_layout.addWidget(self.header)

        # Subtitle
        self.subtitle = QLabel("I'm JARVIS, your personal assistant. Here are some useful developer tools:")
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("font-size: 18px; color: #666; margin-bottom: 30px;")
        main_layout.addWidget(self.subtitle)

        # Tools Section
        tools_layout = QHBoxLayout()

        # Card 1 - Code Snippet Generator
        snippet_card = self.create_tool_card("Code Snippet Generator", "Generate code snippets based on your needs.")
        snippet_card.clicked.connect(self.generate_code_snippet)
        tools_layout.addWidget(snippet_card)

        # Card 2 - API Tester
        api_card = self.create_tool_card("API Tester", "Test your API endpoints easily.")
        api_card.clicked.connect(self.open_api_tester)
        tools_layout.addWidget(api_card)

        # Card 3 - Version Control
        version_control_card = self.create_tool_card("Version Control", "Manage Git repositories and branches.")
        version_control_card.clicked.connect(self.manage_git)
        tools_layout.addWidget(version_control_card)

        main_layout.addLayout(tools_layout)

        # Additional Tools or Coming Soon Section
        coming_soon = QLabel("Coming Soon - Add more tools to your JARVIS")
        coming_soon.setAlignment(Qt.AlignCenter)
        coming_soon.setStyleSheet("font-size: 18px; color: #999; margin-top: 30px;")
        main_layout.addWidget(coming_soon)

        # Bottom Chat Input for additional interaction
        chat_input = QTextEdit()
        chat_input.setPlaceholderText("Ask JARVIS anything, or enter a command...")
        chat_input.setStyleSheet("font-size: 16px; padding: 10px; background-color: #FFF; border: 2px solid #ddd; border-radius: 8px;")
        main_layout.addWidget(chat_input)

        # Submit Button for chat input
        submit_button = QPushButton("Submit")
        submit_button.setStyleSheet(self.get_button_style())
        submit_button.clicked.connect(lambda: self.process_task(chat_input.toPlainText()))
        main_layout.addWidget(submit_button)

    def create_tool_card(self, title, description):
        """Creates a styled button representing a tool in the dashboard."""
        card = QPushButton()
        card.setText(f"{title}\n{description}")
        card.setIcon(QIcon("icon.png"))  # Use appropriate icons for each card
        card.setStyleSheet("""
            QPushButton {
                background-color: #e8f1f8;
                border-radius: 10px;
                padding: 20px;
                font-size: 18px;
                color: #333;
                text-align: left;
                border: none;
                height: 150px;
            }
            QPushButton:hover {
                background-color: #d7e9f3;
            }
        """)
        card.setIconSize(QSize(40, 40))
        return card

    def process_task(self, task):
        """Process the user's task with JARVIS using Gemini."""
        if task:
            try:
                # Generate response using Gemini
                response = model.generate_content(task)
                ai_response = response.text

                # Speak the response
                engine.say(f"Here's what I found: {ai_response}")
                engine.runAndWait()

                # Update UI with the response
                self.update_output(ai_response)
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                print(error_message)
                self.update_output(error_message)
                engine.say("I'm sorry, but an error occurred while processing your request.")
                engine.runAndWait()
                
    def update_output(self, text):
            """Update the output area with the given text."""
            # Create a QTextEdit for output if it doesn't exist
            if not hasattr(self, 'output_area'):
                self.output_area = QTextEdit()
                self.output_area.setReadOnly(True)
                self.output_area.setStyleSheet("font-size: 16px; padding: 10px; background-color: #FFF; border: 2px solid #ddd; border-radius: 8px;")
                self.centralWidget().layout().addWidget(self.output_area)
            
            self.output_area.setText(text)
        
    def generate_code_snippet(self):
        """Generate code snippet using Gemini."""
        prompt = "Generate a Python function that calculates the Fibonacci sequence. Ensure proper indentation."
        try:
            response = model.generate_content(prompt)
            snippet = response.text

            # Clean up the snippet
            cleaned_snippet = "\n".join(line.strip() for line in snippet.split("\n"))

            engine.say("Here's a code snippet for calculating the Fibonacci sequence:")
            engine.runAndWait()

            self.update_output(cleaned_snippet)
        except Exception as e:
            error_message = f"Error generating code snippet: {str(e)}"
            print(error_message)
            self.update_output(error_message)
            engine.say("I'm sorry, but an error occurred while generating the code snippet.")
            engine.runAndWait()

    def open_api_tester(self):
        """Opens an API tester."""
        engine.say("Opening API tester")
        engine.runAndWait()
        webbrowser.open("https://www.postman.com/")

    def manage_git(self):
        """Manage Git repositories (future)."""
        engine.say("Managing your Git repository.")
        engine.runAndWait()
        # Future: Git commands can be executed here

    def get_button_style(self):
        """Style for modern-looking buttons."""
        return """
            QPushButton {
                background-color: #007BFF;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """

def main():
    app = QApplication(sys.argv)
    jarvis = DeveloperJarvis()
    jarvis.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
