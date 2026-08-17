# Implementation order

A common safe order is:
1. domain/schema contracts
2. backend/service logic
3. authorization
4. external/async integration
5. UI
6. tests
7. observability
8. deployment/migration

Change order when the repository architecture suggests a better dependency flow.
