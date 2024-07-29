import pandas as pd


def load_etho_file(file_path: str, experiment):
    if experiment == "TCHT":
        skip_rows = 38
    else:
        skip_rows = 37
    dataframe = pd.read_excel(file_path, skiprows=[x for x in range(skip_rows)])
    print(dataframe.head())
    curated_dataframe = selecting_columns_from_full_dataframe(dataframe, experiment)

    return curated_dataframe.reset_index()


def selecting_columns_from_full_dataframe(dataframe, experiment: str):
    if experiment == "TCHT":
        curated_dataframe = dataframe[["Trial time",
                                       "In chambers(Center chamber / Center-point)",
                                       "In chambers(Left chamber / Center-point)",
                                       "In chambers(Right chamber / Center-point)"]]
        curated_dataframe = curated_dataframe.rename(columns={"In chambers(Center chamber / Center-point)": "center",
                                                              "In chambers(Left chamber / Center-point)": "left",
                                                              "In chambers(Right chamber / Center-point)": "right"})
        curated_dataframe = curated_dataframe.drop(index=0)
        return curated_dataframe
    elif experiment == "OF":
        curated_dataframe = dataframe[["Trial time",
                                       "In Center",
                                       "Out of Center"]]

        curated_dataframe = curated_dataframe.drop(index=0)
        return curated_dataframe


def load_excel_file(file_path: str):
    dataframe = pd.read_excel(file_path)
    return dataframe


def export_file_into_excel(dataframe: pd.DataFrame, output_path):
    print(f"exporting to {output_path}")
    dataframe.to_excel(output_path)
