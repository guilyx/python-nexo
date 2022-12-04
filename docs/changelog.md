# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 04/12/2022
### Changed
- Readme Examples

## [1.0.2] - 04/12/2022
### Added
- Asynchronous Client
- New Endpoints

### Removed
- Code Coverage for upper Clients classes

## [1.0.1] - 05-10-2022
### Added
- Example for placing order
- More Unit Tests
### Changed
- POST Requests are functional
- Sleep in test to avoid blowing up the rate limit
- Improve error management and exceptions

## [1.0.0] - 03-10-2022
### Added
- This CHANGELOG file to hopefully serve as an evolving example of a
  standardized open source project CHANGELOG.
- Class Objects for API Responses, serialized from JSON.
- Endpoints documentation

### Changed
- HMAC Signature Generation has been fixed

### Removed
- main.py is now removed. To try out the library, users will now use docker-compose, attach to it, run python, import the project and run some methods.

## [0.0.1] - 02-10-2022
### Added
- Basic API Client with faulty HMAC Signature Generation
- All Endpoints wrapped
- Readme with examples, setup steps
- Custom Exceptions based on Nexo's API
- Basic Tests
