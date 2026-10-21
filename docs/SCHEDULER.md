# Scheduler

The scheduler receives clean domain objects instead of Django ORM instances. Candidate placements are derived from:

- course offering requirements
- eligible teachers
- compatible rooms
- active day definitions
- valid imported time-slot blocks

The CP-SAT model will choose assignments that satisfy all hard constraints and minimize weighted soft-constraint penalties.

