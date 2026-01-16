SELECT 'duplicate_transaction_ids' AS check_name,
       COUNT(*) AS failures
FROM (
  SELECT transaction_id
  FROM ledger_transactions
  GROUP BY transaction_id
  HAVING COUNT(*) > 1
) d;

SELECT 'stuck_transactions' AS check_name,
       COUNT(*) AS failures
FROM ledger_transactions
WHERE status IN ('processing', 'pending')
  AND updated_time < NOW() - INTERVAL '1 minute';

SELECT 'missing_required_fields' AS check_name,
       COUNT(*) AS failures
FROM ledger_transactions
WHERE transaction_id IS NULL OR merchant_id IS NULL OR amount IS NULL OR status IS NULL;

SELECT 'recent_failures_over_threshold' AS check_name,
       CASE WHEN SUM(CASE WHEN status IN ('failed','declined') THEN 1 ELSE 0 END) > 2
            THEN 1 ELSE 0 END AS failures
FROM ledger_transactions
WHERE created_time > NOW() - INTERVAL '30 minutes';
