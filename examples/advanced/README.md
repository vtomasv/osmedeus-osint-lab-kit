# Nivel complejo: workflow autorizado externo

Este nivel ilustra un flujo responsable contra `vtomasv.net`, dominio indicado por Tom como sitio personal autorizado. Por defecto el script solo ejecuta `--dry-run`. Para una ejecución real no intrusiva de enumeración de subdominios, el instructor debe habilitar explícitamente `RUN_REAL=1`.

```bash
cd compose
./scripts/04-authorized-vtomasv.sh
RUN_REAL=1 ./scripts/04-authorized-vtomasv.sh
```

La actividad debe registrar autorización, fecha, objetivo exacto, comandos usados, resultados y limitaciones.
