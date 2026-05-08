#!/usr/bin/env bash
set -euo pipefail
printf '\n╔══════════════════════════════════════════════════════════════╗\n'
printf '║        OSMEDEUS OSINT LAB · DEMO DIDÁCTICA AUTORIZADA       ║\n'
printf '╚══════════════════════════════════════════════════════════════╝\n\n'
printf '[0] Levantando laboratorio...\n'
docker compose up -d --build
printf '\n[1] Preflight...\n'
./scripts/00-preflight.sh
printf '\n[2] Ejercicio básico dry-run...\n'
./scripts/01-basic-dry-run.sh || true
printf '\n[3] Ejercicio vtomasv.net en modo dry-run...\n'
./scripts/04-authorized-vtomasv.sh || true
printf '\n[FIN] Revise compose/reports/ y workspaces de Osmedeus.\n'
