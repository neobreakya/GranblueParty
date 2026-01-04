#!/usr/bin/env python3

from config import dbconfig

cursor = dbconfig.getCursor()

# Get all tables
cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORDER BY table_name;
""")

tables = cursor.fetchall()
print(f'Total tables: {len(tables)}\n')
print('Tables in database:')
for table in tables:
    print(f'  - {table[0]}')

# Get row counts for each table
print('\nRow counts:')
for table in tables:
    table_name = table[0]
    cursor.execute(f'SELECT COUNT(*) FROM {table_name};')
    count = cursor.fetchone()[0]
    print(f'  {table_name}: {count} rows')

# Get column info for main tables
main_tables = ['character', 'summon', 'weapon', 'class']
print('\n\nColumn information for main tables:')
for table_name in main_tables:
    cursor.execute(f"""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position;
    """)
    columns = cursor.fetchall()
    print(f'\n{table_name}:')
    for col in columns:
        print(f'  - {col[0]}: {col[1]}')

dbconfig.getConnection().close()
