# API Introduction

The current API project is a mentoring application which connects members to mentors. This is a simple API built with Django Rest Framework that meets the following requirements:

1. The API should allow users:
   - to sign-up using their e-mail and password;
   - to authenticate using their e-mail and password.
2. Registered users should go thought an onbording processing to complete their profile as one of two types available: **mentor** or **member**;
3. Both users, mentor or member, share the following information:
   - name;
   - location;
   - employer;
   - title;
   - select multiple expertises.
     - Some examples are: UX/UX Design, Product Design, AI Design.
4. Mentors are able to:
   - select multiple areas of mentorship during onboarding process;
     - Some examples are: Career Advice, Portfolio Review, Interview Techniques.
   - add time availability to indicate times that they are available for mentorship;
5. Mentors who complete the mentor onboarding process are placed in the pending state waiting to be approved;
6. Both users should be able to update their profile details;
7. The API should provide and endpoint to approve mentors that are in pending state and that should be only done by a super user;
8. The API should have an endpoint to list all mentors, and the ability to filter them based on approved or pending state based in a paginated approach;
9. The API should have an endpoint to list all members in a paginated approach with the ability to search and filter by expertise;
10. The API should have an endpoint to fetch a specific mentor or member usign their primary key;
11. From mentor's availability, members should be able to book times with them (only approved mentors).
    - when booking time, it has to run a validation to check if mentor has available time at same time member expect.

Global requirements:

- It must apply the REST pattern and design style;
- Use PostgresSQL or any other RDBMS database;
- Document API by using Postman or any other software;
- Deploy API.