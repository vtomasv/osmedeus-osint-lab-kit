#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/_osmedeus-common.sh"
printf '\n[01] Básico: listar ayuda y previsualizar workflow sin ejecutar escaneo real\n'
osmedeus_exec osmedeus --help | sed -n '1,80p'
printf '\n[01] Dry-run contra dominio ficticio interno\n'
osmedeus_exec osmedeus run -f general -t web-alpha.lab --dry-run | tee reports/basic-dry-run-web-alpha.log
