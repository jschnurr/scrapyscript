# Change Log

## [1.1.5] - 2021-12-11

-   Fix #3 which caused deadlocks and process to hang forever. Thanks @vidakDK and @covuworie!
-   Docs update to factor changes into CHANGELOG.md
-   Added internal feature to have CI set PyPi version from git tag on release
-   Refactored tests and increased coverage to 100%


## [1.1.4] - 2021-10-10

-   Remove support for Python 3.6 and 3.7
-   Add support for Python 3.10
-   Fix docs to specify supported OS (Linux, MacOS)
-   Update CI to including MacOS, Python 3.10 tests
-   Bump dependencies

## [1.1.3] - 2021-07-01

-   Add support for Python 3.9
-   Add examples for basic and Celery-based use cases to /examples
-   Add tests for Celery using a real localhost broker
-   Improvements to readme content and format
-   Bump dependencies

## [1.1.2] - 2021-07-01

-   Fix #11 to allow billiard version to float

## [1.1.0] - 2020-06-27

-   Remove support for Python 2.7. Now Python 3.6+ only
-   Migrate from TravisCI to Github actions
-   Migrate from setup.py to Poetry
-   Add tests for invalid return values from Spiders
-   Bump dependencies

## [1.0.0] - 2017-12-10

-   Breaking API changes to allow passing of \*args and \*\*kwargs to running spider

## [0.1.0] - 2017-05-28

-   Patches to support Celery 4+ and Billiard 3.5.+. Thanks to @mrge and @bmartel.

## [0.0.6] - 2016-10-30

-   Fix to allow Scrapy version to float in requirements.txt

## [0.0.5] - 2016-10-30

-   Pin Scrapy and billiard versions

## [0.0.4] - 2016-06-20

-   Initial release