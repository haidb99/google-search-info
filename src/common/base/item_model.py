import inspect
import json
import typing
from datetime import datetime, date
from decimal import Decimal


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


class ItemModel:
    def __init__(self, *args, **kwargs):
        pass

    def to_dict(self):
        dict_item = {attr: self._serialize(getattr(self, attr)) for attr in self._get_serializable_attrs()}
        return dict_item

    def _serialize(self, value):
        if isinstance(value, list):
            return [self._serialize(item) for item in value]
        elif isinstance(value, datetime):
            return value.isoformat()
        elif isinstance(value, ItemModel):
            return value.to_dict()
        else:
            return value

    def _get_serializable_attrs(self):
        attrs = [attr for attr in dir(self) if not attr.startswith("__") and not callable(getattr(self, attr))]
        try:
            attrs += [attr for attr in vars(type(self))["__annotations__"].keys() if not attr.startswith("__")]
        except KeyError:
            pass
        return set(attrs)

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except AttributeError:
            return None

    def to_string(self):
        return json.dumps(self.to_dict())

    def __setattr__(self, key, value):
        attr_type = type(self).__annotations__.get(key)
        if attr_type in (str, int, float, bool) and value is not None:
            value = attr_type(value)
        super().__setattr__(key, value)

    def __set_values__(self, json_data):
        keys = self._get_serializable_attrs()
        for key in keys:
            if key not in json_data.keys():
                continue

            if json_data[key] is None:
                continue

            prepare_new_value = self._prepare_value(json_data[key])
            new_value = prepare_new_value
            if (self.__annotations__ is not None) and (key in self.__annotations__):
                _type = self.__annotations__[key]
                origin_type = typing.get_origin(_type)
                if origin_type == list:
                    item_type = typing.get_args(_type)[0]
                    if inspect.isclass(item_type) and issubclass(item_type, ItemModel):
                        new_value = [item_type().__set_values__(p) for p in prepare_new_value]
                elif inspect.isclass(_type) and issubclass(_type, ItemModel):
                    new_value = _type().__set_values__(prepare_new_value)
            setattr(self, key, new_value)
        return self

    @classmethod
    def bigquery_table_schema(cls):
        convert_types = {
            int: 'INTEGER',
            float: 'FLOAT',
            str: 'STRING',
            bool: 'BOOLEAN',
            date: "DATE",
            datetime: "TIMESTAMP",
            Decimal: "NUMERIC"
        }

        schema = []
        for column, _type in cls.__annotations__.items():
            schema.append({
                "name": column,
                "type": convert_types[_type] if _type in convert_types else 'STRING'
            })
        return schema

    def _prepare_value(self, value):
        return value
