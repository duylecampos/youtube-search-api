import pytest
from app.services.youtube.respositories import Youtube


@pytest.mark.parametrize(
    "input,expected",
    [
        (80, [50, 30]),
        (10, [10]),
        (150, [50, 50, 50]),
        (168, [50, 50, 50, 18]),
        (0, []),
    ],
)
def test__page_generator(input, expected):
    repo = Youtube()
    output = list(repo._page_generator(input))
    assert output == expected


@pytest.mark.parametrize(
    "max_results", [3, 55, 200],
)
def test_search(max_results):
    repo = Youtube()
    output = list(repo.search("biscoito", max_results))
    assert len(output) == max_results
