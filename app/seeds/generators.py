from pathlib import Path
import random
from datetime import datetime, timedelta, timezone
from flask_seeder import generator

names_path = "app/seeds/data/names.txt"


def read_resource(path):
    lines = []
    with open(Path(path).absolute()) as source:
        lines = source.read().splitlines()

    return lines


class SequenceArray(generator.Sequence):
    def __init__(self, data: list = []):
        super().__init__(start=0, end=len(data))
        self._data = data

    def generate(self):
        value = self._next
        self._next += 1

        return self._data[value]


class NameGenerator(generator.Generator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._lines = None

    def generate(self):
        if self._lines is None:
            self._lines = read_resource(names_path)

        result = self.rnd.choice(self._lines)

        return result


class DateGenerator(generator.Generator):

    def __init__(self, start_date: datetime, **kwargs):
        super().__init__(**kwargs)
        self.start_date = start_date

    def generate(self):
        step = timedelta(days=8)
        end_date = datetime.now(timezone.utc)
        random_date = self.start_date + \
            random.randrange((end_date - self.start_date) // step + 1) * step

        return random_date
