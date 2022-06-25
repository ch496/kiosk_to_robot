process_transaction_with_accessory(accessory_id=30, json_object={"command": "turn_on", "index": 0})

current_value = \
process_transaction_with_accessory(accessory_id=30, json_object={"command": "get_actual_pose", "index": 2})['value']

if (current_value <= 2):
    process_transaction_with_accessory(accessory_id=30, json_object={"command": "move", "index": 2, "target": 180})
else:
    process_transaction_with_accessory(accessory_id=30, json_object={"command": "move", "index": 2, "target": 0})
