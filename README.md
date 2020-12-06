# WAREHOUSE_INVENTORY

## Methods

##### GET '/'

Response
    
    200 {product:{product_info}, stock:int}

##### POST /buy
    
    param 
    
    json {product_id:str,
          quantity:int}

Response
    
    200 OK
    
    400 Bad request invalid Quantity
    
    400 Bad request invalid Product
    
    500 Not enough inventory
    
    500 Product not found
    
    500 Something went wrong. Please try again


