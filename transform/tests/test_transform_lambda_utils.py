import pandas as pd
import pytest, datetime, os
from unittest.mock import patch

with patch.dict(os.environ, {"ingestion_zone_bucket": "temp", "processed_data_zone_bucket": "temp2"}):
    from transform.src.transform_lambda import conversion_for_dim_counterparty, \
        conversion_for_dim_currency, conversion_for_dim_date, conversion_for_dim_design, \
        conversion_for_dim_location, conversion_for_dim_staff, conversion_for_fact_sales_order, \
        date_helper

@pytest.mark.describe("test conversion_for_dim_location")
class TestDimLocation:
    input_file = 'transform/tests/data/address.json'
    location_df = pd.read_json(input_file)
    output_df = conversion_for_dim_location(location_df)

    @pytest.mark.it("check the number of columns without primary key column")
    def test_number_of_columns(self):
        assert len(self.output_df.columns) == 8

    @pytest.mark.it("check the column names match schema")
    def test_valid_column_names_only(self):
        expected_columns = ['location_id', 'address_line_1','address_line_2','district','city','postal_code','country','phone']
        assert list(self.output_df.columns) == expected_columns

    @pytest.mark.it("check the column datatypes match schema")
    def test_column_data_types_match_schema(self):
       for column in self.output_df.columns:
           assert type(column) ==  str

    @pytest.mark.it("check output is a dataframe")
    def test_output_is_a_dataframe(self):
        assert isinstance(self.output_df, pd.DataFrame)


@pytest.mark.describe("test conversion_for_dim_currency")
class TestDimCurrency:
    input_file = 'transform/tests/data/currency.json'
    currency_df = pd.read_json(input_file)
    output_df = conversion_for_dim_currency(currency_df)

    @pytest.mark.it("check the column names match schema")
    def test_valid_column_names_only(self):
        expected_columns = ['currency_id', 'currency_code','currency_name']
        assert list(self.output_df.columns) == expected_columns

    @pytest.mark.it("check the column datatypes match schema")
    def test_column_data_types_match_schema(self):
        for column in self.output_df.columns:
            assert type(column) == str

    @pytest.mark.it("check output is a dataframe")
    def test_output_is_a_dataframe(self):
        assert isinstance(self.output_df, pd.DataFrame)


@pytest.mark.describe("test conversion_for_dim_design")
class TestDimDesign:
    input_file = 'transform/tests/data/design.json'
    design_df = pd.read_json(input_file)
    output_df = conversion_for_dim_design(design_df)

    @pytest.mark.it("check the column names match schema")
    def test_valid_column_names_only(self):
        expected_columns = ['design_id', 'design_name','file_location','file_name']
        assert list(self.output_df.columns) == expected_columns

    @pytest.mark.it("check the column datatypes match schema")
    def test_column_data_types_match_schema(self):
        for column in self.output_df.columns:
            assert type(column) == str

    @pytest.mark.it("check output is a dataframe")
    def test_output_is_a_dataframe(self):
        assert isinstance(self.output_df, pd.DataFrame)


@pytest.mark.describe("test conversion_for_dim_counterparty")
class TestDimCounterparty:
    
    input_ad_file = 'transform/tests/data/address.json'
    input_cp_file = 'transform/tests/data/counterparty.json'
    address_df = pd.read_json(input_ad_file)
    counterparty_df = pd.read_json(input_cp_file)
    output_df = conversion_for_dim_counterparty(address_df,counterparty_df)

    @pytest.mark.it("check the column names match schema")
    def test_valid_column_names_only(self):
        expected_columns = ['counterparty_id', 'counterparty_legal_name', 'counterparty_legal_address_line_1','counterparty_legal_address_line_2','counterparty_legal_district','counterparty_legal_city','counterparty_legal_postal_code','counterparty_legal_country','counterparty_legal_phone_number']
        assert list(self.output_df.columns) == expected_columns

    @pytest.mark.it("check the column datatypes match schema")
    def test_column_data_types_match_schema(self):
        for column in self.output_df.columns:
            assert type(column) == str

    @pytest.mark.it("check output is a dataframe")
    def test_output_is_a_dataframe(self):
        assert isinstance(self.output_df, pd.DataFrame)


@pytest.mark.describe("test conversion_for_dim_staff")
class TestDimStaff:
    input_dep_file = 'transform/tests/data/department.json'
    input_staff_file = 'transform/tests/data/staff.json'
    department_df = pd.read_json(input_dep_file)
    staff_df = pd.read_json(input_staff_file)
    output_df = conversion_for_dim_staff(department_df,staff_df)

    @pytest.mark.it("check the column names match schema")
    def test_valid_column_names_only(self):
        expected_columns = ['staff_id', 'first_name','last_name','department_name','location','email_address']
        for column in self.output_df.columns:
            assert column in expected_columns

    @pytest.mark.it("check the column datatypes match schema")
    def test_column_data_types_match_schema(self):
        for column in self.output_df.columns:
            assert type(column) == str

    @pytest.mark.it("check output is a dataframe")
    def test_output_is_a_dataframe(self):
        assert isinstance(self.output_df, pd.DataFrame)


@pytest.mark.describe("test date_helper")
class TestDimDateHelper:
    input_file = 'transform/tests/data/sales_order.json'
    df = pd.read_json(input_file)
    column = 'created_at'
    created_at_df = df[[column]]
    output_df = date_helper(created_at_df, column)

    @pytest.mark.it("check the column names match schema")
    def test_valid_column_names_only(self):
        expected_columns = ['date_id','year','month','day','day_of_week','day_name','month_name','quarter']
        for column in self.output_df.columns:
            assert column in expected_columns

    @pytest.mark.it("check the column datatypes match schema")
    def test_column_data_types_match_schema(self):
        assert self.output_df.date_id.dtype == object
        assert self.output_df.year.dtype == 'Int32'
        assert self.output_df.month.dtype == 'Int32'
        assert self.output_df.day.dtype == 'Int32'
        assert self.output_df.day_of_week.dtype == 'Int32'
        assert self.output_df.day_name.dtype == 'string[python]'
        assert self.output_df.month_name.dtype == 'string[python]'
        assert self.output_df.quarter.dtype == 'Int32'

    @pytest.mark.it("check values in date_id are of date type")
    def test_values_in_date_id(self):
        for i in self.output_df.index:
            assert isinstance(self.output_df.loc[i,"date_id"], datetime.date)

    @pytest.mark.it("check output is a dataframe")
    def test_output_is_a_dataframe(self):
        assert isinstance(self.output_df, pd.DataFrame)


@pytest.mark.describe("test conversion_for_dim_date_tb")
class TestDimDateTb:
    input_file = 'transform/tests/data/sales_order.json'
    date_df = pd.read_json(input_file)
    output_df = conversion_for_dim_date(date_df)

    @pytest.mark.it("check there are no duplicate rows")
    def test_no_duplicate_rows(self):
        result = self.output_df.duplicated()
        assert all([value == False for value in result.values])

    @pytest.mark.it("check output is a dataframe")
    def test_output_is_a_dataframe(self):
        assert isinstance(self.output_df, pd.DataFrame)


@pytest.mark.describe("test conversion_for_fact_sales_order")
class TestFactSalesOrder:
    input_file = 'transform/tests/data/sales_order.json'
    sales_df = pd.read_json(input_file)
    output_df = conversion_for_fact_sales_order(sales_df)

    @pytest.mark.it("check the column names match schema")
    def test_valid_column_names_only(self):
        expected_columns = ["sales_record_id", "sales_order_id","created_date","created_time","last_updated_date","last_updated_time","sales_staff_id","counterparty_id","units_sold","unit_price","currency_id","design_id","agreed_payment_date","agreed_delivery_date","agreed_delivery_location_id"]
        for column in self.output_df.columns:
            assert column in expected_columns


    @pytest.mark.it("check the column datatypes match schema")
    def test_column_data_types_match_schema(self):
        assert self.output_df.sales_record_id.dtype == 'int64'
        assert self.output_df.sales_order_id.dtype == 'int64'
        assert self.output_df.design_id.dtype == 'int64'
        assert self.output_df.sales_staff_id.dtype == 'int64'
        assert self.output_df.counterparty_id.dtype == 'int64'
        assert self.output_df.units_sold.dtype == 'int64'
        assert self.output_df.unit_price .dtype == 'float64'
        assert self.output_df.currency_id.dtype == 'int64'
        assert self.output_df.agreed_delivery_date.dtype == object
        assert self.output_df.agreed_payment_date.dtype == object
        assert self.output_df.agreed_delivery_location_id.dtype == 'int64'
        assert self.output_df.created_date.dtype == object
        assert self.output_df.created_time.dtype == object
        assert self.output_df.last_updated_date.dtype == object
        assert self.output_df.last_updated_time.dtype == object

    @pytest.mark.it("check values of agreed_delivery_date, agreed_payment_date, created_date, last_updated_date are of date type")
    def test_values_in_date_type(self):
        for i in self.output_df.index:
            assert isinstance(self.output_df.loc[i,"agreed_delivery_date"], datetime.date)
            assert isinstance(self.output_df.loc[i,"agreed_payment_date"], datetime.date)
            assert isinstance(self.output_df.loc[i,"created_date"], datetime.date)
            assert isinstance(self.output_df.loc[i,"last_updated_date"], datetime.date)
    
    @pytest.mark.it("check values of created_time and last_updated_time are of time type")
    def test_values_in_time_type(self):
        for i in self.output_df.index:
            assert isinstance(self.output_df.loc[i,"created_time"], datetime.time)
            assert isinstance(self.output_df.loc[i,"last_updated_time"], datetime.time)

    @pytest.mark.it("check output is a dataframe")
    def test_output_is_a_dataframe(self):
        assert isinstance(self.output_df, pd.DataFrame)