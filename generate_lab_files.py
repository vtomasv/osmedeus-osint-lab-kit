from pathlib import Path
import textwrap

ROOT = Path('/home/ubuntu/osmedeus-lab-kit')
C = ROOT / 'compose'

def w(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding='utf-8')

w(C / 'docker-compose.yml', r'''

    name: osmedeus-osint-lab

    services:
      local-dns:
        image: coredns/coredns:1.11.3
        container_name: osint-local-dns
        command: -conf /etc/coredns/Corefile
        volumes:
          - ./dns/Corefile:/etc/coredns/Corefile:ro
          - ./dns/lab.zone:/zones/lab.zone:ro
        networks:
          osint-lab:
            ipv4_address: 172.28.0.53
        restart: unless-stopped

      web-alpha:
        image: nginx:1.27-alpine
        container_name: web-alpha.lab
        volumes:
          - ./targets/web-alpha:/usr/share/nginx/html:ro
        networks:
          osint-lab:
            ipv4_address: 172.28.0.11
            aliases:
              - web-alpha.lab
              - alpha.academy.lab
        labels:
          lab.role: "web-target"
          lab.level: "basic"

      web-beta:
        image: nginx:1.27-alpine
        container_name: web-beta.lab
        volumes:
          - ./targets/web-beta:/usr/share/nginx/html:ro
        networks:
          osint-lab:
            ipv4_address: 172.28.0.12
            aliases:
              - web-beta.lab
              - beta.academy.lab
        labels:
          lab.role: "web-target"
          lab.level: "intermediate"

      blog-gamma:
        image: nginx:1.27-alpine
        container_name: blog-gamma.lab
        volumes:
          - ./targets/blog-gamma:/usr/share/nginx/html:ro
        networks:
          osint-lab:
            ipv4_address: 172.28.0.13
            aliases:
              - blog-gamma.lab
              - gamma.academy.lab
        labels:
          lab.role: "blog-target"
          lab.level: "intermediate"

      mail-delta:
        image: mailhog/mailhog:v1.0.1
        container_name: mail-delta.lab
        networks:
          osint-lab:
            ipv4_address: 172.28.0.14
            aliases:
              - mail-delta.lab
              - smtp.academy.lab
        labels:
          lab.role: "mail-target"
          lab.level: "advanced"

      student-console:
        build:
          context: ./student-console
        container_name: student-console
        dns:
          - 172.28.0.53
        depends_on:
          - local-dns
          - web-alpha
          - web-beta
          - blog-gamma
          - mail-delta
        volumes:
          - ./reports:/lab/reports
          - ./scripts:/lab/scripts:ro
        working_dir: /lab
        command: sleep infinity
        networks:
          osint-lab:
            ipv4_address: 172.28.0.100
        labels:
          lab.role: "analyst-workstation"

      osmedeus:
        image: j3ssie/osmedeus:latest
        container_name: osmedeus-runner
        dns:
          - 172.28.0.53
        depends_on:
          - local-dns
          - web-alpha
          - web-beta
          - blog-gamma
          - mail-delta
        volumes:
          - osmedeus-base:/root/osmedeus-base
          - osmedeus-workspaces:/root/workspaces-osmedeus
          - ./reports:/reports
          - ./scripts:/lab/scripts:ro
          - ./targets.txt:/lab/targets.txt:ro
          - ./osmedeus/workflows:/root/osmedeus-base/workflows/lab:ro
          - ./osmedeus/osm-settings.lab.yaml:/root/osmedeus-base/osm-settings.yaml:ro
        # La imagen oficial define ENTRYPOINT ["osmedeus"]. Para que el laboratorio
        # quede disponible para `docker compose exec`, se reemplaza por un proceso
        # pasivo y estable, sin mezclar /bin/sh -c con command multiline.
        entrypoint: ["tail", "-f", "/dev/null"]
        healthcheck:
          test: ["CMD-SHELL", "command -v osmedeus >/dev/null 2>&1"]
          interval: 20s
          timeout: 5s
          retries: 5
          start_period: 20s
        restart: unless-stopped
        networks:
          osint-lab:
            ipv4_address: 172.28.0.10
            aliases:
              - osmedeus.lab
        labels:
          lab.role: "osmedeus-runner"

      redis:
        image: redis:7-alpine
        container_name: osmedeus-lab-redis
        command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
        volumes:
          - osmedeus-redis-data:/data
        healthcheck:
          test: ["CMD", "redis-cli", "ping"]
          interval: 10s
          timeout: 5s
          retries: 5
        restart: unless-stopped
        networks:
          osint-lab:
            ipv4_address: 172.28.0.20
            aliases:
              - redis.lab
        labels:
          lab.role: "osmedeus-queue"

      osmedeus-server:
        image: j3ssie/osmedeus:latest
        container_name: osmedeus-web
        dns:
          - 172.28.0.53
        depends_on:
          redis:
            condition: service_healthy
          local-dns:
            condition: service_started
          web-alpha:
            condition: service_started
          web-beta:
            condition: service_started
          blog-gamma:
            condition: service_started
          mail-delta:
            condition: service_started
        ports:
          - "127.0.0.1:${OSMEDEUS_WEB_PORT:-8002}:8002"
        volumes:
          - osmedeus-base:/root/osmedeus-base
          - osmedeus-workspaces:/root/workspaces-osmedeus
          - ./reports:/reports
          - ./scripts:/lab/scripts:ro
          - ./targets.txt:/lab/targets.txt:ro
          - ./osmedeus/workflows:/root/osmedeus-base/workflows/lab:ro
          - ./osmedeus/osm-settings.lab.yaml:/root/osmedeus-base/osm-settings.yaml:ro
        command: ["serve", "--master", "--redis-url", "redis://redis:6379"]
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
          interval: 30s
          timeout: 10s
          start_period: 30s
          retries: 5
        restart: unless-stopped
        networks:
          osint-lab:
            ipv4_address: 172.28.0.21
            aliases:
              - osmedeus-web.lab
              - console.osmedeus.lab
        labels:
          lab.role: "osmedeus-web-console"
          lab.exposed_port: "8002"

      osmedeus-worker:
        image: j3ssie/osmedeus:latest
        container_name: osmedeus-worker
        dns:
          - 172.28.0.53
        depends_on:
          redis:
            condition: service_healthy
          osmedeus-server:
            condition: service_healthy
          local-dns:
            condition: service_started
        volumes:
          - osmedeus-base:/root/osmedeus-base
          - osmedeus-workspaces:/root/workspaces-osmedeus
          - ./reports:/reports
          - ./scripts:/lab/scripts:ro
          - ./targets.txt:/lab/targets.txt:ro
          - ./osmedeus/workflows:/root/osmedeus-base/workflows/lab:ro
          - ./osmedeus/osm-settings.lab.yaml:/root/osmedeus-base/osm-settings.yaml:ro
        command: ["worker", "join", "--redis-url", "redis://redis:6379"]
        restart: unless-stopped
        networks:
          osint-lab:
            ipv4_address: 172.28.0.22
            aliases:
              - osmedeus-worker.lab
        labels:
          lab.role: "osmedeus-worker"

    networks:
      osint-lab:
        driver: bridge
        ipam:
          config:
            - subnet: 172.28.0.0/24

    volumes:
      osmedeus-base:
      osmedeus-workspaces:
      osmedeus-redis-data:
''')

w(C / 'student-console/Dockerfile', r'''
    FROM alpine:3.20
    RUN apk add --no-cache bash curl bind-tools jq nmap nmap-scripts tree ca-certificates openssl
    WORKDIR /lab
    CMD ["sleep", "infinity"]
''')

w(C / 'dns/Corefile', r'''
    lab:53 {
        file /zones/lab.zone lab
        log
        errors
    }

    .:53 {
        forward . 1.1.1.1 8.8.8.8
        cache 30
        log
        errors
    }
''')

w(C / 'dns/lab.zone', r'''

    $ORIGIN lab.
    $TTL 60
    @       IN SOA  local-dns.lab. admin.lab. (2026050802 60 30 120 60)
            IN NS   local-dns.lab.
    local-dns       IN A 172.28.0.53
    osmedeus        IN A 172.28.0.10
    redis           IN A 172.28.0.20
    osmedeus-web    IN A 172.28.0.21
    console.osmedeus IN A 172.28.0.21
    osmedeus-worker IN A 172.28.0.22
    web-alpha       IN A 172.28.0.11
    alpha.academy   IN A 172.28.0.11
    web-beta        IN A 172.28.0.12
    beta.academy    IN A 172.28.0.12
    blog-gamma      IN A 172.28.0.13
    gamma.academy   IN A 172.28.0.13
    mail-delta      IN A 172.28.0.14
    smtp.academy    IN A 172.28.0.14
    student-console IN A 172.28.0.100
''')

w(C / 'targets.txt', r'''
    web-alpha.lab
    web-beta.lab
    blog-gamma.lab
''')

site_common = '''
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<style>
:root { color-scheme: dark; --bg:#11140f; --ink:#f0ead8; --green:#8df36b; --amber:#d9a441; --muted:#9aa38d; }
body { margin:0; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; background: var(--bg); color: var(--ink); }
main { max-width: 920px; margin: 0 auto; padding: 48px 24px; }
.badge { display:inline-block; border:1px solid var(--amber); color:var(--amber); padding:4px 8px; letter-spacing:.08em; text-transform:uppercase; }
h1 { font-size: clamp(2rem, 6vw, 4rem); line-height:.95; max-width: 760px; }
a { color: var(--green); }
.card { border:1px solid rgba(240,234,216,.28); padding:20px; margin:18px 0; background:rgba(255,255,255,.035); }
code { color: var(--green); }
small, .muted { color: var(--muted); }
</style>
'''

w(C / 'targets/web-alpha/index.html', f'''
    <!doctype html><html lang="es"><head>{site_common}<title>web-alpha.lab</title></head><body><main>
    <span class="badge">LAB BASIC TARGET</span>
    <h1>web-alpha.lab</h1>
    <p>Este objetivo ficticio representa un sitio institucional simple para practicar descubrimiento HTTP, revisión de cabeceras, lectura de robots.txt y documentación de evidencia.</p>
    <section class="card"><h2>Rutas de práctica</h2><p><a href="/about.html">/about.html</a> · <a href="/robots.txt">/robots.txt</a> · <a href="/.well-known/security.txt">/.well-known/security.txt</a></p></section>
    <section class="card"><h2>Regla pedagógica</h2><p>No hay datos reales. Todo hallazgo debe reportarse como evidencia de laboratorio y no como vulnerabilidad real.</p></section>
    </main></body></html>
''')

w(C / 'targets/web-alpha/about.html', f'''
    <!doctype html><html lang="es"><head>{site_common}<title>Acerca de Alpha</title></head><body><main>
    <span class="badge">PUBLIC INFO</span><h1>Academia Alpha</h1><p>Unidad ficticia de capacitación. Versión de contenido: 1.0. Contacto simulado: training@web-alpha.lab.</p>
    <div class="card"><p>Objetivo de aprendizaje: diferenciar información pública, metadatos y conclusiones inferidas.</p></div>
    </main></body></html>
''')

w(C / 'targets/web-alpha/robots.txt', 'User-agent: *\nDisallow: /private-lab-not-real/\nAllow: /\n')
w(C / 'targets/web-alpha/.well-known/security.txt', 'Contact: mailto:security@web-alpha.lab\nPolicy: https://web-alpha.lab/policy\nExpires: 2027-12-31T00:00:00Z\n')

w(C / 'targets/web-beta/index.html', f'''
    <!doctype html><html lang="es"><head>{site_common}<title>web-beta.lab</title></head><body><main>
    <span class="badge">LAB INTERMEDIATE TARGET</span><h1>web-beta.lab</h1>
    <p>Servicio ficticio con señales tecnológicas y rutas de contenido para practicar correlación responsable sin explotación.</p>
    <section class="card"><h2>Señales públicas</h2><p>Header simulado en contenido: <code>X-Lab-Stack: nginx/static/cms-mock</code>. Ruta: <a href="/changelog.html">/changelog.html</a>.</p></section>
    <section class="card"><h2>Interpretación</h2><p>El alumno debe separar observación verificable, hipótesis y recomendación defensiva.</p></section>
    </main></body></html>
''')

w(C / 'targets/web-beta/changelog.html', f'''
    <!doctype html><html lang="es"><head>{site_common}<title>Changelog Beta</title></head><body><main>
    <span class="badge">CHANGELOG</span><h1>Registro de cambios</h1><div class="card"><p>2026-05-01: actualización de plantilla educativa. 2026-04-10: se agregó página de mantenimiento ficticia.</p></div>
    </main></body></html>
''')
w(C / 'targets/web-beta/robots.txt', 'User-agent: *\nDisallow: /staging-note-fictional/\n')

w(C / 'targets/blog-gamma/index.html', f'''
    <!doctype html><html lang="es"><head>{site_common}<title>blog-gamma.lab</title></head><body><main>
    <span class="badge">BLOG TARGET</span><h1>blog-gamma.lab</h1>
    <p>Blog ficticio para enseñar enumeración de contenidos públicos y construcción de un inventario de activos.</p>
    <section class="card"><h2>Entradas</h2><p><a href="/post-osint.html">Buenas prácticas OSINT responsable</a> · <a href="/feed.xml">feed.xml</a></p></section>
    </main></body></html>
''')

w(C / 'targets/blog-gamma/post-osint.html', f'''
    <!doctype html><html lang="es"><head>{site_common}<title>Post Gamma</title></head><body><main>
    <span class="badge">PUBLIC BLOG</span><h1>Buenas prácticas OSINT responsable</h1><p>Este texto ficticio recuerda que la automatización debe respetar autorización, minimización y reproducibilidad.</p>
    </main></body></html>
''')
w(C / 'targets/blog-gamma/feed.xml', '<?xml version="1.0"?><rss version="2.0"><channel><title>Gamma Lab</title><item><title>OSINT responsable</title><link>https://blog-gamma.lab/post-osint.html</link></item></channel></rss>')



w(C / 'osmedeus/osm-settings.lab.yaml', r'''

    # Configuración local del laboratorio Osmedeus OSINT.
    # No reutilizar estas credenciales en producción: están pensadas para docencia local.

    # Osmedeus actual resuelve rutas desde `environments`. Se mantiene además
    # `environment` como bloque de compatibilidad para imágenes antiguas que aún lo lean.
    environments:
      external_binaries_path: "/root/osmedeus-base/external-binaries"
      external_data: "/root/osmedeus-base/external-data"
      external_configs: "/root/osmedeus-base/external-configs"
      workspaces: /root/workspaces-osmedeus
      workflows: "/root/osmedeus-base/workflows"
      snapshot: "/root/osmedeus-base/snapshot"
      markdown_report_templates: "/root/osmedeus-base/markdown-templates"
      external_agent_configs: "/root/osmedeus-base/agents"
      external_scripts: "/root/osmedeus-base/scripts"

    environment:
      binaries: "/root/osmedeus-base/external-binaries"
      external_data: "/root/osmedeus-base/external-data"
      external_configs: "/root/osmedeus-base/external-configs"
      workspaces: /root/workspaces-osmedeus
      workflows: "/root/osmedeus-base/workflows"
      snapshot: "/root/osmedeus-base/snapshot"

    database:
      db_engine: sqlite
      db_path: "/root/osmedeus-base/database-osm.sqlite"
      connection_timeout: 60

    server:
      host: "0.0.0.0"
      port: 8002
      ui_path: "/root/osmedeus-base/ui/"
      workspace_prefix_key: "lab-workspaces"
      enabled_auth_api: true
      auth_api_key: "osmedeus-lab-api-key-change-me"
      simple_user_map_key:
        admin: "osmedeus-lab-admin"
      jwt:
        secret_signing_key: "osmedeus-lab-jwt-secret-change-me-2026"
        expiration_minutes: 1440

    scan_tactic:
      aggressive: 20
      default: 8
      gently: 3

    redis:
      host: redis
      port: 6379
      username: ""
      password: ""
      db: 0
      connection_timeout: 60

    global_vars:
      custom_vars: []

    global_variables: []

    notification:
      telegram:
        enabled: false
        bot_token: ""
        chat_id: 0

    storage:
      enabled: false
      access_key_id: ""
      secret_access_key: ""
      bucket: ""
      region: ""
      endpoint: ""

    cdn_storage:
      enabled: false
      access_key_id: ""
      secret_access_key: ""
      bucket: ""
      region: ""
      endpoint: ""

    llm_config:
      enabled_tool_call: false
      llm_providers: []

    llm:
      enabled: false
      provider: openai
      api_key: ""
      model: "gpt-4"
      base_url: ""
''')
w(C / 'osmedeus/workflows/README.md', r'''
    # Workflows locales del laboratorio

    Esta carpeta queda montada dentro de `/root/osmedeus-base/workflows/lab` para que el instructor pueda agregar workflows YAML revisados. Por seguridad, la receta principal usa workflows oficiales de Osmedeus y comandos `--dry-run` antes de cualquier ejecución real.

    Antes de usar workflows de terceros, se debe revisar el YAML completo. El repositorio oficial advierte que Osmedeus puede ejecutar comandos arbitrarios desde workflows y entradas de usuario, por lo que la revisión previa es parte obligatoria del ejercicio.
''')

scripts = {
'_osmedeus-common.sh': r'''
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

osmedeus_exec() {
  ensure_osmedeus_running
  docker compose exec -T osmedeus "$@"
}
''',
'00-preflight.sh': r'''
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
''',
'01-basic-dry-run.sh': r'''
#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/_osmedeus-common.sh"
printf '\n[01] Básico: listar ayuda y previsualizar workflow sin ejecutar escaneo real\n'
osmedeus_exec osmedeus --help | sed -n '1,80p'
printf '\n[01] Dry-run contra dominio ficticio interno\n'
osmedeus_exec osmedeus run -f general -t web-alpha.lab --dry-run | tee reports/basic-dry-run-web-alpha.log
''',
'02-lab-scan-alpha.sh': r'''
#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/_osmedeus-common.sh"
printf '\n[02] Medio: ejecutar workflow general controlado contra web-alpha.lab\n'
printf '[ALCANCE] Solo red Docker interna. No usar contra terceros.\n'
osmedeus_exec osmedeus run -f general -t web-alpha.lab -x portscan -X vuln | tee reports/lab-scan-web-alpha.log
''',
'03-intermediate-multi-target.sh': r'''
#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/_osmedeus-common.sh"
printf '\n[03] Medio: múltiples objetivos internos con targets.txt\n'
osmedeus_exec osmedeus run -m recon -T /lab/targets.txt --concurrency 2 --dry-run | tee reports/intermediate-multi-target-dry-run.log
''',
'04-authorized-vtomasv.sh': r'''
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
''',
'05-export-report.sh': r'''
#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/_osmedeus-common.sh"
printf '\n[05] Exportar evidencias disponibles desde workspaces-osmedeus\n'
osmedeus_exec sh -lc 'find /root/workspaces-osmedeus -maxdepth 4 -type f | sed -n "1,120p"' | tee reports/workspace-files.txt
printf '\n[05] Resumen guardado en compose/reports/workspace-files.txt\n'
''',
'lab-demo.sh': r'''
#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/_osmedeus-common.sh"
printf '\n╔══════════════════════════════════════════════════════════════╗\n'
printf '║        OSMEDEUS OSINT LAB · DEMO DIDÁCTICA AUTORIZADA       ║\n'
printf '╚══════════════════════════════════════════════════════════════╝\n\n'
printf '[0] Levantando laboratorio...\n'
docker compose up -d --build
ensure_osmedeus_running
printf '\n[1] Preflight...\n'
./scripts/00-preflight.sh
printf '\n[2] Ejercicio básico dry-run...\n'
./scripts/01-basic-dry-run.sh || true
printf '\n[3] Ejercicio vtomasv.net en modo dry-run...\n'
./scripts/04-authorized-vtomasv.sh || true
printf '\n[FIN] Revise compose/reports/ y workspaces de Osmedeus.\n'
''',
}
for name, content in scripts.items():
    p = C / 'scripts' / name
    w(p, content)
    p.chmod(0o755)

w(ROOT / 'examples/basic/README.md', r'''
    # Nivel básico: observar antes de ejecutar

    El objetivo de este nivel es que el alumno comprenda la diferencia entre levantar el laboratorio, resolver dominios ficticios y previsualizar un workflow de Osmedeus con `--dry-run`. El comando principal es:

    ```bash
    cd compose
    docker compose up -d --build
    ./scripts/01-basic-dry-run.sh
    ```

    El resultado esperado no es “encontrar vulnerabilidades”, sino entender qué pasos intentaría ejecutar Osmedeus y dónde quedaría la evidencia.
''')

w(ROOT / 'examples/intermediate/README.md', r'''
    # Nivel medio: múltiples objetivos y lectura de evidencias

    Este nivel usa `targets.txt` para mostrar cómo separar objetivos internos y controlar la concurrencia. Se recomienda ejecutar primero en modo `--dry-run` y después revisar los logs antes de cualquier ejecución real.

    ```bash
    cd compose
    ./scripts/03-intermediate-multi-target.sh
    ```

    La discusión en clase debe centrarse en alcance, trazabilidad, reproducibilidad y falsos positivos.
''')

w(ROOT / 'examples/advanced/README.md', r'''
    # Nivel complejo: workflow autorizado externo

    Este nivel ilustra un flujo responsable contra `vtomasv.net`, dominio indicado por Tom como sitio personal autorizado. Por defecto el script solo ejecuta `--dry-run`. Para una ejecución real no intrusiva de subdomain enumeration, el instructor debe habilitar explícitamente `RUN_REAL=1`.

    ```bash
    cd compose
    ./scripts/04-authorized-vtomasv.sh
    RUN_REAL=1 ./scripts/04-authorized-vtomasv.sh
    ```

    La actividad debe registrar autorización, fecha, objetivo exacto, comandos usados, resultados y limitaciones.
''')

w(ROOT / 'legal/chile-osint-notas.md', r'''
    # Notas legales para Chile en ejercicios OSINT

    Este laboratorio es material educativo y no constituye asesoría legal. En Chile, los ejercicios de OSINT y seguridad deben realizarse con autorización previa, alcance documentado y minimización de datos. Para clases y laboratorios, se recomienda trabajar con dominios propios, objetivos ficticios o servicios preparados por el instructor.

    La metodología debe evitar acceso no autorizado, evasión de controles, extracción de datos personales innecesarios, explotación, persistencia o afectación de disponibilidad. Si se analizan dominios reales, debe existir permiso expreso del titular o responsable del sistema, y el informe debe separar observaciones técnicas de afirmaciones no verificadas.

    En informes para alumnos, incluya una sección de alcance, autorización, fecha, herramientas, limitaciones, tratamiento de datos, hallazgos reproducibles y recomendaciones defensivas. Si aparecen datos personales, se deben anonimizar y conservar solo si son estrictamente necesarios para el objetivo pedagógico.
''')

w(ROOT / 'README.md', r'''
    # Laboratorio Didáctico Osmedeus OSINT

    Este kit entrega una receta Docker Compose para enseñar el uso responsable de Osmedeus en un entorno autocontenido. Incluye dominios ficticios `.lab`, servicios internos, un contenedor `osmedeus-runner`, una consola de alumno y scripts por nivel.

    ## Inicio rápido

    ```bash
    cd compose
    docker compose up -d --build
    ./scripts/lab-demo.sh
    ```

    ## Topología

    | Servicio | Dominio ficticio | IP interna | Propósito pedagógico |
    |---|---:|---:|---|
    | osmedeus | osmedeus.lab | 172.28.0.10 | Ejecutar workflows de Osmedeus |
    | web-alpha | web-alpha.lab | 172.28.0.11 | Objetivo web básico |
    | web-beta | web-beta.lab | 172.28.0.12 | Objetivo web intermedio |
    | blog-gamma | blog-gamma.lab | 172.28.0.13 | Inventario de contenido público |
    | mail-delta | mail-delta.lab | 172.28.0.14 | Servicio de correo ficticio |
    | local-dns | local-dns.lab | 172.28.0.53 | Resolución DNS `.lab` |
    | student-console | student-console.lab | 172.28.0.100 | Puesto de trabajo del alumno |

    ## Flujo autorizado externo

    El script `scripts/04-authorized-vtomasv.sh` prepara un flujo contra `vtomasv.net`, indicado por Tom como sitio personal autorizado. Por seguridad, el script ejecuta `--dry-run` por defecto y solo realiza ejecución real si se define `RUN_REAL=1`.

    ## Regla de oro

    Use Osmedeus únicamente contra activos propios, laboratorios o objetivos donde exista autorización explícita. Revise workflows antes de ejecutarlos porque Osmedeus puede orquestar comandos definidos en YAML.
''')

print(f'Archivos generados en {ROOT}')
