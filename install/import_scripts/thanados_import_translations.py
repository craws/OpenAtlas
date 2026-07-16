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
            skipped = 0
            conflicts = 0
            for entity in entities:
                entity_id = entity["id"]
                description_translated = entity["description_translated"]
                # Original description captured when the snapshot/JSON was built.
                original_description = entity.get("description")

                # Fetch the current model.entity entry to make sure it exists
                # before replacing its description (secure, no blind updates).
                g.cursor.execute(
                    "SELECT id, description FROM model.entity WHERE id = %s",
                    (entity_id,)
                )
                row = g.cursor.fetchone()
                if row is None:
                    print(f"Warning: entity {entity_id} not found in database, skipping.")
                    skipped += 1
                    continue

                # Skip if the description is already up to date.
                if row["description"] == description_translated:
                    skipped += 1
                    continue

                # Safety guard: only apply the correction if the current
                # description still matches the original snapshot. If it was
                # changed in the meantime (e.g. a manual fix by a colleague),
                # skip it so we never overwrite newer edits with stale data.
                if original_description is not None and row["description"] != original_description:
                    print(
                        f"Conflict: entity {entity_id} was modified since the "
                        f"snapshot was taken, skipping to avoid overwriting."
                    )
                    conflicts += 1
                    continue

                g.cursor.execute(
                    "UPDATE model.entity SET description = %s WHERE id = %s",
                    (description_translated, entity_id)
                )
                count += 1
                if count % 2000 == 0:
                    print(f"Updated {count} / {len(entities)} entities...")

            Transaction.commit()
            print(
                f"Successfully committed {count} entity description updates "
                f"to the database ({skipped} skipped, {conflicts} conflicts)."
            )
        except Exception as e:
            Transaction.rollback()
            print(f"Error during updates, transaction rolled back: {e}")
            raise e


if __name__ == "__main__":
    main()
