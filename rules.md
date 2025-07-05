# Memex Operating Rules

## Cloud Provider Interaction

- When interacting with cloud providers like GCP or AWS, I cannot use the user's local, pre-authenticated CLI.
- My execution environment is sandboxed and does not have access to the user's local credential files or authenticated sessions.
- The standard and secure procedure is for the user to create a dedicated service account with scoped permissions for the project.
- I will provide the user with the necessary commands to create and configure these resources. The user will then execute these commands in their authenticated environment.
- Service account keys should be stored as secrets in the CI/CD system (e.g., GitHub Secrets) and not committed to the repository.
