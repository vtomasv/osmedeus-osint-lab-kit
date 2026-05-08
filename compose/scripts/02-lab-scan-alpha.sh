#!/usr/bin/env bash
set -euo pipefail
printf '\n[02] Medio: ejecutar workflow general controlado contra web-alpha.lab\n'
printf '[ALCANCE] Solo red Docker interna. No usar contra terceros.\n'
docker compose exec -T osmedeus osmedeus run -f general -t web-alpha.lab -x portscan -X vuln | tee reports/lab-scan-web-alpha.log
