from db import Connection
from typing import List, Tuple

BRANDS = sorted(["Milwaukee", "Makita", "Metabo", "Dewalt", "Bosch", "Ryobi"])
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
    print(l)
    return "\n".join(f"({i}) {e}" for (i, e) in l)

class CLI:
    def __init__(self, args) -> None:
        self.args = args
        self.con = Connection("data.db")

    def scrape(self):
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
        optioned_tools = optionize_list([f"{name} - {model}" for name, model, _ in tools])
        choice = input(f"\n Please chose grom the following tools:\n\n{join_list(optioned_tools)}\n\n")
        print(choice)

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
