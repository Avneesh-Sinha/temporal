from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import json
import os
from docx import Document

model = OllamaLLM(model="llama3")

class bot():
    
    chain: OllamaLLM
    template: ChatPromptTemplate
    conversation: list[tuple]

    def __init__(self):
        self.conversation = []

    def system(self, text):
        template = ChatPromptTemplate([
        ("system", text),
        ("human","{user_input}")
        ])
        self.conversation = []
        self.conversation.append(("system", text))
        self.template = template

    def sys_up(self):
        self.template = ChatPromptTemplate(self.conversation + [("human", "{user_input}")])
        self.bind()

    def bind(self):
        self.chain = self.template | model
    
    def doc(self, path):
        try:
            ext = os.path.splitext(path)[1].lower()
            if ext == '.txt':
                with open(path, 'r') as f:
                    text = f.read()
            elif ext == '.json':
                with open(path, 'r') as f:
                    data = json.load(f)
                    text = json.dumps(data, indent=4)
            elif ext == '.docx':
                doc = Document(path)
                text = '\n'.join([para.text for para in doc.paragraphs])
            else:
                print(f"Error: Unsupported file type '{ext}'")
                return
            self.conversation.append(("system", "You will now receive text from the user that you need to remember and answer questions based on that text."))
            self.conversation.append(("human", text))
            self.sys_up()
        except FileNotFoundError:
            print(f"Error: The file '{path}' was not found.")

    def gen_out(self, text):
        out = self.chain.invoke(text)
        print(out, '\n')
        self.conversation.append(("human", text))
        self.conversation.append(("ai", out))
        self.sys_up()

    def get_conv(self):
        for dialogue in self.conversation:
            print(dialogue)

cb2 = bot()
sys_text = "You are an AI assistant. You will receive the entire conversation with each prompt so answer in context of the conversation."

cb2.system(sys_text)
cb2.bind()

ch = 0
while ch != 4:
    print("1. Enter text")
    print("2. Enter Document")
    ch = int(input("Enter Choice: "))
    if ch == 1:
        s = input("\nText: ")
        print()
        cb2.gen_out(s)
    elif ch == 2:
        s = input("\nEnter Path: ")
        cb2.doc(s)
        print("Memory Updated.")
        print()
