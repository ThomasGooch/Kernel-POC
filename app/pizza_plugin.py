from semantic_kernel.connectors.ai.ollama import OllamaTextCompletion
from semantic_kernel.functions import kernel_function

class PizzaPlugin:
    @kernel_function(description="Checks balance amount in rupees on users pizza wallet; returns the balance amount")
    def get_pizza_wallet_balance(self, wallet_password:str):
        # may be we can integrate a real wallet service here to get the balance amount
        print("Invoked get_pizza_wallet_balance function !!")
        balance = 144.34
        return f"balance : Rs.{balance}"

    @kernel_function(description="Checks for available pizzas and return them.")
    def get_available_pizza(self):
        # this is static data and later may be we can  setup a database kind of 
        pizzas = {"Pizza 1" : {"Name" : "Bryon's Bigdamaka pizza", "Price" : 180.76},
        "Pizza 2" : {"Name" : "Gramin's Small Pizza", "Price" : 129.87},
        "Pizza 3" : {"Name" : "Jaorin's Special Pizza", "Price" : 239.76},
        }
        print(f"Invoked get_available_pizza function !!")
        return str(pizzas)
    
    @kernel_function(description="Order a pizza with the given pizza name and user wallet balance; return the confirmation message for the order")
    def order_pizza(self, pizza_name:str, pizza_price: float, wallet_balance:float):
        # her we can use some logic to detect the amount from user wallet
        print("Invoked Pizza order function !!")
        if wallet_balance < pizza_price:
            return f"You wallet balance is insufficient to place an order for {pizza_name}. Please recharge your wallet."
        return f"Your order for {pizza_name} has been placed successfully."

    