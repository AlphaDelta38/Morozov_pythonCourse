class DataProcessor:
    def process_data(self, data):
        return [x * 2 for x in data]

    def analyze_data(self, data):
        processed_data = self.process_data(data)
        return sum(processed_data)