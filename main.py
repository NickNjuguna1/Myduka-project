from flask import Flask, render_template, request, redirect, url_for
from database import fetch_data, insert_products, insert_sales, insert_stock

#instance of the Flask class
app=Flask(__name__)

@app.route('/')
def home():
    return  render_template ('index.html')

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



app.run(debug=True)