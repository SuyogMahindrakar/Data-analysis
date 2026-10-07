import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def execute_python_code(code, df):
    """
    Execute AI-generated Python code.

    Expected:
        result -> mandatory
        fig    -> optional (matplotlib figure)

    Returns:
        {
            "success": bool,
            "result": object,
            "figure": matplotlib figure or None,
            "error": error message or None
        }
    """

    local_vars = {
        "df": df.copy(),
        "pd": pd,
        "np": np,
        "plt": plt,
        "result": None,
        "fig": None,
    }

    try:

        exec(code, {}, local_vars)

        return {
            "success": True,
            "result": local_vars.get("result"),
            "figure": local_vars.get("fig"),
            "error": None,
        }

    except Exception as ex:

        return {
            "success": False,
            "result": None,
            "figure": None,
            "error": str(ex),
        }


def is_dataframe(obj):
    return isinstance(obj, pd.DataFrame)


def is_series(obj):
    return isinstance(obj, pd.Series)


def is_scalar(obj):
    return isinstance(
        obj,
        (
            int,
            float,
            str,
            bool,
            np.integer,
            np.floating,
        ),
    )


def format_result(result_dict):
    """
    Convert execution result into something Streamlit can display.
    """

    if not result_dict["success"]:

        return {
            "text": f"❌ {result_dict['error']}",
            "table": None,
            "chart": None,
        }

    result = result_dict["result"]

    chart = result_dict["figure"]

    if result is None:

        text = "Code executed successfully."

    elif is_scalar(result):

        text = str(result)

    elif is_series(result):

        text = ""
        result = result.reset_index()

    elif is_dataframe(result):

        text = ""

    else:

        text = str(result)

    return {
        "text": text,
        "table": result if isinstance(result, (pd.DataFrame, pd.Series)) else None,
        "chart": chart,
    }