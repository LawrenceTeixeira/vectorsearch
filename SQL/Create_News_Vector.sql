-- =============================================
-- Author:      Lawrence Teixeira
-- Create Date: 11-24-2023
-- Description: This stored procedure creates vectors for news titles and contents.
-- It processes data from the 'news' table and stores the vectors in separate tables.
-- =============================================

CREATE PROCEDURE [dbo].[Create_News_Vector]
AS
BEGIN
    SET NOCOUNT ON; -- Prevents the sending of DONE_IN_PROC messages to the client.

    -- Extract and store title vectors:
    -- First, check if the 'news_titles_vector' table exists and drop it if it does.
    IF OBJECT_ID('dbo.news_titles_vector', 'U') IS NOT NULL
        DROP TABLE dbo.news_titles_vector;

    -- Using a Common Table Expression (CTE) to process title vectors.
    WITH cte AS
    (
        SELECT 
            v.article_id,    
            CAST(tv.[key] AS INT) AS vector_value_id, -- Casting 'key' as INT for vector ID.
            CAST(tv.[value] AS FLOAT) AS vector_value   -- Casting 'value' as FLOAT for vector value.
        FROM 
            dbo.news AS v 
        CROSS APPLY 
            OPENJSON(v.title_vector) tv -- Parses JSON of title_vector in the 'news' table.
    )
    -- Create 'news_titles_vector' table with processed vectors.
    SELECT
        article_id,
        vector_value_id,
        vector_value
    INTO
        dbo.news_titles_vector
    FROM
        cte;

    -- Extract and store content vectors:
    -- Check and drop 'news_contents_vector' table if it exists.
    IF OBJECT_ID('dbo.news_contents_vector', 'U') IS NOT NULL
        DROP TABLE dbo.news_contents_vector;

    -- CTE for processing content vectors.
    WITH cte AS
    (
        SELECT 
            v.article_id,    
            CAST(tv.[key] AS INT) AS vector_value_id, -- Casting 'key' as INT for vector ID.
            CAST(tv.[value] AS FLOAT) AS vector_value   -- Casting 'value' as FLOAT for vector value.
        FROM 
            dbo.news AS v 
        CROSS APPLY 
            OPENJSON(v.content_vector) tv -- Parses JSON of content_vector in the 'news' table.
    )
    -- Create 'news_contents_vector' table with processed vectors.
    SELECT
        article_id,
        vector_value_id,
        vector_value
    INTO
        dbo.news_contents_vector
    FROM
        cte;

    -- Columnstore indexes creation is advised outside the stored procedure.
    -- These indexes optimize data storage and query performance on vector tables.
    CREATE CLUSTERED COLUMNSTORE INDEX cci_news_titles_vector
    ON dbo.news_titles_vector 
	order (article_id);

    CREATE CLUSTERED COLUMNSTORE INDEX cci_news_contents_vector
    ON dbo.news_contents_vector
	order (article_id);
END