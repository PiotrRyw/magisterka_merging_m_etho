#Piotr Rywczak
# eksportowanie do plików dla GraphPad 8
import pandas as pd
from loading_files import load_excel_file
from os import listdir
from os.path import join
from config import open_field_group_con, open_field_group_exp, graph_pad_dict


# open Excel file for each rat
# save each behavior in a separate dataframe
# record data from each rat into separate rows in dataframe
# control and exp animals in separate columns
# save all the resulting dataframes


def rat_experiment_value(file_path: str, column_name: str):
    dataframe = load_excel_file(file_path)

    return dataframe.at[1, column_name]


def export_graphpad_excel(file_path: str, dataframe: pd.DataFrame):
    dataframe.to_excel(file_path)


def fetch_input_filepaths(directory_path: str):
    filepaths_dir = {}
    files = listdir(directory_path)
    for file in files:
        filepaths_dir[file] = join(directory_path, file)

    return filepaths_dir


def generate_output_directory_and_paths(directory: str, dataframe):
    filepaths_dir = {}

    for category in list(dataframe.columns)[1:-1]:
        file_name = category + ".xlsx"
        filepaths_dir[category] = join(directory, file_name)

    return filepaths_dir


def creating_graphpad_files(experiment_summary: str):

    of_dir_path = graph_pad_dict[experiment_summary]["input"]
    output_of_dir_path = graph_pad_dict[experiment_summary]["output"]

    input_files_dir = fetch_input_filepaths(of_dir_path)
    print(input_files_dir)

    df = load_excel_file(input_files_dir[list(input_files_dir.keys())[0]])

    graphpad_file_paths = generate_output_directory_and_paths(output_of_dir_path, dataframe=df)
    print(graphpad_file_paths)

    rats = input_files_dir.keys()

    experiments = graphpad_file_paths.keys()

    con = open_field_group_con

    exp = open_field_group_exp

    for experiment in experiments:

        df = pd.DataFrame()

        con_index = 0
        exp_index = 0
        for rat in rats:
            rat_name = rat[:-5]
            if rat_name in con:
                df.at[con_index, "con"] = rat_experiment_value(input_files_dir[rat], experiment)
                con_index += 1
            elif rat_name in exp:
                df.at[exp_index, "exp"] = rat_experiment_value(input_files_dir[rat], experiment)
                exp_index += 1
        print(df)
        export_graphpad_excel(graphpad_file_paths[experiment], df)
        print(f"Exported to {graphpad_file_paths[experiment]}")

    print("Done")
