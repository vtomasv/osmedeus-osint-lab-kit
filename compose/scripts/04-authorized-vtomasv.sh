#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/_osmedeus-common.sh"
printf '\n[04] Externo autorizado: workflow responsable para vtomasv.net\n'
printf '[ALCANCE] Ejecutar solo si Tom confirma autorización sobre vtomasv.net.\n'
printf '[MODO] Primero se realiza dry-run. Para ejecución real, exportar RUN_REAL=1.\n\n'
osmedeus_exec osmedeus run -m enum-subdomain -t vtomasv.net --dry-run | tee reports/vtomasv-subdomain-dry-run.log
if [ "${RUN_REAL:-0}" = "1" ]; then
  printf '\n[04] RUN_REAL=1 detectado: ejecución real no intrusiva de subdomain.\n'
  osmedeus_exec osmedeus run -m enum-subdomain -t vtomasv.net --timeout 30m | tee reports/vtomasv-subdomain-real.log
else
  printf '\n[04] Ejecución real omitida. Use: RUN_REAL=1 ./scripts/04-authorized-vtomasv.sh\n'
fi
