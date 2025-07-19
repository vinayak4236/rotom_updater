# modules/chatbot.py

def reply(query):
    query = query.lower()

    # Greetings
    if "hello" in query or "hi" in query:
        return "Hi there!"
    elif "how are you" in query:
        return "I'm just a bunch of code, but I'm functioning as expected!"
    elif "your name" in query:
        return "I am Rotom, your offline assistant."
    elif "who created you" in query:
        return "I was created by my developer friend using Python."

    # Facts
    elif "what is python" in query:
        return "Python is a powerful programming language known for simplicity and readability."
    elif "capital of india" in query:
        return "The capital of India is New Delhi."
    elif "what is ai" in query:
        return "AI stands for Artificial Intelligence. It's the simulation of human intelligence by machines."
    elif "about your self" in query or "yourself" in query:
        return "I am Rotom, your personal offline AI assistant. I can respond to text or voice commands."

    # Commands
    elif "open notepad" in query:
        import os
        os.system("notepad.exe")
        return "Opening Notepad..."
    elif "open calculator" in query:
        import os
        os.system("calc.exe")
        return "Opening Calculator..."

    # Help
    elif "help" in query:
        return ("You can try asking me:\n"
                "- 'what is python'\n"
                "- 'capital of india'\n"
                "- 'how are you'\n"
                "- 'open notepad'\n"
                "- 'open calculator'\n"
                "- or just say 'hi'.")

    # Unknown
    else:
        return "I'm still learning. Can you rephrase that?"
