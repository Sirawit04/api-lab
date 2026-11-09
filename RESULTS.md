# API lab results

## Part 0

- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401 (body {"error":"authentication failed"})
- Step 0.4, the name of your pizza: The Mighty Romana (every ingredient has "vegetarian":true)
- Step 0.12, results of the three runs without a session (optional): skipped
- Step 0.16, blocks of "how many of the three tools are excluded":
  - 0 tools excluded (covered by `[]`)
  - 1 tool excluded (covered by `["Knife"]` and `["Scissors"]`)
  - 2 tools excluded (covered by `["Knife", "Pizza cutter"]`)
  - 3 tools excluded (no tool left; this block gave the 500, so it has its own xfail test test_all_tools_excluded_is_refused_with_400)

## Defect report

- Title: Defect 1, excluding all three tools makes POST /api/pizza answer 500 with an empty body
- Request: POST /api/pizza with header Authorization: token <token> and body {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]} (file all_tools_excluded.json)
- Expected result: status 400 and a JSON body with an error message, because no pizza can be cut without a tool
- Actual result: status 500 and an empty body (0 bytes), seen with curl and with the test
- Severity: Medium. A customer can really send this input, the server fails instead of refusing it, and the caller gets no message to show or log. No data is lost.

## Part A

- Step A4, status codes when the other user reads, changes and deletes: read 404 ({"error":"not found"}), change 400 ({"error":"rating ID ... not found"}), delete 400 ({"error":"rating ID ... not found"}). The owner read the rating back with 200 and it was unchanged.

## Part B

1. Two failures that tests against the real server find and a unit test with stubs cannot: (a) the load balancer sends a request to a server that does not know the user, so a login fails at random; (b) the real server breaks on an input that a stub never produced, such as the 500 in Step 0.16, or answers with a different status code or message than the code expects. A unit test with stubs is still worth writing because it runs in milliseconds, needs no network, never fails because of the shared server, and points to the exact function that is wrong.
2. Ratings made with the public token belong to everyone, so another student could change or delete them while my test runs and my test would fail for a reason that has nothing to do with my code. A new user per test gives each test data that only it can touch, so tests are independent and can run in any order. In Project 2 I will create my own customer, cart or booking in each test (or fixture), use unique names, delete what I made after the test, and never touch the data of other groups.
3. The load balancer keeps one server per user and remembers my server in the AWSALB cookie. One requests.Session stores that cookie and sends it with every request, so the user that I create and the login that follows reach the same server. Without a session each request can land on a different server. (I skipped Step 0.12, so I have no three runs to describe.)
4. The defect appears in the block where all three tools are excluded, because no tool is left for the pizza. A 500 with an empty body tells the calling app nothing: it cannot tell a bad request from a broken server, cannot show the user a useful message, and may retry for nothing. A 400 with a message says that the input was the problem and what to change. The test stays as xfail(strict=True) so that the defect stays visible in every run, the rest of the suite stays green, and the run fails as soon as QuickPizza fixes the defect, which tells me to remove the mark.
5. Base choice coverage needs 1 base test + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 1 + 2 + 3 + 1 + 2 = 9 tests. All combinations needs 3 x 4 x 2 x 3 = 72 tests.
6. I got 404 for the read, 400 for the change and 400 for the delete. I expected a 4xx code such as 403 Forbidden (the rating exists but is not yours) or 404 Not Found (hide that it exists). The read (404) is fine. The change and delete answer 400 with the message "rating ID ... not found", which is a small defect in the status code only: the rating was not found for this user, so 404 (or 403) is the right code, and 400 wrongly says that my request was malformed. It is not a security defect, because nothing was read, changed or deleted and the owner still saw the rating unchanged. A 200 or 204 would have been serious.
7. The command answers 200 with a list of ratings (ids 1, 2, 3, 4, ...), although the token 0000000000000000 was never given out by a login. Yes, this is a defect: the API accepts a token that nobody created, and the list looks like the shared ratings of the public token, so it seems to accept any token of 16 characters (a short token was refused with 401 in Step A2). On a real system a stranger could guess or invent a token and read data without logging in, and if the same flaw covers create, change and delete, could also alter other users' data. I only read with this token.
8. An API test checks the rules of the server directly and quickly, for example every status code, every error message, boundary values such as 0 and 6 stars, and the data that is saved, without depending on the layout of a page. A test through the web pages is the only one that can check what a user actually sees and does: the page renders, the buttons work, the text is readable and the JavaScript in the browser talks to the API correctly.
