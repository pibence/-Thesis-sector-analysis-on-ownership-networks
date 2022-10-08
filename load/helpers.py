import yaml
import os
import pandas as pd
import logging

logging.basicConfig(
    filename="logs/load.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def parse_yaml(config):
    with open(config, "r") as stream:
        try:
            ret_dict = yaml.load(stream, Loader=yaml.Loader)
        except yaml.YAMLError as exc:
            print(exc)
    return ret_dict


def parse_csvs_from_folder(folder_path):
    files = os.listdir(folder_path)

    df_list = []
    for file in files:
        fl = pd.read_csv(f"{folder_path}{file}")
        df_list.append(fl)

    ret_df = pd.concat(df_list)
    ret_df.columns = ret_df.columns.str.lower()
    return ret_df


def parse_financials_from_folder(folder_path):
    """
    Function that parses together the data containing financial info and cleanes it.
    NAs and wrong entries are removed, financial colums are converted to numeric type.
    """

    files = os.listdir(folder_path)

    df_list = []
    for file in files:
        fl = pd.read_csv(f"{folder_path}{file}", sep=";")

        fl[["Total Assets", "Total Liabilities", "Total Equity"]] = fl[
            ["Total Assets", "Total Liabilities", "Total Equity"]
        ].apply(lambda x: x.str.replace(",", ".", regex=False))

        fl[["Total Assets", "Total Liabilities", "Total Equity"]] = fl[
            ["Total Assets", "Total Liabilities", "Total Equity"]
        ].apply(lambda x: x.str.replace(" ", "", regex=False))

        fl[["Total Assets", "Total Liabilities", "Total Equity"]] = fl[
            ["Total Assets", "Total Liabilities", "Total Equity"]
        ].apply(lambda x: pd.to_numeric(x, errors="coerce"))

        fl = fl.dropna()

        fl = fl[
            (fl["Total Equity"] > 0)
            & (fl["Total Assets"] > 0)
            & (fl["Total Liabilities"] > 0)
        ]
        fl.columns = fl.columns.str.replace(" ", "_")
        df_list.append(fl)

    ret_df = pd.concat(df_list)
    ret_df.columns = ret_df.columns.str.lower()
    return ret_df
