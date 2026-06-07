# Troubleshooting

Backend ready check shows database error:

- Verify `DATABASE_URL`
- Confirm network access from the runtime to PostgreSQL

Frontend sign-in fails:

- Check `NEXT_PUBLIC_ENTRA_FRONTEND_CLIENT_ID`
- Check `NEXT_PUBLIC_ENTRA_API_SCOPE`
- Check whether the app authority is `https://login.microsoftonline.com/common`
- Confirm `NEXT_PUBLIC_ENTRA_API_SCOPE` uses the backend Application ID URI, not the backend client ID
- Confirm frontend API helpers are not generating `/api/api/...` paths when `NEXT_PUBLIC_API_BASE_URL` is already `/api`
- Verify redirect URIs in the Entra app registration

Login redirects back to the same page and shows raw HTML in red:

- The frontend likely received an HTML fallback page instead of a JSON API response
- Check the browser network tab for `/api/auth/me`
- If the request path is `/api/api/auth/me`, the frontend API base path is being prefixed twice
- The shared `buildApiUrl` helper in this repo now normalizes duplicate `/api` prefixes and converts HTML error responses into readable messages

Azure sign-in page says "You can't sign in here with a personal account":

- The Entra app registration is still restricted to work or school accounts
- Or the frontend authority is still `organizations` instead of `common`

Backend token validation fails:

- Check `ENTRA_BACKEND_AUDIENCE`
- Check `ENTRA_AUTHORITY`
- Confirm the frontend requested the backend scope

Document scan produces fallback results:

- Verify Azure Document Intelligence endpoint
- Verify Azure AI Foundry endpoint and deployment
- Confirm managed identity has access
