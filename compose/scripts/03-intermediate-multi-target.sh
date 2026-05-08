#!/usr/bin/env bash
set -euo pipefail
printf '\n[03] Medio: múltiples objetivos internos con targets.txt\n'
docker compose exec -T osmedeus osmedeus run -m recon -T /lab/targets.txt --concurrency 2 --dry-run | tee reports/intermediate-multi-target-dry-run.log
