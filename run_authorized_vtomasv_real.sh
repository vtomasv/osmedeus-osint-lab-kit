#!/usr/bin/env bash
set -u
BIN="/home/ubuntu/osmedeus-bin/osmedeus"
OUT="/home/ubuntu/osmedeus-lab-kit/console/vtomasv-enum-subdomain-real-rerun.log"
STATUS="/home/ubuntu/osmedeus-lab-kit/console/vtomasv-enum-subdomain-real-rerun.status"
mkdir -p /home/ubuntu/osmedeus-lab-kit/console
rm -f "$OUT" "$STATUS"
{
  echo "# Ejecución real autorizada de Osmedeus"
  echo "fecha=$(date -Iseconds)"
  echo "binario=$BIN"
  echo "target=vtomasv.net"
  echo "workflow=enum-subdomain"
  echo
  echo "## versión"
  "$BIN" version --disable-color 2>&1 || true
  echo
  echo "## ejecución"
} | tee -a "$OUT"
# Se acota externamente para evitar procesos prolongados en entornos de clase.
timeout 150s "$BIN" run -m enum-subdomain -t vtomasv.net --timeout 2m --disable-color 2>&1 | tee -a "$OUT"
code=${PIPESTATUS[0]}
echo "exit_code=$code" | tee "$STATUS" | tee -a "$OUT"
exit 0
