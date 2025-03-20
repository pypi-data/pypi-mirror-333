from pathlib import Path
from typing import Any, List, Union

import networkx as nx
import pandas as pd


def merge_unique_lists(list1: List[Any], list2: List[Any]) -> List[Any]:
    """Merge two lists and return a new list containing only unique elements.

    Args:
        list1 (List[Any]): First list
        list2 (List[Any]): Second list

    Returns:
        List[Any]: List containing all unique elements of first and second list
    """
    seen = set()
    result = []
    for element in list1 + list2:
        if element not in seen:
            result.append(element)
            seen.add(element)
    return result


def check_file_type(file_path: Union[Path, str], valid_extensions: list) -> bool:
    """
    Check if a file at file_path exists and has one of the valid extensions.

    Parameters
    ----------
    file_path : Union[Path, str]
        File path to check.
    valid_extensions : list of str
        List of valid file extensions (e.g., ['.xml', '.txt', '.csv']).

    Returns
    -------
    bool
        True if the file exists and has one of the valid extensions, False otherwise.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        print(f"File '{file_path}' does not exist.")
        return False

    actual_extension = file_path.suffix.lower()
    for ext in valid_extensions:
        if actual_extension == ext.lower():
            return True

    print(f"File '{file_path}' has an invalid extension '{actual_extension}'.")
    return False


def serialize_df(dataframe: pd.DataFrame):
    if isinstance(dataframe, pd.DataFrame):
        return dataframe.to_dict("records")
    else:
        raise ValueError(
            f"Provided object needs to be a pandas-DataFrame instance but is of type ({type(dataframe)})"
        )


def get_graph_layout_pos(nx_graph_obj):
    pos = None

    try:

        pass

        pos = nx.nx_agraph.graphviz_layout(nx_graph_obj, prog="dot")

    except ImportError as err:
        print(
            f"ImportError: {str(err)}. \nTo support proper layout consider installing pygraphviz http://pygraphviz.github.io/"
        )

    return pos if pos is not None else nx.spring_layout(nx_graph_obj)
