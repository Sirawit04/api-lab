import pytest

# The rating fixture starts with 3 stars. 0 and 6 are just outside the rule
# of 1 to 5 stars, 1 and 5 are the two edges that the rule still accepts.
ORIGINAL_STARS = 3


# Boundary values: 1 and 5 are saved, 0 and 6 are refused and change nothing.
@pytest.mark.parametrize(
    "stars, expected_status",
    [(0, 400), (1, 200), (5, 200), (6, 400)],
)
def test_update_boundaries(api, auth, rating, stars, expected_status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == expected_status

    saved = api.get(path, headers=auth)
    assert saved.status_code == 200
    expected_stars = stars if expected_status == 200 else ORIGINAL_STARS
    assert saved.json()["stars"] == expected_stars
