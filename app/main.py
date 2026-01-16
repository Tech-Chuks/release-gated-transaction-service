import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import psycopg2

DB = os.environ["DATABASE_URL"]

def get_conn():
    return psycopg2.connect(DB)

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode("utf-8"))

    def do_GET(self):
        if self.path == "/health":
            return self._send(200, {"status": "ok"})
        return self._send(404, {"error": "not_found"})

    def do_POST(self):
        if self.path != "/transactions":
            return self._send(404, {"error": "not_found"})

        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length).decode("utf-8"))

        tx_id = payload["transaction_id"]
        merchant_id = payload["merchant_id"]
        amount = payload["amount"]
        status = payload.get("status", "approved")

        try:
            with get_conn() as conn, conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO ledger_transactions (transaction_id, merchant_id, amount, status)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (transaction_id) DO NOTHING
                    """,
                    (tx_id, merchant_id, amount, status),
                )
            return self._send(200, {"message": "recorded", "transaction_id": tx_id})
        except Exception as e:
            return self._send(500, {"error": str(e)})

if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
