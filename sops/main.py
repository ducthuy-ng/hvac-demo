import pathlib
import yaml
import psycopg2


base_path = pathlib.Path(__file__) / "team_A/"

key_path = base_path / "key.yaml"

with open(key_path, "r") as file:
    credential = yaml.safe_load(file).get("data")

connection = psycopg2.connect(
    dbname="postgres",
    user=credential.get("username"),
    password=credential.get("password"),
    host=credential.get("server"),
    port=credential.get("port"),
)

print("Create connection successfully!")
print("Your data:")

cursor = connection.cursor()

cursor.execute("SELECT * FROM DEPARTMENT;")
records = cursor.fetchall()
print(records)
