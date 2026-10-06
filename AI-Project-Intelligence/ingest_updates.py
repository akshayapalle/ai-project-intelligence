import os
import psycopg
from datetime import datetime

connection = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="shopsphere",
    user="postgres",
    password="x"
)

cursor = connection.cursor()

updates_folder = "dataset/updates"

for filename in sorted(os.listdir(updates_folder)):

    if not filename.endswith(".txt"):
        continue

    file_path = os.path.join(updates_folder, filename)

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # --------------------------------
    # Extract information from the file
    # --------------------------------

    lines = content.splitlines()

    date_value = None
    submitted_by = None
    update_type = None

    for line in lines:

        if line.startswith("Date:"):
            date_text = line.replace("Date:", "").strip()
            date_value = datetime.strptime(date_text, "%Y-%m-%d").date()

        elif line.startswith("From:"):
            submitted_by = line.replace("From:", "").strip()

        elif line.startswith("Type:"):
            update_type = line.replace("Type:", "").strip()

    update_id = filename.replace(".txt", "")

    # --------------------------------
    # Insert into PostgreSQL
    # --------------------------------

    cursor.execute("""
        INSERT INTO updates
        (
            update_id,
            project_id,
            submitted_by,
            update_date,
            update_type,
            source,
            content
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)

        ON CONFLICT (update_id)
        DO UPDATE SET
            submitted_by = EXCLUDED.submitted_by,
            update_date = EXCLUDED.update_date,
            update_type = EXCLUDED.update_type,
            content = EXCLUDED.content;
    """, (
        update_id,
        "P001",
        submitted_by,
        date_value,
        update_type,
        "TEXT_FILE",
        content
    ))

    print(f"Processed: {filename}")

connection.commit()

print("\nAll project updates processed successfully!")

cursor.close()
connection.close()
