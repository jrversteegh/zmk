import glob
import os
from datetime import datetime
from pathlib import Path

import tomli
from git import Repo
from invoke import task

# Run from project root directory
script_dir = Path(__file__).absolute().parent
os.chdir(script_dir)

zmk_config=f"{script_dir}/zmk-config"
defines=f"-DZMK_EXTRA_MODULES={zmk_config} -DZMK_CONFIG={zmk_config}/config"

@task
def init(ctx):
    """Initialize zephyr through west"""
    west_dir = script_dir / ".west"
    if not west_dir.exists():
        for cmd in [
                "west init -l app",
                "west update"
        ]:
            ctx.run(cmd, echo=True)


@task(init)
def build(ctx):
    """Build"""
    sides = ["left", "right"]
    versions = ["3.0.0", "2.0.0"]
    for cmd in [
        f"west build -p -b nice_nano@{version} -d build/{side} app -- {defines} -DSHIELD=\"splitkb_aurora_lily58_{side} nice_view_nano_adapter nice_view_orca\" --preset=release" for (side, version) in zip(sides, versions)
    ] \
    + [f"cp build/{side}/zephyr/zmk.uf2 lily58_{side}.uf2" for side in sides]:
        ctx.run(cmd, echo=True)


@task
def debug(ctx):
    """Build"""
    sides = ["left", "right"]
    versions = ["3.0.0", "2.0.0"]
    for cmd in [
        f"west build -p -b nice_nano@{version} -d build/{side} app -- {defines} -DSHIELD=\"splitkb_aurora_lily58_{side} nice_view_nano_adapter nice_view_orca\" --preset=debug" for (side, version) in zip(sides, versions)
    ] \
    + [f"cp build/{side}/zephyr/zmk.uf2 lily58_{side}-debug.uf2" for side in sides]:
        ctx.run(cmd, echo=True)


@task
def clean(ctx):
    """Build"""
    for cmd in (
        "rm -rf app/build",
    ):
        ctx.run(cmd, echo=True)
