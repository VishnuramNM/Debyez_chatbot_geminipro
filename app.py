import google.generativeai as genai
import gradio as gr
import os  # Import the os module for environment variables
from dotenv import load_dotenv

load_dotenv()
# Get the API Key from Hugging Face Secrets
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Initialize model and chat (outside the function)
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    full_response = ""
    for chunk in response:
        full_response += chunk.text
    return full_response

# Interface using Gradio
theme = gr.themes.Soft()  
with gr.Blocks(theme=theme, css=".gradio-container {background-color: #f0f5f9}") as demo:
    gr.Markdown(
        """
        <div style="text-align: center;">
            <h1 style="color: #007bff;">Debyez Chatbot</h1>
            <p style="color: #6c757d;">Ask me anything! 💬</p>
        </div>
        """
    )

    chatbot = gr.Chatbot(elem_classes="colorful-chatbot") 
    msg = gr.Textbox(label="Your Message", placeholder="Type your message here...")

    # Colorful Clear Button
    clear = gr.ClearButton(
        [msg, chatbot],
        value="Clear Conversation",
        variant="primary",  
    )

    # Response Function (unchanged)
    def respond(message, chat_history):
        bot_message = get_gemini_response(message)
        chat_history.append((message, bot_message))
        return "", chat_history
    
    # Submit Message & Update Chat
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

# Launch the Chat Interface
if __name__ == "__main__":
    demo.launch()