from binance.client import Client
import pandas as pd
import mysql.connector
import datetime

# MySQL database connection settings
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "CryptoDreamDB"
}

# Initialize Binance Client (No API key required for public data)
client = Client()

# List of coins to fetch in EUR
# bitcoin, ethereum, tether, xrp, bnb, solana, usdc, dogecoin, cardano, tron
symbols = ["BTCEUR", "ETHEUR", "BNBEUR", "XRPEUR", "ADAEUR", "SOLEUR",  "DOGEEUR", "TRXEUR" ]
interval = Client.KLINE_INTERVAL_1DAY
start_date = "2017-01-01"
end_date = "2025-03-27"

# Connect to MySQL and create table if not exists
def create_table():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historical_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME,
            symbol VARCHAR(10),
            open DECIMAL(18,8),
            high DECIMAL(18,8),
            low DECIMAL(18,8),
            close DECIMAL(18,8),
            volume DECIMAL(18,8)
        )
    """)
    conn.commit()
    conn.close()

# Function to store data in MySQL
def store_data(df, symbol):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO historical_data (timestamp, symbol, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (row.name, symbol, row.open, row.high, row.low, row.close, row.volume))
    
    conn.commit()
    conn.close()

# Create table
create_table()

# Fetch and store data for each symbol
for symbol in symbols:
    print(symbol)
    klines = client.get_historical_klines(symbol, interval, start_date, end_date)
    
    # Convert to DataFrame
    df = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", 
                                        "volume", "close_time", "quote_asset_volume", 
                                        "number_of_trades", "taker_buy_base", 
                                        "taker_buy_quote", "ignore"])
    
    # Convert timestamp to readable date
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    df = df[["open", "high", "low", "close", "volume"]]
    
    # Store data in MySQL
    store_data(df, symbol)
    
    # Save data to CSV
    csv_filename = f"{symbol}_historical_data.csv"
    df.to_csv(csv_filename)
    
    print(f"Stored data for {symbol} and saved to {csv_filename}")



def get_coin_data(currency):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)  # Para retornar os dados como um dicionario
    
    symbol = currency + "EUR"
    try:
        query = """
            SELECT timestamp, open, high, low, close, volume
            FROM historical_data
            WHERE symbol = %s
            ORDER BY timestamp ASC
        """
        
        cursor.execute(query, (symbol,))
        
        rows = cursor.fetchall()
        
        data = []
        for row in rows:
            data.append({
                "timestamp": row["timestamp"],
                "open": row["open"],
                "high": row["high"],
                "low": row["low"],
                "close": row["close"],
                "volume": row["volume"]
            })
        
        return data
    except Exception as e:
        print(f"Can't find the currency in the database. Error: {e}")
        return []
    finally:
        conn.close()


def get_coin_data_by_date(currency, date):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)  
    
    symbol = currency + "EUR"
    
    try:
        # Consulta SQL para obter o primeiro dado encontrado para a moeda e a data especificada
        query = """
            SELECT timestamp, open, high, low, close, volume
            FROM historical_data
            WHERE symbol = %s AND DATE(timestamp) = %s
            ORDER BY timestamp ASC
        """
        
        cursor.execute(query, (symbol, date.date()))
        
        # Obter o primeiro resultado
        row = cursor.fetchone()  # Use fetchone para pegar o primeiro registro encontrado
        
        if not row:
            print(f"Não foram encontrados dados para {currency}.")
            return []
        
        data = {
            "timestamp": row["timestamp"],
            "open": row["open"],
            "high": row["high"],
            "low": row["low"],
            "close": row["close"],
            "volume": row["volume"]
        }
        
        return data
    
    except mysql.connector.Error as err:
        print(f"Erro MySQL: {err}")
        return {}
    
    except Exception as e:
        print(f"Erro: {e}")
        return {}
    
    finally:
        conn.close()