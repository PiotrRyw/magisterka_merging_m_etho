# Piotr Rywczak

import pandas as pd
import numpy as np
from config import (OF_headers, TCHT_headers_1st_trial, TCHT_headers_2nd_trial, TCHT_headers_3rd_trial,
                    TCHT_default_headers, ignored_time_in_sec)
from config import ethovision_file_paths_dict, manual_laberer_file_paths_dict, output_file_paths_dict
from config import trials_first_ids, trials_second_ids, trials_third_ids, first_stranger_location
from config import frame_rate, OF_time_bucket
from loading_files import load_excel_file, export_file_into_excel
import benchmarking


def total_time(raw_df, summary_df, headers, trial_time=0, ignore_first_seconds=0):
    print(headers)
    if trial_time == 0:
        trial_time = raw_df["Trial time"].iloc[-1]

    if ignore_first_seconds != 0:
        trial_time = trial_time - ignore_first_seconds
        raw_df = raw_df.loc[raw_df["Trial time"] > ignore_first_seconds]

    for behavior_and_location in headers:
        behavior = behavior_and_location[0]
        location = behavior_and_location[1]
        column_name = behavior + " " + location

        number_of_frames_no_location = raw_df[behavior].count()

        time_in_seconds_no_location = number_of_frames_no_location / frame_rate
        summary_df.at[0, f"{behavior} Total"] = number_of_frames_no_location
        summary_df.at[1, f"{behavior} Total"] = time_in_seconds_no_location
        summary_df.at[2, f"{behavior} Total"] = (time_in_seconds_no_location * 100) / trial_time
        benchmarking.benchmark.prepare_dataframe_timer()
        df_behavior_and_location = raw_df[(raw_df[behavior] == behavior) & (raw_df[location] == 1)]
        benchmarking.benchmark.update_dataframe_timer()

        number_of_frames_per_location = df_behavior_and_location[behavior].count()

        time_in_seconds = number_of_frames_per_location / frame_rate

        summary_df.at[0, column_name] = number_of_frames_per_location
        summary_df.at[1, column_name] = time_in_seconds
        summary_df.at[2, column_name] = (time_in_seconds * 100) / trial_time

    summary_df.at[0, "Total"] = f"{raw_df['Trial time'].count()} frames"
    summary_df.at[1, "Total"] = f"{trial_time} s"
    summary_df.at[2, "Total"] = "100%"


def second_trial_stranger_location(df, rat_id):
    original_headers = df.columns
    new_headers = []

    stranger_rat_location = first_stranger_location[rat_id]
    if stranger_rat_location == "right":
        for column_name in original_headers:
            new_column = column_name.replace("right", "stranger")
            new_column = new_column.replace("left", "object")
            new_headers.append(new_column)
    else:
        for column_name in original_headers:
            new_column = column_name.replace("right", "object")
            new_column = new_column.replace("left", "stranger")
            new_headers.append(new_column)

    replacing_dict = {x: y for x, y in zip(original_headers, new_headers)}

    return df.rename(columns=replacing_dict)


def third_trial_stranger_location(df, rat_id):
    original_headers = df.columns
    new_headers = []

    familiar_rat_location = first_stranger_location[rat_id-1]
    if familiar_rat_location == "right":
        for column_name in original_headers:
            new_column = column_name.replace("right", "familiar")
            new_column = new_column.replace("left", "stranger")
            new_headers.append(new_column)
    else:
        for column_name in original_headers:
            new_column = column_name.replace("right", "stranger")
            new_column = new_column.replace("left", "familiar")
            new_headers.append(new_column)

    replacing_dict = {x: y for x, y in zip(original_headers, new_headers)}

    return df.rename(columns=replacing_dict)

# def third_trial_stranger_location(df, rat_id):
#     familiar_location = first_stranger_location[rat_id-1]
#     if familiar_location == "right":
#         stranger_location = "left"
#     else:
#         stranger_location = "right"
#
#     new_df = pd.DataFrame()
#
#     for behavior_and_location in TCHT_headers_3rd_trial:
#         behavior = behavior_and_location[0]
#         location = behavior_and_location[1]
#         column_name = behavior + " " + location
#
#         if location == "stranger":
#             location = stranger_location
#         else:
#             location = familiar_location
#
#         new_df.at[0, column_name] = df.at[0, f"{behavior} {location}"]
#         new_df.at[1, column_name] = df.at[1, f"{behavior} {location}"]
#         new_df.at[2, column_name] = df.at[2, f"{behavior} {location}"]
#
#     return new_df


def generate_summary_for_trial(trial_file_path: str, rat_id, headers):
    benchmarking.benchmark.prepare_loading_timer()
    raw_dataframe = load_excel_file(trial_file_path)
    benchmarking.benchmark.update_loading_timer()
    header_columns = [f"{names[0]} {names[1]}" for names in headers]
    print(header_columns)

    summary_dataframe = pd.DataFrame()
    total_time(raw_dataframe, summary_dataframe, TCHT_default_headers, 0, ignored_time_in_sec)

    if rat_id in trials_second_ids:
        summary_dataframe = second_trial_stranger_location(summary_dataframe, rat_id)

    if rat_id in trials_third_ids:
        summary_dataframe = third_trial_stranger_location(summary_dataframe, rat_id)

    return summary_dataframe


def summarise_TCHT(experiment_name: str):
    input_files_paths_dict = output_file_paths_dict[experiment_name]
    output_files_paths_dict = output_file_paths_dict[experiment_name + "_summary"]

    rat_ids = output_files_paths_dict.keys()

    for rat_id in rat_ids:
        print(f"input: {input_files_paths_dict[rat_id]}")

        dataframe = generate_summary_for_trial(input_files_paths_dict[rat_id], rat_id, TCHT_default_headers)

        benchmarking.benchmark.prepare_saving_timer()
        export_file_into_excel(dataframe, output_files_paths_dict[rat_id])
        benchmarking.benchmark.update_saving_timer()

        print(f"output: {output_files_paths_dict[rat_id]}")
        print(f"Done rat id {rat_id} in {experiment_name}")


def generate_summary_for_OF(trial_file_path: str):
    raw_dataframe = load_excel_file(trial_file_path)
    header_columns = [f"{names[0]} {names[1]}" for names in OF_headers]
    print(header_columns)

    summary_dataframe = pd.DataFrame()
    total_time(raw_dataframe, summary_dataframe, OF_headers)

    return summary_dataframe


def generate_summary_for_OF_with_buckets(trial_file_path: str, starting_time, ending_time):
    print(f"{starting_time} - {ending_time}")
    raw_dataframe = load_excel_file(trial_file_path)
    df_filter = raw_dataframe["Trial time"] < ending_time
    bucket_dataframe = raw_dataframe.where(df_filter)
    bucket_time = OF_time_bucket

    filtered = np.where((raw_dataframe["Trial time"] < ending_time) & (raw_dataframe["Trial time"] >= starting_time))

    header_columns = [f"{names[0]} {names[1]}" for names in OF_headers]
    bucket_dataframe = raw_dataframe.loc[filtered]

    summary_dataframe = pd.DataFrame()

    total_time(bucket_dataframe, summary_dataframe, OF_headers, bucket_time)

    return summary_dataframe


def summarise_OF(experiment_name: str):
    input_files_paths_dict = output_file_paths_dict[experiment_name]
    output_files_paths_dict = output_file_paths_dict[experiment_name + "_summary"]

    rat_ids = output_files_paths_dict.keys()

    for rat_id in rat_ids:
        trial_headers = []
        print(f"input: {input_files_paths_dict[rat_id]}")

        dataframe = generate_summary_for_OF(input_files_paths_dict[rat_id])

        export_file_into_excel(dataframe, output_files_paths_dict[rat_id])
        print(f"output: {output_files_paths_dict[rat_id]}")
        print(f"Done rat id {rat_id} in {experiment_name}")


def summarise_OF_with_buckets(experiment_name: str):
    input_files_paths_dict = output_file_paths_dict[experiment_name]
    output_files_paths_dict = output_file_paths_dict[experiment_name + "_time_buckets"]

    rat_ids = input_files_paths_dict.keys()

    for rat_id in rat_ids:
        print(f"input: {input_files_paths_dict[rat_id]}")

        current_time = 0
        for i in range(5):

            dataframe = generate_summary_for_OF_with_buckets(input_files_paths_dict[rat_id], current_time,
                                                             current_time + OF_time_bucket)

            export_file_into_excel(dataframe, output_files_paths_dict[(rat_id-1)*5+i+1])
            print(f"output: {output_files_paths_dict[(rat_id-1)*5+i+1]}")
            print(f"Done rat id {(rat_id-1)*5+i+1} in {experiment_name}")

            current_time += OF_time_bucket


def summarise_experiment(experiment_name: str):
    if experiment_name == "TCHT":
        summarise_TCHT(experiment_name)
    elif experiment_name == "OF":
        summarise_OF(experiment_name)
    elif experiment_name == "OF_time_buckets":
        summarise_OF_with_buckets("OF")


def check_for_dropped_frames(experiment_name: str):
    input_files_paths_dict = output_file_paths_dict[experiment_name + "_summary"]

    rat_ids = input_files_paths_dict.keys()

    absolute_min = 100
    for rat_id in rat_ids:
        print(input_files_paths_dict[rat_id])
        dataframe = load_excel_file(input_files_paths_dict[rat_id])

        total = 0
        columns_sum = 0
        skip = True

        for column_name in dataframe.columns:
            if "Total" in column_name:
                if skip:
                    print(column_name)
                    total = dataframe.loc[0, column_name]
                    skip = False
                    continue
                print(f"{total} = {columns_sum}")
                if total != 0:
                    percentage = (columns_sum * 100)/total
                    print(f"{percentage:.2f} %")
                    if percentage < absolute_min:
                        absolute_min = percentage
                else:
                    print("100 %")
                print(column_name)
                total = dataframe.loc[0, column_name]
                columns_sum = 0
            else:
                columns_sum += dataframe.loc[0, column_name]
        print(f"{total}")

        print(f"current min = {absolute_min}")

    print(f"absolute min = {absolute_min}")

