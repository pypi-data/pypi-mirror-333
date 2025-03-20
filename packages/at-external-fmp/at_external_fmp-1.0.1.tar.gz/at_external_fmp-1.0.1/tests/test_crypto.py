import pytest
from at_external_fmp.crypto import *

@pytest.mark.asyncio
async def test_cryptocurrency_list():
    result = await cryptocurrency_list()
    assert result is not None and len(result) > 0