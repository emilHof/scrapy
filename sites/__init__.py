from typing import TypedDict
import sites.ebay

class ProductPreview(TypedDict):
    url: str  # url to full product page
    title: str
    price: float
    condition: str
    shipping: float
    # shipping: str
    # list_date: str
    # subtitles: List[str]
    # photo: str  # image url
    # rating: str
    # rating_count: str

def make_prettier(p: ProductPreview) -> str:
    return f'''=================================
title: {p['title']}
price: {p['price']:.2f}
condition: {p['condition']}
url: {p['url']}
shipping: {p['shipping']:.2f}
'''

class PreviewConverter:
    def from_ebay(product: ebay.ProductPreviewResult) -> ProductPreview:
        if product["price"] == "" or product["shipping"] == "": return None
        _shipping = product["shipping"].split(" ")[0]
        return {
            "url": product["url"],
            "title": product["title"],
            "price": float(product["price"][1:]),
            "condition": product["condition"],
            "shipping": float(_shipping[2:]) if _shipping[0] == '+' else 0.0
        }
