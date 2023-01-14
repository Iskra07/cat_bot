def get_products_query():
    sql = "SELECT name from products"

    return sql

def create_new_user(id):
    sql = f"INSERT INTO user (id) VALUES({id})"

    return sql
