# Piotr Rywczak

from loading_files import load_etho_file, load_excel_file, export_file_into_excel
from config import ethovision_file_paths_dict, manual_laberer_file_paths_dict, output_file_paths_dict
import pandas as pd


def load_ethovision_file_to_dataframe(file_path: str, experiment):
    print(f"loading {file_path}")
    etho_frame = load_etho_file(file_path, experiment)
    return etho_frame


def load_manual_laberer_file_to_dataframe(file_path: str):
    print(f"loading {file_path}")
    manual_frame = load_excel_file(file_path)
    return manual_frame


def merge_two_files(etho_file_path, manual_file_path, experiment):
    etho_frame = load_ethovision_file_to_dataframe(etho_file_path, experiment)
    manual_frame = load_manual_laberer_file_to_dataframe(manual_file_path)

    print(f"merging frames {etho_file_path} {manual_file_path}")
    merged_frame = pd.merge(etho_frame, manual_frame, left_on="index", right_on="Frame No.", how="inner")

    return merged_frame


def merge_singular_experiment(experiment_name: str):
    print(f"doing {experiment_name}")

    if experiment_name == "OF_time_buckets":  # no separate merged files for OF with buckets
        experiment_name = "OF"

    etho_files_paths_dict = ethovision_file_paths_dict[experiment_name]
    manual_files_paths_dict = manual_laberer_file_paths_dict[experiment_name]
    output_files_paths_dict = output_file_paths_dict[experiment_name]

    rat_ids = output_files_paths_dict.keys()

    for rat_id in rat_ids:
        merged_frame = merge_two_files(etho_files_paths_dict[rat_id], manual_files_paths_dict[rat_id], experiment_name)
        export_file_into_excel(merged_frame, output_files_paths_dict[rat_id])
        print(f"Done rat id {rat_id} in {experiment_name}")
