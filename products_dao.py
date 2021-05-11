from sql_connection import get_sql_connection
import codecs


connection = get_sql_connection()


def get_all_products(connection):

    cursor = connection.cursor()

    query = 'SELECT products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name ' + \
        'FROM products inner join uom on products.uom_id=uom.uom_id;'

    cursor.execute(query)

    response = []

    for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
        response.append(
            {
                'product_id': product_id,
                'name': name,
                'uom_id': uom_id,
                'price_per_unit': price_per_unit,
                'uom_name': uom_name
            }
        )
    return response


def get_all_units(connection):

    cursor = connection.cursor()

    query = 'SELECT uom.uom_id, uom.uom_name FROM uom'

    cursor.execute(query)

    response = []

    for (uom_id, uom_name) in cursor:
        response.append(
            {
                'uom_id': uom_id,
                'uom_name': uom_name
            }
        )
    return response


def insert_new_product(connection, product):
    
    cursor = connection.cursor()
    
    query = 'INSERT INTO products (name, uom_id, price_per_unit) VALUES (%s, %s, %s)'

    data = (product['product_name'], product['uom_id'], product['price_per_unit'])
    cursor.execute(query, data)
    connection.commit()


def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = 'DELETE FROM products where product_id=' + str(product_id)
    cursor.execute(query)
    connection.commit()


def product_table(connection):
    products = get_all_products(connection)
    
    html = 'C:/Users/Festa/Desktop/VS code/grocery_store/templates/product.html'
    
    f = codecs.open(html,'r')
    beginning = f.readlines()
    f.close()

    del beginning[27:]

    f = codecs.open(html,'w+')

    for line in beginning:
        f.write(line)

    for i in range(len(products)):
        temp = """
                    <tr>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td><input type="checkbox" name="product_id" value={}><label>Delete</label></td>
                    </tr>
                """
        f.write(temp.format(products[i]['name'],products[i]['uom_name'],products[i]['price_per_unit'],products[i]['product_id']))

    end = """
                </tbody>
            </table>
            <br/><input type = "submit">
        </form>
    </div>

    <div class='AddProduct'>
        <form class='my-form' method='POST'>
            <h3>Add Product</h3>
            <div class='form-group'>
                <label>Name: </label>
                <input type="text" name="name">
            </div>
            <div class='form-group'>
                <label>Unit: </label>
                <input type="text" name="unit">
            </div>
            <div class='form-group'>
                <label>Price per Unit: </label>
                <input type="text" name="price">
            </div>
            <input type = "submit">
        </form>
    </div>

</body>
</html>
    """

    f.write(end)
    f.close

