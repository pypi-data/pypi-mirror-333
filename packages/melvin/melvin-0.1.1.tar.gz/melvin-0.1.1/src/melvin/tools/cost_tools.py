from typing import Optional

import pandas as pd
import snowflake.connector
from utils import _err, _log_with_details, store_object


class SnowflakeCostQueryTool:
    def __init__(self):
        self.connection = None

    def connect(self, user: str):
        self.connection = self.connection or snowflake.connector.connect(
            account="hza50686",
            user=user,
            warehouse="ANALYST_WAREHOUSE",
            database="DATAMART_PROD",
            schema="CONSUMPTION",
            authenticator="externalbrowser",  # Uses Okta login
        )

    def build_query(
        self,
        account_name: Optional[str],
        timestamp_start: Optional[str],
        timestamp_end: Optional[str],
    ) -> str:
        """
        Build the SQL query based on the input filters and groupings.
        """
        base_query = """
        SELECT
            ACCOUNT_NAME,
            UNIT,
            SUM(QUANTITY) AS QUANTITY,
            COALESCE(metadata:instance_type::string, 'Unknown') AS Instance_Type,
            COALESCE(metadata:job_type::string, 'Unknown') AS Job_Type,
            COALESCE(metadata:tecton_object_name::string, 'Unknown') AS FV_Name,
            COALESCE(metadata:workspace::string, 'Unknown') AS Workspace,
            TO_CHAR(TIMESTAMP, 'YYYY-MM-DD') AS TIMESTAMP,
            BASE_TECTON_CREDITS_PER_UNIT,
            SUM(QUANTITY) * BASE_TECTON_CREDITS_PER_UNIT AS TOTAL_TECTON_CREDITS
        FROM
            COMBINED_CONSUMPTION_METRICS_WITH_CREDITS_V2
        """

        # Add WHERE clause for filters
        where_clauses = []
        if account_name:
            where_clauses.append(f"ACCOUNT_NAME = '{account_name}'")
        if timestamp_start and timestamp_end:
            where_clauses.append(
                f"TIMESTAMP >= '{timestamp_start}' AND TIMESTAMP < '{timestamp_end}'"
            )

        if where_clauses:
            base_query += "WHERE " + " AND ".join(where_clauses) + " "

        # Add GROUP BY clause
        group_by_fields = [
            "ACCOUNT_NAME",
            "Workspace",
            "UNIT",
            "FV_Name",
            "Job_Type",
            "Instance_Type",
            "TO_CHAR(TIMESTAMP, 'YYYY-MM-DD')",
            "BASE_TECTON_CREDITS_PER_UNIT",
        ]

        base_query += "GROUP BY " + ", ".join(group_by_fields) + " "

        # Add ORDER BY clause
        base_query += "ORDER BY TIMESTAMP, UNIT, QUANTITY DESC"

        return base_query

    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute the SQL query and fetch results.
        """
        cursor = self.connection.cursor()
        try:
            _log_with_details(":question: Fetching cost information", f"```sql {query}")

            cursor.execute(query)
            df = cursor.fetch_pandas_all()
            df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"]).astype("datetime64[us]")
            return df
        finally:
            cursor.close()

    def query_cost_data(
        self,
        user: str,
        account_name: str,
        timestamp_start: Optional[str] = None,
        timestamp_end: Optional[str] = None,
    ) -> str:
        """
        Query Tecton cost data. This is a dataframe generator.

        Parameters:
        - user: The full email address of the currently logged in user
        - account_name: The name of the currently logged into Tecton account to filter by (e.g., "tecton-staging").
        - timestamp_start: Start of the timestamp range (e.g., "2024-05-01").
        - timestamp_end: End of the timestamp range

        Returns:
            - str: A session object key of the cost data or an error message

        Note:

        - The output columns are TIMESTAMP, INSTANCE_TYPE, JOB_TYPE, FV_NAME, WORKSPACE, TOTAL_TECTON_CREDITS
        """
        if not timestamp_start or not timestamp_end:
            return _err("Both timestamp_start and timestamp_end must be provided.")

        try:
            self.connect(user)

            query = self.build_query(
                account_name=account_name,
                timestamp_start=timestamp_start,
                timestamp_end=timestamp_end,
            )
            df = self.execute_query(query)[
                [
                    "TIMESTAMP",
                    "INSTANCE_TYPE",
                    "JOB_TYPE",
                    "FV_NAME",
                    "WORKSPACE",
                    "TOTAL_TECTON_CREDITS",
                ]
            ]
            description = """
Schema of the cost table: (format: name (type): description)

TIMESTAMP (timestamp): timestamp of the job
INSTANCE_TYPE (string): cloud instance type
JOB_TYPE (string): job type
WORKSPACE (string): workspace name
FV_NAME (string): feature view name
TOTAL_TECTON_CREDITS (float): total credits consumed by the job
"""
            return store_object({"df": df, "description": description}, "df")
        except Exception as e:
            return _err(e)
