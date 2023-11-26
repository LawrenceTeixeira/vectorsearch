/*
    Create database credentials to store API key
*/
if exists(select * from sys.[database_scoped_credentials] where name = 'https://<YOUR APP>.openai.azure.com')
begin
	drop database scoped credential [https://<YOUR APP>.openai.azure.com];
end
create database scoped credential [https://<YOUR APP>.openai.azure.com]
with identity = 'HTTPEndpointHeaders', secret = '{"api-key": "YOUR API AZURE OPEN AI API KEY"}';
go