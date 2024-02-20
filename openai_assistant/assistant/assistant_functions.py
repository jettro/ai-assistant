def_add_grocery_to_shopping_list = {
    "name": "add_grocery_to_shopping_list",
    "description": "Add a grocery item to the shopping list. The shopping list is a list that I use when going to the "
                   "store to buy stuff. The result is ERROR or OK, you can use this to notify the user",
    "parameters": {
        "type": "object",
        "properties": {
            "grocery_name": {
                "type": "string",
                "description": "The grocery item to add to the shopping list"
            },
            "quantity": {
                "type": "integer",
                "description": "The quantity of the grocery item to add to the shopping list"
            }
        },
        "required": ["grocery_name", "quantity"]
    }
}

def_set_alarm_clock = {
    "name": "set_alarm_clock",
    "description": "Set an alarm clock, the result is ERROR or OK, you can use this to notify the user",
    "parameters": {
        "type": "object",
        "properties": {
            "time": {
                "type": "string",
                "description": "The time to set the alarm to in the format HH:MM, examples are 09:00, 21:30"
            },
            "date": {
                "type": "string",
                "description": "The date to set the alarm to in the format YYYY-MM-DD, examples are 2022-12-31, 2023-01-01"
            }
        },
        "required": ["time"]
    }
}

def_order_food_delivery = {
    "name": "order_food_delivery",
    "description": "Order food or drinks for delivery, the result is ERROR or OK, you can use this to notify the user",
    "parameters": {
        "type": "object",
        "properties": {
            "product_name": {
                "type": "string",
                "description": "The name of the product to order"
            },
            "quantity": {
                "type": "integer",
                "description": "The quantity of the product to order"
            }
        },
        "required": ["product_name", "quantity"]
    }
}

def_finalize_order_food_delivery = {
    "name": "finalize_order_food_delivery",
    "description": "Finalize the order of food or drinks for delivery, the result is ERROR or OK, you can use this to "
                   "notify the user",
}


def set_alarm_clock(time: str, date: str = None):
    print(f"Setting alarm clock to {time} on {date}")
    return "OK"


def add_grocery_to_shopping_list(grocery_name: str, quantity: int):
    print(f"Adding {quantity} {grocery_name} to the shopping list")
    return "OK"


def order_food_delivery(product_name: str, quantity: int):
    print(f"Ordering {quantity} {product_name}")
    return "OK"


def finalize_order_food_delivery():
    print(f"Finalizing order")
    return "OK"
