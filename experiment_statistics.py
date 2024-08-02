# Piotr Rywczak
from os import listdir
from os.path import join
from time import sleep

import pandas as pd
from scipy.stats._morestats import ShapiroResult
import numpy as np
import scipy.stats

from config import experiment_OF_path
from loading_files import load_excel_file
import statistics
from scipy.stats import shapiro, stats


# load experiment
# test for normal distribution for each group
# determine outliers
# exclude outliers
# test for variance equality
# T test
# nonparametric test
# save result
# save aggregate results for every experiment

# future: todo - adjust p-value for number of T tests

def f_test(group1, group2):
    f = np.var(group1, ddof=1) / np.var(group2, ddof=1)
    nun = group1.size - 1
    dun = group2.size - 1
    p_value = 1 - scipy.stats.f.cdf(f, nun, dun)

    return f, p_value


class ExperimentResult:
    def __init__(self):
        self.name = ""
        self.normality_con = ShapiroResult(0, 0)
        self.normality_exp = ShapiroResult(0, 0)
        self.variances_equality = False
        self.dataframe = pd.DataFrame()
        self.t_test_p_value = 0
        self.t_test_value = 0
        self.p_value = 0.05

    @property
    def normal_distribution_control(self):
        return self.normality_con.pvalue < self.p_value

    @property
    def normal_distribution_exp(self):
        return self.normality_exp.pvalue < self.p_value

    @property
    def distributions_are_normal(self):
        return self.normal_distribution_exp and self.normal_distribution_control

    @property
    def variances_are_equal(self):
        return self.variances_equality

    def __str__(self):
        return (f"{self.name}\n"
                f"con normality: {self.normality_con.pvalue} "
                f"exp normality: {self.normality_exp.pvalue} "
                f"variances: {self.variances_equality}\n"
                f"T Test: value: {self.t_test_value} p: {self.t_test_p_value}"
                f"{self.dataframe.to_string()}")


def check_normality(experiment_data: ExperimentResult):
    print(experiment_data.dataframe["con"])
    experiment_data.normality_con = shapiro(experiment_data.dataframe["con"])
    experiment_data.normality_exp = shapiro(experiment_data.dataframe["exp"])


def check_variances(experiment_data: ExperimentResult):
    f_test_values = f_test(experiment_data.dataframe["con"], experiment_data.dataframe["exp"])
    experiment_data.variances_equality = f_test_values[1] < experiment_data.p_value


def qualify_for_parametric_tests(experiment_data: ExperimentResult):
    check_normality(experiment_data)
    check_variances(experiment_data)

    return experiment_data.distributions_are_normal and experiment_data.variances_are_equal


def do_parametric_test_on_property(experiment_data: ExperimentResult):
    t_stat, p_value = stats.ttest_ind(experiment_data.dataframe["con"], experiment_data.dataframe["exp"])

    experiment_data.t_test_p_value = p_value
    experiment_data.t_test_value = t_stat


def do_nonparametric_test_on_property(experiment_data: ExperimentResult):
    result_dataframe: pd.DataFrame


def generate_experiment_summary(file_path: str, trial_key: str):
    # load single property
    property_dataframe = load_excel_file(file_path)

    experiment_data = ExperimentResult()
    experiment_data.dataframe = property_dataframe
    experiment_data.name = trial_key

    print(experiment_data)

    # determine which test needs to be done

    if qualify_for_parametric_tests(experiment_data):
        do_parametric_test_on_property(experiment_data)
    else:
        do_nonparametric_test_on_property(experiment_data)

    # do parametric/nonparametric test
    # return result
    return experiment_data


def generate_statistics_results():
    # load tests
    experiment_files_dictionary: dict

    filepaths_dir = {}
    files = listdir(experiment_OF_path)
    for file in files:
        filepaths_dir[file] = join(experiment_OF_path, file)

    print(filepaths_dir)
    i = 1
    for trial_key in filepaths_dir.keys():
        experiment_data = generate_experiment_summary(filepaths_dir[trial_key], trial_key)
        print(experiment_data)
        i -= 1
        if i < 0:
            break

    return filepaths_dir
