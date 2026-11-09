# A user must never read, change or delete the rating of another user.
# Each attempt must be refused with a 4xx code, and the owner must still see
# the rating exactly as it was. The exact code of each attempt goes in RESULTS.md.


def assert_unchanged(api, auth, rating):
    res = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert res.status_code == 200
    assert res.json() == rating


# Another user cannot read my rating.
def test_other_user_cannot_read(api, auth, other_auth, rating):
    res = api.get(f"/api/ratings/{rating['id']}", headers=other_auth)
    print("read by other user:", res.status_code)
    assert 400 <= res.status_code <= 499
    assert_unchanged(api, auth, rating)


# Another user cannot change my rating.
def test_other_user_cannot_update(api, auth, other_auth, rating):
    res = api.put(
        f"/api/ratings/{rating['id']}", json={"stars": 1}, headers=other_auth
    )
    print("update by other user:", res.status_code)
    assert 400 <= res.status_code <= 499
    assert_unchanged(api, auth, rating)


# Another user cannot delete my rating.
def test_other_user_cannot_delete(api, auth, other_auth, rating):
    res = api.delete(f"/api/ratings/{rating['id']}", headers=other_auth)
    print("delete by other user:", res.status_code)
    assert 400 <= res.status_code <= 499
    assert_unchanged(api, auth, rating)
