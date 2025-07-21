# chatbot.py
from groq import Groq
from json import load, dump 
import datetime
from dotenv import dotenv_values
import os

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

SystemChatBot = [
    {"role": "system", "content": f"""
Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""}
]

def RealtimeInformation():
    now = datetime.datetime.now()
    return f"""Please use this real-time information if needed,
Day: {now.strftime("%A")}
Date: {now.strftime("%D")}
Month: {now.strftime("%B")}
Year: {now.strftime("%Y")}
Time: {now.strftime("%H")} hours :{now.strftime("%M")} minutes:{now.strftime("%S")} seconds.
"""

def AnswerModifier(answer):
    return "\n".join([line.strip() for line in answer.split('\n') if line.strip()])

def ChatBot(query):
    chatlog_path = "Data/ChatLog.json"
    try:
        if os.path.exists(chatlog_path):
            with open(chatlog_path, "r") as f:
                messages = load(f)
        else:
            messages = []

        messages.append({"role": "user", "content": query})
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
        )

        answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content
        answer = answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": answer})

        with open(chatlog_path, "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(answer)
    except Exception as e:
        print(f"Error: {e}")
        with open(chatlog_path, "w") as f:
            dump([], f)
        return "Something went wrong. Try again."
