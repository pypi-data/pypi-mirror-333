import json
from datetime import datetime
from typing import Any, Dict, Sequence, Tuple, Union
from urllib.parse import urljoin

from requests.models import Response
from tecton_core import http


def ingest(
    cluster_url: str,
    workspace: str,
    api_key: str,
    push_source_name: str,
    ingestion_records: Sequence[Dict[str, Any]],
    timeout_sec: float,
) -> Dict[str, Any]:
    if not cluster_url.startswith("https://preview."):
        cluster_url = cluster_url.replace("https://", "https://preview.")
    status_code, reason, response = IngestionClient(
        cluster_url=cluster_url, api_key=api_key
    ).ingest(
        workspace_name=workspace,
        push_source_name=push_source_name,
        ingestion_records=ingestion_records,
        timeout_sec=timeout_sec,
    )
    if status_code >= 500:
        raise Exception(json.dumps(response))
    elif status_code >= 400:
        raise Exception(
            json.dumps(dict(status_code=status_code, reason=reason, response=response))
        )
    else:
        return response


# TODO: This is a temporary solution until TectonClient is available
# This is modified version from tecton._internals.ingestion.IngestionClient
# The reason for this duplication:
# 1. The original class is inside tecton library, and dependency on tecton library is not necessary and causes problems
# 2. This logic should run both locally or inside a RTFV
# 3. This logic should be inside TectonClient, but it is not available now
# https://linear.app/tecton/issue/FE-2663/add-steam-ingest-api-support-to-python-http-client
class IngestionClient:
    def __init__(self, cluster_url: str, api_key: str):
        self.ingestion_url = urljoin(cluster_url, "ingest")
        self.api_key = api_key

    def ingest(
        self,
        workspace_name: str,
        push_source_name: str,
        ingestion_records: Sequence[Dict[str, Any]],
        timeout_sec: float,
        dry_run: bool = False,
    ) -> Tuple[int, str, Union[Dict[str, Any], None]]:
        http_request = {
            "workspace_name": workspace_name,
            "dry_run": dry_run,
            "records": {
                push_source_name: [
                    {
                        "record": self._serialize_record(ingestion_record),
                    }
                    for ingestion_record in ingestion_records
                ]
            },
        }
        response = http.session().post(
            self.ingestion_url,
            json=http_request,
            headers=self._prepare_headers(),
            timeout=timeout_sec,
        )
        return self._extract_from_response(response)

    @staticmethod
    def _extract_from_response(
        response: Response,
    ) -> Tuple[int, str, Union[Dict[str, Any], None]]:
        # NOTE: Responses not coming from our system will not necessarily be in JSON format

        if response.status_code != 200:
            error_message = f"Failed to ingest records: {response.reason}"
            try:
                response_data = response.json()
            except ValueError:
                response_data = None
                error_message += f"\nAdditionally, response content is not valid JSON: {response.text}"
            return response.status_code, error_message, response_data

        try:
            response_data = response.json()
        except ValueError:
            error_message = f"Response content is not valid JSON: {response.text}"
            return response.status_code, error_message, None
        return response.status_code, response.reason, response_data

    def _prepare_headers(self) -> Dict[str, str]:
        return {
            "authorization": f"Tecton-key {self.api_key}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _serialize_record(record: Dict[str, Any]) -> Dict[str, Any]:
        serialized_record = {}
        for k, v in record.items():
            if isinstance(v, datetime):
                serialized_record[k] = v.isoformat()
            else:
                serialized_record[k] = v
        return serialized_record
