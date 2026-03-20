from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import CreateOrderRequest, OrderResponse, Order, PRINTING_PRICES
from database import db
import json

app = FastAPI(
    title="FastAPI Printing Management Backend",
    description="A system to manage printing orders and automatically compute costs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Welcome to FastAPI Printing Management Backend",
        "available_endpoints": {
            "POST /orders": "Create a new order",
            "GET /orders": "Get all orders",
            "GET /orders/{order_id}": "Get specific order by ID",
            "GET /orders/customer/{customer_name}": "Get orders by customer name",
            "GET /prices": "Get all printing prices"
        }
    }

@app.post("/orders", response_model=OrderResponse)
def create_order(request: CreateOrderRequest):
    """
    Create a new printing order.
    
    Parameters:
    - customer_name: Name of the customer
    - items: List of printing items (type and pages)
    - payment_amount: Amount paid by customer
    
    Returns order details with computed total cost and change
    """
    try:
        for item in request.items:
            if item.printing_type not in PRINTING_PRICES:
                raise ValueError(f"Invalid printing type: {item.printing_type}")
        
        order = db.create_order(
            customer_name=request.customer_name,
            items=request.items,
            payment_amount=request.payment_amount
        )
        
        return OrderResponse(
            success=True,
            message="Order created successfully",
            data=order
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")

@app.get("/orders", response_model=dict)
def get_all_orders():
    """
    Retrieve all orders in the system.
    
    Returns list of all orders
    """
    orders = db.get_all_orders()
    return {
        "success": True,
        "message": f"Retrieved {len(orders)} orders",
        "data": orders
    }

@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int):
    """
    Retrieve a specific order by ID.
    
    Parameters:
    - order_id: The ID of the order to retrieve
    
    Returns order details if found, otherwise error
    """
    order = db.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    
    return OrderResponse(
        success=True,
        message="Order retrieved successfully",
        data=order
    )

@app.get("/orders/customer/{customer_name}", response_model=dict)
def get_customer_orders(customer_name: str):
    """
    Retrieve all orders for a specific customer.
    
    Parameters:
    - customer_name: Name of the customer
    
    Returns list of orders for that customer
    """
    orders = db.get_orders_by_customer(customer_name)
    return {
        "success": True,
        "message": f"Retrieved {len(orders)} orders for {customer_name}",
        "data": orders
    }

@app.get("/prices")
def get_prices():
    """
    Get all printing prices.
    
    Returns dictionary of printing types and their prices per page
    """
    return {
        "success": True,
        "message": "Printing prices",
        "data": PRINTING_PRICES
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
