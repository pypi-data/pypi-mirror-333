#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import subprocess

from SCons.Script import Builder


def ninja_action(target, source, env):
    ninja_targets = " ".join(str(t) for t in target)

    ninja_exe = env.get("NINJA_EXE", "ninja")
    ninja_flags = env.get("NINJA_FLAGS", "")

    cmd = f"{ninja_exe} {ninja_flags} {ninja_targets}"
    result = subprocess.run(
        args=cmd,
        capture_output=False,
        check=False,
        shell=True,
    )

    return result.returncode


def generate(env):
    ninja_binary_builder = Builder(action=ninja_action)

    env.Append(BUILDERS={"NinjaBinary": ninja_binary_builder})


def exists(env):
    return env.Detect("ninja")
