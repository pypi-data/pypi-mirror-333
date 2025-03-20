# Changelog
All notable changes to charset-normalizer will be documented in this file. This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## 0.2.3 (2025-03-12)

### Changed
- Improved DOM pre-processing before sending it to the LLM for analysis. This improve the overall performance.

## 0.2.2 (2025-03-11)

### Fixed
- Parsing of Playwright selector having nested parenthesis in it.
- Retry in case of Playwright timeout on elements/actions.

### Changed
- Improved overall (world) prompt performance by simplifying it.

## 0.2.1 (2025-03-07)

### Fixed
- Parsing kwargs given by the LLM.
- Processing large HTML DOM. Starting now, we minify the HTML to save tokens.

### Misc
- Add command '/c' for setting a context in CLI.

## 0.2.0 (2025-03-07)

### Fixed
- Handling the case where the LLM hint us toward using the `mouse` property exposed by Playwright.

### Added
- A debug / companion CLI to effortlessly improve your tests. Run it by either `python -m playsmart` or simply `playsmart`
  in your shell.

## 0.1.3 (2025-03-06)

### Fixed
- Unstable cache key with no workaround to force it (see README to see how to apply `PLAYSMART_CACHE_PRESET` environment variable)
- No retries if the LLM gave unparsable content

## 0.1.2 (2025-02-25)

### Fixed
- Not auto retrying prompt on LLM bad code/selector generation.
- Weak fingerprint matching for caching. We started using resources content instead of their uris.

## 0.1.1 (2025-02-21)

### Fixed
- Unparsable LLM answer when the output purposely skip the intended (markdown) format.

## 0.1.0 (2025-02-21)

### Added
- initial release
