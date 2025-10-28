from flask import Flask, render_template
from database import fetch_data

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

@app.route('/sales')
def sales():
    sales=fetch_data('sales')
    return render_template ('sales.html', my_sales=sales)

@app.route('/stock')
def stock():
    stock=fetch_data('stock')
    return render_template ('stock.html', my_stock=stock)

app.run(debug=True)
