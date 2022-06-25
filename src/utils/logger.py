class Logger:
    def __init__(self):
        pass

    def log_info(self, info):
        print(f"Log event: {info}")

    def log_metric(self, metric_name, value):
        print(f"Log metric: {metric_name} with {value}")

    def log_error(self, error):
        print(f"Error occured: {error}")
