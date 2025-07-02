
# 🧠 # kopi chatbot  🧠

A chatbot that can hold a debate and attempt to convince the other side of its views (regardless of how irrational the point).

# Requirements

**Phyton 3.12**
**node.js 20** 

# Run the chatbot

1 Clone the Repo 

    git clone https://github.com/bet02024/kopi_chatbot.git

Create a .env file with 

OPENAI_API_KEY=YOUR_OPENAI_API_KEY    **Replace with your own YOUR_OPENAI_API_KEY**

# Run the chatbot with Vercel CLI

From terminal 


    cd kopi_chatbot
    make install
    make run

# Run whitout Vercel CLI

    cd kopi_chatbot
    python3.13 -m venv ./
    source  ./bin/activate 
    pip3.13 install -r requirements.txt 
    flask --app api/index run


# Available commands

#  Help

    make help

# Install dependencies & Activate Virtual Env

    make install

# Run API 

    make run

# Shutdown services

    make down

# clean data

    make clean

# Run unit testing

    make test

 
 







