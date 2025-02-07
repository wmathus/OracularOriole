import mysql.connector
from config import DB_CONFIG

def test_snp_query():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Replace this with a real SNP ID from your database
        test_snp_id = "rs10916784-G"
        cursor.execute("SELECT * FROM snps WHERE snp_id = %s", (test_snp_id,))
        results = cursor.fetchall()

        if results:
            print("✅ Data retrieved from MySQL:", results)
        else:
            print("❌ No data found for SNP ID:", test_snp_id)

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"❌ MySQL connection error: {err}")

# Run the test
test_snp_query()


