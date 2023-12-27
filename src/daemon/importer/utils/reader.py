from csv import DictReader
import pandas as pd

class CSVReader:

    def __init__(self, path, part, delimiter=','):
        self._path = path
        self._part = part
        self._delimiter = delimiter

    def read_and_split_csv(self):
        df = pd.read_csv(self._path)
        rows_per_part = len(df) // 10

        csv_data = None

        for i in range(10):
            start_idx = i * rows_per_part
            end_idx = start_idx + rows_per_part
            
            if i == 10 - 1:
                part_df = df.iloc[start_idx:]
            else:
                part_df = df.iloc[start_idx:end_idx]

            if i == self._part : 
                csv_data = part_df.to_csv(index=False, sep=self._delimiter)

        return csv_data

    def loop(self):
        csv_part = self.read_and_split_csv()
        if csv_part is not None:
            # Use StringIO para converter a string CSV em um objeto de arquivo
            from io import StringIO
            with StringIO(csv_part) as file:
                for row in DictReader(file, delimiter=self._delimiter):
                    yield row

    def read_entities(self, attr, builder, after_create=None):
        entities = {}
        for row in self.loop():
            e = row[attr]
            if e not in entities:
                entities[e] = builder(row)
                after_create is not None and after_create(entities[e], row)

        return entities
