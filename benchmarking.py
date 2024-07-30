import time


class MeasuringBenchmark:
    def __init__(self):
        self.current_operation_timer = None
        self.current_saving_timer = None
        self.current_loading_timer = None
        self.start_time = time.time()
        self.loading_files = 0
        self.saving_files = 0
        self.dataframe_operations = 0
        self.saving_counter = 0
        self.loading_counter = 0
        self.dataframe_operations_counter = 0

    def prepare_loading_timer(self):
        self.current_loading_timer = time.time()

    def update_loading_timer(self):
        self.loading_files += time.time() - self.current_loading_timer
        self.loading_counter += 1

    def prepare_saving_timer(self):
        self.current_saving_timer = time.time()
    def update_saving_timer(self):
        self.saving_files += time.time() - self.current_saving_timer
        self.saving_counter += 1

    def prepare_dataframe_timer(self):
        self.current_operation_timer = time.time()

    def update_dataframe_timer(self):
        self.dataframe_operations += time.time() - self.current_operation_timer
        self.dataframe_operations_counter += 1

    def print_out_results(self):
        print(f"Total loading time: {self.loading_files} - average: {self.loading_files / self.loading_counter}")
        print(f"Total saving time: {self.saving_files} - average: {self.saving_files / self.saving_counter}")
        print(f"Total operations time: {self.dataframe_operations} - average: {self.dataframe_operations / self.dataframe_operations_counter}")
        print(f"Total time: {time.time() - self.start_time}")


def init():
    global benchmark
    benchmark = MeasuringBenchmark()
