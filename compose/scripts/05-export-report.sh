#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/_osmedeus-common.sh"
printf '\n[05] Exportar evidencias disponibles desde workspaces-osmedeus\n'
osmedeus_exec sh -lc 'find /root/workspaces-osmedeus -maxdepth 4 -type f | sed -n "1,120p"' | tee reports/workspace-files.txt
printf '\n[05] Resumen guardado en compose/reports/workspace-files.txt\n'
