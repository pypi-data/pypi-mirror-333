from datetime import date
import polars as pl

from glacify.base import ValidationBase
from glacify.settings import ValidationSettings
from glacify.wrappers import validation_check
from glacify.column import Column


class NewClass(ValidationBase):
    settings = ValidationSettings(strict=True, shift_to_row=1)
    index: int = Column(name="Index", is_identifier=True)
    string_column: str = Column(name="String Column", strict=True)
    int_column: int = Column(name="Int Column")
    float_column: float = Column(name="Float Column")
    list_column: list[str] = Column(name="List Column")
    date_column: date = Column(name="Date Column", default="")

    @validation_check(mode="model")
    def test():
        pass


if __name__ == "__main__":
    dataframe = pl.read_csv("./test.csv", separator=";", infer_schema_length=0)
    model = NewClass()

    print(dataframe)

    model.validate(dataframe=dataframe)

    result = model.dump()

    print(result)
