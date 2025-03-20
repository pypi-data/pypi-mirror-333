#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#
import pytest

from snowflake.core._root import Root


API_NOT_ENABLED = "Cortex Embed API is not enabled"


@pytest.fixture(autouse=True)
def precheck_cortex_embed_enabled(cortex_embed_service):
    try:
        cortex_embed_service.embed("e5-base-v2", ["foo", "bar"])
    except Exception as err:
        if API_NOT_ENABLED in err.body:
            pytest.xfail(API_NOT_ENABLED)
        raise


# Test embed through CortexEmbedService
# TODO(SNOW-1895432): Please remove these fixtures to disable in Notebook and StoredProcedure once this is fixed
@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_embed(root: Root):
    resp = root.cortex_embed_service.embed(
        "e5-base-v2",
        ["foo", "bar"],
    )

    assert len(resp.data) == 2
    assert resp.model == "e5-base-v2"
    assert resp.usage.total_tokens >= 0
