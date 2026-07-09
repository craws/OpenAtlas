import json
import os
from flask import g
from openatlas import app
from openatlas.database.connect import Transaction

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_path, "thanados_all_corrected.json")
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} does not exist.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        entities = json.load(f)

    print(f"Loaded {len(entities)} entities from {input_path}")

    with app.test_request_context():
        app.preprocess_request()
        
        print("Starting database updates...")
        Transaction.begin()
        try:
            count = 0
            for entity in entities:
                entity_id = entity["id"]
                description_translated = entity["description_translated"]
                
                g.cursor.execute(
                    "UPDATE model.entity SET description = %s WHERE id = %s",
                    (description_translated, entity_id)
                )
                count += 1
                if count % 2000 == 0:
                    print(f"Updated {count} / {len(entities)} entities...")
            
            Transaction.commit()
            print(f"Successfully committed {count} entity description updates to the database.")
        except Exception as e:
            Transaction.rollback()
            print(f"Error during updates, transaction rolled back: {e}")
            raise e

if __name__ == "__main__":
    main()
