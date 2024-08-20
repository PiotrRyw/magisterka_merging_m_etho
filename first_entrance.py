# Piotr Rywczak
number_of_rats = 19
from config import TCHT_manual_laberer_file_names_partial
from config import three_chamber_group_con
from config import three_chamber_group_exp
import pandas as pd

trial_list = [f"trial {x}" for x in range(1, number_of_rats*3 + 1)]

first_trial_ids = [x*3+1 for x in range(number_of_rats)]
second_trial_ids = [x*3+2 for x in range(number_of_rats)]
third_trial_ids = [x*3+3 for x in range(number_of_rats)]

where_entered_first_by_trial_number = {
    1: "right",
    2: "left",
    3: "none",
    4: "left",
    5: "right",
    6: "left",
    7: "right",
    8: "right",
    9: "right",
    10: "right",
    11: "left",
    12: "left",
    13: "right",
    14: "left",
    15: "left",
    16: "left",
    17: "left",
    18: "left",
    19: "right",
    20: "left",
    21: "left",
    22: "left",
    23: "left",
    24: "right",
    25: "right",
    26: "right",
    27: "right",
    28: "right",
    29: "right",
    30: "left",
    31: "right",
    32: "left",
    33: "left",
    34: "right",
    35: "right",
    36: "left",
    37: "right",
    38: "left",
    39: "left",
    40: "left",
    41: "none",
    42: "none",
    43: "right",
    44: "right",
    45: "left",
    46: "right",
    47: "right",
    48: "right",
    49: "right",
    50: "right",
    51: "right",
    52: "right",
    53: "left",
    54: "right",
    55: "right",
    56: "left",
    57: "left",
}

group = ["con" if TCHT_manual_laberer_file_names_partial[int((trial_id-1)/3)] in three_chamber_group_con else "exp" for trial_id in range(57)]

first_chamber_data_dict = {trial_id: [TCHT_manual_laberer_file_names_partial[int((trial_id-1)/3)], where_entered_first_by_trial_number[trial_id], group[trial_id - 1]] for trial_id in where_entered_first_by_trial_number}

print(three_chamber_group_exp)
print(three_chamber_group_con)

def generate_first_chamber_dataframe_for_each_trial():
    common_columns = ["trial", "animal", "first chamber", "group"]
    first_trial_df = pd.DataFrame(columns=common_columns)
    second_trial_df = pd.DataFrame(columns=common_columns)
    third_trial_df = pd.DataFrame(columns=common_columns)

    for rat_id in first_chamber_data_dict.keys():
        new_row = pd.Series({"trial": rat_id, "animal": first_chamber_data_dict[rat_id][0], "first chamber": first_chamber_data_dict[rat_id][1], "group": first_chamber_data_dict[rat_id][2]})

        if rat_id in first_trial_ids:
            # first_trial_df = first_trial_df._append(new_row, ignore_index = True)
            first_trial_df.loc[len(first_trial_df), first_trial_df.columns] = new_row["trial"], new_row["animal"], new_row["first chamber"], new_row["group"],
        elif rat_id in second_trial_ids:
            second_trial_df.loc[len(second_trial_df), second_trial_df.columns] = new_row["trial"], new_row["animal"], new_row["first chamber"], new_row["group"],
        elif rat_id in third_trial_ids:
            third_trial_df.loc[len(third_trial_df), third_trial_df.columns] = new_row["trial"], new_row["animal"], new_row["first chamber"], new_row["group"],

    print(first_trial_df)
    print(second_trial_df)
    print(third_trial_df)

    # first_trial_df.to_excel(r"D:\Neuro\Magisterka2024\Dane_GraphPad\TCHT\pierwszy_chamber\text.xlsx")
    sums_first_trial = first_trial_df.groupby(["first chamber", "group"]).size().unstack(fill_value=0)
    print(sums_first_trial)
    sums_second_trial = second_trial_df.groupby(["first chamber", "group"]).size().unstack(fill_value=0)
    print(sums_second_trial)
    sums_third_trial = third_trial_df.groupby(["first chamber", "group"]).size().unstack(fill_value=0)
    print(sums_third_trial)

print(first_chamber_data_dict)
print("END")
