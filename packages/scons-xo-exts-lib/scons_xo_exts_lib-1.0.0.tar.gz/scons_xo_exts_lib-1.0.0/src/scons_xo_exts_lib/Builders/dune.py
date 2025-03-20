#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import os
import subprocess

from SCons.Script import Builder
from SCons.Script import Environment


def _get_dune_project(sources: list):
    for source in sources:
        source_str = str(source)

        if "dune-project" in source_str:
            return source_str

    raise RuntimeError("No dune-project in specified sources")


def dune_build_action(target, source, env) -> int:
    dune_project = _get_dune_project(sources=source)
    dune_base_dir = os.path.dirname(dune_project)

    dune_exe = env.get("DUNE_EXE", "dune")
    dune_flags = env.get("DUNE_FLAGS", "--display=short")

    cmd = f"{dune_exe} build {dune_flags} @install"
    result = subprocess.run(
        args=cmd,
        capture_output=False,
        check=False,
        cwd=dune_base_dir,
        shell=True,
    )

    return result.returncode


def generate(env: Environment) -> None:
    dune_binary_builder = Builder(action=dune_build_action)

    env.Append(BUILDERS={"DuneBinary": dune_binary_builder})


def exists(env: Environment):
    return env.Detect("dune")
