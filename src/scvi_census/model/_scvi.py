import logging
from typing import Literal, Optional, Union

import numpy as np
from anndata import AnnData
from scvi.model import SCVI as _SCVI
from somacore import AxisQuery

from scvi_census.data import Query

logger = logging.getLogger(__name__)


class SCVI(_SCVI):
    def __init__(self, query_name: str, *args, **kwargs):
        query = self._query_store[query_name]
        self._summary_stats = query

        super().__init__(self._dummy_adata_store[query_name], *args, **kwargs)

    @classmethod
    def _get_dummy_adata(
        cls,
        layer: Literal["raw"] = "raw",
        batch_key: str | None = None,
        labels_key: str | None = None,
        size_factor_key: str | None = None,
        categorical_covariate_keys: Optional[list[str]] = None,
        continuous_covariate_keys: Optional[list[str]] = None,
    ) -> AnnData:
        adata = AnnData(np.ones((1, 1), dtype=np.float32))
        if layer is not None:
            adata.layers[layer] = np.ones((1, 1), dtype=np.float32)
        if batch_key is not None:
            adata.obs[batch_key] = "batch"
        if labels_key is not None:
            adata.obs[labels_key] = "label"
        if size_factor_key is not None:
            adata.obs[size_factor_key] = 1.0
        if categorical_covariate_keys is not None:
            for key in categorical_covariate_keys:
                adata.obs[key] = "covariate"
        if continuous_covariate_keys is not None:
            for key in continuous_covariate_keys:
                adata.obs[key] = 1.0
        return adata

    @property
    def summary_stats(self):
        return self._summary_stats

    @summary_stats.setter
    def summary_stats(self, value):
        pass

    @classmethod
    def setup_query(
        cls,
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
        """Sets up the data for this model."""
        if not hasattr(cls, "_query_store"):
            cls._query_store = {}
        if not hasattr(cls, "_dummy_adata_store"):
            cls._dummy_adata_store = {}

        query = Query(
            query_name=query_name,
            organism=organism,
            measurement_name=measurement_name,
            layer=layer,
            batch_key=batch_key,
            labels_key=labels_key,
            size_factor_key=size_factor_key,
            categorical_covariate_keys=categorical_covariate_keys,
            continuous_covariate_keys=continuous_covariate_keys,
            obs_filter=obs_filter,
            var_filter=var_filter,
            census_version=census_version,
        )
        cls._query_store[query_name] = query
        logger.info(f"Query {query_name} set up with {query.n_obs} obsevations and " f"{query.n_vars} variables.")

        dummy_adata = cls._get_dummy_adata()
        cls._dummy_adata_store[query_name] = dummy_adata
        cls.setup_anndata(dummy_adata)
