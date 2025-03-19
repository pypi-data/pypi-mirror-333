from enum import Enum
import pandas as pd


class CategoriesLevelColumns(Enum):
    LEVEL = "level"
    NAME = "name"
    _TYPES = [int, object]

class StoresColumns(Enum):
    STORE = "store"
    COUNTRY = "country"
    ADDITIONAL_COLUMNS = ["state", "city"]  # currently only state supported
    _TYPES = [object, object, object]

class ProductsColumns(Enum):
    PRODUCT = "product"
    CATEGORY = "category"
    _TYPES = [object, object]

class TimeSkuColumns(Enum):
    DATE = "date"
    STORE = "store"
    PRODUCT = "product"
    SALES = "sales"
    _TYPES = [pd.Timestamp, object, object, object]

class NotAvailableColumns(Enum):
    DATE = "date"
    STORE = "store"
    PRODUCT = "product"
    _TYPES = [pd.Timestamp, object, object]

class NotForSalesColumns(Enum):
    DATE = "date"
    STORE = "store"
    PRODUCT = "product"
    _TYPES = [pd.Timestamp, object, object]

class StoreFeatureDescriptionColumns(Enum):
    NAME = "name"
    DESCRIPTION = "description"
    _TYPES = [object, object]

class StoreFeatureColumns(Enum):
    STORE = "store"
    FEATURE = "feature"
    VALUE = "value"
    _TYPES = [object, object, object]

class ProductFeatureDescriptionColumns(Enum):
    NAME = "name"
    DESCRIPTION = "description"
    _TYPES = [object, object]

class ProductFeatureColumns(Enum):
    PRODUCT = "product"
    FEATURE = "feature"
    VALUE = "value"
    _TYPES = [object, object, object]

class TimeProductFeatureDescriptionColumns(Enum):
    NAME = "name"
    DESCRIPTION = "description"
    _TYPES = [object, object]

class TimeProductFeatureColumns(Enum):
    DATE = "date"
    PRODUCT = "product"
    FEATURE = "feature"
    VALUE = "value"
    _TYPES = [pd.Timestamp, object, object, object]

class TimeRegionFeatureDescriptionColumns(Enum):
    NAME = "name"
    DESCRIPTION = "description"
    _TYPES = [object, object]

class TimeRegionFeatureColumns(Enum):
    DATE = "date"
    COUNTRY = "country"
    FEATURE = "feature"
    VALUE = "value"
    ADDITIONAL_COLUMNS = ["state", "city"] 
    _TYPES = [pd.Timestamp, object, object, object, object, object]

class TimeStoreFeatureDescriptionColumns(Enum):
    NAME = "name"
    DESCRIPTION = "description"
    _TYPES = [object, object]

class TimeStoreFeatureColumns(Enum):
    DATE = "date"
    STORE = "store"
    FEATURE = "feature"
    VALUE = "value"
    _TYPES = [pd.Timestamp, object, object, object]
