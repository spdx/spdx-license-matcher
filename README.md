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

#### Linux

```shell
sudo apt-get install redis-server
```

#### macOS

```shell
brew install redis
brew services start redis
```

#### Windows

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
     ignoring replaceable text and focusing on substantial text.
   - Tokenizes the normalized text into a list of bigrams.
   - Use a token-based similarity metric algorithm, namely the
     [Sørensen-Dice algorithm][sorensen-dice], to find close matches.
   - A threshold value is used to filter out low-confidence matches.
   - If the match is 100%, it's a perfect match.
   - If the match is between the threshold and 100%, we apply the full matching
     algorithm from the [SPDX Java Tools][method].
     - If there is a match, the text is considered to match the standard license.
     - If not, the tool displays the differences.

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
