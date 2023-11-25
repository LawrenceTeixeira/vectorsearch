/****** Object:  Table [dbo].[news]    Script Date: 11/25/2023 6:14:12 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[news](
	[article_id] [int] NOT NULL,
	[source_id] [nvarchar](50) NULL,
	[source_name] [nvarchar](max) NULL,
	[author] [nvarchar](max) NULL,
	[title] [nvarchar](max) NULL,
	[description] [nvarchar](300) NULL,
	[url] [nvarchar](max) NULL,
	[url_to_image] [nvarchar](max) NULL,
	[content] [nvarchar](250) NULL,
	[category] [nvarchar](50) NULL,
	[full_content] [nvarchar](max) NULL,
	[title_vector] [varchar](max) NULL,
	[content_vector] [varchar](max) NULL,
	[published] [datetime] NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO


