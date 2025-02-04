WITH country_revenue AS (
    SELECT
        c1.COUNTRY_NAME AS country_a,
        c2.COUNTRY_NAME AS country_b,
        SUM(s.REVENUE) AS total_revenue
    FROM
        sales s
        JOIN country c1 ON s.ID_SELLER_COUNTRY = c1.ID_COUNTRY
        JOIN country c2 ON s.ID_BUYER_COUNTRY = c2.ID_COUNTRY
    WHERE
        c1.ID_COUNTRY <> c2.ID_COUNTRY
    GROUP BY
        c1.COUNTRY_NAME,
        c2.COUNTRY_NAME
),
bidirectional_revenue AS (
    SELECT
        LEAST(country_a, country_b) AS country_x,
        GREATEST(country_a, country_b) AS country_y,
        SUM(total_revenue) AS combined_revenue
    FROM
        country_revenue
    GROUP BY
        country_x,
        country_y
)
SELECT
    country_x,
    country_y,
    combined_revenue
FROM
    bidirectional_revenue
ORDER BY
    combined_revenue DESC
LIMIT
    1;