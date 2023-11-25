-- This Azure SQL function finds news articles similar to the given content vector.
CREATE function [dbo].[SimilarNewsContentArticles](
    @vector nvarchar(max) -- Input parameter: JSON string representing a content vector.
)
returns table -- The function returns a table.
as
return with 

-- CTE for processing the input vector.
cteVector as
(
    select 
        cast([key] as int) as [vector_value_id], -- Extracts and casts the 'key' from JSON to int.
        cast([value] as float) as [vector_value] -- Extracts and casts the 'value' from JSON to float.
    from 
        openjson(@vector) -- Parses the input JSON vector.
),

-- CTE for calculating similarity scores with existing articles.
cteSimilar as
(
    select top (50)
        v2.article_id, 
        sum(v1.[vector_value] * v2.[vector_value]) as cosine_distance 
        -- Calculates cosine similarity (distance) between vectors.
    from 
        cteVector v1 -- Uses the processed input vector.
    inner join 
        dbo.news_contents_vector v2 
        on v1.vector_value_id = v2.vector_value_id -- Joins with stored article vectors.
    group by
        v2.article_id
    order by
        cosine_distance desc -- Orders by similarity score, descending.
)

-- Final selection combining article data with similarity scores.
select 
    a.*, -- Selects all columns from the news article.
    r.cosine_distance -- Includes the calculated similarity score.
from 
    cteSimilar r -- Uses the similarity scores CTE.
inner join 
    dbo.news a on r.article_id = a.article_id -- Joins with the news articles table.
GO