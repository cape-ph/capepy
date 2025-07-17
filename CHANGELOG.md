# Changelog

## [2.1.0](https://github.com/cape-ph/capepy/compare/v2.0.0...v2.1.0) (2025-07-17)


### Features

* **dynamodb:** add `CrawlerTable` for Glue Crawler dynamodb table ([64fccdb](https://github.com/cape-ph/capepy/commit/64fccdbfeca140784d15bff288a9f74f6bec8c60))
* **dynamodb:** add `CrawlerTable` for Glue Crawler dynamodb table ([817fb71](https://github.com/cape-ph/capepy/commit/817fb71b617b18ae4d8048e9644eab4a3924a78d))
* **dynamodb:** add `UserTable` for user attributes DyanmoDB table ([5cc7e2a](https://github.com/cape-ph/capepy/commit/5cc7e2a8335be4ba65934e31c0192b5cb9452561))
* **dynamodb:** add `UserTable` for user attributes DyanmoDB table ([eda9b0e](https://github.com/cape-ph/capepy/commit/eda9b0e06063598445c0b12b87cdac833bf0c748))

## [2.0.0](https://github.com/cape-ph/capepy/compare/v1.0.2...v2.0.0) (2025-01-23)


### ⚠ BREAKING CHANGES

* **glue:** terminology was shifted upstream to use `src`/`sink` rather than `raw`/`clean`

### Bug Fixes

* **glue:** terminology was shifted upstream to use `src`/`sink` rather than `raw`/`clean` ([fd43b0d](https://github.com/cape-ph/capepy/commit/fd43b0d866f8fbc83a26aad0bc465061bf622208))

## [1.0.2](https://github.com/cape-ph/capepy/compare/v1.0.1...v1.0.2) (2025-01-23)


### Bug Fixes

* **ci:** correctly set release type to python for updating the `pyproject.toml` file ([c74793a](https://github.com/cape-ph/capepy/commit/c74793ac008e34ccefecb6a6b91fa1bb3e471173))
* **dynamodb:** handle the case where getting an item from a DynamoDB table doesn't return a value ([9f01fde](https://github.com/cape-ph/capepy/commit/9f01fde28c08d72e2d579455f89447481290c972))

## [1.0.1](https://github.com/cape-ph/capepy/compare/v1.0.0...v1.0.1) (2024-11-08)


### Bug Fixes

* bump version in `pyproject.toml` to 1.0.1 ([30cab7e](https://github.com/cape-ph/capepy/commit/30cab7e9cf0fcb1a121d5dfabfafd9505ac9dcfb))

## 1.0.0 (2024-11-06)


### ⚠ BREAKING CHANGES

* downgrade from python 3.11 to 3.10 for Glue support

### Features

* **aws.dynamodb:** auto fill table names from environment when possible ([817a2cc](https://github.com/cape-ph/capepy/commit/817a2cccaf3a211b12d710df27e26909ce0b6404))
* **aws.dynamodb:** classes for working with Pipeline and ETL Job DynamoDB tables ([db921f9](https://github.com/cape-ph/capepy/commit/db921f90323300c0be895876236c24b74e1a4cb4))
* **aws.glue:** add `ETLJob` class for parsing parameters, reading raw files, and writing clean files ([abe10cc](https://github.com/cape-ph/capepy/commit/abe10ccdeab1d0408b1693c6a8954ec99ee4c5ab))
* **aws.lambda:** add `ETLRecord` and `BucketNotificationRecord` entries ([e1ca446](https://github.com/cape-ph/capepy/commit/e1ca446c66604a889aa2b8dc73aa5d96cb19fef5))
* **aws.lambda:** add objects for working with different Lambda event records ([31199e4](https://github.com/cape-ph/capepy/commit/31199e464a7e78c97c259763d95802fc5ea320a0))
* **aws.meta:** add `Boto3Object` for working with `boto3` library in general ([6a04f1b](https://github.com/cape-ph/capepy/commit/6a04f1b8f754a96e5ba6d6d80d53005d9f532cef))
* **aws.utils:** add `decode_error` utility ([29ef499](https://github.com/cape-ph/capepy/commit/29ef4992e1e919826df76050b5e944e57b24ba17))


### Bug Fixes

* **aws.dynamodb:** fix typos ([49edf61](https://github.com/cape-ph/capepy/commit/49edf61a3a48989e24a39ab33a256febe3e96e7c))
* **aws.glue:** `ALERT_OBJ_KEY` renamed to `OBJECT_KEY` ([3a57085](https://github.com/cape-ph/capepy/commit/3a570856f5a65a1315389b3a980cec603e121e42))
* **aws.lambda:** add missing `super` call ([94ab21c](https://github.com/cape-ph/capepy/commit/94ab21ca23431f09e2d6a02f20fb072871bf71df))
* **aws.lambda:** module cannot be named `lambda`, rename to `lambda_` ([cebd3cf](https://github.com/cape-ph/capepy/commit/cebd3cf57351ef29a96fda54b4b9a98b66cb6a37))
* **aws.lambda:** update record name from `parameters` to `pipeline_parameters` ([1c631cb](https://github.com/cape-ph/capepy/commit/1c631cb77a0bd28994381e85cb3f314bc5135e4e))


### Code Refactoring

* downgrade from python 3.11 to 3.10 for Glue support ([63f3bc8](https://github.com/cape-ph/capepy/commit/63f3bc80da8415e783239837c6e3e600719eb444))
