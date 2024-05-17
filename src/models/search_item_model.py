from src.common.base.item_model import ItemModel


class SearchItemModel(ItemModel):
    key_word: str = ""
    name: str = ""
    phone_number: str = ""
    address: str = ""
    rating: str = ""
    url: str = ""
