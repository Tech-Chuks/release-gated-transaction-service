import os
import psycopg2
from datetime import datetime

DB = os.environ["DATABASE_URL"]
CHECKS_SQL_PATH = os.path.join(os.path.dirname(__file__), "checks.sql")

def run_checks():
    with open(CHECKS_SQL_PATH, "r", encoding="utf-8") as f:
        sql = f.read()

    results = []
    with psycopg2.connect(DB) as conn, conn.cursor() as cur:
        statements = [s.strip() for s in sql.split(";") if s.strip()]
        for stmt in statements:
            cur.execute(stmt)
            row = cur.fetchone()
            results.append((row[0], int(row[1])))

    return results

def main():
    results = run_checks()
    now = datetime.utcnow().isoformat() + "Z"

    lines = [f"POST-DEPLOY VALIDATION REPORT - {now}", "-" * 50]
    failed = False
    for name, failures in results:
        status = "PASS" if failures == 0 else "FAIL"
        lines.append(f"{name}: {status} (failures={failures})")
        if failures != 0:
            failed = True

    report = "\n".join(lines)
    print(report)
    raise SystemExit(1 if failed else 0)

if __name__ == "__main__":
    main()
