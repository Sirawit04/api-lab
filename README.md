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

## Input domain model for POST /api/ratings (Step A1)

| Characteristic | Blocks | Values in the tests |
|---|---|---|
| C1 Value of stars | below 1, 1 to 5 (base), above 5 | 0, 3, 6 |
| C2 Type of stars | whole number (base), decimal, text, missing | 3, 3.5, "3", no field |
| C3 Pizza | exists (base), does not exist | a new pizza, 999999999 |
| C4 Token | the user's own (base), none, wrong length | from auth, no header, token short |
