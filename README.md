# Release-Gated Transaction Service (Local Docker Demo)

This is a small local project that demonstrates a **post-deployment validation gate**.

It runs three containers on your laptop using Docker Compose:

- **Postgres DB**: stores transactions in a ledger table
- **API service**: accepts transactions and inserts them into the DB
- **Validator**: runs SQL checks after “deployment” and outputs **PASS/FAIL**
  - exits `0` when healthy (PASS)
  - exits `1` when unhealthy (FAIL)

This mirrors how real CI/CD pipelines block a release or trigger rollback when validation fails.

---

## What this demonstrates 

After a release, it’s possible for the service to be “up” but still unhealthy (stuck transactions, failure spikes, etc.).
This project simulates a **release gate** that checks database integrity signals after deployment.

Checks included:
- Duplicate transaction IDs (should be 0)
- Stuck transactions (pending/processing older than 1 minute)
- Missing required fields (should be 0)
- Failure spike threshold in last 30 minutes (FAIL if failures > 2)

---

## Requirements

- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)

---

## Run the system (deploy locally)

From the project root:

```bash
docker compose up --build -d
