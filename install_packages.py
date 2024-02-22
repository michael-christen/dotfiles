#!/usr/bin/env python3

import argparse
import os
import pathlib
import subprocess
import sys
from typing import List


def is_apt_repository_added(repo_url: str) -> bool:
    try:
        # XXX: not checking
        result = subprocess.run(['apt-cache', 'policy'], capture_output=True, text=True, check=True)
        return repo_url in result.stdout
    except subprocess.CalledProcessError:
        return False


def add_apt_repository(repo: str, url: str, dry_run: bool) -> None:
    if is_apt_repository_added(url):
        print(f"APT repository '{repo}' is already added.")
        return

    if not dry_run:
        subprocess.run(['sudo', 'add-apt-repository', '-y', repo])
    else:
        print(f"Would add APT repository: {repo}")


def update_apt(dry_run: bool) -> None:
    if not dry_run:
        subprocess.run(['sudo', 'apt', 'update'])
    else:
        print('Would update APT')


def install_packages(packages: List[str], dry_run: bool) -> None:
    if not dry_run:
        cmd = ['sudo', 'apt', 'install', '-y']
        cmd.extend(packages)
        subprocess.run(cmd)
    else:
        package_str = '\n'.join(packages)
        print(f'Would install packages:\n{package_str}')


def download_file(url: str, path: pathlib.Path, dry_run: bool) -> bool:
    """Returns True if was already cached."""
    if path.exists():
        return True
    if not dry_run:
        subprocess.run(['wget', '-O', path, url])
    else:
        print(f'Would download: {url} to {path}')
    return False


def download_and_install_package(package_url: str, dry_run: bool, force: bool) -> None:
    package_name = pathlib.Path(package_url).name
    cache_dir = pathlib.Path(os.environ.get(
        'XDG_CACHE_HOME', pathlib.Path.home() / '.cache')) / 'apt_packages'
    cache_dir.mkdir(parents=True, exist_ok=True)
    cached_package_path = cache_dir / package_name
    was_cached = download_file(url=package_url, path=cached_package_path, dry_run=dry_run)
    if force or not was_cached:
        if not dry_run:
            subprocess.run(['sudo', 'dpkg', '-i', cached_package_path])
            subprocess.run(['sudo', 'apt', 'install', '-f', '-y'])
        else:
            print(f'Would install package: {cached_package_path}')


# Define APT repositories
APT_REPOSITORIES_WITH_URL = [
    ('ppa:kicad/kicad-7.0-releases',
     'http://ppa.launchpad.net/kicad/kicad-7.0-releases/ubuntu'),
    ('ppa:fish-shell/release-3',
     'http://ppa.launchpad.net/fish-shell/release-3/ubuntu'),
    # syncthing, necessitates setting this up
    ('deb [signed-by=/etc/apt/keyrings/syncthing-archive-keyring.gpg] https://apt.syncthing.net/ syncthing stable',
     'https://apt.syncthing.net'),



]

# Define packages to install from APT repositories
APT_PACKAGES = [
    # TODO: versions?
    # Maybe ctags and clang-format?
    'neovim',
    'git',
    'tmux',
    'htop',
    'xclip',
    'curl',
    # get say
    'gnustep-gui-runtime',
    # gcc
    # TODO: Determine how to get bazel running without this installed
    'build-essential',
    # java
    # TODO: same deal as build-essential
    # - openjdk-19-jre-headless
    # Switched from ^ to have gui
    'openjdk-19-jre',
    # For development purposes
    'python3.10-venv',
    # Directory Viewing Utilities
    'tree',
    'ranger',
    # Searching
    'silversearcher-ag',
    # AppImage Support
    # was originally fuse, but hopefully this is fine (fuse conflicts w/ ubuntu-desktop)
    'fuse3',
    'libfuse2',
    # Sharing notes
    # TODO: COnfigure as a service
    'syncthing',
    # XXX: waveforms is crashing when attempting to start
    # NOTE: Can start fine from application launcher :shrug:
    # TODO: digilent-agent isn't working though / no launcher
    'libqt5serialport5-dev',
    'xterm',
    'libxcb-xinput-dev',
    # - qt5-default  # XXX: This should fix, but is unavailable
    'arduino',
    # Using blender 4.0, this is the 3.0 installation
    # - blender
    'kicad',
    # https://code.visualstudio.com/download#
    # Visualization of system metrics in toolbar
    'gnome-system-monitor',
    # post 22.04 use gnome-browser-connector
    'chrome-gnome-shell',
    'gir1.2-gtop-2.0',
    'gir1.2-nm-1.0',
    'gir1.2-clutter-1.0',
    # Ensure usual settings, etc. are accessible, reruns every time ...
    'ubuntu-desktop',
    # Shells
    'zsh',
    'fish',
    # For docker, see https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
    # There are a few manual steps to setup the keyrings
    'docker-ce',
    'docker-ce-cli',
    'containerd.io',
    'docker-buildx-plugin',
    'docker-compose-plugin',
    # For rootless docker
    'uidmap',
    'dbus-user-session',
    'docker-ce-rootless-extras',
    # For ssl usage / rust
    'libssl-dev',
    # For rust embedded
    'gdb-multiarch',
    'openocd',
    'qemu-system-arm',
    # Miscellaneous tools use it, eg) nvim obsidian
    'ripgrep',
    # 2 finger right click
    'xserver-xorg-input-synaptics',
    'gnome-tweaks',
]

# Define other packages to download and install
OTHER_PACKAGES = [
    # Install Digilent Adept for Waveforms
    'https://digilent.s3.us-west-2.amazonaws.com/Software/Adept2+Runtime/2.27.9/digilent.adept.runtime_2.27.9-amd64.deb',
    # Install Waveforms
    'https://digilent.s3.us-west-2.amazonaws.com/Software/Waveforms2015/3.21.3/digilent.waveforms_3.21.3_amd64.deb',
    # Install Waveforms Agent
    'https://s3-us-west-2.amazonaws.com/digilent/Software/Digilent+Agent/1.0.1/digilent-agent_1.0.1-1_amd64.deb',
    # Install vscode
    'https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64',
]


def main():
    parser = argparse.ArgumentParser(description="APT package management script")
    parser.add_argument('--dry-run', action='store_true', help="Show what would be done without actually doing it")
    parser.add_argument('--force', action='store_true', help="Re-install cached .deb even if already found")
    args = parser.parse_args()

    # Request sudo permissions if not running in dry-run mode
    # XXX: Probably be better about anouncing this
    if not args.dry_run:
        subprocess.run(['sudo', '-v'], check=True)

    # Download keyrings
    download_file(url='https://syncthing.net/release-key.gpg',
                  path=pathlib.Path('/etc/apt/keyrings/syncthing-archive-keyring.gpg'),
                  dry_run=args.dry_run)
    # Add APT repositories
    for repo, url in APT_REPOSITORIES_WITH_URL:
        add_apt_repository(repo, url=url, dry_run=args.dry_run)

    # Update APT
    # TODO: Takes a significant amount of time
    # update_apt(dry_run=args.dry_run)

    # Install packages from APT repositories
    install_packages(APT_PACKAGES, dry_run=args.dry_run)

    # Download and install other packages
    for package in OTHER_PACKAGES:
        download_and_install_package(package, dry_run=args.dry_run,
                                     force=args.force)


if __name__ == '__main__':
    main()
