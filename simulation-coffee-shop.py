# Importing libraries
import simpy
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dataframe_image as dfi

# Initialising dictionary
menu = {1:["Black Coffee", 4, 6],
        2:["Latte", 5, 8],
        3:["Cappuccino", 6, 8],
        4:["Espresso", 5, 7],
        5:["Tea", 3, 5]}

payment_option = {1:["Card", 2, 4],
                  2:["Cash", 3, 5]}
                  
# Initialising variables
num_of_cashier = 2
num_of_barista = 3

# Generate customers 

# Arrival rate of 20 customers/hour, based on a Poisson distribution
num_of_customers = int(np.random.poisson(20, 1)+1)
num_of_customers

def generate_cust(env, cashier, barista):
    for i in range(num_of_customers):
        yield env.timeout(random.randint(1, 60))
        env.process(customer(env, cashier, barista))
 
 
# Define customer processes
def customer(env, cashier, barista):
    with cashier.request() as req:
        start_cq = env.now
        yield req
        payment_wait_time.append(env.now - start_cq)
        menu_item = random.randint(1, 5) # Choosing random menu
        payment_type = random.randint(1, 2) # Generate random payment type
        time_to_order = random.randint(payment_option[payment_type][1], payment_option[payment_type][2])
        yield env.timeout(time_to_order)
        payment_time.append(env.now - start_cq)
    
    with barista.request() as req:
        start_bq = env.now
        yield req
        order_wait_time.append(env.now - start_bq)
        time_to_collect = random.randint(menu[menu_item][1], menu[menu_item][2])
        yield env.timeout(time_to_collect)
        order_time.append(env.now - start_bq)
        
# Run the model 100 times
results = []

for i in range(100):
    payment_wait_time = []
    payment_time = []
    order_wait_time = []
    order_time = []
    
    env = simpy.Environment()
    cashier = simpy.Resource(env, num_of_cashier)
    barista = simpy.Resource(env, num_of_barista)
    
    for i in range(8): # 8 hours
        env.process(generate_cust(env, cashier, barista))
        
    env.run(until=480)
    #print(len(payment_time))
    #print(payment_time)
    
    results.append([np.mean(payment_wait_time), np.mean(payment_time),
                   np.mean(order_wait_time), np.mean(order_time)])

# Create dataframe for the results
df = pd.DataFrame(results,columns=["payment_wait_time", "payment_time", "order_wait_time", "order_time"])

df["total_time"] = df.sum(axis=1)

print(df.head())

# Descriptive statistics
print(df.describe())

# Line graph
plt.title("Coffee Shop Wait Time")

plt.plot(df.payment_wait_time)
plt.plot(df.payment_time)
plt.plot(df.order_wait_time)
plt.plot(df.order_time)
plt.plot(df.total_time)
plt.legend(["payment_wait_time", "payment_time", "order_wait_time", "order_time", "total_time"],
          bbox_to_anchor = (1.05, 0.6))

plt.show()


# Histogram

plt.title("Total Wait Time")

plt.hist(df.total_time)
plt.show()