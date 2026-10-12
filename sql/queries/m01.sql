-- Transient event-replayed snapshot at as_of; {filters} is server-built SQL.
SELECT SUM(p_status='met') numerator,
       SUM(p_status IN ('met','breached')) denominator,
       SUM(p_status='pending') pending
FROM snapshot WHERE {filters} AND created_at>=? AND created_at<?;
