import pandas as pd
import random
from faker import Faker
from datetime import date
from pathlib import Path

# init
fake = Faker()
start_date = date(2024, 1, 1)
end_date = date(2024, 12, 31)

# read original data
original_file = r'Excel_file_to_upload/sales_analytics_2022.xlsx'
df_users = pd.read_excel(original_file, sheet_name="users")
df_transactions = pd.read_excel(original_file, sheet_name="transactions")
df_items = pd.read_excel(original_file, sheet_name="items")

# print columns for reference
print("ITEMS colums: ", df_items.columns.tolist())
print("USERS colums: ", df_users.columns.tolist())
print("TRANSACTIONS colums: ", df_transactions.columns.tolist())

# generate users
def generate_users(n):
    users = []
    for i in range(1, n + 1):
        first_name = fake.first_name()
        last_name = fake.last_name()
        full_name = f"{first_name} {last_name}"
        gender = random.choice(["male", "female"])
        birth_date = fake.date_of_birth(minimum_age=7, maximum_age=120)
        users.append([i, first_name, last_name, full_name, gender, birth_date])
    return pd.DataFrame(users, columns=df_users.columns)

# generate products
def generate_items(n):
    items = []
    # 修正季节格式以匹配过滤器
    seasons = ['spring/summer', 'fall/winter']
    colors = ['Red', 'Blue', 'Green', 'Black', 'White', 'Yellow']
    printings = ['Floral', 'Solid', 'Striped', 'Polka Dot', 'Geometric']
    fabrics = ['Cotton', 'Linen', 'Silk', 'Wool', 'Polyester']
    categories = ['Tops', 'Bottoms', 'Dresses', 'Outerwear', 'Accessories']

    for i in range(1, n + 1):
        item_id = i
        # 确保item_tags包含性别标签
        gender = random.choice(['male', 'female'])
        additional_tags = ', '.join(fake.words(nb=random.randint(1, 2)))
        item_tags = f"{gender}, {additional_tags}" if additional_tags else gender
        
        season = random.choice(seasons)  # 使用正确的季节格式
        category = random.choice(categories)
        price = round(random.uniform(5.0, 200.0), 2)
        color = random.choice(colors)
        printing = random.choice(printings)
        fabric = random.choice(fabrics)
        item_name = f"{fabric} {printing} {category}"
        image_url = fake.image_url(width=300, height=400)
        
        items.append([
            item_id, item_tags, season, category, price, color,
            printing, fabric, item_name, image_url
        ])
    
    return pd.DataFrame(items, columns=df_items.columns)

# generate transactions
def generate_transactions(n, user_ids, item_ids):
    transactions = []
    for _ in range(n):
        user_id = random.choice(user_ids)
        item_id = random.choice(item_ids)
        amount = random.randint(1, 5)  # 减小数量范围使其更现实
        order_date = fake.date_between(start_date=start_date, end_date=end_date)
        transactions.append([user_id, item_id, amount, order_date])
    return pd.DataFrame(transactions, columns=df_transactions.columns)

# 
new_users = generate_users(500)  # 生成500个用户
new_items = generate_items(300)  # 生成300个商品
new_transactions = generate_transactions(3200, new_users["user_id"].tolist(), new_items["item_id"].tolist())  # 生成3200笔交易

# save Excel file
output_file = r'Excel_file_to_upload/sales_analytics_2024.xlsx'
with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
    new_users.to_excel(writer, sheet_name="users", index=False)
    new_transactions.to_excel(writer, sheet_name="transactions", index=False)
    new_items.to_excel(writer, sheet_name="items", index=False)

print(f"✅ Fake data generated at: {Path(output_file).absolute()}") 