#!/usr/bin/env bash
set -euo pipefail
printf '\n[OSMEDEUS LAB] Verificación de entorno\n'
docker --version
docker compose version
printf '\n[OSMEDEUS LAB] Servicios esperados\n'
docker compose ps
printf '\n[OSMEDEUS LAB] Resolución DNS interna desde student-console\n'
docker compose exec -T student-console sh -lc 'dig +short web-alpha.lab && dig +short web-beta.lab && dig +short blog-gamma.lab'
