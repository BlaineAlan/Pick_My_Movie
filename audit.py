import json
import csv 
from db import cur, conn

def log_action(user_id, action_type, metadata=None):
    """Insert an action into the audit_log table."""
    try:
        cur.execute("""
            INSERT INTO audit_log (user_id, action_type, metadata)
            VALUES (%s, %s, %s)
        """, (user_id, action_type, json.dumps(metadata) if metadata else None))
        conn.commit()
    except Exception as e:
        print(f"Failed to log action: {e}")


def export_audit_log(filename="audit_log.csv"):
    cur.execute("SELECT * FROM audit_log ORDER BY action_timestamp ASC")
    rows = cur.fetchall()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([i[0] for i in cur.description])  # column headers
        writer.writerows(rows)
    print(f"Audit log exported to {filename}")
