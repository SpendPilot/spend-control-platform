# Troubleshooting

Backend ready check shows database error:

- Verify `DATABASE_URL`
- Confirm network access from the runtime to PostgreSQL

Frontend sign-in fails:

- Check `NEXT_PUBLIC_ENTRA_FRONTEND_CLIENT_ID`
- Check `NEXT_PUBLIC_ENTRA_API_SCOPE`
- Verify redirect URIs in the Entra app registration

Backend token validation fails:

- Check `ENTRA_BACKEND_AUDIENCE`
- Check `ENTRA_AUTHORITY`
- Confirm the frontend requested the backend scope

Document scan produces fallback results:

- Verify Azure Document Intelligence endpoint
- Verify Azure AI Foundry endpoint and deployment
- Confirm managed identity has access
