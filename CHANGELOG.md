# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0]
- Migrated the check logic out of the Endpoint and into Utils.
- User-Agent String now follows the Integration/1.0 Standard
- Added documentation around usage
- Switched antipatterns for Parent classes to using `super` in a py2 & py3 compatible way.

## [1.0.3]
### Added
- Added support for extensible retry logic.
- Added support for both relative, and absolute, and full URI paths.

## [1.0.2]
### Modified
- Improved documentation

## [1.0.1]
### Added
- Added trunc utility to restfly.utils

### Modified
- APIEndpoint now inherits the logging facility from the APISession passed to it
  at instantiation.

## [1.0.0]
- Initial Version

[1.1.0]: https://github.com/tenable/pyTenable/compare/1.0.3...1.1.0
[1.0.3]: https://github.com/tenable/pyTenable/compare/1.0.2...1.0.3
[1.0.2]: https://github.com/tenable/pyTenable/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/tenable/pyTenable/compare/96c389866da658374736942a0771bf47ff0ccb4c...1.0.1
[1.0.0]: https://github.com/SteveMcGrath/restfly/commit/96c389866da658374736942a0771bf47ff0ccb4c