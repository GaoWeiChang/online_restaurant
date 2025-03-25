import datetime

def generate_order_number(pk):
    current_date = datetime.datetime.now().strftime('%Y%m%d%H%S') # year, month, day, hour, minute, second (20211231235959)
    order_number = current_date + str(pk) # Concatenate current date and primary key
    
    return order_number