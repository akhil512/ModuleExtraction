from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

class WebScraper:
    def __init__(self, base_url):
        self.url = [base_url]

    async def page_loader(self):
        self.loader = AsyncChromiumLoader(self.url, user_agent="MyAppUserAgent")
        self.doc = await self.loader.aload()
        return self.doc

    async def doc_transformer(self):
        unwanted_tags = ["header", "footer", "nav", "script", "style"]
        tags_to_extract = ["p", "li", "div", "a"]
        unwanted_classnames = ["navbar", "sidebar", "footer", "header"]
        self.soup_transformer = BeautifulSoupTransformer()
        self.docs_transformed = self.soup_transformer.transform_documents(
            self.doc,
            unwanted_tags=unwanted_tags,
            tags_to_extract=tags_to_extract,
            remove_lines=True,
            unwanted_classnames=unwanted_classnames,
            remove_comments=True
        )
        return self.docs_transformed

    async def get_text(self):
        self.doc = await self.page_loader()
        await self.doc_transformer()
        return self.docs_transformed[0].page_content if self.docs_transformed else ""