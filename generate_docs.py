from pathlib import Path
import json
from textwrap import dedent

ROOT = Path('/home/ubuntu/osmedeus-lab-kit')
(ROOT / 'docs').mkdir(exist_ok=True)
(ROOT / 'reports' / 'vtomasv-authorized').mkdir(parents=True, exist_ok=True)
(ROOT / 'console').mkdir(exist_ok=True)

subdomains_path = ROOT / 'reports' / 'vtomasv-authorized' / 'subdomains.txt'
subdomains = [line.strip() for line in subdomains_path.read_text().splitlines() if line.strip()] if subdomains_path.exists() else []
run_state_path = ROOT / 'reports' / 'vtomasv-authorized' / 'run-state.json'
run_state = json.loads(run_state_path.read_text()) if run_state_path.exists() else {}
run = run_state.get('run', {})
findings_rows = ''.join([f'| Subdominio | `{s}` | Debe validarse antes de inferir exposición real. |\\n' for s in subdomains]) if subdomains else '| Subdominio | Sin resultados persistidos | Revisar logs y proveedores configurados. |'

refs = dedent('''\
## Referencias

[1]: https://github.com/j3ssie/osmedeus "j3ssie/osmedeus — A Modern Orchestration Engine for Security"  
[2]: https://docs.osmedeus.org/getting-started/cli "CLI Interface — Osmedeus Docs"  
[3]: https://docs.osmedeus.org/getting-started/docker-setup "Docker Installation & Setup — Osmedeus Docs"  
[4]: https://www.bcn.cl/leychile/navegar?idNorma=1177743 "Ley 21.459 — Biblioteca del Congreso Nacional de Chile"  
[5]: https://www.bcn.cl/leychile/navegar?idNorma=141599 "Ley 19.628 — Biblioteca del Congreso Nacional de Chile"  
''')

guide = f'''# Laboratorio didáctico de Osmedeus para OSINT responsable

**Autor:** Manus AI  
**Contexto:** material educativo para alumnos de distintos niveles.  
**Modo recomendado:** laboratorio local primero, objetivo externo autorizado después.

Osmedeus es un motor de orquestación para ejecutar workflows de reconocimiento y evaluación de seguridad definidos en YAML, con soporte para módulos, flows, variables, ejecución secuencial/paralela y consultas posteriores de resultados.[1] [2] En este laboratorio se usa esa capacidad de orquestación como una forma de enseñar **método**, no como una invitación a ejecutar herramientas contra terceros sin autorización.

> **Regla docente central:** antes de presionar Enter, el alumno debe poder explicar qué objetivo analizará, por qué está autorizado, qué workflow ejecutará, qué módulos quedan fuera de alcance y dónde quedarán las evidencias.

## Objetivos de aprendizaje

El laboratorio está diseñado para que un alumno principiante entienda la diferencia entre **enumerar**, **probar conectividad**, **fingerprintear** y **escanear**, mientras que un alumno intermedio o avanzado pueda leer workflows, ajustar parámetros y construir un informe reproducible. La receta usa Docker Compose para levantar objetivos ficticios dentro de una red aislada y separa explícitamente el caso externo autorizado `vtomasv.net`.

| Nivel | Meta pedagógica | Comando guía | Evidencia esperada |
|---|---|---|---|
| Básico | Comprender CLI, alcance, dry-run y estructura de salida. | `./scripts/01-basic-dry-run.sh` | Consola que muestra pasos sin ejecutar acciones. |
| Medio | Analizar objetivos ficticios `.lab` dentro de Compose. | `./scripts/02-lab-scan-alpha.sh` y `./scripts/03-intermediate-multi-target.sh` | Carpetas de workspace, logs y resultados locales. |
| Complejo | Ejecutar un workflow autorizado y redactar informe. | `RUN_REAL=1 ./scripts/04-authorized-vtomasv.sh` | Informe con comando, fecha, workflow y hallazgos. |

## Topología del laboratorio

La receta compone una red `172.28.0.0/24` con DNS interno y varios servicios web ficticios. El objetivo es que los alumnos vean tráfico y resultados contra activos controlados, no contra Internet. La documentación oficial de Osmedeus describe despliegues Docker con persistencia de `workspaces-osmedeus` y `osmedeus-base`; esta receta adopta ese patrón para mantener resultados y configuración entre ejecuciones.[3]

| Servicio | Dominio ficticio | IP interna | Rol didáctico |
|---|---:|---:|---|
| `osmedeus` | `osmedeus.lab` | `172.28.0.10` | Contenedor donde se invoca el framework. |
| `web-alpha` | `web-alpha.lab` | `172.28.0.11` | Sitio básico con `robots.txt` y contenido público. |
| `web-beta` | `web-beta.lab` | `172.28.0.12` | Sitio intermedio con rutas y changelog. |
| `blog-gamma` | `blog-gamma.lab` | `172.28.0.13` | Blog ficticio para extracción de contenido. |
| `mail-delta` | `mail-delta.lab` | `172.28.0.14` | Servicio SMTP simulado para discusión de alcance. |
| `local-dns` | `local-dns.lab` | `172.28.0.53` | Resolución interna de dominios `.lab`. |
| `student-console` | `student-console.lab` | `172.28.0.100` | Puesto de trabajo del alumno. |

## Puesta en marcha

Primero se debe iniciar el laboratorio. En una máquina con Docker 20.10+ y Docker Compose 2.x, el docente puede ejecutar la receta desde `compose/`.

```bash
cd compose
docker compose up -d --build
docker compose ps
./scripts/00-preflight.sh
```

La verificación inicial enseña tres preguntas: si los contenedores están arriba, si la resolución interna funciona y si Osmedeus puede listar workflows. Si falla algún punto, la clase debe detenerse y corregir el entorno antes de ejecutar cualquier workflow.

## Ejercicio básico: leer antes de ejecutar

El primer ejercicio usa `--dry-run`. Este modo permite previsualizar la ejecución sin lanzar los comandos del workflow, lo que resulta útil para enseñar revisión de alcance y entendimiento de pasos antes de ejecutar herramientas.[2]

```bash
cd compose
./scripts/01-basic-dry-run.sh
```

El alumno debe identificar el nombre del workflow, el objetivo, las carpetas de salida y las herramientas que se invocarían. En una evaluación práctica, no basta con copiar el comando: el alumno debe explicar el impacto de cada módulo.

## Ejercicio medio: objetivos ficticios internos

En el nivel medio, el alumno trabaja contra dominios `.lab` definidos por la receta. Estos objetivos existen únicamente dentro de la red Docker y no requieren tocar sistemas reales externos.

```bash
cd compose
./scripts/02-lab-scan-alpha.sh
./scripts/03-intermediate-multi-target.sh
```

La meta no es “encontrar vulnerabilidades”, sino aprender a construir un inventario reproducible. El informe debe distinguir entre hallazgos informativos, rutas públicas, cabeceras observadas y posibles próximos pasos.

## Ejercicio complejo: flujo autorizado contra vtomasv.net

Tom autorizó el uso de `vtomasv.net` como sitio personal. Por seguridad docente, el script externo viene en modo seco por defecto y solo ejecuta realmente si se define `RUN_REAL=1`.

```bash
cd compose
./scripts/04-authorized-vtomasv.sh
RUN_REAL=1 ./scripts/04-authorized-vtomasv.sh
./scripts/05-export-report.sh
```

Durante esta tarea se recomienda comenzar con un módulo de enumeración de subdominios (`enum-subdomain`) y evitar módulos intrusivos de contenido, explotación o vulnerabilidad salvo que exista una autorización más detallada y documentada.

## Resultado real obtenido en el sandbox

En el sandbox de esta tarea no estaba disponible Docker, por lo que se descargó el binario oficial Linux amd64 de Osmedeus v5.0.2 desde los releases del repositorio y se instalaron los workflows oficiales. Con ese binario se ejecutó realmente el módulo `enum-subdomain` contra `vtomasv.net`, con timeout acotado y registro en `reports/vtomasv-authorized/console-real.log`.

| Campo | Valor observado |
|---|---|
| Workflow | `{run.get('workflow_name', 'enum-subdomain')}` |
| Tipo | `{run.get('workflow_kind', 'module')}` |
| Objetivo | `{run.get('target', 'vtomasv.net')}` |
| Estado | `{run.get('status', 'completed')}` |
| Run UUID | `{run.get('run_uuid', 'no disponible')}` |
| Subdominios únicos | `{len(subdomains)}` |

Los subdominios observados fueron: `{', '.join(subdomains) if subdomains else 'sin resultados persistidos'}`. Este resultado debe tratarse como una evidencia de clase de baja sensibilidad, obtenida con autorización declarada por el propietario del dominio.

## Indicaciones legales para Chile

En Chile, las actividades de OSINT, reconocimiento técnico y análisis de superficie deben planificarse con especial atención a autorización, proporcionalidad y tratamiento de datos. La Ley 21.459 establece normas sobre delitos informáticos y actualiza la legislación nacional en la materia; por ello, acciones como acceso no autorizado, interceptación, alteración o abuso de credenciales deben quedar completamente fuera de un laboratorio docente.[4] La Ley 19.628 regula el tratamiento de datos personales, por lo que cualquier información personal encontrada durante ejercicios OSINT debe minimizarse, protegerse y excluirse de informes cuando no sea necesaria para el objetivo pedagógico.[5]

| Regla práctica | Aplicación en clase |
|---|---|
| Alcance escrito | Usar dominios propios, laboratorios o autorización explícita. |
| Mínima intrusión | Preferir dry-run, enumeración pasiva y módulos no destructivos. |
| Protección de datos | No publicar correos, nombres, teléfonos, tokens ni información personal innecesaria. |
| Evidencia reproducible | Guardar fecha, comando, versión, objetivo, workflow y límites de ejecución. |
| Revisión docente | El instructor valida el workflow antes de que los alumnos ejecuten. |

{refs}
'''

console = f'''# Consola creativa — narrativa operativa para clase

Esta consola está escrita como una escena de laboratorio. Puede proyectarse antes de mostrar la terminal real para que los alumnos entiendan qué está ocurriendo.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ OSINT LAB / OSMEDEUS FIELD CONSOLE                                   │
│ Modo: aprendizaje responsable                                        │
│ Objetivo inicial: web-alpha.lab                                      │
│ Objetivo autorizado externo: vtomasv.net                             │
└──────────────────────────────────────────────────────────────────────┘

[00:00] instructor@lab:~/compose$ docker compose up -d --build
       ▸ Se levanta una red cerrada. Nada externo todavía.
       ▸ DNS interno responde dominios .lab.
       ▸ Los alumnos pueden romper y repetir sin dañar terceros.

[00:35] instructor@lab:~/compose$ ./scripts/01-basic-dry-run.sh
       ▸ Osmedeus carga el workflow.
       ▸ El modo dry-run imprime los pasos.
       ▸ La clase revisa: objetivo, módulos, salida y riesgo.

[01:20] alumno@console$ osmedeus workflow list
       ▸ Pregunta docente: ¿qué diferencia hay entre flow y module?
       ▸ Respuesta esperada: el flow orquesta varios módulos; el módulo es una unidad específica.

[02:10] alumno@console$ osmedeus run -m enum-subdomain -t vtomasv.net --dry-run
       ▸ No se ejecuta nada todavía.
       ▸ Se observa que enum-subdomain llama fuentes como subfinder y fuentes adicionales.
       ▸ Se decide si el alcance permite continuar.

[03:00] instructor@lab$ RUN_REAL=1 ./scripts/04-authorized-vtomasv.sh
       ▸ Solo porque el dominio pertenece a Tom y fue autorizado.
       ▸ Timeout acotado.
       ▸ Se recolecta evidencia mínima: subdominios y estado del run.

[03:13] osmedeus → status: completed
       ▸ Workflow: {run.get('workflow_name', 'enum-subdomain')}
       ▸ Run UUID: {run.get('run_uuid', 'no disponible')}
       ▸ Subdominios: {', '.join(subdomains) if subdomains else 'sin resultados'}

[CIERRE] La herramienta no reemplaza el criterio. Osmedeus automatiza; el analista decide.
```

## Lectura guiada de la consola

La parte importante de la demostración no es la estética de la salida, sino el hábito que instala. Primero se declara el objetivo, después se revisa el workflow con `--dry-run`, luego se ejecuta solo si hay autorización y finalmente se documenta el resultado.
'''

report = f'''# Informe didáctico de ejecución autorizada — vtomasv.net

**Autor:** Manus AI  
**Fecha de ejecución:** 2026-05-08  
**Herramienta:** Osmedeus v5.0.2  
**Objetivo autorizado:** `vtomasv.net`  
**Workflow ejecutado:** `{run.get('workflow_name', 'enum-subdomain')}`  
**Modo:** ejecución real acotada por timeout.

## Resumen ejecutivo

Se ejecutó un workflow de enumeración de subdominios contra `vtomasv.net`, dominio indicado por Tom como sitio personal autorizado. La actividad tuvo un propósito exclusivamente docente: mostrar cómo se prepara, ejecuta y documenta una tarea OSINT con Osmedeus manteniendo límites claros de alcance. Osmedeus se utilizó como motor de orquestación de workflows de seguridad, conforme a su diseño documentado.[1] [2]

| Campo | Valor |
|---|---|
| Run UUID | `{run.get('run_uuid', 'no disponible')}` |
| Estado | `{run.get('status', 'completed')}` |
| Tipo de workflow | `{run.get('workflow_kind', 'module')}` |
| Objetivo | `{run.get('target', 'vtomasv.net')}` |
| Total de pasos declarados | `{run.get('total_steps', 'no disponible')}` |
| Workspace local | `{run_state.get('workspace', {}).get('local_path', 'no disponible')}` |

## Comando reproducible

```bash
timeout 150s /home/ubuntu/osmedeus-bin/osmedeus \
  run -m enum-subdomain \
  -t vtomasv.net \
  --timeout 2m \
  --disable-color
```

El timeout externo se incluyó para que la ejecución sea apropiada para una sala de clases y para evitar procesos prolongados. La salida completa quedó guardada en `reports/vtomasv-authorized/console-real.log`.

## Hallazgos

| Tipo | Valor | Comentario didáctico |
|---|---|---|
{findings_rows}

El resultado muestra que incluso una ejecución simple produce evidencia que debe interpretarse con cautela. Un subdominio observado no implica vulnerabilidad; solo indica un punto de inventario que puede requerir validación posterior.

## Observaciones de ejecución

Durante la ejecución se completaron los pasos principales del módulo. El paso de Amass quedó omitido por configuración del workflow, mientras que fuentes adicionales y normalización produjeron una lista final. Este comportamiento es útil para enseñar que los workflows tienen parámetros y ramas condicionales, y que el informe debe explicar qué se ejecutó realmente, no solo qué se pretendía ejecutar.

## Recomendaciones para alumnos

Antes de ampliar el análisis se debe actualizar el documento de alcance. Para ejercicios introductorios, se recomienda permanecer en enumeración pasiva y evitar módulos de fuerza bruta, escaneo agresivo o pruebas de vulnerabilidad. Si se agregan módulos más intensivos, el informe debe incluir autorización explícita, horario, límites de tasa, persona responsable y plan de detención.

## Advertencia legal y ética

Este informe no debe reutilizarse como autorización genérica para analizar otros dominios. En Chile, la Ley 21.459 sobre delitos informáticos y la Ley 19.628 sobre protección de datos personales obligan a mantener autorización, proporcionalidad y resguardo de datos al realizar ejercicios técnicos.[4] [5]

{refs}
'''

(ROOT / 'docs' / 'guia-didactica-osmedeus.md').write_text(guide)
(ROOT / 'console' / 'consola-creativa.md').write_text(console)
(ROOT / 'reports' / 'vtomasv-authorized' / 'informe-vtomasv-autorizado.md').write_text(report)
print('documentos_generados=ok')
