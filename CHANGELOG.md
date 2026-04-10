# Changelog

All notable changes to `x2fromx` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2026-04-10
### Added
- CLI: `--version` flag to display package version
- CLI: `--verbose` / `-v` flag for detailed output
- CLI: All messages migrated to English for international compatibility
- API: `verbose` parameter to `DirectoryScanner.save()` and `ProjectBuilder.build()`
- pyproject.toml: Added comprehensive classifiers and optional dev dependencies

### Changed
- **Breaking**: CLI help/error messages now in English (commands `scan`/`build` unchanged)
- Improved error handling with `raise` instead of `sys.exit()` for library usage
- Code cleanup: fixed syntax issues from original scripts

### Fixed
- Parser: Better handling of edge cases in tree file indentation
- Builder: Proper overwrite logic with `--overwrite` flag

## [0.1.1] - 2026-04-07
### Added
- Initial PyPI release with Trusted Publishing support
- GitHub Actions workflow for automated publishing

## [0.1.0] - 2026-04-07
### Added
- First functional release: `scan` and `build` commands
- ASCII tree generation with emojis and smart comments
- Smart filtering of `.git`, `__pycache__`, binaries, etc.