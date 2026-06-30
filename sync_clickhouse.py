import os
import django
import clickhouse_connect

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wichit2s.settings')
django.setup()

from sales.models import Order

def sync_data():
    print("Connecting to ClickHouse...")
    # Connect to ClickHouse (default credentials)
    client = clickhouse_connect.get_client(host='localhost', port=8123, username='default', password='')

    print("Creating table in ClickHouse...")
    client.command('''
        CREATE TABLE IF NOT EXISTS sales_order (
            id UInt32,
            order_number String,
            quantity UInt32,
            total_price Float32,
            status String,
            created_at DateTime
        ) ENGINE = MergeTree()
        ORDER BY id
    ''')

    print("Fetching data from Django (SQLite)...")
    orders = Order.objects.all().values_list('id', 'order_number', 'quantity', 'total_price', 'status', 'created_at')
    
    # Convert data for ClickHouse
    data = []
    for order in orders:
        data.append([
            order[0], 
            order[1], 
            order[2], 
            float(order[3]), # total_price Decimal to float
            order[4], 
            order[5].replace(tzinfo=None) # remove timezone for ClickHouse DateTime
        ])

    if data:
        print(f"Inserting {len(data)} records into ClickHouse...")
        client.insert('sales_order', data, column_names=['id', 'order_number', 'quantity', 'total_price', 'status', 'created_at'])
        print("Integration Complete! Data is now in ClickHouse.")
    else:
        print("No data found in Django. Please run generate_sale.py first.")

if __name__ == '__main__':
    sync_data()
