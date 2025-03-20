from financial_dataset_preprocessor import get_preprocessed_menu8186_snapshot, get_fund_codes_main, filter_df_by_fund_codes_main
from .general_utils import get_mapping_fund_names_filtered_by_fund_codes
from .consts import MANAGERS_OF_DIVISION_01, MANAGERS_OF_DIVISION_02

def get_fund_codes_by_managers(managers, date_ref=None, option_main=True):
    df = get_preprocessed_menu8186_snapshot(date_ref=date_ref)
    managers_pattern = '|'.join(managers)    
    df = df[df['운용역'].str.contains(managers_pattern, na=False)]
    if option_main:
        df = filter_df_by_fund_codes_main(df)
    fund_codes = list(df.index)
    return fund_codes

def get_fund_codes_of_division_01(date_ref=None, option_main=True):
    return get_fund_codes_by_managers(managers=MANAGERS_OF_DIVISION_01, date_ref=date_ref, option_main=option_main)

def get_fund_codes_of_division_02(date_ref=None, option_main=True):
    return get_fund_codes_by_managers(managers=MANAGERS_OF_DIVISION_02, date_ref=date_ref, option_main=option_main)

def get_mapping_fund_names_of_division_01(date_ref=None, option_main=True):
    fund_codes = get_fund_codes_of_division_01(date_ref=None, option_main=option_main)
    mapping = get_mapping_fund_names_filtered_by_fund_codes(fund_codes=fund_codes, date_ref=date_ref)
    return mapping

def get_mapping_fund_names_of_division_02(date_ref=None, option_main=True):
    fund_codes = get_fund_codes_of_division_02(date_ref=None, option_main=option_main)
    mapping = get_mapping_fund_names_filtered_by_fund_codes(fund_codes=fund_codes, date_ref=date_ref)
    return mapping
