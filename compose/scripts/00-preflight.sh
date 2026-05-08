#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/_osmedeus-common.sh"
require_compose_dir
printf '\n[OSMEDEUS LAB] Verificación de entorno\n'
docker --version
docker compose version
printf '\n[OSMEDEUS LAB] Levantando servicios del laboratorio\n'
docker compose up -d --build
printf '\n[OSMEDEUS LAB] Servicios esperados\n'
docker compose ps
ensure_osmedeus_running
printf '\n[OSMEDEUS LAB] Logs iniciales de osmedeus runner\n'
docker compose logs --tail=30 osmedeus
printf '\n[OSMEDEUS LAB] Resolución DNS interna desde student-console\n'
docker compose exec -T student-console sh -lc 'dig +short web-alpha.lab && dig +short web-beta.lab && dig +short blog-gamma.lab && dig +short console.osmedeus.lab'
printf '\n[OSMEDEUS LAB] Verificación CLI desde el nodo osmedeus\n'
osmedeus_exec osmedeus --help | sed -n '1,60p'
ensure_osmedeus_web_running
printf '\n[OSMEDEUS LAB] Verificación HTTP de la consola web\n'
docker compose exec -T osmedeus-server sh -lc 'curl -sf http://localhost:8002/server-info | sed -n "1,40p"'
printf '\n[OSMEDEUS LAB] Consola web: http://127.0.0.1:%s | usuario: admin | contraseña: osmedeus-lab-admin\n' "${OSMEDEUS_WEB_PORT:-8002}"
