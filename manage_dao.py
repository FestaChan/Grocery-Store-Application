from sql_connection import get_sql_connection
import codecs


connection = get_sql_connection()


def get_customerOrders(connection):
    cursor = connection.cursor()

    query = "SELECT order_details.order_id, order_details.total_price, orders.customer_name " + \
        "FROM order_details inner join orders on order_details.order_id = orders.order_id"

    cursor.execute(query)

    response = []

    for (order_id, total_price, customer_name) in cursor:
        response.append(
            {
                'order_id': order_id,
                'customer_name': customer_name,
                'total_price': total_price
            }
        )
    return response 


def get_customers(connection):
    cursor = connection.cursor()

    query = "SELECT orders.order_id, orders.customer_name, orders.total, orders.datetime FROM orders"
    cursor.execute(query)

    response = []

    for (order_id, customer_name, total, datetime) in cursor:
        response.append(
            {
                'order_id': order_id,
                'customer_name': customer_name,
                'total': total,
                'datetime': datetime
            }
        )
    return response 


def update_order(connection, order):
    cursor = connection.cursor()
    
    order_query = ("UPDATE orders SET total = %s WHERE (order_id = %s)")
    order_data = (order['total'], order['order_id'])

    cursor.execute(order_query, order_data)
    connection.commit()


def update_table(connection):
    customers = get_customers(connection)
    orders = get_customerOrders(connection)
    final = []
    
    for i in range(len(customers)):
        total = 0
        for j in range(len(orders)):
            if customers[i]['order_id'] == orders[j]['order_id']:
                total += float(orders[j]['total_price'])
        final.append(
            {
                'order_id': customers[i]['order_id'],
                'customer_name': customers[i]['customer_name'],
                'total': str(total),
                'datetime': customers[i]['datetime']
            }
        )

    for i in range(len(final)):
        update_order(connection, final[i])

    
def manage_table(connection):
    html = 'C:/Users/Festa/Desktop/VS code/grocery_store/templates/manage.html'
    orders = get_customers(connection)

    f = codecs.open(html,'r')
    beginning = f.readlines()
    f.close()

    del beginning[30:]

    f = codecs.open(html,'w+')

    for line in beginning:
        f.write(line)

    for i in range(len(orders)):
        temp = """
                    <tr>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                    </tr>
                """
        f.write(temp.format(orders[i]['order_id'],orders[i]['customer_name'],orders[i]['total'],orders[i]['datetime']))

    end = """
                </tbody>
            </table>
        </form>
    </div>
</body>
</html>
    """

    f.write(end)
    f.close