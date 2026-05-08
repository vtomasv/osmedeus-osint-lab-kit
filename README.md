# Laboratorio Didáctico Osmedeus OSINT

Este repositorio contiene un kit educativo para enseñar el uso responsable de [Osmedeus](https://github.com/j3ssie/osmedeus) en clases de OSINT. El laboratorio combina una receta Docker Compose autocontenida, dominios ficticios `.lab`, objetivos web internos, scripts progresivos y evidencia de una ejecución autorizada contra `vtomasv.net`.

El propósito del material es que los alumnos aprendan una forma de trabajo reproducible: definir alcance, revisar workflows antes de ejecutarlos, limitar el objetivo, guardar evidencia y redactar un informe técnico. El repositorio está diseñado para docencia y no debe usarse para escanear terceros sin autorización explícita.

## Contenido del kit

| Ruta | Contenido | Uso docente |
|---|---|---|
| `compose/docker-compose.yml` | Laboratorio con Osmedeus, DNS local, sitios ficticios y consola de alumno. | Levantar una red aislada para practicar sin depender de objetivos externos. |
| `compose/scripts/` | Scripts de nivel básico, intermedio y avanzado. | Guiar a los alumnos desde dry-run hasta ejecución autorizada. |
| `docs/guia-didactica-osmedeus.md` | Guía paso a paso para el instructor y los alumnos. | Explicar metodología, comandos, ejercicios y cierre del informe. |
| `console/consola-creativa.md` | Narrativa de consola para presentar la práctica en clase. | Mostrar el flujo de trabajo de forma visual y memorable. |
| `reports/vtomasv-authorized/` | Evidencia de ejecución real autorizada contra `vtomasv.net`. | Enseñar cómo preservar logs, subdominios observados y run-state. |
| `legal/chile-osint-notas.md` | Indicaciones legales de uso responsable en Chile. | Reforzar autorización, proporcionalidad y protección de datos. |

## Inicio rápido

Para levantar el laboratorio local, entra a la carpeta `compose`, construye los servicios y ejecuta el demo guiado.

```bash
cd compose
docker compose up -d --build
./scripts/lab-demo.sh
```

El laboratorio crea servicios ficticios en una red privada. Los dominios `.lab` se resuelven dentro del entorno Docker mediante el servicio DNS local, por lo que no representan activos reales en Internet.

## Topología del laboratorio

| Servicio | Dominio ficticio | IP interna | Propósito pedagógico |
|---|---:|---:|---|
| `osmedeus` | `osmedeus.lab` | `172.28.0.10` | Ejecutar workflows de Osmedeus. |
| `web-alpha` | `web-alpha.lab` | `172.28.0.11` | Objetivo web básico. |
| `web-beta` | `web-beta.lab` | `172.28.0.12` | Objetivo web intermedio con rutas de práctica. |
| `blog-gamma` | `blog-gamma.lab` | `172.28.0.13` | Inventario de contenido público ficticio. |
| `mail-delta` | `mail-delta.lab` | `172.28.0.14` | Servicio de correo ficticio. |
| `local-dns` | `local-dns.lab` | `172.28.0.53` | Resolución DNS interna para `.lab`. |
| `student-console` | `student-console.lab` | `172.28.0.100` | Puesto de trabajo del alumno. |

## Ruta de aprendizaje

| Nivel | Script | Objetivo |
|---|---|---|
| Básico | `compose/scripts/01-basic-dry-run.sh` | Revisar comandos y workflows sin ejecutar acciones reales. |
| Intermedio | `compose/scripts/02-lab-scan-alpha.sh` y `03-intermediate-multi-target.sh` | Practicar contra dominios ficticios dentro de Docker Compose. |
| Avanzado | `compose/scripts/04-authorized-vtomasv.sh` | Ejecutar un flujo externo autorizado, con `--dry-run` por defecto y ejecución real solo con `RUN_REAL=1`. |

## Flujo autorizado contra `vtomasv.net`

El script `compose/scripts/04-authorized-vtomasv.sh` está preparado para trabajar contra `vtomasv.net`, indicado por Tom como sitio personal autorizado. Por seguridad, el script ejecuta `--dry-run` por defecto y solo realiza la ejecución real si se define explícitamente la variable `RUN_REAL=1`.

```bash
cd compose
./scripts/04-authorized-vtomasv.sh
RUN_REAL=1 ./scripts/04-authorized-vtomasv.sh
```

La evidencia incluida en `reports/vtomasv-authorized/` documenta una ejecución real acotada del módulo `enum-subdomain`, junto con el log de consola, el estado de ejecución y los subdominios observados.

## Regla de oro

> Usa Osmedeus únicamente contra activos propios, laboratorios o objetivos donde exista autorización explícita. Revisa los workflows antes de ejecutarlos porque Osmedeus puede orquestar múltiples comandos definidos en YAML.

## Consideraciones legales para Chile

Este material es educativo. No autoriza acceso no consentido, explotación de vulnerabilidades, abuso de credenciales, extracción de datos personales ni publicación innecesaria de información sensible. Para clases en Chile, se recomienda revisar especialmente el alcance de la Ley 21.459 sobre delitos informáticos y la Ley 19.628 sobre protección de la vida privada y datos personales.

## Licencia

El material de este repositorio se distribuye bajo licencia MIT. El uso de Osmedeus se rige por la licencia y condiciones del proyecto original.
