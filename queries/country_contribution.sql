WITH total_sales AS (
    SELECT
        SUM(REVENUE) AS total_revenue,
        COUNT(*) AS total_items_sold
    FROM
        sales
),
country_sales AS (
    SELECT
        c.COUNTRY_NAME,
        SUM(s.REVENUE) AS country_revenue,
        COUNT(*) AS country_items_sold
    FROM
        sales s
        JOIN country c ON s.ID_SELLER_COUNTRY = c.ID_COUNTRY
    GROUP BY
        c.COUNTRY_NAME
)
SELECT
    cs.COUNTRY_NAME,
    (cs.country_revenue / ts.total_revenue) * 100 AS revenue_contribution_percentage,
    (
        cs.country_items_sold :: FLOAT / ts.total_items_sold
    ) * 100 AS items_sold_contribution_percentage
FROM
    country_sales cs,
    total_sales ts;