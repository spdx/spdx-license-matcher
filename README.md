# SPDX License Matcher

A Python tool which takes the license text from the user,
compares it with the [SPDX License List][spdx-license-list]
using an algorithm which finds close matches and returns differences
if the input license text is found to be a close match.

A Redis (or Valkey) server is used to store the license texts.

Requires Python 3.9+ and Java 11+ (for SPDX Java Tools).

## Usage

```shell
spdx-license-matcher -f filename -t threshold
```

- `filename` is the file with the license text
  (required)
- `threshold` is a value up to which we will just won't consider a match
  (optional; default: 0.9)

Run `spdx-license-matcher --help` for more info.

## Installation

```shell
pipx install license-matcher
```

Or with uv:

```shell
uv tool install license-matcher
```

The package bundles [SPDX Java Tools][tools-java].
No separate jar download needed.

To use a different jar version,
set the `SPDX_TOOLS_JAR` environment variable to its path before running.

[tools-java]: https://github.com/spdx/tools-java

### Install Redis/Valkey

Redis or Valkey stores the pre-processed SPDX License List.
Install it once, then keep it running while using the tool.

- Linux

  ```shell
  sudo apt-get install redis-server
  ```

- macOS

  ```shell
  brew install redis
  brew services start redis
  ```

- Windows

  Download from [microsoftarchive/redis][ms-redis] and install.

#### Verify installation

Verify Redis is running: `redis-cli ping` should return `PONG`.

By default, the tool connects to Redis at `localhost:6379`.
Set `SPDX_REDIS_HOST` to override the hostname.

[ms-redis]: https://github.com/microsoftarchive/redis/releases

### Development Installation

1. Clone the repository

    ```shell
    git clone https://github.com/spdx/spdx-license-matcher.git
    cd spdx-license-matcher
    ```

2. Install in editable mode

    ```shell
    pip install -e .
    ```

## Workflow

The workflow of the tool is as follows:

1. Reads the license text as input from the user.
2. Build a Redis/Valkey database with all the license text present on the
    SPDX License List.
3. Compare the license text with the license text present in the database.

    - Normalizes the license text based on the SPDX Matching guidelines while
      ignore the replaceable text
      and only focusing on substantial text for matching purposes.
    - Tokenizes the normalized text into a list of bigrams. This is necessary
      for the token-based algorithm we are using for our use case.
    - Use a token based similarity metric algorithm namely
      [Sørensen-Dice algorithm][sorensen-dice] which is based on the logic
      to find the common tokens, and divide it by the total number of tokens
      present by combining both of the sets.
      This algorithm helps us to distinguish our close matches.
    - A threshold value is used where we just won't consider a match.
    - If the match is 100% then we say it's a perfect match.
    - If the match is between a threshold value and 100% then we apply the
      full matching algorithms and compares the closely matched license text
      to the license text of SPDX Standard License using a [method][method]
      present in the SPDX tools.
      - If there is a match then the given license text matches with the SPDX
        standard license.
      - If there is no match then we simply display the differences of the given
        license text with that of SPDX License List.

## History

- This project started as [a Google Summer of Code 2019 project][gsoc2019],
  with contribution from [@ugtan].
- Now maintained by the SPDX community and updated for Python 3.
- See SPDX's participation in Google Summer of Code (GSoC):
  <https://github.com/spdx/GSoC>.

[spdx-license-list]: https://spdx.org/licenses/
[sorensen-dice]: https://en.wikipedia.org/wiki/Dice-S%C3%B8rensen_coefficient
[method]: https://github.com/spdx/tools/blob/1f4f85ad3fdb63577f9e4db4ccce0c7f894e2f04/src/org/spdx/compare/LicenseCompareHelper.java#L592
[gsoc2019]: https://summerofcode.withgoogle.com/archive/2019/projects/5687492043341824
[@ugtan]: https://github.com/ugtan
