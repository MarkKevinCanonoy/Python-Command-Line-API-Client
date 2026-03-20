from datetime import datetime
from typing import List, Optional
from models import Order, PrintingItem, PRINTING_PRICES

class OrderDatabase:
    """In-memory database for storing orders"""
    
    def __init__(self):
        self.orders: List[Order] = []
        self.next_order_id = 1
    
    def calculate_total_cost(self, items: List[PrintingItem]) -> float:
        """Calculate total cost based on printing items"""
        total = 0.0
        for item in items:
            price_per_page = PRINTING_PRICES.get(item.printing_type, 0)
            total += price_per_page * item.pages
        return total
    
    def create_order(self, customer_name: str, items: List[PrintingItem], payment_amount: float) -> Order:
        """Create a new order"""
        total_cost = self.calculate_total_cost(items)
        change = payment_amount - total_cost
        
        order = Order(
            order_id=self.next_order_id,
            customer_name=customer_name,
            items=items,
            total_cost=total_cost,
            payment_amount=payment_amount,
            change=change,
            created_at=datetime.now()
        )
        
        self.orders.append(order)
        self.next_order_id += 1
        return order
    
    def get_all_orders(self) -> List[Order]:
        """Retrieve all orders"""
        return self.orders
    
    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        """Retrieve a specific order by ID"""
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None
    
    def get_orders_by_customer(self, customer_name: str) -> List[Order]:
        """Retrieve all orders for a specific customer"""
        return [order for order in self.orders if order.customer_name.lower() == customer_name.lower()]

db = OrderDatabase()
