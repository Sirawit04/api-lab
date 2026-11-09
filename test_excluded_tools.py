import pytest


# The pizza never needs a tool that the customer excluded.
# Blocks of "how many of the three tools are excluded": 0, 1, 2 (3 is below).
@pytest.mark.parametrize(
    "excluded",
    [
        ["Knife"],                 # block: 1 excluded
        ["Scissors"],              # block: 1 excluded
        [],                        # block: 0 excluded
        ["Knife", "Pizza cutter"], # block: 2 excluded
    ],
)
def test_excluded_tool_is_not_used(api, auth, excluded):
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


# Defect 1: when all three tools are excluded no pizza can be cut. The product
# owner wants a 400 with a JSON error message, never a 500.
@pytest.mark.xfail(
    reason="Defect 1: excluding all three tools makes QuickPizza answer 500 "
    "with an empty body instead of 400 with a JSON error message",
    strict=True,
)
def test_all_tools_excluded_is_refused_with_400(api, auth):
    body = {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()
