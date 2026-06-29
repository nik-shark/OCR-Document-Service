from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from services.get_text import get_recognized_text


@pytest.mark.anyio
async def test_get_recognized_text_success():
    db = AsyncMock(spec=AsyncSession)

    recognized_text = Mock()

    document = Mock()
    document.text = recognized_text

    query_result = Mock()
    query_result.scalar_one_or_none.return_value = document

    db.execute.return_value = query_result

    result = await get_recognized_text(
        item_id=1,
        db=db,
    )

    assert result is recognized_text

    db.execute.assert_awaited_once()
    query_result.scalar_one_or_none.assert_called_once_with()


@pytest.mark.anyio
async def test_get_recognized_text_not_found():
    db = AsyncMock(spec=AsyncSession)

    query_result = Mock()
    query_result.scalar_one_or_none.return_value = None

    db.execute.return_value = query_result

    with pytest.raises(HTTPException) as exc:
        await get_recognized_text(
            item_id=999_999_999,
            db=db,
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Text not found"

    db.execute.assert_awaited_once()
    query_result.scalar_one_or_none.assert_called_once_with()