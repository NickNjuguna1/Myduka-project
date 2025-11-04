from flask import Flask, render_template, request, redirect, url_for
from database import fetch_data, insert_products, insert_sales, insert_stock, product_profit, products_sales, day_sales, daily_profits

#instance of the Flask class
app=Flask(__name__)

@app.route('/')
def home():
    return render_template ('index.html')

# Products route
@app.route('/products')
def products():
    products=fetch_data('products')
    return render_template ('products.html', my_products= products)

 # Create a function that receives data from UI to the server side
@app.route('/add_products', methods=['GET', 'POST'])
def add_products():
     # checking method 
    if request.method=='POST':
        # get form input
        product_name = request.form['name']
        bp=request.form['buying_price']
        sp=request.form['selling_price']
        # print(product_name,bp,sp)
        new_products=(product_name,bp,sp)
        # insert to database
        insert_products(new_products)
    return redirect(url_for('products'))

# Sales route 
@app.route('/add_sales', methods=['GET', 'POST'])
def add_sales():
    if request.method=='POST':
        product_sale = request.form['product_id']
        quantity = request.form['quantity']
        new_sales=(product_sale,quantity)
        insert_sales(new_sales)
    return redirect(url_for('sales'))


@app.route('/sales')
def sales():
    sales = fetch_data('sales')
    # fetch products to display on Select
    products = fetch_data('products')
    return render_template('sales.html', my_sales=sales, products=products )
 
# Stock route
@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method=='POST':
        product_stock = request.form['product_id']
        quantity = request.form['stock_quantity']
        new_stock=(product_stock, quantity)
        insert_stock(new_stock)
    return redirect(url_for('stock'))

@app.route('/stock')
def stock():
    stock=fetch_data('stock')
    return render_template ('stock.html', my_stock=stock)

@app.route('/dashboard')
def dashboard():
    profit=product_profit()
    print(profit)
    # a variable with an empty list to show all products
    product_names=[]
    product_profits=[]
    for i in profit:
        product_names.append(i[0])
        product_profits.append(float(i[2]))

    sale = products_sales()
    print(sale)
    product_names=[]
    product_sales=[]
    for i in sale:
        product_names.append(i[0])
        product_sales.append(float(i[1]))

    sales_per_day = day_sales()
    print(sales_per_day)
    product_names=[]
    sale_per_day=[]
    for i in sales_per_day:
        product_names.append(i[0])
        sale_per_day.append(float(i[1]))

    profits_per_day = daily_profits()
    print(profits_per_day)
    product_names=[]
    profit_per_day=[]
    for i in profits_per_day:
        product_names.append(i[0])
        profit_per_day.append((i[0]))

    return render_template ('dashboard.html', product_names=product_names, product_profits=product_profits, product_sales=product_sales,
                            sale_per_day=sale_per_day, profit_per_day=profit_per_day)
    
    

app.run(debug=True)