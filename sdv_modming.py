#!/usr/bin/env python3
"""
A script to automate updating Stardew Valley mods.
"""
from concurrent.futures import ThreadPoolExecutor
from glob import glob
from os.path import dirname, exists, normpath
from shutil import move, rmtree
from zipfile import ZipFile

__author__ = "Jasmine Webb"
__version__ = "0.1.0"
__license__ = "MIT"


def clean_outdated(mod, outdated):
    """Relocates the config file to the updated mod directory, then removes the
    outdated mod directory.
    """
    # Move config file from outdated mod dir to extracted update dir
    if mod != "ContentPatcher":
        print(f"  📃 Relocating {mod} config file...")
        config_path = normpath(mod + "/config.json")
        move(normpath(f"../{config_path}"), config_path)

    # Remove outdated mod dir
    print(f"    🧹 Removing old version of {mod}...")
    rmtree(outdated)


def install_mod(updated_mod_dir):
    """Handles the process of extracting, updating, and setting the config of a
    given mod.
    """
    mod_name = ""

    print(f"📁 Extracting {updated_mod_dir}...")
    with ZipFile(updated_mod_dir, "r") as updated_mod:
        mod_name = normpath(dirname(updated_mod.namelist()[0]))
        updated_mod.extractall()

    outdated_mod_dir = normpath(f"../{mod_name}")

    if exists(outdated_mod_dir):
        clean_outdated(mod_name, outdated_mod_dir)

    # Replace with extracted update dir
    print(f"      🚛 Moving {mod_name} to Mods folder...")
    move(mod_name, outdated_mod_dir)

    print(f"        🎉 {mod_name} has been updated!")


def main():
    """Main entry point of the app."""
    updates = glob("*.zip")  # Determine mods to update

    with ThreadPoolExecutor() as executor:
        executor.map(install_mod, updates)


if __name__ == "__main__":
    """This is executed when run from the command line."""
    main()
