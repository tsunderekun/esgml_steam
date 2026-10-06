"""
ESGML SDK - Steam Workshop Item Status Checker
Uses official public Steam Web API (ISteamRemoteStorage/GetPublishedFileDetails).
Supports batch queries (up to 100 items per single HTTP request) with zero API key required.
Zero external dependencies.
"""

import urllib.request
import urllib.parse
import json
import time
from typing import Dict, List, Optional


class SteamWorkshopChecker:
    """Checks the status of Steam Workshop items via official Steam Web API."""

    API_URL = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
    USER_AGENT = "ESGML-SDK/4.1 (Steam Workshop Analyzer)"

    # Steam EResult enum values
    # 1: k_EResultOK
    # 9: k_EResultFileNotFound (deleted)
    # 15: k_EResultAccessDenied (banned / hidden)
    # 16: k_EResultTimeout

    @classmethod
    def check_item(cls, workshop_id: str, timeout: int = 10) -> Dict[str, any]:
        """Check status of a single workshop item."""
        batch_results = cls.check_batch([workshop_id], timeout=timeout)
        if str(workshop_id) in batch_results:
            return batch_results[str(workshop_id)]
        return {
            "id": str(workshop_id),
            "status": "ERROR",
            "title": None,
            "error": "No response for ID"
        }

    @classmethod
    def check_batch(cls, workshop_ids: List[str], timeout: int = 15) -> Dict[str, Dict[str, any]]:
        """
        Check status of up to 100 workshop items in a single fast HTTP request.
        Returns: { id: { "id": str, "status": "ACTIVE" | "DELETED" | "BANNED" | "ERROR", "title": str, ... } }
        """
        results = {}
        if not workshop_ids:
            return results

        # Deduplicate and format IDs
        clean_ids = [str(x).strip() for x in workshop_ids if str(x).strip().isdigit()]
        if not clean_ids:
            return results

        post_data = {"itemcount": len(clean_ids)}
        for idx, item_id in enumerate(clean_ids):
            post_data[f"publishedfileids[{idx}]"] = item_id

        encoded_data = urllib.parse.urlencode(post_data).encode("utf-8")
        req = urllib.request.Request(
            cls.API_URL,
            data=encoded_data,
            headers={
                "User-Agent": cls.USER_AGENT,
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                resp_json = json.loads(response.read().decode("utf-8"))
                items = resp_json.get("response", {}).get("publishedfiledetails", [])

                for item in items:
                    fid = str(item.get("publishedfileid"))
                    result_code = item.get("result", 9)
                    title = item.get("title")

                    if result_code == 1:
                        status = "ACTIVE"
                        err = None
                    elif result_code == 9:
                        status = "DELETED"
                        err = "Удалён из мастерской (k_EResultFileNotFound)"
                    elif result_code == 15:
                        status = "BANNED"
                        err = "Заблокирован или скрыт (k_EResultAccessDenied)"
                    else:
                        status = "DELETED" if not title else "UNKNOWN"
                        err = f"EResult code: {result_code}"

                    results[fid] = {
                        "id": fid,
                        "status": status,
                        "result_code": result_code,
                        "title": title,
                        "creator": item.get("creator"),
                        "subscriptions": item.get("subscriptions", 0),
                        "views": item.get("views", 0),
                        "file_size": item.get("file_size", 0),
                        "error": err
                    }

        except Exception as e:
            for fid in clean_ids:
                results[fid] = {
                    "id": fid,
                    "status": "ERROR",
                    "title": None,
                    "error": str(e)
                }

        return results
