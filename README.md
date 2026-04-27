# SPDX License Match Tool

A Python tool which takes the license text from the user,
compares it with the [SPDX License List][spdx-license-list]
using an algorithm which finds close matches and returns differences
if the input license text is found to be a close match.

[spdx-license-list]: https://spdx.org/licenses/

## Requirements

- Python 3.8+
- Java 11+ (required by the bundled SPDX Tools jar)
- Redis server

## Installation

**As a command-line tool** (recommended — isolated environment, no dependency conflicts):

```sh
pipx install spdx-license-matcher
```

**As a library** (inside a project's virtual environment):

```sh
pip install spdx-license-matcher
```

The package bundles `tool.jar` (SPDX Java Tools).
No separate jar download needed.

To use a different jar version,
set the `SPDX_TOOLS_JAR` environment variable to its path before running.

### Install Redis

Redis stores the pre-processed SPDX License List.
Install it once, then keep it running while using the tool.

#### Linux

```sh
sudo apt-get install redis-server
```

#### macOS

```sh
brew install redis
brew services start redis
```

#### Windows

Download from [microsoftarchive/redis][ms-redis]
and install.

#### Verify installation

Verify Redis is running: `redis-cli ping` should return `PONG`.

By default the tool connects to Redis at `localhost:6379`.
Set `SPDX_REDIS_HOST` to override the hostname.

[ms-redis]: https://github.com/microsoftarchive/redis/releases

## Usage

To run the tool just use the command

```sh
spdx-license-matcher -f <file-name> -t <threshold>
```

- `filename` is the file with the license text(if you don't provide the file as
  well then it will prompt you to add it).
- `threshold` is a value upto which we will just won't consider a match.
  (optional)

You can also run `spdx-license-matcher --help` for more info.

## Workflow

The workflow of the tool is as follows:

- Reads the license text as input from the user.
- Build a redis database with all the license text present on the
  SPDX License List.
- Compare the license text with the license text present in the database.
  - Normalises the license text based on the SPDX Matching guidelines while
    ignore the replaceable text
    and only focusing on substantial text for matching purposes.
  - Tokenizes normalised text into a list of bigrams. This is necessary for the
    token based algorithm we are using for our use case.
  - Use a token based similarity metric algorithm namely
    [Dice-Sørensen algorithm][dice-sorensen] which is based on the logic to find
    the common tokens, and divide it by the total number of tokens present by
    combining both of the sets. This algorithm helps us to distinguish our close
    matches.
  - A threshold value is used where we just won't consider a match.
  - If the match is 100% then we say its a perfect match.
  - If the match is between a threshold value and 100%,
    then we apply the full matching algorithms and compares the closely matched
    license text to the license text of SPDX Standard License using a
    [method] present in the SPDX tools.
    - If there is a match then the given license text matches with the SPDX
      standard license.
    - If there is no match then we simply display the differences of the given
      license text with that of SPDX license list.

[dice-sorensen]: https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient
[method]: https://github.com/spdx/tools/blob/b61e655ad997d7669faab65cff7d0b36da03cab5/src/org/spdx/compare/LicenseCompareHelper.java#L568
