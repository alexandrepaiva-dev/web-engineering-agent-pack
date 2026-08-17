# IDOR and multi-tenancy

Every protected object lookup must enforce ownership/tenant scope.

Bad pattern:
1. fetch record by arbitrary ID
2. check only that user is logged in

Prefer scoping the query itself to the authorized tenant/user when practical.

Never trust tenant ID supplied by the browser as authority.
