--How many food providers and receivers are there in each city?
SELECT
    c.city,
    COALESCE(p.providers_count, 0) AS providers_count,
    COALESCE(r.receivers_count, 0) AS receivers_count
FROM (
    SELECT city FROM providers_data
    UNION
    SELECT city FROM receivers_data
) c
LEFT JOIN (
    SELECT city, COUNT(DISTINCT provider_id) AS providers_count
    FROM providers_data
    GROUP BY city
) p ON c.city = p.city
LEFT JOIN (
    SELECT city, COUNT(DISTINCT receiver_id) AS receivers_count
    FROM receivers_data
    GROUP BY city
) r ON c.city = r.city
ORDER BY c.city;

--Which type of food provider contributes the most food? (based on listed quantity)
SELECT
    p.Type,
    SUM(l.quantity) AS total_listed_quantity
FROM food_listings_data l
JOIN providers_data p ON l.provider_id = p.provider_id
GROUP BY p.Type
ORDER BY total_listed_quantity DESC;

--Contact info of food providers in a specific city
SELECT
    Provider_ID,
    Name,
    Type,
    City,
    Contact,
    Address
FROM providers_data
WHERE city = 'Jasonland';

--Which receivers have claimed the most food?
SELECT Top 10
    r.Receiver_ID,
    r.Name,
    COUNT(*) AS completed_claims
FROM claims_data c
JOIN receivers_data r
    ON c.Receiver_ID = r.Receiver_ID
WHERE LOWER(c.Status) = 'completed'
GROUP BY r.Receiver_ID, r.Name
ORDER BY completed_claims DESC;

--Total quantity of food available from all providers
SELECT 
    p.Provider_ID,
    p.Name,
    SUM(TRY_CAST(fl.Quantity AS DECIMAL(18,2))) AS total_food_available
FROM food_listings_data fl
JOIN providers_data p
    ON fl.Provider_ID = p.Provider_ID
GROUP BY p.Provider_ID, p.Name
ORDER BY total_food_available DESC;

--City with the highest number of food listings
SELECT TOP 1
    Location AS City,
    COUNT(*) AS total_listings
FROM food_listings_data
GROUP BY Location
ORDER BY total_listings DESC;

--Most commonly available food types
SELECT
    Food_Type,
    COUNT(*) AS listings_count
FROM food_listings_data
GROUP BY Food_Type
ORDER BY listings_count DESC;

--How many food claims have been made for each food item?
SELECT
    fl.Food_Name,
    COUNT(*) AS total_claims
FROM claims_data c
JOIN food_listings_data fl
    ON c.Food_ID = fl.Food_ID
GROUP BY fl.Food_Name
ORDER BY total_claims DESC;

--Which provider has had the highest number of successful food claims?
SELECT TOP 1
    p.Provider_ID,
    p.Name,
    COUNT(*) AS successful_claims
FROM claims_data c
JOIN food_listings_data fl
    ON c.Food_ID = fl.Food_ID
JOIN providers_data p
    ON fl.Provider_ID = p.Provider_ID
WHERE LOWER(c.Status) = 'completed'
GROUP BY p.Provider_ID, p.Name
ORDER BY successful_claims DESC;

--Percentage of food claims by status (completed vs. pending vs. canceled)
SELECT
    Status,
    COUNT(*) AS claim_count,
    CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims_data) AS DECIMAL(5,2)) AS percentage
FROM claims_data
GROUP BY Status
ORDER BY percentage DESC;

--Average quantity of food claimed per receiver
SELECT
    r.Receiver_ID,
    r.Name,
    AVG(TRY_CAST(fl.Quantity AS DECIMAL(18,2))) AS avg_claimed_quantity
FROM claims_data c
JOIN receivers_data r
    ON c.Receiver_ID = r.Receiver_ID
JOIN food_listings_data fl
    ON c.Food_ID = fl.Food_ID
WHERE LOWER(c.Status) = 'completed'
GROUP BY r.Receiver_ID, r.Name
ORDER BY avg_claimed_quantity DESC;

--Which meal type is claimed the most?
SELECT
    fl.Meal_Type,
    COUNT(*) AS claims_count
FROM claims_data c
JOIN food_listings_data fl
    ON c.Food_ID = fl.Food_ID
WHERE LOWER(c.Status) = 'completed'
GROUP BY fl.Meal_Type
ORDER BY claims_count DESC;

--Total quantity of food donated by each provider
SELECT
    p.Provider_ID,
    p.Name,
    SUM(TRY_CAST(fl.Quantity AS DECIMAL(18,2))) AS total_donated_quantity
FROM food_listings_data fl
JOIN providers_data p
    ON fl.Provider_ID = p.Provider_ID
GROUP BY p.Provider_ID, p.Name
ORDER BY total_donated_quantity DESC;