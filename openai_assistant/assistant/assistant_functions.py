add_grocery_to_shopping_list = {
    "name": "add_grocery_to_shopping_list",
    "description": "Add a grocery item to the shopping list, the result is ERROR or OK, you can use this to notify the user",
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

set_alarm_clock = {
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
