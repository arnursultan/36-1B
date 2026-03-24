from Lesson8db import get_connection


def create_tables():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    price INTEGER NOT NULL,
                    category_id INTEGER REFERENCES categories(id)
                )
            """)

            cursor.execute("SELECT COUNT(*) FROM categories")
            count = cursor.fetchone()[0]

            if count == 0:
                cursor.execute("""
                    INSERT INTO categories (name) VALUES 
                    ('Электроника'),
                    ('Одежда'),
                    ('Еда')
                """)

        conn.commit()
    except Exception as e:
        print("Ошибка create_tables:", e)
        conn.rollback()
    finally:
        conn.close()


def get_products():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT p.id, p.name, p.price, COALESCE(c.name, 'Без категории')
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
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
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name FROM categories ORDER BY id")
            result = cursor.fetchall()
            print("Категории из БД:", result)
            return result
    except Exception as e:
        print("Ошибка get_categories:", e)
        return []
    finally:
        conn.close()


def add_product(name, price, category_id):
    conn = get_connection()
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