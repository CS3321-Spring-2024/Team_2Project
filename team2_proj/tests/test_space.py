import pytest
from team2_proj.POTD import get_potd, validate_date
from unittest.mock import patch
from team2_proj.space import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    client =  app.test_client()
    yield client


@pytest.mark.asyncio
async def test_index(client):
    response = await client.get('/')
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'

@pytest.mark.asyncio
async def test_POTD(client):
    response = await client.get('/POTD')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    j = await response.json
    assert j["Query"] == "Get More context from Wikipedia."


@pytest.mark.asyncio
async def test_pastPOTD(client):
    response = await client.get('/pastPOTD/2021-11-29')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    j = await response.json
    assert j["Query"] == "Get More context from Wikipedia."


@pytest.mark.asyncio
@patch('team2_proj.POTD.validate_date', return_value=False)
async def test_wrong_date_format(mock_validate_date, client):
    response = await client.get('/pastPOTD/2021-11-29')
    response2 = await client.get('/POTD')
    assert response.status_code == 200
    j1 = await response.json
    j2 = await response2.json
    assert j1 == j2



