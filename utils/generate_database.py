from faker import Faker
import random
import mysql.connector

# --- 1. Kết nối tới MySQL database ---
conn = mysql.connector.connect(
    host="localhost",        # Địa chỉ host MySQL (localhost nếu chạy trên máy tính local)
    user="root",             # Tên người dùng MySQL
    password="your_password",# Mật khẩu MySQL
    database="smartshop"     # Tên database bạn muốn sử dụng
)
cursor = conn.cursor()

# --- 2. Khởi tạo Faker ---
fake = Faker()

# --- 3. Sinh dữ liệu cho bảng users ---
def generate_users(total=100, admins=10):
    customers = total - admins
    users = []

    # Tạo admin trước
    for _ in range(admins):
        users.append((
            fake.unique.email(),
            fake.password(length=10),
            fake.address().replace("\n", ", "),
            "admin"
        ))

    # Tạo customer
    for _ in range(customers):
        users.append((
            fake.unique.email(),
            fake.password(length=10),
            fake.address().replace("\n", ", "),
            "customer"
        ))

    random.shuffle(users)  # Trộn ngẫu nhiên để không bị dồn admin lên đầu
    cursor.executemany(
        "INSERT INTO users (email, password, address, role) VALUES (%s, %s, %s, %s)",
        users
    )
    conn.commit()
    print(f"✅ Đã thêm {admins} admin và {customers} customer.")

# --- 4. Sinh dữ liệu cho bảng categories ---
def generate_categories(n=100):
    categories = [(fake.unique.word().capitalize(),) for _ in range(n)]
    cursor.executemany(
        "INSERT INTO categories (category_name) VALUES (%s)",
        categories
    )
    conn.commit()
    print(f"✅ Đã thêm {n} categories.")

# --- 5. Sinh dữ liệu cho bảng products ---
def generate_products(n=10000):
    cursor.execute("SELECT id FROM categories")
    category_ids = [row[0] for row in cursor.fetchall()]
    if not category_ids:
        print("⚠️ Chưa có dữ liệu categories, hãy chạy generate_categories trước!")
        return

    products = []
    for _ in range(n):
        products.append((
            fake.word().capitalize() + " " + fake.word().capitalize(),
            random.choice(category_ids),
            fake.sentence(nb_words=10),
            round(random.uniform(5, 500), 2)
        ))

    # Chèn theo batch để tránh quá tải
    BATCH_SIZE = 1000
    for i in range(0, len(products), BATCH_SIZE):
        cursor.executemany(
            "INSERT INTO products (product_name, category_id, description, price) VALUES (%s, %s, %s, %s)",
            products[i:i+BATCH_SIZE]
        )
        conn.commit()

    print(f"✅ Đã thêm {n} products.")

# --- 6. Chạy toàn bộ ---
if __name__ == "__main__":
    generate_users(total=100, admins=10)
    generate_categories(100)
    generate_products(10000)

    conn.close()
    print("🎉 Hoàn tất sinh dữ liệu vào MySQL.")
