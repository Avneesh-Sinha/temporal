import pandas as pd
import numpy as np

def detect_data_types(df, param=0.1, min_rows=10):
    n_rows = max(int(len(df) * param), min_rows)
    sample_df = df.head(n_rows)
    data_types = {}
    for column in sample_df.columns:
        inferred_type = pd.api.types.infer_dtype(sample_df[column], skipna=True)
        data_types[column] = inferred_type
    return data_types

def user_confirmation(data_types):
    print("Detected data types:")

    for column, dtype in data_types.items():
        print(f"Column: {column}, Detected Data type: {dtype}")

    print("\nSpecify any changes in the format -> 'column_name:new_type'.")
    
    changes = input("Enter changes (comma-separated): ")

    if changes:
        changes = changes.split(',')
        for change in changes:
            column, new_type = change.split(':')
            data_types[column.strip()] = new_type.strip().lower()
    return data_types

def validate_data_types(df, data_types):
    errors = []
    for column, dtype in data_types.items():
        if dtype == 'datetime':
            try:
                pd.to_datetime(df[column], format='%d:%m:%Y')
            except ValueError:
                errors.append(f"Column '{column}' has invalid datetime format. Expected format is 'dd:mm:yyyy'.")
        else:
            if dtype == 'string' and not pd.api.types.is_string_dtype(df[column]):
                errors.append(f"Column '{column}' has non-string values.")
            elif dtype == 'integer' and not pd.api.types.is_integer_dtype(df[column]):
                errors.append(f"Column '{column}' has non-integer values.")
            elif dtype == 'float' and not pd.api.types.is_float_dtype(df[column]):
                errors.append(f"Column '{column}' has non-float values.")
            elif dtype == 'boolean' and not pd.api.types.is_bool_dtype(df[column]):
                errors.append(f"Column '{column}' has non-boolean values.")

    return errors

df = pd.read_excel("sample_large_data.xlsx")
data_types = detect_data_types(df)
confirmed_data_types = user_confirmation(data_types)

print("\nFinal column data types:")
for column, dtype in confirmed_data_types.items():
    print(f"Column: {column}, Data type: {dtype}")

validation_errors = validate_data_types(df, confirmed_data_types)
if validation_errors:
    print("\nData Validation Errors:")
    for error in validation_errors:
        print(error)
else:
    print("No Errors")