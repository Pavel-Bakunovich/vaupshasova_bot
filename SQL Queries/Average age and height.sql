SELECT 
    ROUND(AVG(Height), 2) AS "Average Height (cm)",
    ROUND(AVG(EXTRACT(YEAR FROM AGE(Birthday))), 2) AS "Average Age (years)"
FROM Players
WHERE Height IS NOT NULL
    AND Birthday IS NOT NULL;