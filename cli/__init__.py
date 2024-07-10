from db import Connection
from typing import List, Tuple
import asyncio
import httpx
from sites.ebay import scrape
from sites import make_prettier, PreviewConverter, ProductPreview

NEWLINE = "\n"
def charify(i):
    o = ""
    while i > 25:
        o += "z"
        i -= 26
    return o + chr(ord('a') + i)
def optionize_list(l: List[str]):
    return [(charify(i), e) for i, e in enumerate(l)]

def join_list(l: List[Tuple[str, str]]):
    return "\n".join(f"({i}) {e}" for (i, e) in l)

def make_session():
    return httpx.AsyncClient(
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

class CLI:
    def __init__(self, args) -> None:
        self.args = args
        self.con = Connection("data.db")
        self.session = None

    def scrape(self):
        self.session = make_session()
        mode = input(f"Please select from the following options:\n\n{join_list(optionize_list(['Brand', 'Category']))}\n\n")
        if mode == "a" or mode == "Brand":
            self.__scrape_brand()
        elif mode == "b" or mode == "Category":
            pass
        else:
            print(f"{mode} is not a valid mode!")
            quit(1)
        pass

    def __scrape_brand(self):
        optioned_brands = optionize_list(self.con.get_brands())
        choice = input(f"\nPlease select from the following brands:\n\n{join_list(optioned_brands)}\n\n")
        if not (any(choice == option for (option, _) in optioned_brands)
            or any(choice == brand for (_, brand) in optioned_brands)):
            print("Invalid brand choice")
            quit(1)
        (_, brand) = list(filter(lambda e: e[0] == choice or e[1] == choice, optioned_brands))[0]

        tools = self.con.get_brand_tools(brand)
        optioned_tools = optionize_list([(n, m) for (n, m, _) in tools])
        pretty_optioned_tools = [(o, f"{n} - {m}") for (o, (n, m)) in optioned_tools]
        choice = input(f"\n Please chose grom the following tools:\n\n{join_list(pretty_optioned_tools)}\n\n")
        if not any(choice == o or choice == n or choice == m for (o, (n, m)) in optioned_tools):
            print("Invalid tool choice")
            quit(1)
        (_, (name, model)) = list(filter(lambda e: choice in [e[0], e[1][0], e[1][1]], optioned_tools))[0]
        # print(name, model)

        products = asyncio.run(scrape(
            query=f"{model}", 
            session=self.session, 
            brands=[brand],
            conditions=self.args.condition
        ))
        print(products)
        converted = filter(lambda x: x is not None, [PreviewConverter.from_ebay(product) for product in products])
        for c in converted:
            print(make_prettier(c))
        pass

    def _list(self):
        if self.args.mode == "tools" and not self.args.brand:
            print("Pleas specify a brand when listing tools")
            quit(1)
        
        if self.args.mode == "tools":
            tools = self.con.get_brand_tools(self.args.brand)

            for (name, model, _) in tools:
                print("----------------------------------------------------------------------------------------------------------------")
                print(f"Name: {name}")
                print(f"Model: {model}")
        else:
            brands = self.con.get_brands()
            for brand in brands:
                print(brand)

    def add(self):
        self.con.add_tool(self.args.brand, self.args.name, self.args.model)
        pass
