import datetime
import simplejson as json

def generate_order_number(pk):
    current_date = datetime.datetime.now().strftime('%Y%m%d%H%S') # year, month, day, hour, minute, second (20211231235959)
    order_number = current_date + str(pk) # Concatenate current date and primary key
    
    return order_number

def order_total_by_vendor(order, vendor_id):
    total_data = json.loads(order.total_data)
    data = total_data.get(str(vendor_id))
    subtotal = 0
    tax = 0
    tax_dict = {}
    
    for key, val in data.items():
            subtotal += float(key)
            val = val.replace("'", '"') # replace single quote with double quote to convert to JSON
            val = json.loads(val) # print example {'subtotal': '1020.00', 'tax_type': {'vat': {'5': '51.00'}}}
            tax_dict.update(val) 
            
            # calculate tax
            for i in val:
                for j in val[i]:
                    # print(val[i][j]) # print example {'vat': {'5': '51.00'}}
                    tax += float(val[i][j])
    grand_total = float(subtotal) + float(tax)
    context = {
        'subtotal': subtotal,
        'grand_total': grand_total,
        'tax_dict': tax_dict
    }
    return context