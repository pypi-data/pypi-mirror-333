import threading
import time
import webbrowser
from functools import reduce
from typing import Any, Dict, List

import pandas as pd
import plotly.graph_objects as go
from dash import MATCH, Dash, Input, Output, State, dcc, html

from bayesnestor.reporting.ReportingContainers import (
    EReportOrigin,
    EReportScope,
    ReportEntry,
)
from bayesnestor.reporting.ReportingUtils import convert_nxgraph_to_plotly
from bayesnestor.utils.Utils import serialize_df


# Singleton
class ReportVisualizer:
    _instance = None
    _thread_handle = None
    _app = None
    _data_dict = None
    NO_CONTENT_MSG = "No content to display"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ReportVisualizer, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Helper function to set up the Singletons infrastructure."""
        self._app = Dash(__name__, prevent_initial_callbacks="initial_duplicate")
        print(">> Info: This feature is currently experimental - proceed with care.")
        print(
            ">> Info: BasicEntries are manually reduced to visualizing the graph only -- please consider installing graphviz."
        )

    def visualize(
        self, reported_results: List[ReportEntry], delay_mainproc: float = None
    ) -> None:
        """Main function used to visualize collected report results.
            Internally plotly is usesd as a dashboard. Due to it blocking the main process,
            threading is used. If execution if visualize(...) proceeds immediatly after (usually if a script is executed directly)
            using the dashboard is hard. To allow 'playing around' with the results an
            artifical time-out can be provided as part of the call.

        Args:
            reported_results (List[ReportEntry]): List of report results to visualize.
            delay_mainproc (float, optional): Sleep time for the main process until it progresses. Defaults to None.
        """
        self._prepare_reported_data(reported_results)

        if not self._thread_handle:
            self.build_dashboard()
            self.start_dashboard_thread()

        # Open the browser
        time.sleep(3)
        webbrowser.open("http://127.0.0.1:8050/")

        if delay_mainproc:
            time.sleep(delay_mainproc)

    def _prepare_reported_data(self, reported_results: List[ReportEntry]) -> None:
        """Internal helper function to pre-process provided report entries in "serialized"-dataformats compatible with plotly.

        Args:
            reported_results (List[ReportEntry]): List of report results to visualize
        """

        segregated_reports = {
            e: [res for res in reported_results if res.report_origin == e]
            for e in EReportOrigin
        }

        self._data_dict = {
            "tab_BasicReport": self._prepare_basic_reported_data(
                segregated_reports[EReportOrigin.BASIC_REPORTER]
            ),
            "tab_DoWhyReport": self._prepare_dowhy_reported_data(
                segregated_reports[EReportOrigin.DOWHY_REPORTER]
            ),
        }

    def _prepare_dowhy_reported_data(
        self, reported_results: List[ReportEntry]
    ) -> Dict[str, Any]:
        """Internal helper function to pre-process report results from the DoWhyReporter-class.

        Args:
            reported_results (List[ReportEntry]): List of report results to visualize.

        Returns:
            Dict[str, Any]: Pre-processed 'serialized' data to use with plotly.
        """
        primary_nodes = set(
            [
                entry.scoped_name
                for entry in reported_results
                if entry.scope == EReportScope.NODE_LEVEL
            ]
        )

        per_node_aggregated_data = dict.fromkeys(primary_nodes, {})

        for entry in reported_results:
            if entry.scope == EReportScope.NODE_LEVEL:
                per_node_aggregated_data.setdefault(entry.scoped_name, {})[
                    entry.metric
                ] = entry.data


        result = {}

        for primary_node in per_node_aggregated_data.keys():
            df_arr = [
                pd.DataFrame(data.items(), columns=["var", metric.name])
                for metric, data in per_node_aggregated_data[primary_node].items()
            ]
            df = reduce(
                lambda df1, df2: pd.merge(df1, df2, on="var", how="outer"), df_arr
            )
            result[primary_node] = serialize_df(df.round(4))

        return result

    def _prepare_basic_reported_data(
        self, reported_results: List[ReportEntry]
    ) -> Dict[str, Any]:
        """Internal helper function to pre-process report results from the BasicReporter-class.

        Args:
            reported_results (List[ReportEntry]): List of report results to visualize.

        Returns:
            Dict[str, Any]: Pre-processed 'serialized' data to use with plotly.
        """
        nx_graph_obj = [
            entry.data
            for entry in reported_results
            if entry.scope == EReportScope.NETWORK_LEVEL
        ][0]

        return {"Graph": convert_nxgraph_to_plotly(nx_graph_obj)}

    def build_dashboard(self):
        """Main logic to create the dashboard in a tab-like main layout.
        As a side-effect it currently also connect the callback handlers.

        """
        # Create the layout
        self._app.layout = html.Div(
            [
                html.H1("Pynestor result reporting"),
                dcc.Tabs(
                    id="tabs-container",
                    value="tab_BasicReport",
                    children=[
                        dcc.Tab(label="Basic Report", value="tab_BasicReport"),
                        dcc.Tab(label="DoWhy Report", value="tab_DoWhyReport"),
                    ],
                ),
                html.Div(id="tabs-content"),
                dcc.Store(id="store-df-dict", data=self._data_dict),
            ]
        )

        # Connect the callbacks
        self._app.callback(
            Output("tabs-content", "children", allow_duplicate=True),
            Input("tabs-container", "value"),
        )(self.render_content)

        self._app.callback(
            Output(
                {"type": "table-container", "index": MATCH},
                "children",
                allow_duplicate=True,
            ),
            Input({"type": "dropdown", "index": MATCH}, "value"),
            State({"type": "dropdown", "index": MATCH}, "id"),
            State("store-df-dict", "data"),
        )(self.update_table)

    def start_dashboard_thread(self):
        """Helper function to start the dasboard server in a seperate thread.
        Threading is used since starting a dash-server blocks its parent process.
        """
        if not self._thread_handle:
            self._thread_handle = threading.Thread(
                target=self._app.run, kwargs={"debug": True, "use_reloader": False}
            )
            self._thread_handle.start()

    def create_dropdown_tabular_div(
        self, tab_id: str, dataframe_names: List[str]
    ) -> html.Div:
        """Helper function to design the content of a tab.
           Here a dropdown menu is connected with a table that displays a selected dataframe.

        Args:
            tab_id (str): ID of the currently selected tab (with regard to the main dashboard layout)
            dataframe_names (List[str]): List of named dataframes that can be selected for presentation (managed with the global store / _data_dict property of this class)

        Returns:
            html.Div: Division-element.
        """
        options = (
            [{"label": name, "value": name} for name in dataframe_names]
            if dataframe_names
            else [{"label": self.NO_CONTENT_MSG, "value": self.NO_CONTENT_MSG}]
        )
        initial_selection = (
            dataframe_names[0] if dataframe_names else self.NO_CONTENT_MSG
        )
        return html.Div(
            [
                dcc.Dropdown(
                    id={"type": "dropdown", "index": tab_id},
                    options=options,
                    value=initial_selection,
                ),
                html.Div(id={"type": "table-container", "index": tab_id}),
            ]
        )

    def update_table(
        self, selected_df_name: str, dropdown_id: Dict, store_data: Dict
    ) -> dcc.Graph:
        """Callback-handler for displaying tabular content based on a selected DF via a dropdown.

        Args:
            selected_df_name (str): Name of the dropdown selection and therefore the name of the requested dataframe to be displayed.
            dropdown_id (Dict): ID of the triggering dropdown (accounting for multiple dropdowns in the dashboard)
            store_data (Dict): Global data storage that contains the requested dataframe.

        Returns:
            dcc.Graph: Displayable table with the requested data as content.
        """
        tab_id = dropdown_id["index"]
        df_dict = store_data[tab_id]
        df_records = df_dict.get(selected_df_name, None)
        df = pd.DataFrame(df_records) if df_records else pd.DataFrame()
        table = go.Figure(
            data=[
                go.Table(
                    header=dict(values=list(df.columns)),
                    cells=dict(values=[df[col] for col in df.columns]),
                )
            ]
        )
        return dcc.Graph(figure=table, responsive=True)

    def create_figure_div(self, data_dict: Dict[str, Any]) -> html.Div:
        """Helper function to design the content of a tab.
            Currently this is only used experimentally to display the underlying BN.

        Args:
            data_dict (Dict[str, Any]): Dictionary containing data that should be displayed.

        Returns:
            html.Div: Division-element.
        """
        go_fig = data_dict.get("Graph", None)
        if go_fig:
            return html.Div([dcc.Graph(figure=go_fig)])
        else:
            return html.Div([html.P(self.NO_CONTENT_MSG)])

    def render_content(self, tab: str) -> html.Div:
        """Callback-handler for creating tab-specific content to be displayed based on user selection in the main dashboard layout.

        Args:
            tab (str): User-selected tab that he wants to view.

        Returns:
            html.Div: Division-element.
        """
        if tab == "tab_BasicReport":
            return self.create_figure_div(self._data_dict["tab_BasicReport"])

        elif tab == "tab_DoWhyReport":
            return self.create_dropdown_tabular_div(
                tab, list(self._data_dict["tab_DoWhyReport"].keys())
            )
        else:
            return html.Div(self.NO_CONTENT_MSG)
