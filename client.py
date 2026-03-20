import sys
import requests

url = "http://127.0.0.1:8000"

def view():
    print("grabbing all orders from the backend...")
    
    response = requests.get(url + "/orders")
    
    if response.status_code == 200:
        data_dict = response.json()
        
        orders_list = data_dict["data"]
        
        for order in orders_list:
            o_id = order["order_id"]
            name = order["customer_name"]
            cost = order["total_cost"]
            print(f"ID: {o_id} | Name: {name} | Total Cost: {cost}")
            
    else:
        print("failed to fetch orders")

def search(args):
    print("searching for a specific order...")
    
    try:
        order_id = int(args[1])
    except ValueError:
        print("you need to type a real number for the id")
        return
        
    response = requests.get(url + "/orders/" + str(order_id))
    
    if response.status_code == 200:
        data_dict = response.json()
        
        order = data_dict["data"]
        
        name = order["customer_name"]
        
        cost = order["total_cost"]
        
        print(f"found it Name: {name} | Total Cost: {cost}")
        
    else:
        print("order not found in the database")

def order(args):
    print("trying to place a new printing order...")
    
    customer_name = args[1]
    
    printing_type = args[2]
    
    pages = int(args[3])
    
    doc_name = args[4]
    
    payment = float(args[5])
    
    payload = {
        "customer_name": customer_name,
        "items": [
            {
                "printing_type": printing_type,
                "pages": pages,
                "document_name": doc_name
            }
        ],
        "payment_amount": payment
    }
    
    response = requests.post(url + "/orders", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        
        order_data = result["data"]
        
        total = order_data["total_cost"]
        
        change = order_data["change"]
        
        print(f"success! total cost: {total}, your change is: {change}")
        
    else:
        print("error placing order")
        
        print(response.json())

def main():
    command = sys.argv[1]
    
    if command == "order":
        order(sys.argv[1:])
        
    elif command == "search":
        search(sys.argv[1:])
        
    elif command == "view":
        view()
        
if __name__ == "__main__":
    main()