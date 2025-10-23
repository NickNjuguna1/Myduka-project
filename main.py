from flask import Flask, render_template

#instance of the Flask class
app=Flask(__name__)

@app.route('/')
def home():
    return  render_template ('index.html')

@app.route('/products')
def products():
    return render_template ('products.html')

@app.route('/sales')
def sales():
    return render_template ('sales.html')

@app.route('/stock')
def stock():
    return render_template ('stock.html')

app.run()
