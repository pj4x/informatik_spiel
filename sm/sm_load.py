import sqlite3

import sm_item


def load_items_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT ID, type, image FROM items")
    rows = cursor.fetchall()

    items = []
    for row in rows:
        item = sm_item.sm_item(ID=row[0], type=row[1], image=row[2])
        items.append(item)

    conn.close()
    return items


def load_inventory(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT ID, ItemID, place, slot FROM inventory")
    rows = cursor.fetchall()

    storage_ids = [-1] * 42
    armor_ids = [-1] * 2
    equip_ids = [-1] * 4

    for row in rows:
        # check place and slot to put into correct slot in inventory
        if row[2] == 0:
            if row[3] < 42:
                storage_ids[row[3]] = row[1]
            else:
                print("WARNING: invalid data in db")
        elif row[2] == 1:
            if row[3] < 2:
                armor_ids[row[3]] = row[1]
            else:
                print("WARNING: invalid data in db")
        elif row[2] == 2:
            if row[3] < 4:
                equip_ids[row[3]] = row[1]
            else:
                print("WARNING: invalid data in db")

    return (storage_ids, armor_ids, equip_ids)


def store_inventory(db_path, storage_ids, armor_ids, equip_ids):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # empty table before inserting new data
    cursor.execute("DELETE FROM inventory WHERE ID = *")

    ID = 0
    for i in range(len(storage_ids)):
        if not storage_ids[i] == -1:
            cursor.execute(
                f"INSERT INTO inventory (ID, ItemID, place, slot) VALUES ({ID}, {storage_ids[i]}, 0, {i});"
            )
        ID += 1

    for i in range(len(armor_ids)):
        if not armor_ids[i] == -1:
            cursor.execute(
                f"INSERT INTO inventory (ID, ItemID, place, slot) VALUES ({ID}, {armor_ids[i]}, 1, {i});"
            )
        ID += 1

    for i in range(len(equip_ids)):
        if not equip_ids[i] == -1:
            cursor.execute(
                f"INSERT INTO inventory (ID, ItemID, place, slot) VALUES ({ID}, {equip_ids[i]}, 2, {i});"
            )
        ID += 1
