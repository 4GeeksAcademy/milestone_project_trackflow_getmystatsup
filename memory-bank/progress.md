# Progress

## Current State
- Milestone 1: Corporate website created.
- Milestone 2: Business logic module implemented.
- Milestone 3: Initial repository structure established.

## Next Steps
- Implement memory bank and agent rules.
- Develop frontend applications (public website and backoffice).
- Integrate business logic into the backoffice application.
- Define and implement reusable agent skills.

-5/31/26 In milestone 4, I went through the "What We Will Evauate" section and made sure each criteria was met.

-6/23/26 Implemented AUTH-03 password reset flow in `uis/backoffice` with:
- Backend routes `POST /auth/forgot-password` and `POST /auth/reset-password`.
- JWT-based reset tokens with 15-60 minute expiry clamp and single-use invalidation.
- Resend email integration for reset links via environment variables only.
- Frontend pages `/login`, `/forgot-password`, and `/reset-password` including required UX behavior.
- Lint validation passed after implementation.