from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import fetch_data, insert_products, insert_sales, insert_stock, product_profit, products_sales, day_sales, daily_profits, insert_users, check_email, total_sales
from flask_bcrypt import Bcrypt

# instance of the Flask class
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = '1234569'

@app.route('/')
def home():
    return render_template('index.html')

# Products route
@app.route('/products')
def products():
    if 'email' in session:
        products = fetch_data('products')
    else:
        flash('Log in to access Products', 'error')
        return redirect (url_for('login'))
    return render_template('products.html', my_products=products)

 # Create a function that receives data from UI to the server side


@app.route('/add_products', methods=['GET', 'POST'])
def add_products():
     # checking method
    if request.method == 'POST':
        # get form input
        product_name = request.form['name']
        bp = request.form['buying_price']
        sp = request.form['selling_price']
        # print(product_name,bp,sp)
        new_products = (product_name, bp, sp)
        # insert to database
        insert_products(new_products)
        flash('New product added', 'success')
    return redirect(url_for('products'))

# Sales route


@app.route('/add_sales', methods=['GET', 'POST'])
def add_sales():
    if request.method == 'POST':
        product_sale = request.form['product_id']
        quantity = request.form['quantity']
        new_sales = (product_sale, quantity)
        insert_sales(new_sales)
        flash('New Sale Added', 'success')
    return redirect(url_for('sales'))


@app.route('/sales')
def sales():
    if 'email' in session:
        sales = fetch_data('sales')
        # fetch products to display on Select
        products = fetch_data('products')
    else:
        flash('Log in to access Sales', 'error')
        return redirect(url_for('login'))
    
    return render_template('sales.html', my_sales=sales, products=products)

# Stock route


@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        product_stock = request.form['product_id']
        quantity = request.form['stock_quantity']
        new_stock = (product_stock, quantity)
        insert_stock(new_stock)
        flash('New Stock Added', 'success')
    return redirect(url_for('stock'))


@app.route('/stock')
def stock():
    if 'email' in session:
        stock = fetch_data('stock')
    else:
        flash('Log in to access Stock', 'error')
        return redirect (url_for('login'))
    
    return render_template('stock.html', my_stock=stock)

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        profit = product_profit()
        print(profit)
    # a variable with an empty list to show all products
        product_names = []
        product_profits = []
        for i in profit:
            product_names.append(i[0])
            product_profits.append(float(i[2]))

        sale = products_sales()
        print(sale)
        product_names = []
        product_sales = []
        for i in sale:
            product_names.append(i[0])
            product_sales.append(float(i[1]))

        sales_per_day = day_sales()
        print(sales_per_day)
        dates = []
        sale_per_day = []
        for i in sales_per_day:
            dates.append(str(i[0]))
            sale_per_day.append(float(i[1]))

        profits_per_day = daily_profits()
        print(profits_per_day)
        profit_per_day = []
        for i in profits_per_day:
            profit_per_day.append(float(i[1]))

        total_sale = total_sales()
    else:
        flash('Log in to access Dashboard', 'error')
        return redirect (url_for('login'))

    return render_template('dashboard.html', product_names=product_names, product_profits=product_profits, product_sales=product_sales,
                            sale_per_day=sale_per_day, profit_per_day=profit_per_day, dates=dates, total_sale=total_sale)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
 # Check if user is registered
        check = check_email(email)
        if check == None:
            flash("User doesn't exist. Please register", 'error')
            return redirect(url_for('register'))
        else:
        # Check if password matches password
            if password == check[3]:
                session['email'] = email
                flash('Login Successful', 'success')
                return redirect (url_for('dashboard'))
            else:
            # check if password matches check password
                # if password == check[3]:
                if bcrypt.check_password_hash(check[3],password):
                    # check_password_hash allows created users with a password to login
                    session['email'] = email
                    flash('Login Successful', 'success')
                    return redirect (url_for('dashboard'))
                else:
                    flash("Wrong password or email", 'error')
                    return render_template ('login.html')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        fname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
# Insert after checking
        new_user = (fname, email, hashed_password)
        check = check_email(email)
        if check == None:
            # insert user
            insert_users(new_user)
            flash('Registered successful', 'success')
            return redirect(url_for('login'))
        else:
            # Class error or success is introduced to bring color to message flashing
            flash('User exists. Log in or use a different email', 'error')
        return render_template('register.html')

    return render_template ('register.html')

@app.route('/logout')
def logout():
    session.pop('email')
    flash("You've been logged out", 'error')
    return redirect(url_for('login'))

app.run(debug=True)