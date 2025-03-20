from typing import Any, Dict

import networkx as nx
import numpy as np
import plotly.graph_objects as go
from numpy.typing import ArrayLike
from tabulate import tabulate

from bayesnestor.utils.Utils import get_graph_layout_pos


def is_nested_dict(my_dict) -> bool:
    """Test if a dictionary is nested, i.e., it contains at least one dict as a value.

    Args:
        my_dict (Dict): Dictionary to test.

    Returns:
        bool: True if the provided dict is nested.
    """
    return any(isinstance(i, dict) for i in my_dict.values())


def print_dict(my_dict: Dict):
    """'Pretty' print flat a dictionary (one line per key-value pair).

    Args:
        my_dict (Dict): Dictionary to print.
    """
    for k, v in my_dict.items():
        print(f"{k} \t: {v}")


def print_dict_with_meta(
    printable_data: Any,
    preamble: str = None,
    postamble: str = None,
    nested_key_prefix: str = None,
):
    """'Pretty' print a (nested) dictionary with additional meta information.

    Args:
        printable_data (Any): (Nested) Dictionary to print.
        preamble (str, optional): Text that is printed once in advance of the provided dicts content. Defaults to None.
        postamble (str, optional): Text that is printed once after the provided dicts content. Defaults to None.
        nested_key_prefix (str, optional): Additional text that is printed before a top-level key in advance of the nested content of the respective value. Defaults to None.
    """

    if isinstance(preamble, str):
        print(preamble)

    if not is_nested_dict(printable_data):
        print_dict(printable_data)

    else:
        for key, sub_dict in printable_data.items():
            if isinstance(nested_key_prefix, str):
                print(f"{nested_key_prefix} {key}")
            print_dict_with_meta(
                sub_dict,
                preamble=None,
                postamble=None,
                nested_key_prefix=nested_key_prefix,
            )

    if isinstance(postamble, str):
        print(postamble)


def print_2d_table(
    table_data: ArrayLike, col_header: str = None, row_header: str = None
):
    """'Pretty' print a 2 dimensional array-like data.

    Args:
        table_data (ArrayLike): 2-Dimensional array-like data to print.
        col_header (str, optional): Adds column information to the data (lenght needs to match the respecitve data-shape). Defaults to None.
        row_header (str, optional): Adds preceding row information to the data (lenght needs to match the respecitve data-shape). Defaults to None.

    Raises:
        ValueError: Raised if data is not 2-Dimensional.
    """

    table_data = np.array(table_data, dtype=str)

    if not len(table_data.shape) == 2:
        raise ValueError(
            f"The provided data is not 2-Dimensional but has shape {table_data.shape}."
        )
    if row_header:
        row_header = (
            [row_header] * table_data.shape[0] - 1
            if isinstance(row_header, str)
            else row_header
        )

        table_data = np.append(
            np.array(row_header).reshape(table_data.shape[0], 1), table_data, axis=1
        )

    table = tabulate(
        table_data, headers=[""] + col_header, tablefmt="grid", stralign="center"
    )
    print(table)


def convert_nxgraph_to_plotly(nx_graph_obj: nx.DiGraph) -> go.Figure:
    """Convencience function to convert a networkX-DiGraph object to a plotly compatible figure object.

    Args:
        nx_graph_obj (nx.DiGraph): Graph to convert.

    Raises:
        ValueError: Raised if provided graph is not a DiGraph.

    Returns:
        go.Figure: Converted graph that is compatible to use with plotly and/or dash.
    """
    if not nx.is_directed_acyclic_graph(nx_graph_obj):
        raise ValueError(
            f"Provided graph-object is not a networkX-DiGraph but {type(nx_graph_obj)}."
        )

    pos = get_graph_layout_pos(nx_graph_obj)
    edges = [(u, v) for (u, v, d) in nx_graph_obj.edges(data=True)]

    annotate_edges = [
        dict(
            showarrow=True,
            arrowsize=1.0,
            arrowwidth=1.8,
            arrowhead=int(2),
            standoff=24,
            startstandoff=18,
            ax=pos[arrow[0]][0],
            ay=pos[arrow[0]][1],
            axref="x",
            ayref="y",
            x=pos[arrow[1]][0],
            y=pos[arrow[1]][1],
            xref="x",
            yref="y",
        )
        for arrow in edges
    ]

    # edges trace
    edge_x = []
    edge_y = []
    for edge in nx_graph_obj.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(color="black", width=1),
        hoverinfo="none",
        showlegend=False,
        mode="lines",
    )

    # nodes trace
    node_x = []
    node_y = []
    text = []
    for node in nx_graph_obj.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        text=text,
        mode="markers+text",
        showlegend=False,
        hoverinfo="none",
        marker=dict(
            color="pink",
            size=50,
            line=dict(color="black", width=1),
        ),
    )

    # layout of canvas
    layout = dict(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(t=10, b=10, l=10, r=10, pad=0),
        xaxis=dict(
            linecolor="black", showgrid=False, showticklabels=False, mirror=True
        ),
        yaxis=dict(
            linecolor="black", showgrid=False, showticklabels=False, mirror=True
        ),
        annotations=annotate_edges,
    )

    return go.Figure(data=[edge_trace, node_trace], layout=layout)
