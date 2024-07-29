# Piotr Rywczak

from loading_files import load_etho_file, load_excel_file
from config import ethovision_file_paths_dict, manual_laberer_file_paths_dict, output_file_paths_dict
import pandas as pd
from merging_files import merge_singular_experiment
from summarising_beh import summarise_experiment
from config import OF_headers


def merge_files(experiments_list):
    for experiment in experiments_list:
        merge_singular_experiment(experiment)
        print(f"Done {experiment}")


def summarise_trials(experiments_list):
    for experiment in experiments_list:
        summarise_experiment(experiment)
        print(f"Done {experiment}")


if __name__ == '__main__':

    print(OF_headers)

    for dict_a in [ethovision_file_paths_dict, manual_laberer_file_paths_dict, output_file_paths_dict]:
        print(dict_a)

    trials_list = ["TCHT"]

    # merge_files(trials_list)
    summarise_trials(trials_list)
