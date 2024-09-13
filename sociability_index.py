# Piotr Rywczak
# calculating social preference index: (Ts - Tns) / (Ts + Tns) https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8103520/
# Ts  - time with social stimulus, Tns - time with non social stimulus
import re

import pandas as pd

from config import graph_pad_files_dict, three_chamber_group_con
from loading_files import load_excel_file
from os import listdir
from os.path import isfile, join


def calculate_social_preference_index(time_with_social, time_with_nonsocial):
    if time_with_social + time_with_nonsocial != 0:
        return (time_with_social - time_with_nonsocial) / (time_with_social + time_with_nonsocial)
    else:
        return None


def do_single_trial(rat_and_import_file_path, pairs_to_compare, parameter_and_output_file_path, eksp, contr):
    predataframes_dict = dict.fromkeys(pairs_to_compare.keys())
    for key in predataframes_dict.keys():
        predataframes_dict[key] = {eksp: [], contr: []}

    for rat in rat_and_import_file_path.keys():
        file_path = rat_and_import_file_path[rat]
        print(file_path)
        for parameter in pairs_to_compare.keys():
            df = load_excel_file(file_path)
            stranger_prop = pairs_to_compare[parameter][0]
            object_prop = pairs_to_compare[parameter][1]

            spi = calculate_social_preference_index(df.iloc[2][stranger_prop], df.iloc[2][object_prop])
            if rat in three_chamber_group_con:
                predataframes_dict[parameter][contr].append(spi)
            else:
                predataframes_dict[parameter][eksp].append(spi)

    for key in predataframes_dict:
        predataframes_dict[key][contr].append(None)

        df = pd.DataFrame.from_dict(predataframes_dict[key])
        print(key)
        print(df)
        df.to_excel(parameter_and_output_file_path[key])


def export_social_preference_index():

    # for trial 2
    import_file_dict = graph_pad_files_dict["TCHT_trial_2"]["input"]
    output_file_dict = graph_pad_files_dict["TCHT_trial_2"]["output"]

    import_file_paths = [join(import_file_dict, f) for f in listdir(import_file_dict) if
                         isfile(join(import_file_dict, f))]

    rat_names = [name.partition("second\\")[2].partition("_trial")[0] for name in import_file_paths]

    rat_and_import_file_path = dict(zip(rat_names, import_file_paths))

    pairs_to_compare = {
        "exp_cage": ("exp_cage stranger", "exp_cage object"),
        "exp_rearing": ("exp_rearing stranger", "exp_rearing object"),
        "other_rearing": ("other_rearing stranger", "other_rearing object"),
        "grooming": ("grooming stranger", "grooming object"),
        "scratching": ("scratching stranger", "scratching object"),
        "head_scanning": ("head_scanning stranger", "head_scanning object"),
        "quiet_wakefulness": ("quiet_wakefulness stranger", "quiet_wakefulness object")}

    export_file_paths = [join(output_file_dict, f"{f} social preference index.xlsx") for f in pairs_to_compare.keys()]

    parameter_and_output_file_path = dict(zip(pairs_to_compare.keys(), export_file_paths))

    eksp = "Eksp."
    contr = "Kontr."

    do_single_trial(rat_and_import_file_path, pairs_to_compare, parameter_and_output_file_path, eksp, contr)

    # for trial 3

    import_file_dict = graph_pad_files_dict["TCHT_trial_3"]["input"]
    output_file_dict = graph_pad_files_dict["TCHT_trial_3"]["output"]

    import_file_paths = [join(import_file_dict, f) for f in listdir(import_file_dict) if
                         isfile(join(import_file_dict, f))]

    rat_names = [name.partition("third\\")[2].partition("_trial")[0] for name in import_file_paths]

    rat_and_import_file_path = dict(zip(rat_names, import_file_paths))

    pairs_to_compare = {
        "nose_to_nose": ("nose_to_nose stranger", "nose_to_nose familiar"),
        "exp_cage": ("exp_cage stranger", "exp_cage familiar"),
        "exp_rearing": ("exp_rearing stranger", "exp_rearing familiar"),
        "other_rearing": ("other_rearing stranger", "other_rearing familiar"),
        "grooming": ("grooming stranger", "grooming familiar"),
        "scratching": ("scratching stranger", "scratching familiar"),
        "head_scanning": ("head_scanning stranger", "head_scanning familiar"),
        "quiet_wakefulness": ("quiet_wakefulness stranger", "quiet_wakefulness familiar")}

    export_file_paths = [join(output_file_dict, f"{f} social preference index.xlsx") for f in pairs_to_compare.keys()]

    parameter_and_output_file_path = dict(zip(pairs_to_compare.keys(), export_file_paths))

    eksp = "Eksp."
    contr = "Kontr."

    do_single_trial(rat_and_import_file_path, pairs_to_compare, parameter_and_output_file_path, eksp, contr)
