import mysql.connector
from mysql.connector import errorcode


#connection with mysql
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': ''
}

try:
    cnx = mysql.connector.connect(**config)

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is worng with your  username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

def cur():
    cnx = mysql.connector.connect(**config)
    return cnx.cursor()

cursor = cnx.cursor(buffered=True)


#add a new product in db
def new_product(name, serial, manufacturers_id, states_id):
    sql = """INSERT INTO glpi_peripherals (name, serial, manufacturers_id, states_id, date_creation) 
    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP())"""
    record = (name, serial, manufacturers_id, states_id)
    cursor.execute(sql, record)
    cnx.commit()

#update a product information
def update_product_sql(id, **kwargs):
    columns_list = list(kwargs.keys())
    values_list = [kwargs.get(x) for x in columns_list]

    values_list.append(id)
    values_update = 'UPDATE glpi_peripherals SET'

    for x in columns_list:
        column_temp = f' {x} = %s,'
        values_update += column_temp

    values_update+= 'date_mod = CURRENT_TIMESTAMP()'
    sql = values_update + ' WHERE id = %s'
    
    cursor.execute(sql, tuple(values_list))
    cnx.commit()

def delete_product(id):
    update_product_sql(id=id, is_deleted=1)

def get_all_records():
    cursor.execute('SELECT * FROM glpi_peripherals WHERE is_deleted=0')
    return cursor.fetchall()

def get_product(id):
    sql = f"SELECT * FROM glpi_peripherals WHERE id = {id}"
    cursor.execute(sql)
    return cursor.fetchall()


def search_records(name):
    sql = f"SELECT * FROM glpi.glpi_peripherals WHERE MATCH(name) AGAINST ('{name}')"
    cursor.execute(sql)
    return cursor.fetchall()
