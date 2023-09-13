from dataclasses import dataclass


@dataclass
class Pagination:
    offset: int
    records_per_page: int

    def __post_init__(self):
        try:
            self.offset = int(self.offset)
        except ValueError:
            raise ValueError("Offset must be an integer.")
        if self.offset < 0:
            raise ValueError("Offset must be greater than or equal to 0.")

        try:
            self.records_per_page = int(self.records_per_page)
        except ValueError:
            raise ValueError("Offset must be an integer.")
        if self.records_per_page < 0:
            raise ValueError("Records per page must be greater than or equal to 0.")
