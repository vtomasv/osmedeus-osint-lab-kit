#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/_osmedeus-common.sh"
require_compose_dir
printf '\n[OSMEDEUS LAB] Verificación de entorno\n'
docker --version
docker compose version
printf '\n[OSMEDEUS LAB] Levantando servicios mínimos del laboratorio\n'
docker compose up -d --build
printf '\n[OSMEDEUS LAB] Servicios esperados\n'
docker compose ps
ensure_osmedeus_running
printf '\n[OSMEDEUS LAB] Logs iniciales de osmedeus\n'
docker compose logs --tail=30 osmedeus
printf '\n[OSMEDEUS LAB] Resolución DNS interna desde student-console\n'
docker compose exec -T student-console sh -lc 'dig +short web-alpha.lab && dig +short web-beta.lab && dig +short blog-gamma.lab'
printf '\n[OSMEDEUS LAB] Verificación CLI desde el nodo osmedeus\n'
osmedeus_exec osmedeus --help | sed -n '1,60p'
