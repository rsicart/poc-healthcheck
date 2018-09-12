# Poc Healthchecks

Simple middleware testing from a given middleware list defined in settings.

## Setup

1. Copy settings/settings.example.py to settings/settings.py

2. Edit settings/settings.py to add your tests.

3. Launch:

```
python3 -m healthchecks.healthchecks
```


## Unit Tests

Launch:

```
python3 -m unittest tests/healthchecks_tests.py
```
