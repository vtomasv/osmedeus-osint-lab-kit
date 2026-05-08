# Laboratorio didáctico de Osmedeus para OSINT responsable

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
| Workflow | `enum-subdomain` |
| Tipo | `module` |
| Objetivo | `vtomasv.net` |
| Estado | `completed` |
| Run UUID | `c5e78e6a-2965-49b0-9df9-40baace00329` |
| Subdominios únicos | `2` |

Los subdominios observados fueron: `vtomasv.net, www.vtomasv.net`. Este resultado debe tratarse como una evidencia de clase de baja sensibilidad, obtenida con autorización declarada por el propietario del dominio.

## Indicaciones legales para Chile

En Chile, las actividades de OSINT, reconocimiento técnico y análisis de superficie deben planificarse con especial atención a autorización, proporcionalidad y tratamiento de datos. La Ley 21.459 establece normas sobre delitos informáticos y actualiza la legislación nacional en la materia; por ello, acciones como acceso no autorizado, interceptación, alteración o abuso de credenciales deben quedar completamente fuera de un laboratorio docente.[4] La Ley 19.628 regula el tratamiento de datos personales, por lo que cualquier información personal encontrada durante ejercicios OSINT debe minimizarse, protegerse y excluirse de informes cuando no sea necesaria para el objetivo pedagógico.[5]

| Regla práctica | Aplicación en clase |
|---|---|
| Alcance escrito | Usar dominios propios, laboratorios o autorización explícita. |
| Mínima intrusión | Preferir dry-run, enumeración pasiva y módulos no destructivos. |
| Protección de datos | No publicar correos, nombres, teléfonos, tokens ni información personal innecesaria. |
| Evidencia reproducible | Guardar fecha, comando, versión, objetivo, workflow y límites de ejecución. |
| Revisión docente | El instructor valida el workflow antes de que los alumnos ejecuten. |

## Referencias

[1]: https://github.com/j3ssie/osmedeus "j3ssie/osmedeus — A Modern Orchestration Engine for Security"  
[2]: https://docs.osmedeus.org/getting-started/cli "CLI Interface — Osmedeus Docs"  
[3]: https://docs.osmedeus.org/getting-started/docker-setup "Docker Installation & Setup — Osmedeus Docs"  
[4]: https://www.bcn.cl/leychile/navegar?idNorma=1177743 "Ley 21.459 — Biblioteca del Congreso Nacional de Chile"  
[5]: https://www.bcn.cl/leychile/navegar?idNorma=141599 "Ley 19.628 — Biblioteca del Congreso Nacional de Chile"  

