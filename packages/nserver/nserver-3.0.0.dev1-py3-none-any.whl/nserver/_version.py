"""Version information for this package."""
### IMPORTS
### ============================================================================
## Standard Library

## Installed

## Application

### CONSTANTS
### ============================================================================
## Version Information - DO NOT EDIT
## -----------------------------------------------------------------------------
# These variables will be set during the build process. Do not attempt to edit.
PACKAGE_VERSION = "3.0.0.dev1"
BUILD_VERSION = "3.0.0.dev1.dev1730506852"
BUILD_GIT_HASH = "3a23584a1e2f07da7c0fc9694e02fd92ff1b94a4"
BUILD_GIT_HASH_SHORT = "3a23584"
BUILD_GIT_BRANCH = "dev"
BUILD_TIMESTAMP = 1730506852
BUILD_DATETIME = datetime.datetime.utcfromtimestamp(1730506852)

## Version Information Strings
## -----------------------------------------------------------------------------
VERSION_INFO_SHORT = f"{BUILD_VERSION}"
VERSION_INFO = f"{PACKAGE_VERSION} ({BUILD_VERSION})"
VERSION_INFO_LONG = (
    f"{PACKAGE_VERSION} ({BUILD_VERSION}) ({BUILD_GIT_BRANCH}@{BUILD_GIT_HASH_SHORT})"
)
VERSION_INFO_FULL = (
    f"{PACKAGE_VERSION} ({BUILD_VERSION})\n"
    f"{BUILD_GIT_BRANCH}@{BUILD_GIT_HASH}\n"
    f"Built: {BUILD_DATETIME}"
)
