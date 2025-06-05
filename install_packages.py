#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import pathlib
import subprocess
import sys
from typing import List


def is_apt_repository_added(repo_url: str | None) -> bool:
    if repo_url is None:
        return False
    try:
        result = subprocess.run(['apt-cache', 'policy'], capture_output=True, text=True, check=True)
        return repo_url in result.stdout
    except subprocess.CalledProcessError:
        return False


def add_apt_repository(repo: str, url: str | None, dry_run: bool) -> None:
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


def install_apt_packages(packages: List[str], dry_run: bool) -> None:
    if not dry_run:
        cmd = ['sudo', 'apt', 'install', '-y']
        cmd.extend(packages)
        subprocess.run(cmd)
    else:
        package_str = '\n'.join(packages)
        print(f'Would install packages:\n{package_str}')


def install_snap_packages(packages: List[str], dry_run: bool) -> None:
    if not dry_run:
        cmd = ['sudo', 'snap', 'install', '--classic']
        cmd.extend(packages)
        subprocess.run(cmd)
    else:
        package_str = '\n'.join(packages)
        print(f'Would install packages:\n{package_str}')


def download_file(url: str, path: pathlib.Path, dry_run: bool,
                  use_sudo: bool = False) -> bool:
    """Returns True if was already cached."""
    if path.exists():
        return True
    if not dry_run:
        cmd = ['wget', '-O', path, url]
        if use_sudo:
            cmd = ['sudo'] + cmd
        subprocess.run(cmd)
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


def download_and_install_app_image(app_image_url: str, dry_run: bool, force: bool) -> None:
    package_name = pathlib.Path(app_image_url).name
    # XXX: Should I move to a more permanent location?
    cache_dir = pathlib.Path(os.environ.get(
        'XDG_CACHE_HOME', pathlib.Path.home() / '.cache')) / 'app_images'
    cache_dir.mkdir(parents=True, exist_ok=True)
    cached_package_path = cache_dir / package_name
    was_cached = download_file(url=app_image_url, path=cached_package_path, dry_run=dry_run)
    if force or not was_cached:
        os.chmod(cached_package_path, 0o775)
        if not dry_run:
            subprocess.run([cached_package_path, '--appimage-extract'])
        else:
            print(f'Would install package: {cached_package_path}')


def configure_fonts(dry_run: bool) -> None:
    cache_dir = pathlib.Path(os.environ.get(
        'XDG_CACHE_HOME', pathlib.Path.home() / '.cache')) / 'fonts'
    cache_dir.mkdir(parents=True, exist_ok=True)
    ubuntu_zip = cache_dir / 'Ubuntu_v3.1.1.zip'
    ubuntu_mono_zip = cache_dir / 'UbuntuMono_v3.1.1.zip'
    zip_files = [ubuntu_zip, ubuntu_mono_zip]
    was_cached = True
    was_cached &= download_file(
        'https://github.com/ryanoasis/nerd-fonts/releases/download/v3.1.1/Ubuntu.zip',
        ubuntu_zip, dry_run=dry_run)
    was_cached &= download_file(
        'https://github.com/ryanoasis/nerd-fonts/releases/download/v3.1.1/UbuntuMono.zip',
        ubuntu_mono_zip, dry_run=dry_run)
    font_dir = pathlib.Path(os.environ.get(
        'XDG_DATA_HOME', pathlib.Path.home() / '.local/share')) / 'fonts'
    font_dir.mkdir(parents=True, exist_ok=True)
    if not was_cached:
        # Unzip into font_dir
        for zip_file in zip_files:
            if not dry_run:
                subprocess.run(['unzip', '-qq', zip_file, '-d', font_dir])
            else:
                print(f'Would have unzipped: {zip_file} to {font_dir}')
        if not dry_run:
            subprocess.run(['fc-cache', '-fv'])
        else:
            print('Would have reset font cache')
    # Update gnome-tweaks
    if not dry_run:
        subprocess.run(['dconf', 'write',
                        '/org/gnome/desktop/interface/monospace-font-name',
                        '"UbuntuMono Nerd Font Mono 13"'])
    else:
        print('Would have changed monospace-font-name')


def miscellaneous_commands(dry_run: bool) -> None:
    DESCRIPTION_W_CMD = [
        ('alias nvim to vim',
         ['sudo', 'snap', 'alias', 'nvim', 'vim']),
        # NOTE: Requires reboot
        ('update locale for fonts',
         ['sudo', 'update-locale', 'LANG=en_US.UTF-8', 'LANGUAGE=en_US.UTF-8']),
    ]
    for description, cmd in DESCRIPTION_W_CMD:
        if not dry_run:
            subprocess.run(cmd)
        else:
            print(f'Would: {description}')


# Define APT repositories
APT_REPOSITORIES_WITH_URL = [
    # TODO(#30): Try out 8.0
    ('ppa:kicad/kicad-7.0-releases',
     'http://ppa.launchpad.net/kicad/kicad-7.0-releases/ubuntu'),
    ('ppa:fish-shell/release-3',
     'http://ppa.launchpad.net/fish-shell/release-3/ubuntu'),
    # syncthing, necessitates setting this up
    ('deb [signed-by=/etc/apt/keyrings/syncthing-archive-keyring.gpg] https://apt.syncthing.net/ syncthing stable',
     'https://apt.syncthing.net'),
    ('ppa:appimagelauncher-team/stable',
     'https://ppa.launchpadcontent.net/appimagelauncher-team/stable/ubuntu'),
    # github cli
    # XXX: Not quite working
    # ('deb [arch=amd64 signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main',
    #  'https://cli.github.com/packages'),
]

# Define packages to install from APT repositories
APT_PACKAGES = [
    # TODO: versions?
    # Maybe ctags and clang-format?
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
    # TODO(#33): Couldn't install
    # 'docker-ce',
    # 'docker-ce-cli',
    # 'containerd.io',
    # 'docker-buildx-plugin',
    # 'docker-compose-plugin',
    # # For rootless docker
    # 'uidmap',
    # 'dbus-user-session',
    # 'docker-ce-rootless-extras',
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
    # up/down workspace in Ubuntu
    'gnome-shell-extension-manager',
    # inotifywait, etc
    'inotify-tools',
    # obsidian app installed as appImage should be placed in favorites bar
    'appimagelauncher',
    # obsidian.nvim ObsidianPasteImage expects wl-paste
    'wl-clipboard',
    # dot / graphviz renderings
    'graphviz',
    # bambu video
    'gstreamer1.0-plugins-bad',
    # image editing
    'gimp',
    # github CLI for octo.nvim integration
    'gh',
    # kubectl
    'apt-transport-https',
    'ca-certificates',
    'curl',
    'gnupg',
]

SNAP_PACKAGES = [
    'nvim',
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
    # CKAN for KSP
    'https://github.com/KSP-CKAN/CKAN/releases/download/v1.34.4/ckan_1.34.4_all.deb',
    # Rescuetime
    'https://www.rescuetime.com/installers/rescuetime_current_amd64.deb',
    # obsidian
    'https://github.com/obsidianmd/obsidian-releases/releases/download/v1.5.8/obsidian_1.5.8_amd64.deb',
]

APP_IMAGES = [
    'https://github.com/bambulab/BambuStudio/releases/download/v01.09.00.70/Bambu_Studio_linux_ubuntu-v01.09.00.70.AppImage',
]


def main():
    parser = argparse.ArgumentParser(description="APT package management script")
    parser.add_argument('--dry-run', action='store_true', help="Show what would be done without actually doing it")
    parser.add_argument('--force', action='store_true', help="Re-install cached .deb even if already found")
    args = parser.parse_args()

    # Request sudo permissions if not running in dry-run mode
    if not args.dry_run:
        subprocess.run(['sudo', '-v'], check=True)

    # Download keyrings
    download_file(url='https://syncthing.net/release-key.gpg',
                  path=pathlib.Path('/etc/apt/keyrings/syncthing-archive-keyring.gpg'),
                  dry_run=args.dry_run,
                  use_sudo=True)
    download_file(url='https://cli.github.com/packages/githubcli-archive-keyring.gpg',
                  path=pathlib.Path('/etc/apt/keyrings/githubcli-archive-keyring.gpg'),
                  dry_run=args.dry_run,
                  use_sudo=True)

    # Add APT repositories
    for repo, url in APT_REPOSITORIES_WITH_URL:
        add_apt_repository(repo, url=url, dry_run=args.dry_run)

    # Update APT
    # TODO: Takes a significant amount of time
    # update_apt(dry_run=args.dry_run)

    # Install packages from APT & SNAP repositories
    install_apt_packages(APT_PACKAGES, dry_run=args.dry_run)
    install_snap_packages(SNAP_PACKAGES, dry_run=args.dry_run)

    # Download and install other packages
    for package in OTHER_PACKAGES:
        download_and_install_package(package, dry_run=args.dry_run,
                                     force=args.force)
    # Download and install AppImages
    for app_image in APP_IMAGES:
        download_and_install_app_image(app_image, dry_run=args.dry_run,
                                       force=args.force)

    configure_fonts(dry_run=args.dry_run)
    # Do other miscellaneous_commands
    miscellaneous_commands(dry_run=args.dry_run)


if __name__ == '__main__':
    main()
