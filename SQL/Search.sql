declare @response nvarchar(max);
declare @payload nvarchar(max) = json_object('input': 'The future of Generative AI is here.');

exec sp_invoke_external_rest_endpoint
    @url = 'https://<YOUR APP>.openai.azure.com/openai/deployments/embeddings/embeddings?api-version=2023-03-15-preview',
    @credential = [https://<YOUR APP>.openai.azure.com],
    @payload = @payload,
    @response = @response output;

select r.published, r.category, r.author, r.title, r.content, r.cosine_distance
from dbo.SimilarNewsContentArticles(json_query(@response, '$.result.data[0].embedding')) as r
order by cosine_distance desc