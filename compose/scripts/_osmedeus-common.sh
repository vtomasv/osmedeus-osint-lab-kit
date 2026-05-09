#!/usr/bin/env bash
set -euo pipefail

require_compose_dir() {
  if [ ! -f "docker-compose.yml" ]; then
    printf '\n[ERROR] Este script debe ejecutarse desde la carpeta compose/.\n' >&2
    printf 'Ejemplo: cd compose && ./scripts/00-preflight.sh\n' >&2
    exit 2
  fi
}

ensure_osmedeus_running() {
  require_compose_dir
  printf '\n[OSMEDEUS LAB] Asegurando que el nodo osmedeus esté levantado...\n'
  docker compose up -d osmedeus >/dev/null

  local cid state
  cid="$(docker compose ps -q osmedeus || true)"
  if [ -z "$cid" ]; then
    printf '[ERROR] Docker Compose no devolvió contenedor para el servicio osmedeus.\n' >&2
    docker compose ps >&2 || true
    exit 1
  fi

  for _ in $(seq 1 20); do
    state="$(docker inspect -f '{{.State.Running}}' "$cid" 2>/dev/null || echo false)"
    if [ "$state" = "true" ]; then
      printf '[OK] Servicio osmedeus corriendo en contenedor %s\n' "$cid"
      return 0
    fi
    sleep 1
  done

  printf '\n[ERROR] El servicio osmedeus no quedó corriendo. Últimos logs:\n' >&2
  docker compose logs --tail=80 osmedeus >&2 || true
  printf '\n[DIAGNÓSTICO] Pruebe: docker compose pull osmedeus && docker compose up -d osmedeus && docker compose logs -f osmedeus\n' >&2
  exit 1
}

ensure_osmedeus_web_running() {
  require_compose_dir
  printf '\n[OSMEDEUS LAB] Asegurando consola web Osmedeus, Redis y worker...\n'
  docker compose up -d redis osmedeus-server osmedeus-worker >/dev/null

  for _ in $(seq 1 40); do
    if docker compose exec -T osmedeus-server sh -lc 'curl -sf http://localhost:8002/health >/dev/null' 2>/dev/null; then
      docker compose exec -T osmedeus-server sh -lc 'grep -q "^environments:" /root/osmedeus-base/osm-settings.yaml && test -d /root/osmedeus-base/workflows' >/dev/null
      printf '[OK] Consola web Osmedeus disponible en http://127.0.0.1:%s\n' "${OSMEDEUS_WEB_PORT:-8002}"
      printf '[OK] Settings contiene environments y workflows está montado en /root/osmedeus-base/workflows\n'
      printf '[INFO] Usuario local: admin | contraseña: osmedeus-lab-admin\n'
      return 0
    fi
    sleep 2
  done

  printf '\n[ERROR] La consola web Osmedeus no respondió /health. Últimos logs:\n' >&2
  docker compose logs --tail=120 redis osmedeus-server osmedeus-worker >&2 || true
  printf '\n[DIAGNÓSTICO] Pruebe: docker compose rm -sf osmedeus-server osmedeus-worker && docker compose up -d redis osmedeus-server osmedeus-worker && docker compose logs -f osmedeus-server\n' >&2
  exit 1
}

osmedeus_exec() {
  ensure_osmedeus_running
  docker compose exec -T osmedeus "$@"
}
