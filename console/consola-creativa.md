# Consola creativa — narrativa operativa para clase

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
       ▸ Workflow: enum-subdomain
       ▸ Run UUID: c5e78e6a-2965-49b0-9df9-40baace00329
       ▸ Subdominios: vtomasv.net, www.vtomasv.net

[CIERRE] La herramienta no reemplaza el criterio. Osmedeus automatiza; el analista decide.
```

## Lectura guiada de la consola

La parte importante de la demostración no es la estética de la salida, sino el hábito que instala. Primero se declara el objetivo, después se revisa el workflow con `--dry-run`, luego se ejecuta solo si hay autorización y finalmente se documenta el resultado.
