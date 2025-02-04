WITH first_week AS (
    SELECT
        ID_BUYER,
        SUM(REVENUE) AS revenue_week1
    FROM
        sales
    WHERE
        DATE_PAYMENT BETWEEN '2021-01-01'
        AND '2021-01-07'
    GROUP BY
        ID_BUYER
),
second_week AS (
    SELECT
        ID_BUYER,
        SUM(REVENUE) AS revenue_week2
    FROM
        sales
    WHERE
        DATE_PAYMENT BETWEEN '2021-01-08'
        AND '2021-01-14'
    GROUP BY
        ID_BUYER
),
repeat_buyers AS (
    SELECT
        f.ID_BUYER,
        f.revenue_week1,
        s.revenue_week2
    FROM
        first_week f
        JOIN second_week s ON f.ID_BUYER = s.ID_BUYER
)
SELECT
    SUM(revenue_week1) AS total_revenue_week1,
    SUM(revenue_week2) AS total_revenue_week2,
    CASE
        WHEN SUM(revenue_week1) = 0 THEN NULL
        ELSE (SUM(revenue_week2) - SUM(revenue_week1)) * 100.0 / SUM(revenue_week1)
    END AS percentage_change
FROM
    repeat_buyers;