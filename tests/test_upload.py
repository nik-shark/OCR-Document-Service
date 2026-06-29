import pytest
from pathlib import Path

TEST_FILES_DIR = Path(__file__).resolve().parent / 'test_files'

@pytest.mark.anyio
async def test_success_upload_img(client):
    image_path = TEST_FILES_DIR / 'first_img.jpg'

    with image_path.open("rb") as image:
        response = await client.post(
            '/api/upload',
            files={
                'file': (
                    image_path.name,
                    image,
                    'image/jpeg',
                )
            },
        )

    assert response.status_code == 201


@pytest.mark.anyio
async def test_error_upload_img(client):
    image_path = TEST_FILES_DIR / 'second_img.gif'

    with image_path.open("rb") as image:
        response = await client.post(
            '/api/upload',
            files={
                'file': (
                    image_path.name,
                    image,
                    'gif/gif',
                )
            },
        )

    assert response.status_code == 400

