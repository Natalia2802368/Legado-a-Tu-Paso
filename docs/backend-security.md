# Modelo de seguridad previsto

1. El cliente público usa publishable key; nunca la secret/service_role key.
2. El backend valida el token con Supabase Auth y obtiene el `user_id` de la identidad validada.
3. El backend consulta `public.user_roles` con un cliente administrativo separado.
4. El backend autoriza cada operación según rol y acción.
5. El cliente administrativo usa la secret key y no hereda el JWT del usuario.
6. Las escrituras se ejecutan solo desde backend. `service_role` omite RLS, por lo que RLS no sustituye la autorización del backend.
7. No incluir secretos en variables `NEXT_PUBLIC_`, `VITE_`, código móvil, repositorios ni registros.

La migración v1.2 es una propuesta estática. No se ha ejecutado ni probado en Supabase.
