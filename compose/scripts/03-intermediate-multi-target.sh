#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/_osmedeus-common.sh"
printf '\n[03] Medio: múltiples objetivos internos con targets.txt\n'
osmedeus_exec osmedeus run -m recon -T /lab/targets.txt --concurrency 2 --dry-run | tee reports/intermediate-multi-target-dry-run.log
