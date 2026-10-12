-- Counts include all priorities; filters must never replace actual capacity.
SELECT status, COUNT(*) n FROM snapshot WHERE assignee_id=? GROUP BY status;
