# vto_time
This is a custom reusable Django time zones app.

## Disclaimer
This is just a personal test app, it is not intended for use by anyone else.

## Data Fixture
A `seed.json` file is included in the GitHub repository, but not in the `MANIFEST.in` file. It can be downloaded from the GitHub repository to pre-popluate the database with usable data.

The fixture is in the app directory so that it can also be accessed by `loaddata` when the app directory is symlinked in the consuming project directory, during development of the app.

## Required By
- https://pypi.org/project/vto-users/
    - which is in turn required by:
        - https://pypi.org/project/djinntoux/