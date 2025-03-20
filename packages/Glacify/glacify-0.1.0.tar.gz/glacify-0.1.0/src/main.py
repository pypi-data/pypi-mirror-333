import polars as pl
from glacify import ValidationBase, Column

class TestClass(ValidationBase):
    index: int = Column(name="Index", is_identifier=True)
    first_name: str = Column(name="First Name", min_length=10)
    last_name: str = Column(name="Last Name")
    address: str = Column(name="Address")
    gross_income: int = Column(name="Gross-Income", le=3000)


if __name__ == "__main__":
    dataframe = pl.read_csv("test.csv")
    print(dataframe)

    validation_model = TestClass()
    validation_model.validate(dataframe=dataframe)
    dataframe = validation_model.dump()

    print(dataframe)