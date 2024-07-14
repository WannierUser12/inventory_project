import re
import pandas as pd
import pandas_schema as pds
import copy
from datetime import datetime
from sqlalchemy import create_engine
from pandas_schema import Column, Schema
from enum import Enum
from pandas_schema.validation import (LeadingWhitespaceValidation,
                                      TrailingWhitespaceValidation,
                                      CanConvertValidation,
                                      MatchesPatternValidation,
                                      InRangeValidation,
                                      InListValidation)


class XLSXFileEnum(Enum):
    name = 'Наименование'
    article = 'Артикул'
    quantity = 'Количество'
    gtd = 'ГТД'

print("XLSF WORKS HERE")
class XLSXSave:
    schema = pds.Schema([
        Column(XLSXFileEnum.name.value, [LeadingWhitespaceValidation()]),
        Column(XLSXFileEnum.article.value, [LeadingWhitespaceValidation()]),
        Column(XLSXFileEnum.quantity.value, [InRangeValidation(0, 10000000)]),
        Column(XLSXFileEnum.gtd.value, [LeadingWhitespaceValidation()])
    ])

    @staticmethod
    def get_date(gtd):
        date = re.split('/', gtd)[1]
        return datetime.strptime(date, "%d%m%y")

    @staticmethod
    def validate_data(data):
        errors = XLSXSave.schema.validate(data)
        errors_text = [str(error) for error in errors]
        if errors_text:
            raise Exception('\n'.join(errors_text))

    @staticmethod
    def save_data_with_user(data, user):
        XLSXSave.validate_data(data)

        # Process the data
        data['date'] = data['ГТД'].apply(XLSXSave.get_date)
        data['income_quantity'] = copy.deepcopy(data['Количество'])
        data['income_price'] = [0 for x in data['date']]
        data['minimal_price'] = [0 for x in data['date']]
        data['category'] = ["Категория?" for x in data['date']]

        data = data.rename(
            columns={'Наименование': 'name', 'Артикул': 'description', 'Количество': 'quantity', 'ГТД': 'gtd_id'}
        )

        engine = create_engine('postgresql://admin:admin@db:5432/inventory')
        data.to_sql('inventory_import_products', engine, if_exists='append', index=False)
