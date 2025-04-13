import aiosqlite
from datetime import datetime
import logging

async def get_db_connection():
    db_connection = await aiosqlite.connect("db.db")
    await db_connection.execute("PRAGMA journal_mode=WAL;")
    await db_connection.commit()
    return db_connection

async def create_table(db_connection, gift_name):
    table_name = gift_name

    await db_connection.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            number INTEGER PRIMARY KEY,
            model_text TEXT,
            model_percent TEXT,
            backdrop_text TEXT,
            backdrop_percent TEXT,
            symbol_text TEXT,
            symbol_percent TEXT
        )
    """)
    await db_connection.commit()
    # logging.info(f"✅ Таблица для подарка {gift_name} создана.")

async def get_last_number(db_connection, gift_name):
    table_name = gift_name
    cursor = await db_connection.execute(f"SELECT MAX(number) FROM {table_name}")
    result = await cursor.fetchone()
    return result[0] if result[0] else 0

async def save_to_db(db_connection, gift_name, data):
    table_name = gift_name
    await db_connection.execute(f"""
        INSERT OR IGNORE INTO {table_name} (number, model_text, model_percent, backdrop_text, backdrop_percent, symbol_text, symbol_percent) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, data)
    await db_connection.commit()
    # logging.info(f"✅ Данные сохранены для {gift_name}: {data}")

async def get_links_by_model_name(db_connection, gift_name, model_name):
    table_name = gift_name
    query = f"SELECT number FROM {table_name} WHERE model_text = ?"

    try:
        async with db_connection.execute(query, (model_name,)) as cursor:
            rows = await cursor.fetchall()

        if rows:
            links = [f"https://t.me/nft/{gift_name}-{row[0]}" for row in rows]
            return links
        else:
            return []

    except Exception as e:
        logging.error(f"Ошибка при запросе ссылок для {gift_name}: {e}")
        return []

async def get_links_by_backdrop_name(db_connection, gift_name, backdrop_name):
    table_name = gift_name
    query = f"SELECT number FROM {table_name} WHERE backdrop_text = ?"

    try:
        async with db_connection.execute(query, (backdrop_name,)) as cursor:
            rows = await cursor.fetchall()

        if rows:
            links = [f"https://t.me/nft/{gift_name}-{row[0]}" for row in rows]
            return links
        else:
            return []

    except Exception as e:
        logging.error(f"Ошибка при запросе ссылок для {gift_name}: {e}")
        return []

async def get_links_by_model_and_backdrop_name(db_connection, gift_name, model_name, backdrop_name):
    table_name = gift_name
    query = f"SELECT number FROM {table_name} WHERE model_text = ? AND backdrop_text = ?"

    try:
        async with db_connection.execute(query, (model_name, backdrop_name,)) as cursor:
            rows = await cursor.fetchall()

        if rows:
            links = [f"https://t.me/nft/{gift_name}-{row[0]}" for row in rows]
            return links
        else:
            return []

    except Exception as e:
        logging.error(f"Ошибка при запросе ссылок для {gift_name}: {e}")
        return []

async def get_links_by_symbol_name(db_connection, gift_name, symbol_name):
    table_name = gift_name
    query = f"SELECT number FROM {table_name} WHERE symbol_text = ?"

    try:
        async with db_connection.execute(query, (symbol_name,)) as cursor:
            rows = await cursor.fetchall()

        if rows:
            links = [f"https://t.me/nft/{gift_name}-{row[0]}" for row in rows]
            return links
        else:
            return []

    except Exception as e:
        logging.error(f"Ошибка при запросе ссылок для {gift_name}: {e}")
        return []

async def get_links_by_number(db_connection, gift_name, number):
    table_name = gift_name
    
    if isinstance(number, list):
        placeholders = ",".join("?" * len(number))
        query = f"SELECT number FROM {table_name} WHERE number IN ({placeholders})"
        params = tuple(number)
    else:
        query = f"SELECT number FROM {table_name} WHERE number = ?"
        params = (number,)

    try:
        async with db_connection.execute(query, params) as cursor:
            rows = await cursor.fetchall()

        if rows:
            links = [f"https://t.me/nft/{gift_name}-{row[0]}" for row in rows]
            return links
        else:
            return []

    except Exception as e:
        logging.error(f"Ошибка при запросе ссылок для {gift_name}: {e}")
        return []


    except Exception as e:
        logging.error(f"Ошибка при запросе ссылок для {gift_name}: {e}")
        return []
    
async def get_db_info(db_connection):
    
    async with db_connection.execute("SELECT name FROM sqlite_master WHERE type='table';") as cursor:
        tables = await cursor.fetchall()
    
    db_info = {}
    
    for table in tables:
        table_name = table[0]
        async with db_connection.execute(f"SELECT COUNT(*) FROM {table_name}") as cursor:
            row_count = await cursor.fetchone()
            db_info[table_name] = {
                'row_count': row_count[0]
            }
    
    return db_info

async def get_global_links_by_backdrop_name(db_connection, backdrop_name):
    query_tables = "SELECT name FROM sqlite_master WHERE type='table';"
    
    try:
        async with db_connection.execute(query_tables) as cursor:
            tables = await cursor.fetchall()

        if tables:
            all_links = []
            for table in tables:
                table_name = table[0]
                query = f"SELECT number FROM {table_name} WHERE backdrop_text = ?"
                
                async with db_connection.execute(query, (backdrop_name,)) as cursor:
                    rows = await cursor.fetchall()
                
                if rows:
                    links = [f"https://t.me/nft/{table_name}-{row[0]}" for row in rows]
                    all_links.extend(links)
                
            return all_links if all_links else []

        return []

    except Exception as e:
        logging.error(f"Ошибка при запросе ссылок по всем таблицам для {backdrop_name}: {e}")
        return []
    
async def get_global_links_by_symbol_name(db_connection, symbol_name):
    query_tables = "SELECT name FROM sqlite_master WHERE type='table';"
    
    try:
        async with db_connection.execute(query_tables) as cursor:
            tables = await cursor.fetchall()

        if tables:
            all_links = []
            for table in tables:
                table_name = table[0]
                query = f"SELECT number FROM {table_name} WHERE symbol_text = ?"
                
                async with db_connection.execute(query, (symbol_name,)) as cursor:
                    rows = await cursor.fetchall()
                
                if rows:
                    links = [f"https://t.me/nft/{table_name}-{row[0]}" for row in rows]
                    all_links.extend(links)
                
            return all_links if all_links else []

        return []

    except Exception as e:
        logging.error(f"Ошибка при запросе ссылок по всем таблицам для {symbol_name}: {e}")
        return []

async def get_global_links_by_backdrop_and_symbol_name(db_connection, backdrop_name, symbol_name):
    
    query_tables = "SELECT name FROM sqlite_master WHERE type='table';"

    try:
        async with db_connection.execute(query_tables) as cursor:
            tables = await cursor.fetchall()

        if tables:
            all_links = []
            for table in tables:
                table_name = table[0]
                query = f"SELECT number FROM {table_name} WHERE backdrop_text = ? AND symbol_text = ?"
                
                async with db_connection.execute(query, (backdrop_name, symbol_name)) as cursor:
                    rows = await cursor.fetchall()
                
                if rows:
                    links = [f"https://t.me/nft/{table_name}-{row[0]}" for row in rows]
                    all_links.extend(links)
            
            return all_links if all_links else []
        
        return []

    except Exception as e:
        logging.error(f"Ошибка при запросе ссылок по всем таблицам для backdrop_name={backdrop_name} и symbol_name={symbol_name}: {e}")
        return []

async def get_number_of_tables(db_connection):
    query = "SELECT COUNT(name) FROM sqlite_master WHERE type='table';"
    
    try:
        async with db_connection.execute(query) as cursor:
            count = await cursor.fetchone()
        
        return count[0] if count else 0

    except Exception as e:
        logging.error(f"Ошибка при получении количества таблиц: {e}")
        return 0
    
async def get_total_number_gifts(db_connection):
    try:
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        async with db_connection.execute(query) as cursor:
            tables = await cursor.fetchall()

        total_number_gifts = 0

        for table in tables:
            table_name = table[0]
            query = f"SELECT MAX(number) FROM {table_name};"
            
            async with db_connection.execute(query) as cursor:
                result = await cursor.fetchone()
                total_number_gifts += result[0] if result[0] is not None else 0

        return total_number_gifts

    except Exception as e:
        logging.error(f"Ошибка при получении последнего номера 'number': {e}")
        return 0
    
async def get_statistics(db_connections):
    try:
        total_unique_models = 0
        total_unique_backdrops_set = set()
        total_unique_symbols_set = set()

        if not isinstance(db_connections, (list, tuple)):
            db_connections = [db_connections]

        for db_connection in db_connections:
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            async with db_connection.execute(query) as cursor:
                tables = await cursor.fetchall()

            for table in tables:
                table_name = table[0]

                query = f"SELECT COUNT(DISTINCT model_text) FROM {table_name};"
                async with db_connection.execute(query) as cursor:
                    result = await cursor.fetchone()
                    if result[0] is not None:
                        total_unique_models += result[0]

                query = f"SELECT DISTINCT backdrop_text FROM {table_name};"
                async with db_connection.execute(query) as cursor:
                    result = await cursor.fetchall()
                    for row in result:
                        if row[0] is not None:
                            total_unique_backdrops_set.add(row[0])

                query = f"SELECT DISTINCT symbol_text FROM {table_name};"
                async with db_connection.execute(query) as cursor:
                    result = await cursor.fetchall()
                    for row in result:
                        if row[0] is not None:
                            total_unique_symbols_set.add(row[0])

        total_unique_backdrops = len(total_unique_backdrops_set)
        total_unique_symbols = len(total_unique_symbols_set)

        return {
            "total_unique_models": total_unique_models,
            "total_unique_backdrops": total_unique_backdrops,
            "total_unique_symbols": total_unique_symbols,
        }

    except Exception as e:
        logging.error(f"Ошибка при получении статистики из всех баз данных: {e}")
        return {
            "total_unique_models": 0,
            "total_unique_backdrops": 0,
            "total_unique_symbols": 0,
        }
    
async def get_owner_from_db_and_parse(db_connection, session, gift_name, number):
    
    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{gift_name}'"
    async with db_connection.execute(query) as cursor:
        table_exists = await cursor.fetchone()

    if not table_exists:
        logging.error(f"Таблица с именем {gift_name} не существует.")
        return None

    query = f"SELECT number FROM {gift_name} WHERE number = ?"
    try:
        async with db_connection.execute(query, (number,)) as cursor:
            rows = await cursor.fetchall()

        if rows:
            gift_number = rows[0][0]
            from handlers import parse_owner
            number, owner_nick = await parse_owner(session, gift_name, gift_number)
            return owner_nick
        else:
            return None

    except Exception as e:
        logging.error(f"Ошибка при запросе для {gift_name}, {number}: {e}")
        return None
