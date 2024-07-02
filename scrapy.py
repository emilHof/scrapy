import httpx
import asyncio
from typing import TypedDict, List, Literal
from sites import ebay

session = httpx.AsyncClient(
    # for our HTTP headers we want to use a real browser's default headers to prevent being blocked
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    },
    # Enable HTTP2 version of the protocol to prevent being blocked
    http2=True,
    # enable automatic follow of redirects
    follow_redirects=True
)

class ProductPreview(TypedDict):
    url: str  # url to full product page
    title: str
    price: str
    condition: str
    # shipping: str
    # list_date: str
    # subtitles: List[str]
    # photo: str  # image url
    # rating: str
    # rating_count: str

def _print(p: ProductPreview) -> str:
    return f'''=================================
title: {p['title']}
price: {p['price']}
condition: {p['condition']}
url: {p['url']}
'''

class PreviewConverter:
    def from_ebay(product: ebay.ProductPreviewResult) -> ProductPreview:
        return {
            "url": product["url"],
            "title": product["title"],
            "price": product["price"],
            "condition": product["condition"]
        }


# Example run:
if __name__ == "__main__":
    import asyncio
    from arg_parser import parse_args
    from cli import CLI
    from db import Connection

    # ebay_results = asyncio.run(ebay.scrape(args.query, session, brands=args.brands, conditions=args.conditions))
    # for res in ebay_results:
    #     print(_print(PreviewConverter.from_ebay(res)))

    # con = Connection("data.db")
    # print(con.list_tables())
    args = parse_args()
    args.func(CLI(args))