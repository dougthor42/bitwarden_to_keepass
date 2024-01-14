#!/bin/bash

# Install bazel (https://bazel.build) via bazelisk (https://github.com/bazelbuild/bazelisk).
#
# Bazelisk is a wrapper around bazel and can be invoked the same way as the OG `bazel`.
#
# Puts the bazelisk binary at /usr/local/bin/bazelisk and .../bazel

BAZEL_VERSION="v1.19.0"
URL="https://github.com/bazelbuild/bazelisk/releases/download/$BAZEL_VERSION/bazelisk-linux-amd64"

TMP_PATH="/tmp/bazelisk"
BINARY_PATH="/usr/local/bin/bazelisk"

wget $URL -O $TMP_PATH
sudo cp $TMP_PATH $BINARY_PATH
sudo chmod a+x $BINARY_PATH
sudo ln $BINARY_PATH /usr/local/bin/bazel
