# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.4]
### Added
- Can now override the base_path by passing use_base=False in a request.

### Added
- Ability tp separately specify the base path.

## [1.3.3]
### Changes
- Switched to separated version.py file to reduce touchpoints.
- Will now always log the request, regardless of the query params or body.
- Moved docstring from APISession.__init__ to the class to conform to google docstring format.

### Added
- url_validator utility.

### Fixed
- box checking should check that class types equal one another, not that it is an instance of box.

## [1.3.2]
### Changed
- Changed the use of the collections library to be forwards compat with py39
- Modified the Box processing check to use the length of resp.text instead of the Content-Length header.

## [1.3.1]
### Changed
- Reduced min version of "python-box" to a Python 2.7 supported version.

## [1.3.0]
## Added
- Added support for response "Boxification" of JSON content.
- Added support for endpoint verb methods using an endpoint _path attribute.

## [1.2.0]
### Added
- Localized private methods for HTTP verbs using the _path attribute for path prefixing.
- APISession now supports context management.
- Added _authenticate and _deauthenticate stubs for use with context management.

## [1.1.1]
### Fixed
- The Integrations UA string broke on Windows (os.uname vs platform.uname)

### Added
- "Soft" typechecking within the check utility function.

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

[1.3.4]: https://github.com/SteveMcGrath/restfly/compare/1.3.3...1.3.4
[1.3.3]: https://github.com/SteveMcGrath/restfly/compare/1.3.2...1.3.3
[1.3.2]: https://github.com/SteveMcGrath/restfly/compare/1.3.1...1.3.2
[1.3.1]: https://github.com/SteveMcGrath/restfly/compare/1.3.0...1.3.1
[1.3.0]: https://github.com/SteveMcGrath/restfly/compare/1.2.0...1.3.0
[1.2.0]: https://github.com/SteveMcGrath/restfly/compare/1.1.1...1.2.0
[1.1.1]: https://github.com/SteveMcGrath/restfly/compare/1.1.0...1.1.1
[1.1.0]: https://github.com/SteveMcGrath/restfly/compare/1.0.3...1.1.0
[1.0.3]: https://github.com/SteveMcGrath/restfly/compare/1.0.2...1.0.3
[1.0.2]: https://github.com/SteveMcGrath/restfly/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/SteveMcGrath/restfly/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/SteveMcGrath/restfly/commit/96c389866da658374736942a0771bf47ff0ccb4c