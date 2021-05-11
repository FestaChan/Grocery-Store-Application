from sql_connection import get_sql_connection
from products_dao import get_all_products
from datetime import datetime
import codecs


connection = get_sql_connection()


def insert_order_details(connection, order):
    cursor = connection.cursor()

    order_details_query = ("INSERT INTO order_details "
                           "(order_id, product_id, quantity, total_price)"
                           "VALUES (%s, %s, %s, %s)")

    order_details_data = (order['order_id'], order['product_id'], order['quantity'], order['total_price'])

    cursor.execute(order_details_query, order_details_data)
    connection.commit()


def insert_order(connection, order):
    cursor = connection.cursor()
    
    order_query = ("INSERT INTO orders "
             "(customer_name, total, datetime) "
             "VALUES (%s, %s, %s)")
    order_data = (order['customer_name'], order['grand_total'], datetime.now())

    cursor.execute(order_query, order_data)
    connection.commit()


def get_order_details(connection, order_id):
    cursor = connection.cursor()

    query = "SELECT * from order_details where order_id = %s"

    query = "SELECT order_details.order_id, order_details.quantity, order_details.total_price, "\
            "products.name, products.price_per_unit FROM order_details LEFT JOIN products on " \
            "order_details.product_id = products.product_id where order_details.order_id = %s"

    data = (order_id, )

    cursor.execute(query, data)

    records = []
    for (order_id, quantity, total_price, product_name, price_per_unit) in cursor:
        records.append({
            'order_id': order_id,
            'quantity': quantity,
            'total_price': total_price,
            'product_name': product_name,
            'price_per_unit': price_per_unit
        })

    cursor.close()

    return records


def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT * FROM orders")
    cursor.execute(query)
    response = []
    for (order_id, customer_name, total, dt) in cursor:
        response.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total,
            'datetime': dt,
        })

    cursor.close()

    for record in response:
        record['order_details'] = get_order_details(connection, record['order_id'])

    return response


def order_table(connection, name):
    orders = get_all_orders(connection)
    products = get_all_products(connection)

    html = 'C:/Users/Festa/Desktop/VS code/grocery_store/templates/order.html'
    
    options = "<select name='product'>\n"
    for i in range(len(products)):
        temp = """                    
                    <option value={}>{}</option>
               """
        options += temp.format(products[i]['product_id'],products[i]['name'])
    options += """
                </select>
               """

    f = codecs.open(html,'r')
    beginning = f.readlines()
    f.close()

    del beginning[40:]

    f = codecs.open(html,'w')

    for line in beginning:
        f.write(line)

    loO = ""
    for i in range(len(orders)):
        if orders[i]['customer_name'] == name:
            loO = orders[i]

    if loO == "":
        temp = {
            'customer_name':name,
            'grand_total': 0,
        }
        insert_order(connection, temp)
        orders = get_all_orders(connection)
        for i in range(len(orders)):
            if orders[i]['customer_name'] == name:
                loO = orders[i]

    total = loO['total']

    for i in range(len(loO['order_details'])):
        temp = """
                    <tr>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                    </tr>
                """
        f.write(temp.format(loO['order_details'][i]['product_name'], \
            loO['order_details'][i]['price_per_unit'], \
                loO['order_details'][i]['quantity'], \
                    loO['order_details'][i]['total_price']))

    end = """
                </tbody>
            </table>
        </form>
    </div>
    <div class='AddProduct'>
        <h2 class="underline">Welcome {}!</h2>
        <form method='POST'>
            <h3>Add Product</h3>
            <div>
                <label>Product: </label>
                {}
            </div>
            <div>
                <label>Quantity: </label>
                <input type="text" name="quantity">
            </div>
            <input type = "submit">
        </form>
    </div>
</body>
</html>
          """

    f.write(end.format(name,options))
    f.close

    return(loO['order_id'])

