# Legado a tu paso — trabajo aislado por ramas

Este repositorio es una copia de trabajo independiente creada para preparar cambios sin tocar el proyecto Supabase ni ningún repositorio remoto.

## Ramas incluidas

- `baseline-v1.1`: copia de referencia del SQL v1.1 recibido.
- `feature/security-backend`: propuesta de migración completa v1.2 con escrituras reservadas al backend.
- `feature/integrity-hardening`: rama derivada de `feature/security-backend` que añade una migración posterior para reducir riesgos de concurrencia y proteger la compatibilidad de observaciones existentes.

**No se ha creado ni modificado una rama `main`.** No hay remoto configurado, no se ha hecho push y no se ha ejecutado SQL en Supabase.

## Abrir una rama

```bash
git branch -a
git switch feature/security-backend
git switch feature/integrity-hardening
```

La rama `feature/integrity-hardening` contiene también los cambios de seguridad porque parte de `feature/security-backend`. Los cambios están separados por commits.

## Importante

Los SQL son propuestas pendientes de validación en PostgreSQL/Supabase. No aplicar en producción. La migración 002 presupone que la 001 v1.2 se ha aplicado en una base de datos de desarrollo limpia.
