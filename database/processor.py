class DataProcessor:

    def validate(self, data: list or tuple):
        return not (None in data)
