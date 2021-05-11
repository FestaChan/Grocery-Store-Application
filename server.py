from flask import Flask, request, render_template, redirect, url_for
from products_dao import product_table, delete_product,insert_new_product, get_all_units, get_all_products
from order_dao import order_table, insert_order_details
from manage_dao import update_table, manage_table
from sql_connection import get_sql_connection


app = Flask(__name__)


connection = get_sql_connection()


@app.route('/', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        product_table(connection)
        return render_template('product.html')

    if request.method == 'POST':
        lou = get_all_units(connection)

        delete = request.form.getlist("product_id")
        for i in range(len(delete)):
            delete_product(connection,delete[i])
        
        name = request.form.get("name")
        unit = request.form.get("unit")
        price = request.form.get("price")

        if (name != "") and (unit != "") and (price != ""):
            unit_id = ""
            for i in range(len(lou)):
                if lou[i]['uom_name'] == unit:
                    unit_id = lou[i]['uom_id']
            
            if unit_id != "":
                product = {
                    "product_name" : name,
                    "uom_id" : unit_id,
                    "price_per_unit" : price
                }
                insert_new_product(connection, product)

        product_table(connection)
        return render_template('product.html')


@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'GET':
        return render_template('order_og.html')

    if request.method == 'POST':
        name = request.form.get("name")
        
        if name != "":
            temp = "http://127.0.0.1:5000/{}".format(name)
            return redirect(temp)


@app.route("/<name>", methods=['GET', 'POST'])
def user(name):
    loP = get_all_products(connection)

    if request.method == 'GET':
        orderID = order_table(connection, name)
        return render_template('order.html')
    
    if request.method == 'POST':
        product = request.form.get("product")
        quantity = (request.form.get("quantity"))
        
        if product != None and quantity != None:
            orderID = order_table(connection, name)

            for i in range(len(loP)):
                if int(product) == loP[i]['product_id']:
                    price = loP[i]['price_per_unit']
            
            temp = {
                'order_id': str(orderID),
                'product_id': str(product),
                'quantity': float(quantity),
                'total_price': str(float(quantity)*float(price))
            }
            insert_order_details(connection, temp)

            order_table(connection, name)
            return render_template('order.html')

        
@app.route('/manage', methods=['GET'])
def manage():
    if request.method == 'GET':
        update_table(connection)
        manage_table(connection)
        return render_template('manage.html')


if __name__ == '__main__':
    app.run(debug=True)