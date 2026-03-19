from Lesson8db import get_connection


def get_products():
    conn = get_connection()
    if conn is None:
        return []

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT p.id, p.name, p.price, c.name
                FROM products p
                JOIN categories c ON p.category_id = c.id
                ORDER BY p.id
            """)
            return cursor.fetchall()
    except Exception as e:
        print("Ошибка get_products:", e)
        return []
    finally:
        conn.close()


def get_categories():
    conn = get_connection()
    if conn is None:
        return []

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name FROM categories ORDER BY id")
            return cursor.fetchall()
    except Exception as e:
        print("Ошибка get_categories:", e)
        return []
    finally:
        conn.close()


def add_product(name, price, category_id):
    conn = get_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO products (name, price, category_id) VALUES (%s, %s, %s)",
                (name, price, category_id)
            )
        conn.commit()
    except Exception as e:
        print("Ошибка add_product:", e)
        conn.rollback()
    finally:
        conn.close()
