import logging

import pandas as pd
from attr import define
import json

log = logging.getLogger(__name__)

from juice_core_uplink_api_client.api.rest_api import (
    rest_api_plan_list,
    rest_api_plan_read,
    rest_api_trajectory_engineering_segments_list,
    rest_api_trajectory_series_list,
    rest_api_series_list
)
from juice_core_uplink_api_client.client import Client


def convert_times(table, columns=["start", "end"]):
    for c in columns:
        table[c] = pd.to_datetime(table[c]).dt.tz_localize(None)

    return table


@define(auto_attribs=True)
class SHTRestInterface:
    """
    Main entry point for interacting with the Juice Core Uplink API
    """

    client: [None, Client] = None
    timeout: float = 40.0

    def __attrs_post_init__(self):
        if not self.client:
            self.client = Client("https://juicesoc.esac.esa.int")
        self.client.timeout = self.timeout

    @property
    def plans(self):
        """Retrieve all the plans available on the endpoint"""
        return rest_api_plan_list.sync(client=self.client)

    @property
    def plans_dt(self):
        """Retrieve all the plans available on the endpoint as a pandas DataFrame"""
        plans = self.plans
        plans = pd.DataFrame([p.to_dict() for p in plans])
        return convert_times(plans, columns=["created"])

    def plan_id_by_name(self, name):
        """Retrieve the plan id from the plane name"""
        for plan in self.plans:
            if plan.name.lower().strip() == name.lower().strip():
                log.debug(f"Plan {name} has id {plan.id}")
                return plan.id

        log.warning(f"No plan with name {name} found")
        return None

    def plan_segments_dt(self, plan_id_or_name):
        """Retrieve the segments of a plan"""
        plan = self.plan(plan_id_or_name)
        segments = pd.DataFrame(plan.segments)
        return convert_times(segments)

    def engineering_segments(self, mnemonic="CREMA_5_0") -> pd.DataFrame:
        """Retrieve the engineering segments for a mnemonic"""
        eng_segments = rest_api_trajectory_engineering_segments_list.sync(
            mnemonic, client=self.client)
        eng_segments = pd.DataFrame([e.to_dict() for e in eng_segments])
        return convert_times(eng_segments)

    def plan(self, plan_id_or_name):
        """Retrieve the plan from the plan id or name"""
        if isinstance(plan_id_or_name, str):
            plan_id_or_name = self.plan_id_by_name(plan_id_or_name)
        return rest_api_plan_read.sync(plan_id_or_name, client=self.client)

    def trajectory_series(self, mnemonic="CREMA_5_0"):
        """Retrieve all the series available on the endpoint"""
        return rest_api_trajectory_series_list.sync(client=self.client,
                                                    mnemonic=mnemonic)

    def trajectory_series_dt(self, mnemonic="CREMA_5_0"):
        """Retrieve all the series available on the endpoint as a pandas DataFrame"""
        series = self.trajectory_series(mnemonic=mnemonic)
        series = pd.DataFrame([s.to_dict() for s in series])
        return series

    def get_serie(self, start, end, series_name, mnemonic="CREMA_5_0"):
        """Retrieve a serie from the endpoint"""

        q = dict(start=str(start), end=str(end),
                 trajectory=mnemonic, series=series_name)

        body = json.dumps(q)
        return rest_api_series_list.sync(client=self.client, body=body)

    def get_serie_dt(self, start, end, series_name, mnemonic="CREMA_5_0"):
        """Retrieve a serie from the endpoint as a pandas DataFrame"""
        serie = self.get_serie(start, end, series_name, mnemonic=mnemonic)
        serie = pd.DataFrame([s.to_dict() for s in serie])
        return convert_times(serie, ["epoch"])