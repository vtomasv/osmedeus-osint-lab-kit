# Nivel básico: observar antes de ejecutar

El objetivo de este nivel es que el alumno comprenda la diferencia entre levantar el laboratorio, resolver dominios ficticios y previsualizar un workflow de Osmedeus con `--dry-run`. El comando principal es:

```bash
cd compose
docker compose up -d --build
./scripts/01-basic-dry-run.sh
```

El resultado esperado no es “encontrar vulnerabilidades”, sino entender qué pasos intentaría ejecutar Osmedeus y dónde quedaría la evidencia.
