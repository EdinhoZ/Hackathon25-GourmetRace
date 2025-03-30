import mysql.connector

# MySQL database connection settings
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "CryptoDreamDB"
}

# List of coins to store
COINS = [
    {"name": "Bitcoin", "code": "BTC"},
    {"name": "Ethereum", "code": "ETH"},
    {"name": "Tether", "code": "USDT"},
    {"name": "XRP", "code": "XRP"},
    {"name": "BNB", "code": "BNB"},
    {"name": "Solana", "code": "SOL"},
    {"name": "USD Coin", "code": "USDC"},
    {"name": "Dogecoin", "code": "DOGE"},
    {"name": "Cardano", "code": "ADA"},
    {"name": "Tron", "code": "TRX"},
]

# Connect to MySQL
try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Coin (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            code VARCHAR(100) UNIQUE NOT NULL
        )
    """)

    # Function to store the coins in the database
    def store_coins():
        for coin in COINS:
            coin_name = coin["name"]
            coin_code = coin["code"]

            try:
                # Insert or ignore duplicate entries
                cursor.execute("""
                    INSERT INTO Coin (name, code) 
                    VALUES (%s, %s) 
                    ON DUPLICATE KEY UPDATE name=name
                """, (coin_name, coin_code))

                conn.commit()  # Save changes
                print(f"Stored {coin_name} ({coin_code}) in the database.")

            except mysql.connector.Error as err:
                print(f"Error inserting {coin_name}: {err}")

    # Run the function to store coins
    store_coins()

except mysql.connector.Error as err:
    print(f"Database error: {err}")

finally:
    # Close database connection
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()