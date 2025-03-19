from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

import pymongo
import requests

from module_qc_database_tools.db.local import (
    get_component,
    get_qc_result,
    get_qc_status,
)


def recycle_component(
    db: pymongo.database.Database, serial_number: str, *, localdb_uri: str
) -> (bool, dict[str, (bool, dict[str, int])]):
    """
    Recycle all E-SUMMARY across all stages for given component

    Args:
        db (:obj:`pymongo.database.Database`): The database instance for localDB to retrieve information from.
        serial_number (:obj:`str`): the serial number of the component.
        localdb_uri (:obj:`str`): the localDB URI to use for triggering analysis recycling

    Returns:
        success (:obj:`bool`): success or failure for recycling all the E-SUMMARIES
        statuses (:obj:`dict`): dictionary of status for recycling each stage's E-SUMMARY (see :func:`recycle_e_summary`)
    """
    component, _ = get_component(db, serial_number)
    mod_status = get_qc_status(db, component)

    statuses = {}
    for stage, results in mod_status["QC_results"].items():
        e_summary = get_qc_result(db, results["E_SUMMARY"])
        statuses[stage] = recycle_e_summary(e_summary, localdb_uri=localdb_uri)

    return (all(status[0] for status in statuses), statuses)


def recycle_e_summary(
    e_summary: dict[str, Any], *, localdb_uri: str
) -> (bool, dict[str, int]):
    """
    Recycle a given e-summary.

    Args:
        e_summary (:obj:`dict`): the e-summary to recycle
        localdb_uri (:obj:`str`): the localDB URI to use for triggering analysis recycling

    Returns:
        success (:obj:`bool`): success or failure for recycling all the tests
        statuses (:obj:`dict`): dictionary of status for recycling each test
    """

    statuses = {}
    for key, link in e_summary["results"].items():
        if link == 0:
            continue
        if not isinstance(link, str):
            continue
        statuses[key] = recycle_analysis(link, localdb_uri=localdb_uri)

    return (all(status == 200 for status in statuses), statuses)


def recycle_analysis(test_run_id: str | int, *, localdb_uri: str) -> int:
    """
    Recycle a given analysis using it's specific identifier.

    Args:
        test_run_id (:obj:`str`): the identifier of the test run to recycle
        localdb_uri (:obj:`str`): the localDB URI to use for triggering analysis recycling

    Returns:
        status_code (:obj:`int`): the status code of the recycle analysis request

    """
    return requests.post(
        urljoin(localdb_uri, "recycle_analysis"),
        data={"test_run_id": test_run_id},
        timeout=120,
    ).status_code
