# Piotr Rywczak
from benchmarking import MeasuringBenchmark
from experiment_statistics import generate_statistics_results
from loading_files import load_etho_file, load_excel_file
from config import ethovision_file_paths_dict, manual_laberer_file_paths_dict, output_file_paths_dict, \
    merged_experiments_list, summarised_experiments_list, graphpad_export_list
import pandas as pd
from merging_files import merge_singular_experiment
from summarising_beh import summarise_experiment, check_for_dropped_frames
from config import OF_headers
from statistics_export import creating_graphpad_files, list_TCHT_trial_times
import time
import benchmarking


def merge_files(experiments_list):
    for experiment in experiments_list:
        merge_singular_experiment(experiment)
        print(f"Done {experiment}")


def summarise_trials(experiments_list):
    for experiment in experiments_list:
        summarise_experiment(experiment)
        print(f"Done {experiment}")


if __name__ == '__main__':
    trials_list = merged_experiments_list

    start_time = time.time()
    merge_files(trials_list)
    benchmarking.init()

    summarise_trials(trials_list)

    print("--- %s seconds ---" % (time.time() - start_time))

    benchmarking.benchmark.print_out_results()

    experiment_summary = summarised_experiments_list
    for exp in experiment_summary:
        check_for_dropped_frames(exp)

    experiment_summary = graphpad_export_list
    for exp in experiment_summary:
        creating_graphpad_files(exp)

    # for exp in experiment_summary:
    #     list_TCHT_trial_times(exp)

    # generate_statistics_results()
