from multiprocessing import connection
from multiprocessing.connection import Connection
import psycopg2

connect = psycopg2.connect(
    host="localhost",
    user="postgres",
    dbname="myduka_db",
    port=5432,
    password="Nick8957#"
)

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
    query = "insert into stock(id, product_id, stock_quantity) values (%s, %s, %s);"
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
    query = 'select p.name, (selling_price*quantity) as sale from sales as s inner join products as p on s.product_id=p.product_id;'
    curr.execute(query)
    sale = curr.fetchall()
    return sale

def day_sales():
    query = 'select name, (selling_price*quantity) as sale from sales inner join products on ' \
    'sales.product_id=products.product_id group by name, sale, now();'
    curr.execute(query)
    day_sale = curr.fetchall()
    return day_sale

def daily_profits():
    query = 'select name, (selling_price-buying_price) as profit from sales inner join products on ' \
    'sales.product_id=products.product_id group by name, profit, now();'
    curr.execute(query)
    daily_profit = curr.fetchall()
    return daily_profit

my_sum = sales_sum()
# print(f'My sum is {my_sum}')
