/****** Object:  StoredProcedure [dbo].[SearchNews]    Script Date: 11/25/2023 6:25:49 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[SearchNews] 
    @inputText NVARCHAR(MAX)
AS
BEGIN
    -- Declare necessary variables
    DECLARE @response NVARCHAR(MAX);
    DECLARE @payload NVARCHAR(MAX);
    DECLARE @url NVARCHAR(MAX) = 'https://<YOUR APP>.openai.azure.com/openai/deployments/embeddings/embeddings?api-version=2023-03-15-preview';

    -- Construct the payload
    SET @payload = json_object('input': @inputText);

    -- Call the external REST endpoint
    EXEC sp_invoke_external_rest_endpoint
        @url = @url,
        @credential = [https://<YOUR APP>.openai.azure.com],
        @payload = @payload,
        @response = @response OUTPUT;

    -- Query the SimilarNewsContentArticles table using the response
    IF OBJECT_ID('dbo.result', 'U') IS NOT NULL
        DROP TABLE dbo.result;

	SELECT * 
    into result
	FROM dbo.SimilarNewsContentArticles(json_query(@response, '$.result.data[0].embedding')) AS r 
    ORDER BY cosine_distance DESC;
END
