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

zmk_config="/home/jaapie/Work/Devices/Aurora_Lily58/zmk-config"

@task
def build(ctx):
    """Build"""
    sides = ["left", "right"]
    for cmd in [
        f"west build -p -b nice_nano@2.0.0 -d build/{side} app -- -DZMK_EXTRA_MODULES={zmk_config} -DZMK_CONFIG={zmk_config}/config --preset={side}" for side in sides
    ] \
    + [f"cp build/{side}/zephyr/zmk.uf2 lily58_{side}.uf2" for side in sides]:
        ctx.run(cmd, echo=True)


@task
def debug(ctx):
    """Build"""
    sides = ["left", "right"]
    for cmd in [
        f"west build -p -b nice_nano@2.0.0 -d build/{side} app -- -DZMK_EXTRA_MODULES={zmk_config} -DZMK_CONFIG={zmk_config}/config --preset={side}-debug" for side in sides
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
