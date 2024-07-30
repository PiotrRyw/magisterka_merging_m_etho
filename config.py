# Piotr Rywczak
import yaml

OF_time_bucket = 5 * 60  # s
frame_rate = 30

# ########################################## generating file names

OF_ethovision_file_paths = [f"D:/Neuro/Magisterka2024/Dane_pozycyjne_Ethovision/OF/Raw data-OpenField-Trial{x: >6}.xlsx"
                            for x in range(1, 20)]
# Ethovision files maja dodane spacje przed numerem tak zeby calosc numeru miala dokladnie 6 znakow: XXXXX1, XXXX11, etc
TCHT_ethovision_file_paths = [f"D:/Neuro/Magisterka2024/Dane_pozycyjne_Ethovision/TCHT/Raw data-TChT-Trial{x: >6}.xlsx"
                              for x in range(1, 58)]

ethovision_file_paths_dict = {
    "OF": {x + 1: OF_ethovision_file_paths[x] for x in range(19)},
    "TCHT": {x + 1: TCHT_ethovision_file_paths[x] for x in range(57)}
}

OF_manual_laberer_file_dict = "D:/Neuro/Magisterka2024/Dane_surowe_Manual_Laberer/OF/OF"
OF_manual_laberer_file_names = ["Agata", "Alan", "Ania", "Gabrysia", "Gniewosz", "Kamil", "Kasia", "Kinga", "Magda",
                                "Marian", "Martyna", "Ola", "Olga", "Patrycjusz", "Patryk", "Piotr", "Przemek",
                                "Sylwia", "Tomek"]

OF_manual_laberer_file_paths = [f"{OF_manual_laberer_file_dict}/{OF_manual_laberer_file_names[x]}.xlsx" for x in
                                range(19)]

TCHT_manual_laberer_file_dict = "D:/Neuro/Magisterka2024/Dane_surowe_Manual_Laberer/TChT/labelledTChT"
TCHT_manual_laberer_file_names_partial = ["Alter", "Axel", "Buck", "Campbell", "Carlson", "Edwards", "Greengard",
                                          "Hall", "Houghton",
                                          "Kandel", "Lauterbur", "Levi-Montalcini", "Moser Edek", "Moser Majka",
                                          "Nekher", "Patapoutian", "Ratcliffe",
                                          "Rosbash", "Young"]

TCHT_range = len(TCHT_manual_laberer_file_names_partial) * 3

TCHT_manual_laberer_file_names = [f"{TCHT_manual_laberer_file_names_partial[int(x / 3)]}{x % 3 + 1}" for x in
                                  range(TCHT_range)]
TCHT_manual_laberer_file_paths = [f"{TCHT_manual_laberer_file_dict}/{TCHT_manual_laberer_file_names[x]}.xlsx" for x in
                                  range(57)]

manual_laberer_file_paths_dict = {
    "OF": {x + 1: OF_manual_laberer_file_paths[x] for x in range(19)},
    "TCHT": {x + 1: TCHT_manual_laberer_file_paths[x] for x in range(TCHT_range)}
}

OF_output_file_paths = [f"D:/Neuro/Magisterka2024/Scalone_Dane/OF/{OF_manual_laberer_file_names[x]}.xlsx" for x in range(19)]
TCHT_output_file_paths = [f"D:/Neuro/Magisterka2024/Scalone_Dane/TCHT/trial_{x}.xlsx" for x in range(1, 58)]
OF_summary_file_paths = [f"D:/Neuro/Magisterka2024/Scalone_Dane/OF_summary/{OF_manual_laberer_file_names[x]}.xlsx" for x in range(19)]

TCHT_trial_directories = ["first", "second", "third"]
TCHT_summary_file_paths = [f"D:/Neuro/Magisterka2024/Scalone_Dane/TCHT_summary/{TCHT_trial_directories[y-1]}/{TCHT_manual_laberer_file_names_partial[x]}_trial_{y}.xlsx" for x in range(19) for y in range(1, 4)]


buckets = ["0-5", "5-10", "10-15", "15-20", "20-25"]
OF_summary_file_paths_buckets = [f"D:/Neuro/Magisterka2024/Scalone_Dane/OF_time_buckets/{buckets[y-1]}/{OF_manual_laberer_file_names[x]}-{y}.xlsx" for x in range(19) for y in range(1, 6)]

output_file_paths_dict = {
    "OF": {x + 1: OF_output_file_paths[x] for x in range(19)},
    "TCHT": {x + 1: TCHT_output_file_paths[x] for x in range(57)},
    "OF_summary": {x + 1: OF_summary_file_paths[x] for x in range(19)},
    "TCHT_summary": {x + 1: TCHT_summary_file_paths[x] for x in range(57)},
    "OF_time_buckets": {x + 1: OF_summary_file_paths_buckets[x] for x in range(19*5)},
}

# ########################################## trials info

OF_headers_baseline = ["head scanning", "grooming", "rearing", "scratching", "freezing", "quiet wakefulness",
                       "change movement dir"]

OF_options = ["In Center", "Out of Center"]

OF_headers = [[beh, loc] for beh in OF_headers_baseline for loc in OF_options]

# TCHT_headers_1st_trial = ["exp_cage object/2nd stranger  chamber", "exp_cage 1st stranger  chamber",
#                           "exp_rearing object/2nd stranger  chamber", "exp_rearing 1st stranger chamber",
#                           "other_rearing object/2nd stranger chamber", "other_rearing 1st stranger chamber",
#                           "other_rearing middle chamber", "grooming object/2nd stranger chamber",
#                           "grooming 1st stranger chamber", "grooming middle chamber",
#                           "scratching", "head_scanning",
#                           "quiet_wakefulness"]

trials_first_ids = [x*3 + 1 for x in range(19)]

trials_second_ids = [x*3 + 2 for x in range(19)]

trials_third_ids = [x*3 + 3 for x in range(19)]

stranger_locations_int = [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0]
stranger_locations_str = ["right" if x == 1 else "left" for x in stranger_locations_int]

first_stranger_location = {trial_id: location for trial_id, location in zip(trials_second_ids, stranger_locations_str)}

behaviors = ["nose_to_nose", "exp_cage", "exp_rearing", "other_rearing", "grooming", "scratching", "head_scanning",
             "quiet_wakefulness"]

locations = ["left", "right", "center"]

TCHT_headers_1st_trial = []

for behavior in behaviors:
    for location in locations:
        if behavior in ["nose_to_nose", "exp_cage", "exp_rearing"]:
            if location == "center":
                continue
        TCHT_headers_1st_trial.append([behavior, location])


TCHT_default_headers = TCHT_headers_1st_trial

# TCHT_headers_1st_trial = [["exp_cage", "left"], ["exp_cage", "right"], ["exp_rearing", "left"],
#                           ["exp_rearing", "right"],
#                           ["other_rearing", "left"], ["other_rearing", "right"], ["other_rearing", "center"],
#                           ["grooming", "left"], ["grooming", "right"], ["grooming", "center"],
#                           ["scratching", "left"], ["scratching", "right"], ["scratching", "center"],
#                           ["head_scanning", "left"], ["head_scanning", "right"], ["head_scanning", "center"],
#                           ["quiet_wakefulness", "left"], ["quiet_wakefulness", "right"],
#                           ["quiet_wakefulness", "center"]]


# ["nose_to_nose", "exp_cage", "exp_rearing", "other_rearing", "grooming", "scratching",
#                           "head_scanning", "quiet_wakefulness"]


locations = ["stranger", "object", "center"]
TCHT_headers_2nd_trial = []
for behavior in behaviors:
    for location in locations:
        if behavior in ["nose_to_nose", "exp_cage", "exp_rearing"]:
            if location == "center":
                continue
        TCHT_headers_2nd_trial.append([behavior, location])

# TCHT_headers_2nd_trial = ["nose_to_nose stranger", "exp_cage object", "exp_cage stranger",
#                           "exp_rearing object", "exp_rearing stranger",
#                           "other_rearing object", "other_rearing stranger", "other_rearing middle",
#                           "grooming object", "grooming stranger", "grooming middle",
#                           "scratching object", "scratching stranger", "scratching middle",
#                           "head_scanning object", "head_scanning stranger", "head_scanning middle",
#                           "quiet_wakefulness object", "quiet_wakefulness stranger", "quiet_wakefulness middle"]

locations = ["familiar", "stranger", "center"]
TCHT_headers_3rd_trial = []
for behavior in behaviors:
    for location in locations:
        if behavior in ["nose_to_nose", "exp_cage", "exp_rearing"]:
            if location == "center":
                continue
        TCHT_headers_3rd_trial.append([behavior, location])

# TCHT_headers_3rd_trial = ["nose_to_nose familiar", "nose_to_nose stranger",
#                           "exp_cage familiar", "exp_cage stranger",
#                           "exp_rearing familiar", "exp_rearing stranger",
#                           "other_rearing familiar", "other_rearing stranger", "other_rearing middle",
#                           "grooming familiar", "grooming stranger", "grooming middle",
#                           "scratching familiar", "scratching stranger", "scratching middle",
#                           "head_scanning familiar", "head_scanning stranger", "head_scanning middle",
#                           "quiet_wakefulness familiar", "quiet_wakefulness stranger", "quiet_wakefulness middle"]


# generowanie dla GraphPad =============================================================================================

open_field_group_con = ["Kamil", "Kasia", "Kinga", "Magda", "Marian", "Martyna", "Patrycjusz", "Sylwia", "Tomek"]
open_field_group_exp = [rat for rat in OF_manual_laberer_file_names if rat not in open_field_group_con]


three_chamber_group_con = ["Buck", "Campbell", "Edwards", "Houghton", "Kandel", "Montalcini", "Moser Edek", "Nekher",
                           "Patapoutian"]
three_chamber_group_exp = [rat for rat in TCHT_manual_laberer_file_names_partial if rat not in three_chamber_group_con]

graph_pad_rats_dict = {
    "OF": {
        "con": open_field_group_con,
        "exp": open_field_group_exp
    },
    "OF_buckets_1": {
        "con": open_field_group_con,
        "exp": open_field_group_exp
    },
    "OF_buckets_2": {
        "con": open_field_group_con,
        "exp": open_field_group_exp
    },
    "OF_buckets_3": {
        "con": open_field_group_con,
        "exp": open_field_group_exp
    },
    "OF_buckets_4": {
        "con": open_field_group_con,
        "exp": open_field_group_exp
    },
    "OF_buckets_5": {
        "con": open_field_group_con,
        "exp": open_field_group_exp
    },
    "TCHT_trial_1": {
        "con": three_chamber_group_con,
        "exp": three_chamber_group_exp
    },
    "TCHT_trial_2": {
        "con": three_chamber_group_con,
        "exp": three_chamber_group_exp
    },
    "TCHT_trial_3": {
        "con": three_chamber_group_con,
        "exp": three_chamber_group_exp
    }
}

graph_pad_files_dict = {
    "OF": {
        "input": r"D:\Neuro\Magisterka2024\Scalone_Dane\OF_summary",
        "output": r"D:\Neuro\Magisterka2024\Dane_GraphPad\OF"
    },
    "OF_buckets_1": {
        "input": r"D:\Neuro\Magisterka2024\Scalone_Dane\OF_time_buckets\0-5",
        "output": r"D:\Neuro\Magisterka2024\Dane_GraphPad\OF_time_buckets\0-5"
    },
    "OF_buckets_2": {
        "input": r"D:\Neuro\Magisterka2024\Scalone_Dane\OF_time_buckets\5-10",
        "output": r"D:\Neuro\Magisterka2024\Dane_GraphPad\OF_time_buckets\5-10"
    },
    "OF_buckets_3": {
        "input": r"D:\Neuro\Magisterka2024\Scalone_Dane\OF_time_buckets\10-15",
        "output": r"D:\Neuro\Magisterka2024\Dane_GraphPad\OF_time_buckets\10-15"
    },
    "OF_buckets_4": {
        "input": r"D:\Neuro\Magisterka2024\Scalone_Dane\OF_time_buckets\15-20",
        "output": r"D:\Neuro\Magisterka2024\Dane_GraphPad\OF_time_buckets\15-20"
    },
    "OF_buckets_5": {
        "input": r"D:\Neuro\Magisterka2024\Scalone_Dane\OF_time_buckets\20-25",
        "output": r"D:\Neuro\Magisterka2024\Dane_GraphPad\OF_time_buckets\20-25"
    },
    "TCHT_trial_1": {
        "input": r"D:\Neuro\Magisterka2024\Scalone_Dane\TCHT_summary\first",
        "output": r"D:\Neuro\Magisterka2024\Dane_GraphPad\TCHT\first"
    },
    "TCHT_trial_2": {
        "input": r"D:\Neuro\Magisterka2024\Scalone_Dane\TCHT_summary\second",
        "output": r"D:\Neuro\Magisterka2024\Dane_GraphPad\TCHT\second"
    },
    "TCHT_trial_3": {
        "input": r"D:\Neuro\Magisterka2024\Scalone_Dane\TCHT_summary\third",
        "output": r"D:\Neuro\Magisterka2024\Dane_GraphPad\TCHT\third"
    }
}

ignored_time_in_sec = 10
