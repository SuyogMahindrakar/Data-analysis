import pandas as pd


def load_dataframe(uploaded_file):
    """
    Load CSV or Excel into a Pandas DataFrame.
    """

    filename = uploaded_file.name.lower()

    if filename.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    elif filename.endswith(".xlsx") or filename.endswith(".xls"):
        return pd.read_excel(uploaded_file)

    else:
        raise ValueError("Unsupported file format.")


def get_dataframe_info(df):
    """
    Create dataset summary for the AI prompt.
    """

    info = f"""
Dataset Summary
---------------

Rows: {len(df)}
Columns: {len(df.columns)}

Column Names:
{list(df.columns)}

Data Types:
{df.dtypes.to_string()}

Missing Values:
{df.isnull().sum().to_string()}

First 5 Rows:
{df.head().to_string(index=False)}

Descriptive Statistics:
{df.describe(include='all').fillna('').to_string()}
"""

    return info


def detect_numeric_columns(df):
    """
    Return numeric columns.
    """

    return df.select_dtypes(include="number").columns.tolist()


def detect_categorical_columns(df):
    """
    Return categorical columns.
    """

    return df.select_dtypes(exclude="number").columns.tolist()


def dataframe_summary(df):
    """
    Return quick statistics for UI.
    """

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isna().sum().sum()),
        "numeric_columns": detect_numeric_columns(df),
        "categorical_columns": detect_categorical_columns(df),
    }


def sample_data(df, rows=10):
    """
    Return sample rows for prompt.
    """

    return df.head(rows).to_string(index=False)


def get_column_list(df):
    """
    Return list of columns.
    """

    return df.columns.tolist()


def get_shape(df):
    """
    Return DataFrame shape.
    """

    return df.shape