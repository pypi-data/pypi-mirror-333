
from .base import validate_dataframe_columns

import pandas as pd
import typing as t

from ..pandas_columns import *


#################################### checkers ####################################################
def check_company_inputs(name: str, dataset_type: str, description: str, min_date: pd.Timestamp, max_date: pd.Timestamp) -> None:

    if not isinstance(name, str):
        raise ValueError("Company name must be a string.")
    if not isinstance(dataset_type, str):
        raise ValueError("Dataset type must be a string.")
    if not isinstance(description, str):
        raise ValueError("Description must be a string.")
    if not isinstance(min_date, pd.Timestamp):
        raise ValueError("Min date must be a pandas Timestamp.")
    if not isinstance(max_date, pd.Timestamp):
        raise ValueError("Max date must be a pandas Timestamp.")
    
def clean_and_check_store_region_map(store_region_map: pd.DataFrame, copy: bool = False) -> pd.DataFrame:

    if copy:
        store_region_map = store_region_map.copy()

    expected_base_columns = [
        StoresColumns.STORE.value,
        StoresColumns.COUNTRY.value,
    ]

    num_columns = len(store_region_map.columns)
    if num_columns == 2:
        expected_types = StoresColumns._TYPES.value[:2]
        store_region_map = validate_dataframe_columns(store_region_map, expected_base_columns, expected_types, "Store Region Map")

    elif num_columns == 3:
        for column in store_region_map.columns:
            if column in ["store", "country"]:
                continue
            else:
                region_type = column
                break
                # check that the region type is supported
        if region_type not in StoresColumns.ADDITIONAL_COLUMNS.value:
            raise ValueError(f"Region type {region_type} is not supported. Supported types are: {StoresColumns.ADDITIONAL_COLUMNS.values}")
        expected_columns = expected_base_columns + [region_type]
        expected_types = StoresColumns._TYPES.value[:3]
        store_region_map = validate_dataframe_columns(store_region_map, expected_columns, expected_types, "Store Region Map")
    
    else:
        raise ValueError(f"Expected 2 or 3 columns for store-region map, found {num_columns} columns: {store_region_map.columns}")

    return store_region_map



def clean_and_check_categories_level_description(categories_level_description: pd.DataFrame, copy: bool = False) -> pd.DataFrame:
    if copy:
        categories_level_description = categories_level_description.copy()
    
    expected_columns = [col.value for col in list(CategoriesLevelColumns)[:-1]]
    expected_types = CategoriesLevelColumns._TYPES.value
    categories_level_description = validate_dataframe_columns(categories_level_description, expected_columns, expected_types, "Category level descriptions")

    # convert level to int
    categories_level_description[CategoriesLevelColumns.LEVEL.value] = categories_level_description[CategoriesLevelColumns.LEVEL.value].astype(int)
    
    return categories_level_description


def clean_and_check_categories_dict(categories_dict: t.Dict, copy=False) -> t.Dict:

    if copy:
        categories_dict = categories_dict.copy()

    categories_dict = {int(key): value for key, value in categories_dict.items()}

    # Check if the keys are a range from 0 to n-1 without gaps
    if set(categories_dict.keys()) != set(range(0, len(categories_dict))):
        keys = sorted(categories_dict.keys())
        raise ValueError("The keys of the categories dictionary must be a range from 0 to n-1 without gaps, got: {}".format(keys))

    return categories_dict

def clean_and_check_products(products: pd.DataFrame, copy: bool = False) -> pd.DataFrame:

    if copy:
        products = products.copy()

    expected_columns = [col.value for col in list(ProductsColumns)[:-1]]
    expected_types = ProductsColumns._TYPES.value
    products = validate_dataframe_columns(products, expected_columns, expected_types, "Products")

    return products

def clean_and_check_not_for_sales_flag(not_for_sales_flag: pd.DataFrame, copy: bool = False) -> pd.DataFrame:

    if copy:
        not_for_sales_flag = not_for_sales_flag.copy()

    expected_columns = [col.value for col in list(NotForSalesColumns)[:-1]]
    expected_types = NotForSalesColumns._TYPES.value
    not_for_sales_flag = validate_dataframe_columns(not_for_sales_flag, expected_columns, expected_types, "Not For Sales Flag")

    return not_for_sales_flag

def clean_and_check_not_available_flag(not_available_flag: pd.DataFrame, copy: bool = False) -> pd.DataFrame:
    
    if copy:
        not_available_flag = not_available_flag.copy()

    expected_columns = [col.value for col in list(NotAvailableColumns)[:-1]]
    expected_types = NotAvailableColumns._TYPES.value
    not_available_flag = validate_dataframe_columns(not_available_flag, expected_columns, expected_types, "Not Available Flag")

    return not_available_flag

def clean_and_check_time_sku_data(time_sku_data: pd.DataFrame, copy: bool = False) -> pd.DataFrame:

    if copy:
        time_sku_data = time_sku_data.copy()

    expected_columns = [col.value for col in list(TimeSkuColumns)[:-1]]
    expected_types = TimeSkuColumns._TYPES.value
    time_sku_data = validate_dataframe_columns(time_sku_data, expected_columns, expected_types, "Time SKU Data", allow_additional=True)

    return time_sku_data

def clean_and_check_store_feature_description_map(store_feature_description_map: pd.DataFrame, copy: bool = False) -> pd.DataFrame:

    if copy:
        store_feature_description_map = store_feature_description_map.copy()
    
    expected_columns = [col.value for col in list(StoreFeatureDescriptionColumns)[:-1]]
    expected_types = StoreFeatureDescriptionColumns._TYPES.value

    store_feature_description_map = validate_dataframe_columns(store_feature_description_map, expected_columns, expected_types, "Store Feature Description Map")
    
    return store_feature_description_map

def clean_and_check_store_feature_data(store_feature_data: pd.DataFrame, copy: bool = False) -> pd.DataFrame:
    
    if copy:
        store_feature_data = store_feature_data.copy()

    expected_columns = [col.value for col in list(StoreFeatureColumns)[:-1]]
    expected_types = StoreFeatureColumns._TYPES.value

    store_feature_data = validate_dataframe_columns(store_feature_data, expected_columns, expected_types, "Store Feature Data")

    return store_feature_data

def clean_and_check_product_feature_description_map(product_feature_description_map: pd.DataFrame, copy: bool = False) -> pd.DataFrame:

    if copy:
        product_feature_description_map = product_feature_description_map.copy()
    
    expected_columns = [col.value for col in list(ProductFeatureDescriptionColumns)[:-1]]
    expected_types = ProductFeatureDescriptionColumns._TYPES.value

    product_feature_description_map = validate_dataframe_columns(product_feature_description_map, expected_columns, expected_types, "Product Feature Description Map")
    
    return product_feature_description_map

def clean_and_check_product_feature_data(product_feature_data: pd.DataFrame, copy: bool = False) -> pd.DataFrame:

    if copy:
        product_feature_data = product_feature_data.copy()

    expected_columns = [col.value for col in list(ProductFeatureColumns)[:-1]]
    expected_types = ProductFeatureColumns._TYPES.value

    product_feature_data = validate_dataframe_columns(product_feature_data, expected_columns, expected_types, "Product Feature Data")

    return product_feature_data

def clean_and_check_time_product_feature_description_map(time_product_feature_description_map: pd.DataFrame, copy: bool = False) -> pd.DataFrame:

    if copy:
        time_product_feature_description_map = time_product_feature_description_map.copy()
    
    expected_columns = [col.value for col in list(TimeProductFeatureDescriptionColumns)[:-1]]
    expected_types = TimeProductFeatureDescriptionColumns._TYPES.value

    time_product_feature_description_map = validate_dataframe_columns(time_product_feature_description_map, expected_columns, expected_types, "Time Product Feature Description Map")
    
    return time_product_feature_description_map

def clean_and_check_time_product_feature_data(time_product_feature_data: pd.DataFrame, copy: bool = False) -> pd.DataFrame:
        
    if copy:
        time_product_feature_data = time_product_feature_data.copy()

    expected_columns = [col.value for col in list(TimeProductFeatureColumns)[:-1]]
    expected_types = TimeProductFeatureColumns._TYPES.value

    time_product_feature_data = validate_dataframe_columns(time_product_feature_data, expected_columns, expected_types, "Time Product Feature Data")

    return time_product_feature_data

def clean_and_check_time_region_feature_description_map(time_region_feature_description_map: pd.DataFrame, copy: bool = False) -> pd.DataFrame:

    if copy:
        time_region_feature_description_map = time_region_feature_description_map.copy()
    
    expected_columns = [col.value for col in list(TimeRegionFeatureDescriptionColumns)[:-1]]
    expected_types = TimeRegionFeatureDescriptionColumns._TYPES.value

    time_region_feature_description_map = validate_dataframe_columns(time_region_feature_description_map, expected_columns, expected_types, "Time Region Feature Description Map")
    
    return time_region_feature_description_map

def clean_and_check_time_region_feature_data(time_region_feature_data: pd.DataFrame, copy: bool = False) -> pd.DataFrame:

    if copy:
        time_region_feature_data = time_region_feature_data.copy()
    
    expected_base_columns = [
        TimeRegionFeatureColumns.DATE.value,
        TimeRegionFeatureColumns.COUNTRY.value,
        TimeRegionFeatureColumns.FEATURE.value,
        TimeRegionFeatureColumns.VALUE.value
    ]

    num_columns = len(time_region_feature_data.columns)
    if num_columns == 4:
        expected_types = TimeRegionFeatureColumns._TYPES.value[:4]
        time_region_feature_data = validate_dataframe_columns(time_region_feature_data, expected_base_columns, expected_types, "Time Region Feature Data")
    elif num_columns == 5:
        for column in time_region_feature_data.columns:
            if column in ["date", "country", "feature", "value"]:
                continue
            else:
                region_type = column
                break
                # check that the region type is supported
        if region_type not in TimeRegionFeatureColumns.ADDITIONAL_COLUMNS.value:
            raise ValueError(f"Region type {region_type} is not supported. Supported types are: {TimeRegionFeatureColumns.ADDITIONAL_COLUMNS}")
        expected_columns = expected_base_columns + [region_type]
        expected_types = TimeRegionFeatureColumns._TYPES.value[:5]
        time_region_feature_data = validate_dataframe_columns(time_region_feature_data, expected_columns, expected_types, "Time Region Feature Data", allow_additional=True)

    else:
        raise ValueError(f"Expected 4 or 5 columns for time region feature data, found {num_columns} columns: {time_region_feature_data.columns}")

    return time_region_feature_data

def clean_and_check_time_store_feature_description_map(time_store_feature_description_map: pd.DataFrame, copy: bool = False) -> pd.DataFrame:

    if copy:
        time_store_feature_description_map = time_store_feature_description_map.copy()
    
    expected_columns = [col.value for col in list(TimeStoreFeatureDescriptionColumns)[:-1]]
    expected_types = TimeStoreFeatureDescriptionColumns._TYPES.value

    time_store_feature_description_map = validate_dataframe_columns(time_store_feature_description_map, expected_columns, expected_types, "Time Store Feature Description Map")
    
    return time_store_feature_description_map

def clean_and_check_time_store_feature_data(time_store_feature_data: pd.DataFrame, copy: bool = False) -> pd.DataFrame:

    if copy:
        time_store_feature_data = time_store_feature_data.copy()

    expected_columns = [col.value for col in list(TimeStoreFeatureColumns)[:-1]]
    expected_types = TimeStoreFeatureColumns._TYPES.value

    time_store_feature_data = validate_dataframe_columns(time_store_feature_data, expected_columns, expected_types, "Time Store Feature Data")

    return time_store_feature_data