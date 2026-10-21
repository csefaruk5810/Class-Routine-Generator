# Architecture

The application is split into three layers:

- Django apps for persistence, authentication, and API delivery
- A scheduler package that contains pure domain models and solver logic
- A frontend application that consumes REST APIs without depending on solver internals

The provided JSON routine files are treated as importable reference data. Their shape informs configuration, time-slot normalization, and importer validation rules, but they are not hard-coded into the scheduling engine.

