USE SmartLightsDW;

DECLARE @date DATETIME = '2026-05-02 00:00:00'
DECLARE @end  DATETIME = '2026-05-31 23:00:00'
DECLARE @id   INT = 769

WHILE @date <= @end
BEGIN
    INSERT INTO Dim_Date VALUES (
        @id,
        @date,
        DATEPART(HOUR, @date),
        DATEPART(DAY, @date),
        DATEPART(MONTH, @date),
        DATEPART(YEAR, @date),
        DATENAME(WEEKDAY, @date),
        CASE WHEN DATEPART(WEEKDAY, @date) IN (1,7) THEN 1 ELSE 0 END,
        CASE 
            WHEN DATEPART(HOUR,@date) BETWEEN 6  AND 11 THEN 'Morning'
            WHEN DATEPART(HOUR,@date) BETWEEN 12 AND 16 THEN 'Afternoon'
            WHEN DATEPART(HOUR,@date) BETWEEN 17 AND 20 THEN 'Evening'
            ELSE 'Night'
        END
    )
    SET @id   = @id + 1
    SET @date = DATEADD(HOUR, 1, @date)
END



USE SmartLightsDW;

DECLARE @date DATETIME = '2026-06-01 00:00:00'
DECLARE @end  DATETIME = '2026-06-30 23:00:00'
DECLARE @id   INT = 1489

WHILE @date <= @end
BEGIN
    INSERT INTO Dim_Date VALUES (
        @id,
        @date,
        DATEPART(HOUR, @date),
        DATEPART(DAY, @date),
        DATEPART(MONTH, @date),
        DATEPART(YEAR, @date),
        DATENAME(WEEKDAY, @date),
        CASE WHEN DATEPART(WEEKDAY, @date) IN (1,7) THEN 1 ELSE 0 END,
        CASE 
            WHEN DATEPART(HOUR,@date) BETWEEN 6  AND 11 THEN 'Morning'
            WHEN DATEPART(HOUR,@date) BETWEEN 12 AND 16 THEN 'Afternoon'
            WHEN DATEPART(HOUR,@date) BETWEEN 17 AND 20 THEN 'Evening'
            ELSE 'Night'
        END
    )
    SET @id   = @id + 1
    SET @date = DATEADD(HOUR, 1, @date)
END