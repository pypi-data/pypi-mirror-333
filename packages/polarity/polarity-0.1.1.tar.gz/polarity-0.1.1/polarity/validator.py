import math
import re
from datetime import date, datetime, time
from typing import Any, Dict, List, Optional, Tuple, Type, Union

import polars as pl
from dateutil import tz
from dateutil.parser import parse
from pydantic import BaseModel, ValidationError


class PolarsValidator:
    """Class for validating and correcting data in Polars DataFrames using Pydantic models."""

    def __init__(self):
        self.target_timezone = tz.gettz('Europe/Madrid')

    def attempt_cast(self, value: Any, expected_type: Type, verbose: bool = False) -> Any:
        """Attempts to cast a value to the expected type."""
        if verbose:
            print(f"Attempting to cast value: {value} to type: {expected_type}")
        try:
            # Define null values conditionally
            if expected_type == bool or expected_type == Optional[bool]:
                null_values = [None, 'NaN', '<NA>', 'null', 'None']
                is_nan = isinstance(value, float) and math.isnan(value)
            else:
                null_values = [None, float('nan'), 'NaN', '<NA>', 'null', 'None', '', 'NaN']
                is_nan = False

            # Handle null values
            if is_nan or (expected_type != bool and value in null_values):
                return None

            # Type-specific conversions
            if expected_type == int or expected_type == Optional[int]:
                if isinstance(value, str) and not re.match(r'^-?\d+(\.\d+)?$', value):
                    return None
                return int(float(value))

            elif expected_type == float or expected_type == Optional[float]:
                return float(value)

            elif expected_type == str or expected_type == Optional[str]:
                if isinstance(value, str):
                    try:
                        float_value = float(value)
                        if float_value.is_integer():
                            return str(int(float_value))
                        else:
                            return str(float_value)
                    except ValueError:
                        return value.strip()
                return str(value).strip() if value is not None else None

            elif expected_type == date or expected_type == Optional[date]:
                if isinstance(value, date) and not isinstance(value, datetime):
                    return value
                if isinstance(value, datetime):
                    return value.date()

                if value is not None:
                    parsed_date = parse(value, ignoretz=False, dayfirst=False)
                    if parsed_date:
                        if parsed_date.tzinfo:
                            parsed_date = parsed_date.astimezone(self.target_timezone)
                        else:
                            parsed_date = parsed_date.replace(tzinfo=self.target_timezone)
                        return parsed_date.date()
                return None

            elif expected_type == datetime or expected_type == Optional[datetime]:
                if isinstance(value, datetime):
                    if value.tzinfo:
                        value = value.astimezone(self.target_timezone)
                    else:
                        value = value.replace(tzinfo=self.target_timezone)
                    return value.replace(tzinfo=None)

                if value is not None:
                    parsed_datetime = parse(value, ignoretz=False)
                    if parsed_datetime:
                        if parsed_datetime.tzinfo:
                            parsed_datetime = parsed_datetime.astimezone(self.target_timezone)
                        else:
                            parsed_datetime = parsed_datetime.replace(tzinfo=self.target_timezone)
                        return parsed_datetime.replace(tzinfo=None)
                return None

            elif expected_type == bool or expected_type == Optional[bool]:
                if value is None:
                    return None
                if isinstance(value, str):
                    value_lower = value.lower().strip()
                    if value_lower in ['true', '1', 'yes', 'y', 'sí', 'si']:
                        return True
                    elif value_lower in ['false', '0', 'no', 'n']:
                        return False
                    elif value_lower == '':
                        return False
                    return True
                return bool(value)

            elif expected_type == time or expected_type == Optional[time]:
                if isinstance(value, time):
                    return value
                if isinstance(value, datetime):
                    return value.time()
                if isinstance(value, str):
                    parsed_time = parse(value).time()
                    return parsed_time
                return None

            # If value is already of expected type, return it
            if isinstance(value, expected_type):
                return value

            return value

        except (ValueError, TypeError, AttributeError) as e:
            if verbose:
                print(f"Error casting {value} to type {expected_type}: {e}")
            return None

    def enforce_correct_dtypes(self, df: pl.DataFrame, model: Type[BaseModel]) -> pl.DataFrame:
        """Ensures DataFrame columns have correct data types based on the Pydantic model."""
        for field, field_type in model.__annotations__.items():
            if field in df.columns:
                # Handle Optional types
                if hasattr(field_type, '__origin__') and field_type.__origin__ is Union:
                    field_type = [arg for arg in field_type.__args__ if arg is not type(None)][0]

                # Determine Polars type based on expected type
                polars_type = None
                if field_type == datetime or field_type == Optional[datetime]:
                    polars_type = pl.Datetime
                elif field_type == date or field_type == Optional[date]:
                    polars_type = pl.Date
                elif field_type == bool or field_type == Optional[bool]:
                    polars_type = pl.Boolean
                elif field_type == int or field_type == Optional[int]:
                    polars_type = pl.Int64
                elif field_type == float or field_type == Optional[float]:
                    polars_type = pl.Float64
                elif field_type == str or field_type == Optional[str]:
                    polars_type = pl.Utf8
                elif field_type == time or field_type == Optional[time]:
                    polars_type = pl.Time

                if polars_type:
                    col_dtype = df.schema[field]

                    if col_dtype == polars_type:
                        continue

                    try:
                        if polars_type in [pl.Date, pl.Datetime] and col_dtype == pl.Utf8:
                            df = df.with_columns(
                                pl.col(field).str.strptime(polars_type, format=None, strict=False)
                            )
                        else:
                            df = df.with_columns(pl.col(field).cast(polars_type))
                    except Exception as e:
                        print(f"Error converting field {field} to type {polars_type}: {e}")
                        df = df.with_columns(pl.lit(None).alias(field))

        return df

    def validate_dataframe(self, df: pl.DataFrame, model: Type[BaseModel], return_type: str = 'polars') -> Tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
        """Validates a DataFrame against a Pydantic model."""
        corrected_rows = []
        correct_rows = []
        error_rows = []

        for row in df.to_dicts():
            errors = {}
            corrected_row = {}
            casted_row = {}

            for field, expected_type in model.__annotations__.items():
                value = row.get(field)
                casted_value = self.attempt_cast(value, expected_type)
                casted_row[field] = casted_value

            try:
                validated_row = model(**casted_row)
                corrected_row = validated_row.model_dump()
                # corrected_row['errors'] = None
                correct_rows.append(corrected_row)
            except ValidationError as e:
                errors = e.errors()
                for error in errors:
                    loc = error['loc'][0] if isinstance(error['loc'], tuple) else error['loc']
                    casted_row[loc] = None
                # casted_row['errors'] = errors
                # error_rows.append(casted_row)
                corrected_row = casted_row.copy()

            corrected_rows.append(corrected_row)

        corrected_df = pl.DataFrame(corrected_rows)
        correct_df = pl.DataFrame(correct_rows) if correct_rows else pl.DataFrame()
        error_df = pl.DataFrame(error_rows) if error_rows else pl.DataFrame()

        corrected_df = self.enforce_correct_dtypes(corrected_df, model)
        if not correct_df.is_empty():
            correct_df = self.enforce_correct_dtypes(correct_df, model)
        if not error_df.is_empty():
            error_df = self.enforce_correct_dtypes(error_df, model)

        return corrected_df, correct_df, error_df

    def validate_and_correct(self, df: pl.DataFrame, model: Type[BaseModel], return_type: str = 'polars') -> Tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
        """Validates and corrects a DataFrame."""
        # Ignore return_type parameter, always return Polars DataFrame
        return self.validate_dataframe(df, model, return_type='polars')

    def remove_errors_column(self, df: pl.DataFrame) -> pl.DataFrame:
        """Removes the 'errors' column from a DataFrame if it exists."""
        return df.drop("errors") if "errors" in df.columns else df

    def dataframe_to_json(self, df: pl.DataFrame) -> List[Dict[str, Any]]:
        """Converts a Polars DataFrame to a list of dictionaries."""
        return df.to_dicts()

    def split_dataframe(
        self,
        df_new: pl.DataFrame,
        df_db: pl.DataFrame,
        pks: List[str],
        model: Type[BaseModel]
    ) -> Tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
        """Splits DataFrames into insert, equals, and update categories based on primary keys."""
        # Validación de claves primarias no vacías
        if not pks:
            raise ValueError("La lista de claves primarias 'pks' no puede estar vacía.")

        if df_new.is_empty():
            return pl.DataFrame(), pl.DataFrame(), pl.DataFrame()

        if df_db.is_empty():
            return df_new, pl.DataFrame(), pl.DataFrame()

        # Validación de que las claves primarias existen en ambos DataFrames
        for pk in pks:
            if pk not in df_new.columns:
                raise ValueError(f"La clave primaria '{pk}' no existe en df_new.")
            if pk not in df_db.columns:
                raise ValueError(f"La clave primaria '{pk}' no existe en df_db.")

            # Validación de valores nulos en claves primarias
            if df_new.select(pl.col(pk).is_null()).sum().item() > 0:
                raise ValueError(f"La clave primaria '{pk}' contiene valores nulos en df_new.")
            if df_db.select(pl.col(pk).is_null()).sum().item() > 0:
                raise ValueError(f"La clave primaria '{pk}' contiene valores nulos en df_db.")

        # Validar y corregir los DataFrames
        corrected_new, correct_new, _ = self.validate_and_correct(df_new, model)
        corrected_db, correct_db, _ = self.validate_and_correct(df_db, model)

        # Asegurarse de que las claves primarias siguen presentes después de la validación
        for pk in pks:
            if pk not in correct_new.columns:
                raise ValueError(f"La clave primaria '{pk}' no está presente en correct_new después de la validación.")
            if pk not in correct_db.columns:
                raise ValueError(f"La clave primaria '{pk}' no está presente en correct_db después de la validación.")

        correct_new = self.remove_errors_column(correct_new)
        correct_db = self.remove_errors_column(correct_db)

        # Identificar columnas que no son claves primarias
        non_pk_columns = [col for col in correct_new.columns if col not in pks]

        # Realizar un join interno para encontrar filas con claves primarias comunes
        df_joined = correct_new.join(correct_db, on=pks, how='inner', suffix="_db")

        # Comparar celda a celda, asegurando que los valores None se traten como iguales
        comparisons = [
            pl.col(col).eq(pl.col(f"{col}_db")).fill_null(pl.col(col).is_null() & pl.col(f"{col}_db").is_null())
            for col in non_pk_columns
        ]

        # Crear una columna que indique si todas las comparaciones son verdaderas
        df_joined = df_joined.with_columns(
            pl.fold(
                acc=pl.lit(True),
                function=lambda acc, x: acc & x,
                exprs=comparisons
            ).alias("_rows_equal")
        )

        # Filas exactamente iguales
        equals_df = df_joined.filter(pl.col("_rows_equal")).select(correct_new.columns)

        # Filas que requieren actualización (diferencias en columnas no claves)
        update_df = df_joined.filter(~pl.col("_rows_equal")).select(correct_new.columns)

        # Filas nuevas que no existen en df_db
        insert_df = correct_new.join(correct_db, on=pks, how='anti')

        return insert_df, equals_df, update_df


# Create a global instance for the standalone functions to use
_validator = PolarsValidator()

# Standalone functions that delegate to the validator instance
def attempt_cast(value, expected_type, verbose=False):
    return _validator.attempt_cast(value, expected_type, verbose)

def validate_and_correct(df, model, return_type='polars'):
    # Ignore return_type, always use polars
    return _validator.validate_and_correct(df, model)

def validate_dataframe(df, model, return_type='polars'):
    # Ignore return_type, always use polars
    return _validator.validate_dataframe(df, model)

def enforce_correct_dtypes(df, model, has_time_component=None):
    return _validator.enforce_correct_dtypes(df, model)

def remove_errors_column(df):
    return _validator.remove_errors_column(df)

def split_dataframe(df_new, df_db, pks, model):
    return _validator.split_dataframe(df_new, df_db, pks, model)