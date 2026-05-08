#!/usr/bin/env bash
set -euo pipefail
printf '\n[01] Básico: listar ayuda y previsualizar workflow sin ejecutar escaneo real\n'
docker compose exec -T osmedeus osmedeus --help | sed -n '1,80p'
printf '\n[01] Dry-run contra dominio ficticio interno\n'
docker compose exec -T osmedeus osmedeus run -f general -t web-alpha.lab --dry-run | tee reports/basic-dry-run-web-alpha.log
