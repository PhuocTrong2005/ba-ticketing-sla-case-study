SELECT SUM(rejection_count>=1) numerator, COUNT(*) denominator, 0 pending
FROM snapshot WHERE {filters} AND status='CLOSED' AND closed_at>=? AND closed_at<?;
