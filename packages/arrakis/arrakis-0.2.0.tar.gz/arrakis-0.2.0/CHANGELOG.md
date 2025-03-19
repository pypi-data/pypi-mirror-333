# Changelog

## [Unreleased]

## [0.2.0] - 2025-03-11

### Added

- Add publisher metadata to Channel
- Allow multiple data types in find/count requests
- Allow querying by publisher in find/count requests
- Add `from_json` constructor in Channel
- Add arrakis entry point

### Fixed

- Fix issue in parsing response in Publisher registration
- Improve error handling and mitigate timeouts in MultiEndpointStream polling
- Remove initial describe call within stream endpoint

### Changed

- Allow Channel to handle raw numpy dtypes
- Expose domain property for Channel
- Publisher now only requires a `publisher_id` for registration

### Removed

## [0.1.0] - 2024-11-13

- Initial release.

[unreleased]: https://git.ligo.org/ngdd/arrakis-python/-/compare/0.2.0...main
[0.2.0]: https://git.ligo.org/ngdd/arrakis-python/-/tags/0.2.0
[0.1.0]: https://git.ligo.org/ngdd/arrakis-python/-/tags/0.1.0
