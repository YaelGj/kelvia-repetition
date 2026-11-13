#!/usr/bin/env bash
# Installe les outils du cours aux versions figées, à la création du codespace.
set -euo pipefail
pip install -r requirements.txt ansible-core==2.21.6
ansible-galaxy collection install community.docker==5.4.0
