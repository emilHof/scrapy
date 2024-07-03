from db import Connection
BRANDS = sorted(["Milwaukee", "Makita", "Metabo", "Dewalt", "Bosch", "Ryobi"])
NEWLINE = "\n"
def number_list(l: [str]):
    return '\n'.join([f"{i}. {e}" for i, e in enumerate(l)])

class CLI:
    def __init__(self, args) -> None:
        self.args = args
        self.con = Connection("data.db")

    def scrape(self):
        mode = input("Please select from the following options:\n\n0. Brand\n1. Tool\n\n")
        if mode == "0":
            self.__scrape_brand()
        elif mode == "1":
            pass
        else:
            print(f"{mode} is not a valid mode!")
            quit(1)
        pass

    def __scrape_brand(self):
        brands = self.con.get_brands()
        brand = input(f"\nPlease select from the following brands:\n\n{number_list(brands)}\n\n")
        if int(brand) > len(brands):
            print(f"Brand {brand} is invalid")
            quit(1)
        pass

    def _list(self):
        if self.args.mode == "tools" and not self.args.brand:
            print("Pleas specify a brand when listing tools")
            quit(1)
        
        if self.args.mode == "tools":
            tools = self.con.get_brand_tools(self.args.brand)

            for (name, model) in tools:
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
