# Informe didáctico de ejecución autorizada — vtomasv.net

**Autor:** Manus AI  
**Fecha de ejecución:** 2026-05-08  
**Herramienta:** Osmedeus v5.0.2  
**Objetivo autorizado:** `vtomasv.net`  
**Workflow ejecutado:** `enum-subdomain`  
**Modo:** ejecución real acotada por timeout.

## Resumen ejecutivo

Se ejecutó un workflow de enumeración de subdominios contra `vtomasv.net`, dominio indicado por Tom como sitio personal autorizado. La actividad tuvo un propósito exclusivamente docente: mostrar cómo se prepara, ejecuta y documenta una tarea OSINT con Osmedeus manteniendo límites claros de alcance. Osmedeus se utilizó como motor de orquestación de workflows de seguridad, conforme a su diseño documentado.[1] [2]

| Campo | Valor |
|---|---|
| Run UUID | `c5e78e6a-2965-49b0-9df9-40baace00329` |
| Estado | `completed` |
| Tipo de workflow | `module` |
| Objetivo | `vtomasv.net` |
| Total de pasos declarados | `6` |
| Workspace local | `/home/ubuntu/workspaces-osmedeus/vtomasv.net` |

## Comando reproducible

```bash
timeout 150s /home/ubuntu/osmedeus-bin/osmedeus   run -m enum-subdomain   -t vtomasv.net   --timeout 2m   --disable-color
```

El timeout externo se incluyó para que la ejecución sea apropiada para una sala de clases y para evitar procesos prolongados. La salida completa quedó guardada en `reports/vtomasv-authorized/console-real.log`.

## Hallazgos

| Tipo | Valor | Comentario didáctico |
|---|---|---|
| Subdominio | `vtomasv.net` | Debe validarse antes de inferir exposición real. |\n| Subdominio | `www.vtomasv.net` | Debe validarse antes de inferir exposición real. |\n

El resultado muestra que incluso una ejecución simple produce evidencia que debe interpretarse con cautela. Un subdominio observado no implica vulnerabilidad; solo indica un punto de inventario que puede requerir validación posterior.

## Observaciones de ejecución

Durante la ejecución se completaron los pasos principales del módulo. El paso de Amass quedó omitido por configuración del workflow, mientras que fuentes adicionales y normalización produjeron una lista final. Este comportamiento es útil para enseñar que los workflows tienen parámetros y ramas condicionales, y que el informe debe explicar qué se ejecutó realmente, no solo qué se pretendía ejecutar.

## Recomendaciones para alumnos

Antes de ampliar el análisis se debe actualizar el documento de alcance. Para ejercicios introductorios, se recomienda permanecer en enumeración pasiva y evitar módulos de fuerza bruta, escaneo agresivo o pruebas de vulnerabilidad. Si se agregan módulos más intensivos, el informe debe incluir autorización explícita, horario, límites de tasa, persona responsable y plan de detención.

## Advertencia legal y ética

Este informe no debe reutilizarse como autorización genérica para analizar otros dominios. En Chile, la Ley 21.459 sobre delitos informáticos y la Ley 19.628 sobre protección de datos personales obligan a mantener autorización, proporcionalidad y resguardo de datos al realizar ejercicios técnicos.[4] [5]

## Referencias

[1]: https://github.com/j3ssie/osmedeus "j3ssie/osmedeus — A Modern Orchestration Engine for Security"  
[2]: https://docs.osmedeus.org/getting-started/cli "CLI Interface — Osmedeus Docs"  
[3]: https://docs.osmedeus.org/getting-started/docker-setup "Docker Installation & Setup — Osmedeus Docs"  
[4]: https://www.bcn.cl/leychile/navegar?idNorma=1177743 "Ley 21.459 — Biblioteca del Congreso Nacional de Chile"  
[5]: https://www.bcn.cl/leychile/navegar?idNorma=141599 "Ley 19.628 — Biblioteca del Congreso Nacional de Chile"  

