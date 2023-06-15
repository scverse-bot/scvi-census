from typing import Any, Literal, Optional, Union

import cellxgene_census
from somacore import AxisQuery


class Query:
    def __init__(
        self,
        query_name: str,
        organism: Literal["homo_sapiens", "mus_musculus"] = "homo_sapiens",
        measurement_name: Literal["RNA"] = "RNA",
        layer: Literal["raw"] = "raw",
        batch_key: str | None = None,
        labels_key: str | None = None,
        size_factor_key: str | None = None,
        categorical_covariate_keys: Optional[list[str]] = None,
        continuous_covariate_keys: Optional[list[str]] = None,
        obs_filter: Union[str, AxisQuery] = None,
        var_filter: Union[str, AxisQuery] = None,
        census_version: str | None = None,
    ):
        self._query_name = query_name
        self._organism = organism
        self._measurement_name = measurement_name
        self._layer = layer
        self._batch_key = batch_key
        self._labels_key = labels_key
        self._size_factor_key = size_factor_key
        self._categorical_covariate_keys = categorical_covariate_keys
        self._continuous_covariate_keys = continuous_covariate_keys
        self._obs_filter = obs_filter
        self._var_filter = var_filter
        self._census_version = census_version

        self.compute_summary_stats()

    def compute_summary_stats(self):
        census = cellxgene_census.open_soma()["census_data"][self._organism]

        self.n_obs = len(census.obs.read(value_filter=self._obs_filter).concat())
        self.n_vars = len(census.ms[self._measurement_name].var.read(value_filter=self._var_filter).concat())
        self.n_batch = 1
        self.n_labels = 1
        self.n_extra_continuous_covs = 0

    def get(self, key: str, default: Any = None):
        return getattr(self, key, default)
