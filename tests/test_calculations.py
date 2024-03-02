import pytest
from app.calculations import add
from fastapi.testclient import TestClient
from fastapi import FastAPI

app = FastAPI()

client = TestClient(app)


@pytest.fixture
def zero_num():
    return 0


# !!! the function must starts with test_ ....
@pytest.mark.parametrize("num1, num2, expected", [(3, 2, 5), (7, 1, 8), (12, 4, 16)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


# references zero fixture
@pytest.mark.parametrize("num1, expected", [(3, 3), (7, 7), (12, 12)])
def test_add(num1, expected, zero_num):
    assert add(num1, zero_num) == expected


# test exception
# def test_exception_expected():
#     with pytest.raises(Exception):
#         # my fun that raises exception
#         pass
