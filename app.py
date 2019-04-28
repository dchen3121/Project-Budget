from models.item import Item

url = "https://www.johnlewis.com/oscar-jacobson-textured-wool-regular-fit-blazer-dark-blue/p4115058"
tag_name = "p"
query = {"class": "price price--large"}

blazer = Item(url, tag_name, query)



print(blazer.load_price())

