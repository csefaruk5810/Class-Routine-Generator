# Database Model

Core model groups:

- `accounts`: users and roles
- `academics`: departments, sessions, semesters, sections, teachers, courses, offerings
- `resources`: rooms, scheduling configurations, days, time slots, teacher availability, weights
- `routines`: routine versions, assignments, validation snapshots
- `imports`: JSON import jobs and reports

The schema is normalized around reusable configuration entities rather than storing imported timetable rows as the long-term source of truth.

