# PrintManager Command Line Client

This is a tool you use in the terminal to manage printing orders. You can use it to send new orders, see all orders, or find one specific order.

## Features

* It talks directly to the server using just the terminal.
* It prints your total cost and your exact change instantly after you place an order.

## How it works

When you type a command, the script uses a tool to grab every single word you typed. Then, it looks at the first word (like "order" or "view") to decide what function to run. 

The script uses a library called `requests` to talk to the server. basically takes the data you typed, sends it to `http://127.0.0.1:8000`, and waits for the server to answer. Once the server sends the information back, the script just prints it on your screen so you can see it.

## How to use the client

Open your terminal. You will use `python client.py` to run commands. Here is what you can do:

| What you want to do | What to type in the terminal |
| :--- | :--- |
| Make a new order | `python client.py order "Mark Kevin" "colored" 5 "file.pdf" 50.0` |
| See all orders | `python client.py view` |
| Find one order by ID | `python client.py search 1` |