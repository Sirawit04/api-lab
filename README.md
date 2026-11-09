# api-lab

API tests for QuickPizza (https://quickpizza.grafana.com) with pytest and requests.
ITCS386 Software Verification and Validation, API testing lab.

## Install and run

```
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -v
pytest -v --html=report.html --self-contained-html
```

Every test creates its own user (lab-<random>) and its own data, so the tests do
not depend on each other and never touch the shared ratings of the public token.
A full run sends about 140 requests, so do not run it in a loop.

## Input domain model for POST /api/ratings (Step A1)

Base choice coverage: one base block per characteristic, then each test changes
one characteristic to one other block. 1 + 2 + 3 + 1 + 2 = 9 tests.

| Characteristic | Block | Value in the test | Covered by |
|---|---|---|---|
| C1 Value of stars | 1 to 5 (base) | 3 | test_base_choice_is_saved |
| C1 Value of stars | below 1 | 0 | test_stars_out_of_range[0] |
| C1 Value of stars | above 5 | 6 | test_stars_out_of_range[6] |
| C2 Type of stars | whole number (base) | 3 | test_base_choice_is_saved |
| C2 Type of stars | decimal | 3.5 | test_stars_decimal |
| C2 Type of stars | text | "3" | test_stars_text |
| C2 Type of stars | missing | no field | test_stars_missing |
| C3 Pizza | exists (base) | a new pizza | test_base_choice_is_saved |
| C3 Pizza | does not exist | 999999999 | test_pizza_does_not_exist |
| C4 Token | the user's own (base) | from auth | test_base_choice_is_saved |
| C4 Token | none | no header | test_no_token |
| C4 Token | wrong length | token short | test_token_wrong_length |

The blocks of one characteristic do not overlap and together cover every value.
Boundary values for the stars rule (0, 1, 5, 6) are tested for updates in
test_update_rating.py.
