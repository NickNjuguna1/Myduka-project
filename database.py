from multiprocessing import connection
from multiprocessing.connection import Connection
import psycopg2

import os
import psycopg2

# Reads the DATABASE_URL you configured on Render, falling back to localhost for local testing
DATABASE_URL = os.environ.get("DATABASE_URL")

connect = psycopg2.connect(DATABASE_URL)
curr = connect.cursor()

curr = connect.cursor()
#  Fetch data by first executing, then fetch
# curr.execute("select * from products;")
# data=curr.fetchall()
# print(data)

# # create function
# def fetch_prods():
#     curr.execute("select * from products;")
#     prods = curr.fetchall()
#     return prods

# myproducts=fetch_prods()
# print(myproducts)

# curr.execute("select * from stock;")
# data=curr.fetchall()
# # print(data)

# # create function
# def fetchstock():
#     curr.execute("select * from stock; ")
#     stock = curr.fetchall()
#     # return stock

# mystock=fetchstock()
# # print(mystock)

# curr.execute("select * from sales;")
# data=curr.fetchall()
# print(data)

# # create function
# def fetchsales():
#     curr.execute("select * from sales;")
#     sales = curr.fetchall()
#     return sales

# mysales=fetchsales()
# print(mysales)

# fetch data


def fetch_data(table_name):
    curr.execute(f'select * from {table_name}')
    data = curr.fetchall()
    return data


# products = fetch_data('products')
# print('My Products')
# print(products)
# stock = fetch_data('stock')
# print('My stock')
# print(stock)
sales = fetch_data('sales')
# print('My Sales')
# print(sales)

# Insert Products


def insert_products(values):
    query = "insert into products(name, buying_price, selling_price) values (%s, %s, %s);"
    curr.execute(query, values)
    connect.commit()


new_product = ('Mango', 20, 40)
# insert_products(new_product)

products = fetch_data('products')
# print('My Products')
# print(products)


def insert_sales(values):
    query = 'insert into sales(product_id, quantity, created_at) values (%s, %s, now());'
    curr.execute(query, values)
    connect.commit()
# new_sales=(2,5)
# insert_sales(new_sale)
# sales = fetch_data('sales')
# print(sales)


def insert_stock(values):
    query = "insert into stock(product_id, stock_quantity) values (%s, %s);"
    curr.execute(query, values)
    connect.commit()

# new_stock = (43, 6, 59)
# insert_stock(new_stock)
# # the above insert_stock calls the function
# def products_sale():
#     query=


# stock = fetch_data('stock')
# print('My new stock')
# print(stock)

# Profit per Product(profit=(selling price - buying price)*quantity)
def product_profit():
    query = 'select p.name, p.product_id, sum((selling_price-buying_price)*s.quantity) as profit ' \
        'from sales as s inner join products as p on s.product_id = p.product_id group by p.name, p.product_id'
    curr.execute(query)
    profit = curr.fetchall()
    return profit


myprofits = product_profit()
# print( f'My product profit is {myprofits}')


def sales_sum():
    query = 'select sum(products.selling_price*sales.quantity) ' \
        'from sales inner join products on sales.product_id=products.product_id;'
    curr.execute(query)
    sum = curr.fetchall()
    return sum


def products_sales():
    query = 'select p.name, sum(p.selling_price*s.quantity) as total_sales from sales ' \
        'as s inner join products as p on s.product_id=p.product_id group by p.name, p.product_id;'
    curr.execute(query)
    sale = curr.fetchall()
    return sale

# Sales per Day Function


def day_sales():
    query = 'select date(s.created_at), ' \
        'sum(p.selling_price*s.quantity) as total_sales from sales as s inner join' \
        ' products as p on s.product_id=p.product_id group by date(s.created_at);'
    curr.execute(query)
    day_sale = curr.fetchall()
    return day_sale

# profit per Day


def daily_profits():
    query = 'select date(s.created_at), ' \
        'sum(p.selling_price-p.buying_price) as total_sales from sales as s inner join' \
        ' products as p on s.product_id=p.product_id group by date(s.created_at);'
    curr.execute(query)
    day_profit = curr.fetchall()
    return day_profit


def insert_users(user_values):
    query = "insert into users (full_name, email, password) values(%s,%s,%s);"
    curr.execute(query, user_values)
    connect.commit()


my_sum = sales_sum()
# print(f'My sum is {my_sum}')

# Check if user exists


def check_email(email):
    query = 'select * from users where email=%s'
    curr.execute(query, (email,))
    data = curr.fetchone()
    return data

# Sales card on Dashboard


def total_sales():
    query = 'select sum(selling_price*quantity) from products inner join sales on sales.product_id=products.product_id;'
    curr.execute(query)
    data = curr.fetchone()
    return data[0]


print(total_sales())

# Profit card on Dashboard


def total_profits():
    query = 'select sum((selling_price-buying_price)*quantity) from products inner join sales on sales.product_id=products.product_id;'
    curr.execute(query)
    data = curr.fetchone()
    return data[0]

# Stock card on Dashboard


def total_stocks():
    query = 'select sum(stock_quantity) from stock;'
    curr.execute(query)
    data = curr.fetchone()
    return data[0]

# Product with the most profit card on dashboard


def highest_profit_product():
    query = 'select p.name, p.product_id, sum((selling_price-buying_price)*s.quantity) ' \
        'as profit from sales s inner join products p on s.product_id = p.product_id group by p.name, p.product_id order by profit desc limit 1;'
    curr.execute(query)
    data = curr.fetchone()
    return data[0]


def delete_product(product_id):
    query = 'delete from products where product_id=%s;'
    curr.execute(query, (product_id,))
    connect.commit()


def fetch_product(product_id):
    query = 'select * from products where product_id=%s;'
    curr.execute(query, (product_id,))
    product = curr.fetchone()
    return product


def update_product(values):
    query = 'update products set name=%s, buying_price=%s, selling_price=%s where product_id=%s;'
    curr.execute(query, values)
    connect.commit()

# remaining stock for a product (stock entries minus sales) / researched


def get_remaining_stock(product_id):
    # used COALESCE to get 0 instead of crashing when no stock exists
    query = 'select COALESCE(sum(stock_quantity),0) from stock where product_id=%s;'
    curr.execute(query, (product_id,))
    stock_sum = curr.fetchone()[0] or 0
    query2 = 'select COALESCE(sum(quantity),0) from sales where product_id=%s;'
    curr.execute(query2, (product_id,))
    sales_sum = curr.fetchone()[0] or 0
    return int(stock_sum) - int(sales_sum)

def create_tables():
    curr.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id SERIAL PRIMARY KEY,
            -- add your other table columns here based on your app schema
        )
    ''')
    connect.commit()

create_tables()

# def card_profit():
#     query = 'select sum(p.selling_price-p.buying_price) as total_sales from sales as s inner join' \
#     ' products as p on s.product_id=p.product_id;'
#     curr.execute(query)
#     day_profits = curr.fetchall()
#     return day_profits
