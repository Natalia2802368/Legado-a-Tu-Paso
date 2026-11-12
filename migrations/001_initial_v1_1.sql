-- ============================================================================
-- LEGADO A TU PASO
-- Supabase / PostgreSQL - Migración 001
-- Versión: 1.1.0
--
-- ALCANCE
--   - Estructura inicial de datos para ciudades, rutas, tramos, lugares,
--     accesibilidad, evaluaciones, observaciones, barreras, fuentes, evidencias,
--     servicios, alternativas y roles.
--   - PostGIS ya debe estar instalado en el esquema "extensions".
--   - Historial de verificaciones: SOLO observaciones (decisión confirmada).
--   - RLS y permisos de consulta pública / administración.
--   - Restricciones compuestas y triggers para coherencia geográfica y referencial.
--   - Validación estructural de allowed_values y de valores choice.
--
-- IMPORTANTE
--   1. Revisar este archivo antes de ejecutarlo.
--   2. Ejecutarlo una sola vez en el proyecto Supabase de desarrollo.
--   3. No contiene datos reales ni crea el bucket de Storage.
--   4. No modifica los esquemas gestionados por Supabase.
--   5. La migración NO se ha ejecutado ni probado contra tu proyecto Supabase.
--   6. Incluye restricciones y triggers adicionales de coherencia e integridad.
--   7. Tras ejecutarla, asigna el primer administrador siguiendo las instrucciones del bloque final.
--
-- Requisitos previamente comprobados por la usuaria:
--   pgcrypto 1.3 en schema extensions
--   postgis 3.3.7 en schema extensions
-- ============================================================================

BEGIN;

-- --------------------------------------------------------------------------
-- 0. Comprobaciones previas: abortar si faltan extensiones o PostGIS no está
--    disponible en el esquema esperado.
-- --------------------------------------------------------------------------

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_extension e
        JOIN pg_namespace n ON n.oid = e.extnamespace
        WHERE e.extname = 'postgis'
          AND n.nspname = 'extensions'
    ) THEN
        RAISE EXCEPTION
            'No se encuentra PostGIS en el esquema extensions. No se aplica la migración.';
    END IF;

    IF to_regnamespace('public') IS NULL THEN
        RAISE EXCEPTION 'No existe el esquema public.';
    END IF;
END
$$;

-- Esquema privado para funciones auxiliares. No se expone por la API.
CREATE SCHEMA IF NOT EXISTS app_private;
REVOKE ALL ON SCHEMA app_private FROM PUBLIC;
REVOKE ALL ON SCHEMA app_private FROM anon, authenticated;
GRANT USAGE ON SCHEMA app_private TO anon, authenticated;

-- --------------------------------------------------------------------------
-- 1. Tablas principales
-- --------------------------------------------------------------------------

CREATE TABLE public.cities (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL,
    slug text NOT NULL UNIQUE,
    province text,
    autonomous_community text,
    country_code char(2) NOT NULL DEFAULT 'ES',
    unesco_world_heritage boolean NOT NULL DEFAULT false,
    description text,
    publication_status text NOT NULL DEFAULT 'draft'
        CHECK (publication_status IN ('draft', 'in_review', 'published', 'archived')),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE public.routes (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    city_id uuid NOT NULL REFERENCES public.cities(id) ON DELETE RESTRICT,
    name text NOT NULL,
    slug text NOT NULL,
    description text,
    difficulty text CHECK (difficulty IN ('easy', 'moderate', 'hard', 'unknown')),
    estimated_duration_minutes integer CHECK (estimated_duration_minutes IS NULL OR estimated_duration_minutes > 0),
    distance_meters numeric(10,2) CHECK (distance_meters IS NULL OR distance_meters >= 0),
    geom extensions.geometry(LineString, 4326),
    publication_status text NOT NULL DEFAULT 'draft'
        CHECK (publication_status IN ('draft', 'in_review', 'published', 'archived')),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (city_id, slug)
);

CREATE TABLE public.segments (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    route_id uuid NOT NULL REFERENCES public.routes(id) ON DELETE RESTRICT,
    code text,
    name text NOT NULL,
    sequence_number integer NOT NULL CHECK (sequence_number > 0),
    description text,
    distance_meters numeric(10,2) CHECK (distance_meters IS NULL OR distance_meters >= 0),
    geom extensions.geometry(LineString, 4326),
    publication_status text NOT NULL DEFAULT 'draft'
        CHECK (publication_status IN ('draft', 'in_review', 'published', 'archived')),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (route_id, sequence_number)
);

CREATE TABLE public.places (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    city_id uuid NOT NULL REFERENCES public.cities(id) ON DELETE RESTRICT,
    name text NOT NULL,
    slug text,
    description text,
    address text,
    geom extensions.geometry(Point, 4326),
    publication_status text NOT NULL DEFAULT 'draft'
        CHECK (publication_status IN ('draft', 'in_review', 'published', 'archived')),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (city_id, slug)
);

-- Catálogo de necesidades: no almacena diagnósticos médicos personales.
CREATE TABLE public.access_needs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    code text NOT NULL UNIQUE,
    name text NOT NULL,
    category text NOT NULL
        CHECK (category IN ('physical', 'visual', 'hearing', 'cognitive', 'age_related', 'family', 'other')),
    description text,
    is_active boolean NOT NULL DEFAULT true,
    display_order integer NOT NULL DEFAULT 0,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE public.accessibility_attributes (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    code text NOT NULL UNIQUE,
    name text NOT NULL,
    category text NOT NULL,
    data_type text NOT NULL
        CHECK (data_type IN ('boolean', 'number', 'text', 'choice')),
    unit text,
    description text,
    allowed_values jsonb,
    is_active boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE public.assessments (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    segment_id uuid REFERENCES public.segments(id) ON DELETE RESTRICT,
    place_id uuid REFERENCES public.places(id) ON DELETE RESTRICT,
    assessed_at timestamptz NOT NULL DEFAULT now(),
    method text NOT NULL
        CHECK (method IN ('document_review', 'field_inspection', 'user_experience', 'multi_source', 'other')),
    assessor_reference text,
    general_notes text,
    created_by uuid REFERENCES auth.users(id) ON DELETE SET NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK (
        (segment_id IS NOT NULL AND place_id IS NULL)
        OR
        (segment_id IS NULL AND place_id IS NOT NULL)
    )
);

CREATE TABLE public.observations (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id uuid NOT NULL REFERENCES public.assessments(id) ON DELETE RESTRICT,
    attribute_id uuid NOT NULL REFERENCES public.accessibility_attributes(id) ON DELETE RESTRICT,
    result text NOT NULL
        CHECK (result IN (
            'no_barrier_observed',
            'barrier_observed',
            'not_evaluated',
            'insufficient_information'
        )),
    value_boolean boolean,
    value_number numeric,
    value_text text,
    unit text,
    precision_value numeric CHECK (precision_value IS NULL OR precision_value >= 0),
    uncertainty_note text,
    limitations text,
    verification_status text NOT NULL DEFAULT 'PENDIENTE'
        CHECK (verification_status IN (
            'DOCUMENTADO',
            'VERIFICADO_CAMPO',
            'VALIDADO_EXPERIENCIA',
            'CONTRASTADO',
            'DISCREPANCIA',
            'PENDIENTE',
            'CADUCADO'
        )),
    publication_status text NOT NULL DEFAULT 'draft'
        CHECK (publication_status IN ('draft', 'in_review', 'published', 'archived')),
    observed_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CHECK (
        (CASE WHEN value_boolean IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN value_number IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN value_text IS NOT NULL THEN 1 ELSE 0 END) <= 1
    )
);

CREATE TABLE public.observation_access_needs (
    observation_id uuid NOT NULL REFERENCES public.observations(id) ON DELETE CASCADE,
    access_need_id uuid NOT NULL REFERENCES public.access_needs(id) ON DELETE RESTRICT,
    impact_note text,
    PRIMARY KEY (observation_id, access_need_id)
);

CREATE TABLE public.barriers (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id uuid NOT NULL REFERENCES public.assessments(id) ON DELETE RESTRICT,
    observation_id uuid REFERENCES public.observations(id) ON DELETE RESTRICT,
    name text NOT NULL,
    description text NOT NULL,
    severity text CHECK (severity IN ('low', 'medium', 'high', 'critical', 'unknown')),
    geom extensions.geometry(Point, 4326),
    temporary boolean NOT NULL DEFAULT false,
    status text NOT NULL DEFAULT 'open'
        CHECK (status IN ('open', 'mitigated', 'resolved', 'unknown')),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE public.barrier_access_needs (
    barrier_id uuid NOT NULL REFERENCES public.barriers(id) ON DELETE CASCADE,
    access_need_id uuid NOT NULL REFERENCES public.access_needs(id) ON DELETE RESTRICT,
    impact_note text,
    PRIMARY KEY (barrier_id, access_need_id)
);

CREATE TABLE public.sources (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL,
    source_type text NOT NULL
        CHECK (source_type IN ('official_web', 'official_document', 'organization', 'fieldwork', 'user_contribution', 'other')),
    publisher text,
    source_url text,
    published_at timestamptz,
    consulted_at timestamptz NOT NULL DEFAULT now(),
    reliability_note text,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE public.observation_sources (
    observation_id uuid NOT NULL REFERENCES public.observations(id) ON DELETE CASCADE,
    source_id uuid NOT NULL REFERENCES public.sources(id) ON DELETE RESTRICT,
    relationship_note text,
    PRIMARY KEY (observation_id, source_id)
);

-- Metadatos de evidencias. Los archivos se guardarán en Storage privado
-- en una fase posterior; esta migración no crea buckets ni políticas Storage.
CREATE TABLE public.evidences (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    storage_bucket text NOT NULL,
    storage_path text NOT NULL,
    file_name text,
    mime_type text,
    file_size_bytes bigint CHECK (file_size_bytes IS NULL OR file_size_bytes >= 0),
    captured_at timestamptz,
    uploaded_by uuid REFERENCES auth.users(id) ON DELETE SET NULL,
    description text,
    is_private boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (storage_bucket, storage_path)
);

CREATE TABLE public.observation_evidences (
    observation_id uuid NOT NULL REFERENCES public.observations(id) ON DELETE CASCADE,
    evidence_id uuid NOT NULL REFERENCES public.evidences(id) ON DELETE RESTRICT,
    relationship_note text,
    PRIMARY KEY (observation_id, evidence_id)
);

CREATE TABLE public.services (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    city_id uuid NOT NULL REFERENCES public.cities(id) ON DELETE RESTRICT,
    place_id uuid REFERENCES public.places(id) ON DELETE RESTRICT,
    segment_id uuid REFERENCES public.segments(id) ON DELETE RESTRICT,
    name text NOT NULL,
    service_type text NOT NULL,
    description text,
    contact_url text,
    publication_status text NOT NULL DEFAULT 'draft'
        CHECK (publication_status IN ('draft', 'in_review', 'published', 'archived')),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CHECK (NOT (place_id IS NOT NULL AND segment_id IS NOT NULL))
);

CREATE TABLE public.alternatives (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    city_id uuid NOT NULL REFERENCES public.cities(id) ON DELETE RESTRICT,
    route_id uuid REFERENCES public.routes(id) ON DELETE RESTRICT,
    name text NOT NULL,
    description text,
    reason text,
    publication_status text NOT NULL DEFAULT 'draft'
        CHECK (publication_status IN ('draft', 'in_review', 'published', 'archived')),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE public.alternative_segments (
    alternative_id uuid NOT NULL REFERENCES public.alternatives(id) ON DELETE CASCADE,
    segment_id uuid NOT NULL REFERENCES public.segments(id) ON DELETE RESTRICT,
    sequence_number integer NOT NULL CHECK (sequence_number > 0),
    PRIMARY KEY (alternative_id, segment_id),
    UNIQUE (alternative_id, sequence_number)
);

-- Historial de verificaciones: solo observaciones en la migración 001.
-- Registros de solo anexado desde la API: no se conceden UPDATE ni DELETE.
CREATE TABLE public.verification_records (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    observation_id uuid NOT NULL REFERENCES public.observations(id) ON DELETE RESTRICT,
    verification_status text NOT NULL
        CHECK (verification_status IN (
            'DOCUMENTADO',
            'VERIFICADO_CAMPO',
            'VALIDADO_EXPERIENCIA',
            'CONTRASTADO',
            'DISCREPANCIA',
            'PENDIENTE',
            'CADUCADO'
        )),
    verified_at timestamptz NOT NULL DEFAULT now(),
    method text,
    verifier_reference text,
    notes text,
    created_by uuid REFERENCES auth.users(id) ON DELETE SET NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE public.user_roles (
    user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    role text NOT NULL CHECK (role IN ('admin', 'editor')),
    assigned_by uuid REFERENCES auth.users(id) ON DELETE SET NULL,
    assigned_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, role)
);

-- --------------------------------------------------------------------------
-- 1 bis. Claves compuestas para garantizar coherencia entre entidades
-- --------------------------------------------------------------------------

-- Permiten que las relaciones compuestas comprueben también ciudad/ruta,
-- y no únicamente la existencia aislada de cada identificador.
ALTER TABLE public.routes
    ADD CONSTRAINT routes_id_city_uk UNIQUE (id, city_id);

ALTER TABLE public.segments
    ADD CONSTRAINT segments_id_route_uk UNIQUE (id, route_id);

ALTER TABLE public.places
    ADD CONSTRAINT places_id_city_uk UNIQUE (id, city_id);

ALTER TABLE public.observations
    ADD CONSTRAINT observations_id_assessment_uk UNIQUE (id, assessment_id);

-- Un servicio asociado a un lugar debe declarar la ciudad de ese lugar.
ALTER TABLE public.services
    ADD CONSTRAINT services_place_city_fk
    FOREIGN KEY (place_id, city_id)
    REFERENCES public.places (id, city_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT;

-- Una alternativa asociada a una ruta debe pertenecer a la ciudad de esa ruta.
ALTER TABLE public.alternatives
    ADD CONSTRAINT alternatives_route_city_fk
    FOREIGN KEY (route_id, city_id)
    REFERENCES public.routes (id, city_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT;

-- Si una barrera referencia una observación, ambas deben pertenecer
-- a la misma evaluación.
ALTER TABLE public.barriers
    ADD CONSTRAINT barriers_observation_assessment_fk
    FOREIGN KEY (observation_id, assessment_id)
    REFERENCES public.observations (id, assessment_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT;

-- --------------------------------------------------------------------------
-- 2. Índices
-- --------------------------------------------------------------------------

CREATE INDEX routes_city_id_idx ON public.routes(city_id);
CREATE INDEX segments_route_id_idx ON public.segments(route_id);
CREATE INDEX places_city_id_idx ON public.places(city_id);
CREATE INDEX assessments_segment_id_idx ON public.assessments(segment_id);
CREATE INDEX assessments_place_id_idx ON public.assessments(place_id);
CREATE INDEX observations_assessment_id_idx ON public.observations(assessment_id);
CREATE INDEX observations_attribute_id_idx ON public.observations(attribute_id);
CREATE INDEX observations_publication_status_idx ON public.observations(publication_status);
CREATE INDEX barriers_assessment_id_idx ON public.barriers(assessment_id);
CREATE INDEX barriers_observation_id_idx ON public.barriers(observation_id);
CREATE INDEX services_city_id_idx ON public.services(city_id);
CREATE INDEX services_place_id_idx ON public.services(place_id);
CREATE INDEX services_segment_id_idx ON public.services(segment_id);
CREATE INDEX alternatives_city_id_idx ON public.alternatives(city_id);
CREATE INDEX alternative_segments_segment_id_idx ON public.alternative_segments(segment_id);
CREATE INDEX verification_records_observation_id_idx ON public.verification_records(observation_id);
CREATE INDEX verification_records_verified_at_idx ON public.verification_records(verified_at);

CREATE INDEX routes_geom_gix ON public.routes USING gist (geom);
CREATE INDEX segments_geom_gix ON public.segments USING gist (geom);
CREATE INDEX places_geom_gix ON public.places USING gist (geom);
CREATE INDEX barriers_geom_gix ON public.barriers USING gist (geom);

-- --------------------------------------------------------------------------
-- 2 bis. Validaciones de coherencia entre tablas y catálogos
-- --------------------------------------------------------------------------

-- Comprueba que un servicio asociado a un tramo pertenece a la ciudad
-- de la ruta a la que pertenece ese tramo.
CREATE OR REPLACE FUNCTION app_private.validate_service_location()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = ''
AS $$
DECLARE
    v_city_id uuid;
BEGIN
    IF NEW.place_id IS NOT NULL THEN
        SELECT p.city_id
          INTO v_city_id
          FROM public.places p
         WHERE p.id = NEW.place_id;

        IF v_city_id IS DISTINCT FROM NEW.city_id THEN
            RAISE EXCEPTION 'El lugar asociado al servicio no pertenece a la ciudad indicada.';
        END IF;
    END IF;

    IF NEW.segment_id IS NOT NULL THEN
        SELECT r.city_id
          INTO v_city_id
          FROM public.segments s
          JOIN public.routes r ON r.id = s.route_id
         WHERE s.id = NEW.segment_id;

        IF v_city_id IS DISTINCT FROM NEW.city_id THEN
            RAISE EXCEPTION 'El tramo asociado al servicio no pertenece a la ciudad indicada.';
        END IF;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER services_validate_location
BEFORE INSERT OR UPDATE OF city_id, place_id, segment_id
ON public.services
FOR EACH ROW
EXECUTE FUNCTION app_private.validate_service_location();

-- Evita que un cambio posterior en una ruta deje servicios o segmentos
-- de alternativas asociados a una ciudad incorrecta.
CREATE OR REPLACE FUNCTION app_private.prevent_inconsistent_route_city_change()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = ''
AS $$
BEGIN
    IF NEW.city_id IS DISTINCT FROM OLD.city_id THEN
        IF EXISTS (
            SELECT 1
              FROM public.segments s
              JOIN public.services sv ON sv.segment_id = s.id
             WHERE s.route_id = OLD.id
               AND sv.city_id IS DISTINCT FROM NEW.city_id
        ) THEN
            RAISE EXCEPTION 'No se puede cambiar la ciudad de la ruta: existen servicios asociados a sus tramos.';
        END IF;

        IF EXISTS (
            SELECT 1
              FROM public.segments s
              JOIN public.alternative_segments als ON als.segment_id = s.id
              JOIN public.alternatives a ON a.id = als.alternative_id
             WHERE s.route_id = OLD.id
               AND a.city_id IS DISTINCT FROM NEW.city_id
        ) THEN
            RAISE EXCEPTION 'No se puede cambiar la ciudad de la ruta: existen alternativas con tramos asociados.';
        END IF;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER routes_prevent_inconsistent_city_change
BEFORE UPDATE OF city_id ON public.routes
FOR EACH ROW
EXECUTE FUNCTION app_private.prevent_inconsistent_route_city_change();

-- Evita mover un tramo a otra ruta cuando sus servicios o alternativas
-- quedarían asociados a una ciudad/ruta distinta.
CREATE OR REPLACE FUNCTION app_private.prevent_inconsistent_segment_route_change()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = ''
AS $$
DECLARE
    v_new_city_id uuid;
BEGIN
    IF NEW.route_id IS DISTINCT FROM OLD.route_id THEN
        SELECT r.city_id
          INTO v_new_city_id
          FROM public.routes r
         WHERE r.id = NEW.route_id;

        IF EXISTS (
            SELECT 1
              FROM public.services sv
             WHERE sv.segment_id = OLD.id
               AND sv.city_id IS DISTINCT FROM v_new_city_id
        ) THEN
            RAISE EXCEPTION 'No se puede cambiar la ruta del tramo: existen servicios asociados.';
        END IF;

        IF EXISTS (
            SELECT 1
              FROM public.alternative_segments als
              JOIN public.alternatives a ON a.id = als.alternative_id
             WHERE als.segment_id = OLD.id
               AND (
                   a.city_id IS DISTINCT FROM v_new_city_id
                   OR (a.route_id IS NOT NULL AND a.route_id IS DISTINCT FROM NEW.route_id)
               )
        ) THEN
            RAISE EXCEPTION 'No se puede cambiar la ruta del tramo: existen alternativas incompatibles.';
        END IF;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER segments_prevent_inconsistent_route_change
BEFORE UPDATE OF route_id ON public.segments
FOR EACH ROW
EXECUTE FUNCTION app_private.prevent_inconsistent_segment_route_change();

-- Comprueba que los segmentos de una alternativa pertenecen a su ciudad.
-- Si la alternativa tiene route_id, exige además que el segmento pertenezca
-- exactamente a esa ruta.
CREATE OR REPLACE FUNCTION app_private.validate_alternative_segment()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = ''
AS $$
DECLARE
    v_alternative_city uuid;
    v_alternative_route uuid;
    v_segment_city uuid;
    v_segment_route uuid;
BEGIN
    SELECT a.city_id, a.route_id
      INTO v_alternative_city, v_alternative_route
      FROM public.alternatives a
     WHERE a.id = NEW.alternative_id;

    SELECT r.city_id, s.route_id
      INTO v_segment_city, v_segment_route
      FROM public.segments s
      JOIN public.routes r ON r.id = s.route_id
     WHERE s.id = NEW.segment_id;

    IF v_alternative_city IS NULL OR v_segment_city IS NULL THEN
        RAISE EXCEPTION 'La alternativa o el tramo indicado no existe.';
    END IF;

    IF v_alternative_city IS DISTINCT FROM v_segment_city THEN
        RAISE EXCEPTION 'El tramo de la alternativa pertenece a otra ciudad.';
    END IF;

    IF v_alternative_route IS NOT NULL
       AND v_alternative_route IS DISTINCT FROM v_segment_route THEN
        RAISE EXCEPTION 'El tramo no pertenece a la ruta indicada por la alternativa.';
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER alternative_segments_validate_consistency
BEFORE INSERT OR UPDATE OF alternative_id, segment_id
ON public.alternative_segments
FOR EACH ROW
EXECUTE FUNCTION app_private.validate_alternative_segment();

-- allowed_values debe ser un array JSON no vacío de cadenas para atributos
-- choice. Para los demás tipos se exige NULL.
CREATE OR REPLACE FUNCTION app_private.valid_allowed_values(
    p_data_type text,
    p_allowed_values jsonb
)
RETURNS boolean
LANGUAGE plpgsql
IMMUTABLE
SET search_path = ''
AS $$
DECLARE
    v_item jsonb;
BEGIN
    IF p_data_type = 'choice' THEN
        IF p_allowed_values IS NULL THEN
            RETURN false;
        END IF;

        IF jsonb_typeof(p_allowed_values) <> 'array' THEN
            RETURN false;
        END IF;

        IF jsonb_array_length(p_allowed_values) = 0 THEN
            RETURN false;
        END IF;

        FOR v_item IN
            SELECT value FROM jsonb_array_elements(p_allowed_values)
        LOOP
            IF jsonb_typeof(v_item) <> 'string' THEN
                RETURN false;
            END IF;
        END LOOP;

        RETURN true;
    END IF;

    RETURN p_allowed_values IS NULL;
END;
$$;

ALTER TABLE public.accessibility_attributes
    ADD CONSTRAINT accessibility_attributes_allowed_values_ck
    CHECK (app_private.valid_allowed_values(data_type, allowed_values));

-- --------------------------------------------------------------------------
-- 3. Funciones auxiliares de autorización
--    SECURITY DEFINER evita recursión al consultar user_roles desde RLS.
--    search_path vacío y nombres de objetos cualificados.
-- --------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION app_private.has_content_role()
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = ''
AS $$
    SELECT EXISTS (
        SELECT 1
        FROM public.user_roles ur
        WHERE ur.user_id = auth.uid()
          AND ur.role IN ('admin', 'editor')
    );
$$;

CREATE OR REPLACE FUNCTION app_private.is_admin()
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = ''
AS $$
    SELECT EXISTS (
        SELECT 1
        FROM public.user_roles ur
        WHERE ur.user_id = auth.uid()
          AND ur.role = 'admin'
    );
$$;

CREATE OR REPLACE FUNCTION app_private.is_route_public(p_route_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = ''
AS $$
    SELECT EXISTS (
        SELECT 1
        FROM public.routes r
        JOIN public.cities c ON c.id = r.city_id
        WHERE r.id = p_route_id
          AND r.publication_status = 'published'
          AND c.publication_status = 'published'
    );
$$;

CREATE OR REPLACE FUNCTION app_private.is_segment_public(p_segment_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = ''
AS $$
    SELECT EXISTS (
        SELECT 1
        FROM public.segments s
        JOIN public.routes r ON r.id = s.route_id
        JOIN public.cities c ON c.id = r.city_id
        WHERE s.id = p_segment_id
          AND s.publication_status = 'published'
          AND r.publication_status = 'published'
          AND c.publication_status = 'published'
    );
$$;

CREATE OR REPLACE FUNCTION app_private.is_place_public(p_place_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = ''
AS $$
    SELECT EXISTS (
        SELECT 1
        FROM public.places p
        JOIN public.cities c ON c.id = p.city_id
        WHERE p.id = p_place_id
          AND p.publication_status = 'published'
          AND c.publication_status = 'published'
    );
$$;

CREATE OR REPLACE FUNCTION app_private.is_observation_public(p_observation_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = ''
AS $$
    SELECT EXISTS (
        SELECT 1
        FROM public.observations o
        JOIN public.assessments a ON a.id = o.assessment_id
        WHERE o.id = p_observation_id
          AND o.publication_status = 'published'
          AND (
              (a.segment_id IS NOT NULL AND app_private.is_segment_public(a.segment_id))
              OR
              (a.place_id IS NOT NULL AND app_private.is_place_public(a.place_id))
          )
    );
$$;

CREATE OR REPLACE FUNCTION app_private.is_service_public(p_service_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = ''
AS $$
    SELECT EXISTS (
        SELECT 1
        FROM public.services s
        JOIN public.cities c ON c.id = s.city_id
        WHERE s.id = p_service_id
          AND s.publication_status = 'published'
          AND c.publication_status = 'published'
          AND (
              (s.place_id IS NULL AND s.segment_id IS NULL)
              OR
              (s.place_id IS NOT NULL AND app_private.is_place_public(s.place_id))
              OR
              (s.segment_id IS NOT NULL AND app_private.is_segment_public(s.segment_id))
          )
    );
$$;

CREATE OR REPLACE FUNCTION app_private.is_alternative_public(p_alternative_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = ''
AS $$
    SELECT EXISTS (
        SELECT 1
        FROM public.alternatives a
        JOIN public.cities c ON c.id = a.city_id
        WHERE a.id = p_alternative_id
          AND a.publication_status = 'published'
          AND c.publication_status = 'published'
          AND (
              a.route_id IS NULL
              OR app_private.is_route_public(a.route_id)
          )
    );
$$;

-- Las funciones SECURITY DEFINER deben pertenecer a un rol de confianza.
-- En Supabase, la migración debe ejecutarse desde el contexto administrativo
-- habitual (postgres); se fija expresamente el propietario para evitar
-- depender del propietario implícito del objeto.
ALTER FUNCTION app_private.has_content_role() OWNER TO postgres;
ALTER FUNCTION app_private.is_admin() OWNER TO postgres;
ALTER FUNCTION app_private.is_route_public(uuid) OWNER TO postgres;
ALTER FUNCTION app_private.is_segment_public(uuid) OWNER TO postgres;
ALTER FUNCTION app_private.is_place_public(uuid) OWNER TO postgres;
ALTER FUNCTION app_private.is_observation_public(uuid) OWNER TO postgres;
ALTER FUNCTION app_private.is_service_public(uuid) OWNER TO postgres;
ALTER FUNCTION app_private.is_alternative_public(uuid) OWNER TO postgres;

REVOKE ALL ON FUNCTION app_private.has_content_role() FROM PUBLIC;
REVOKE ALL ON FUNCTION app_private.is_admin() FROM PUBLIC;
REVOKE ALL ON FUNCTION app_private.is_route_public(uuid) FROM PUBLIC;
REVOKE ALL ON FUNCTION app_private.is_segment_public(uuid) FROM PUBLIC;
REVOKE ALL ON FUNCTION app_private.is_place_public(uuid) FROM PUBLIC;
REVOKE ALL ON FUNCTION app_private.is_observation_public(uuid) FROM PUBLIC;
REVOKE ALL ON FUNCTION app_private.is_service_public(uuid) FROM PUBLIC;
REVOKE ALL ON FUNCTION app_private.is_alternative_public(uuid) FROM PUBLIC;

GRANT EXECUTE ON FUNCTION app_private.has_content_role() TO authenticated;
GRANT EXECUTE ON FUNCTION app_private.is_admin() TO authenticated;
GRANT EXECUTE ON FUNCTION app_private.is_route_public(uuid) TO anon, authenticated;
GRANT EXECUTE ON FUNCTION app_private.is_segment_public(uuid) TO anon, authenticated;
GRANT EXECUTE ON FUNCTION app_private.is_place_public(uuid) TO anon, authenticated;
GRANT EXECUTE ON FUNCTION app_private.is_observation_public(uuid) TO anon, authenticated;
GRANT EXECUTE ON FUNCTION app_private.is_service_public(uuid) TO anon, authenticated;
GRANT EXECUTE ON FUNCTION app_private.is_alternative_public(uuid) TO anon, authenticated;

-- --------------------------------------------------------------------------
-- 4. Activar RLS en todas las tablas del proyecto
-- --------------------------------------------------------------------------

ALTER TABLE public.cities ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.routes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.segments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.places ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.access_needs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.accessibility_attributes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.observations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.observation_access_needs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.barriers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.barrier_access_needs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.observation_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.evidences ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.observation_evidences ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.services ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.alternatives ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.alternative_segments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.verification_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_roles ENABLE ROW LEVEL SECURITY;

-- --------------------------------------------------------------------------
-- 5. Permisos SQL: mínimos y explícitos
-- --------------------------------------------------------------------------

REVOKE ALL ON
    public.cities,
    public.routes,
    public.segments,
    public.places,
    public.access_needs,
    public.accessibility_attributes,
    public.assessments,
    public.observations,
    public.observation_access_needs,
    public.barriers,
    public.barrier_access_needs,
    public.sources,
    public.observation_sources,
    public.evidences,
    public.observation_evidences,
    public.services,
    public.alternatives,
    public.alternative_segments,
    public.verification_records,
    public.user_roles
FROM anon, authenticated;

-- Lectura para los roles de la API; RLS decide qué filas pueden verse.
GRANT SELECT ON
    public.cities,
    public.routes,
    public.segments,
    public.places,
    public.access_needs,
    public.accessibility_attributes,
    public.assessments,
    public.observations,
    public.observation_access_needs,
    public.barriers,
    public.barrier_access_needs,
    public.sources,
    public.observation_sources,
    public.evidences,
    public.observation_evidences,
    public.services,
    public.alternatives,
    public.alternative_segments,
    public.verification_records,
    public.user_roles
TO anon, authenticated;

-- Escritura editorial: no incluye user_roles ni verification_records.
GRANT INSERT, UPDATE, DELETE ON
    public.cities,
    public.routes,
    public.segments,
    public.places,
    public.access_needs,
    public.accessibility_attributes,
    public.assessments,
    public.observations,
    public.observation_access_needs,
    public.barriers,
    public.barrier_access_needs,
    public.sources,
    public.observation_sources,
    public.evidences,
    public.observation_evidences,
    public.services,
    public.alternatives,
    public.alternative_segments
TO authenticated;

-- Historial: solo INSERT para usuarios con rol editorial, nunca UPDATE/DELETE.
GRANT INSERT ON public.verification_records TO authenticated;

-- Roles: solo SELECT para el propio usuario o administradores; escritura
-- exclusivamente para administradores mediante RLS.
GRANT INSERT, UPDATE, DELETE ON public.user_roles TO authenticated;

-- Secuencias: no se utilizan IDs seriales; no se conceden permisos.

-- --------------------------------------------------------------------------
-- 6. Políticas RLS de contenido editorial
-- --------------------------------------------------------------------------

-- Ciudades: lectura pública solo si publicadas.
CREATE POLICY cities_public_read ON public.cities
FOR SELECT TO anon, authenticated
USING (publication_status = 'published');

CREATE POLICY cities_content_manage ON public.cities
FOR ALL TO authenticated
USING (app_private.has_content_role())
WITH CHECK (app_private.has_content_role());

-- Rutas: la ciudad padre también debe estar publicada.
CREATE POLICY routes_public_read ON public.routes
FOR SELECT TO anon, authenticated
USING (app_private.is_route_public(id));

CREATE POLICY routes_content_manage ON public.routes
FOR ALL TO authenticated
USING (app_private.has_content_role())
WITH CHECK (app_private.has_content_role());

-- Tramos: ruta y ciudad deben estar publicadas.
CREATE POLICY segments_public_read ON public.segments
FOR SELECT TO anon, authenticated
USING (app_private.is_segment_public(id));

CREATE POLICY segments_content_manage ON public.segments
FOR ALL TO authenticated
USING (app_private.has_content_role())
WITH CHECK (app_private.has_content_role());

-- Lugares: lugar y ciudad deben estar publicados.
CREATE POLICY places_public_read ON public.places
FOR SELECT TO anon, authenticated
USING (app_private.is_place_public(id));

CREATE POLICY places_content_manage ON public.places
FOR ALL TO authenticated
USING (app_private.has_content_role())
WITH CHECK (app_private.has_content_role());

-- Catálogos de accesibilidad: consulta pública de elementos activos.
CREATE POLICY access_needs_public_read ON public.access_needs
FOR SELECT TO anon, authenticated
USING (is_active = true);

CREATE POLICY access_needs_content_manage ON public.access_needs
FOR ALL TO authenticated
USING (app_private.has_content_role())
WITH CHECK (app_private.has_content_role());

CREATE POLICY attributes_public_read ON public.accessibility_attributes
FOR SELECT TO anon, authenticated
USING (is_active = true);

CREATE POLICY attributes_content_manage ON public.accessibility_attributes
FOR ALL TO authenticated
USING (app_private.has_content_role())
WITH CHECK (app_private.has_content_role());

-- Evaluaciones: privadas para los roles editoriales.
CREATE POLICY assessments_content_read ON public.assessments
FOR SELECT TO authenticated
USING (app_private.has_content_role());

CREATE POLICY assessments_content_manage ON public.assessments
FOR ALL TO authenticated
USING (app_private.has_content_role())
WITH CHECK (app_private.has_content_role());

-- Observaciones: públicas solo si están publicadas y su objeto padre también.
CREATE POLICY observations_public_read ON public.observations
FOR SELECT TO anon, authenticated
USING (app_private.is_observation_public(id));

CREATE POLICY observations_content_read ON public.observations
FOR SELECT TO authenticated
USING (app_private.has_content_role());

CREATE POLICY observations_content_insert ON public.observations
FOR INSERT TO authenticated
WITH CHECK (app_private.has_content_role());

CREATE POLICY observations_content_update ON public.observations
FOR UPDATE TO authenticated
USING (app_private.has_content_role())
WITH CHECK (app_private.has_content_role());

CREATE POLICY observations_content_delete ON public.observations
FOR DELETE TO authenticated
USING (app_private.has_content_role());

CREATE POLICY observation_needs_public_read ON public.observation_access_needs
FOR SELECT TO anon, authenticated
USING (
    app_private.is_observation_public(observation_id)
    AND EXISTS (
        SELECT 1
        FROM public.access_needs n
        WHERE n.id = access_need_id
          AND n.is_active = true
    )
);

CREATE POLICY observation_needs_content_manage ON public.observation_access_needs
FOR ALL TO authenticated
USING (app_private.has_content_role())
WITH CHECK (app_private.has_content_role());

-- Barreras: privadas en la versión 001; solo usuarios editoriales.
CREATE POLICY barriers_content_manage ON public.barriers
FOR ALL TO authenticated
USING (app_private.has_content_role())
WITH CHECK (app_private.has_content_role());

CREATE POLICY barrier_needs_content_manage ON public.barrier_access_needs
FOR ALL TO authenticated
USING (app_private.has_content_role())
WITH CHECK (app_private.has_content_role());

-- Fuentes y evidencias: privadas por defecto.
CREATE POLICY sources_content_manage ON public.sources
FOR ALL TO authenticated
USING (app_private.has_content_role())
WITH CHECK (app_private.has_content_role());

CREATE POLICY observation_sources_content_manage ON public.observation_sources
FOR ALL TO authenticated
USING (app_private.has_content_role())
WITH CHECK (app_private.has_content_role());

CREATE POLICY evidences_content_manage ON public.evidences
FOR ALL TO authenticated
USING (app_private.has_content_role())
WITH CHECK (app_private.has_content_role());

CREATE POLICY observation_evidences_content_manage ON public.observation_evidences
FOR ALL TO authenticated
USING (app_private.has_content_role())
WITH CHECK (app_private.has_content_role());

-- Servicios: el servicio, la ciudad y, cuando exista, el lugar/tramo padre.
CREATE POLICY services_public_read ON public.services
FOR SELECT TO anon, authenticated
USING (app_private.is_service_public(id));

CREATE POLICY services_content_manage ON public.services
FOR ALL TO authenticated
USING (app_private.has_content_role())
WITH CHECK (app_private.has_content_role());

-- Alternativas: alternativa, ciudad y ruta asociada (si existe) publicadas.
CREATE POLICY alternatives_public_read ON public.alternatives
FOR SELECT TO anon, authenticated
USING (app_private.is_alternative_public(id));

CREATE POLICY alternatives_content_manage ON public.alternatives
FOR ALL TO authenticated
USING (app_private.has_content_role())
WITH CHECK (app_private.has_content_role());

CREATE POLICY alternative_segments_content_manage ON public.alternative_segments
FOR ALL TO authenticated
USING (app_private.has_content_role())
WITH CHECK (app_private.has_content_role());

-- Los tramos de alternativas solo se exponen cuando alternativa y tramo
-- relacionados están publicados.
CREATE POLICY alternative_segments_public_read ON public.alternative_segments
FOR SELECT TO anon, authenticated
USING (
    app_private.is_alternative_public(alternative_id)
    AND app_private.is_segment_public(segment_id)
);

-- --------------------------------------------------------------------------
-- 7. Historial de verificaciones: solo observaciones y solo anexado
-- --------------------------------------------------------------------------

CREATE POLICY verification_records_content_read ON public.verification_records
FOR SELECT TO authenticated
USING (app_private.has_content_role());

CREATE POLICY verification_records_content_insert ON public.verification_records
FOR INSERT TO authenticated
WITH CHECK (app_private.has_content_role());

-- No se crean políticas UPDATE ni DELETE y tampoco se conceden esos permisos.
-- Por tanto, la API no puede modificar ni borrar registros históricos.

-- --------------------------------------------------------------------------
-- 8. Roles: el usuario puede leer sus propios roles; solo admin gestiona roles.
-- --------------------------------------------------------------------------

CREATE POLICY user_roles_read_self_or_admin ON public.user_roles
FOR SELECT TO authenticated
USING (user_id = auth.uid() OR app_private.is_admin());

CREATE POLICY user_roles_admin_insert ON public.user_roles
FOR INSERT TO authenticated
WITH CHECK (app_private.is_admin());

CREATE POLICY user_roles_admin_update ON public.user_roles
FOR UPDATE TO authenticated
USING (app_private.is_admin())
WITH CHECK (app_private.is_admin());

CREATE POLICY user_roles_admin_delete ON public.user_roles
FOR DELETE TO authenticated
USING (app_private.is_admin());

-- --------------------------------------------------------------------------
-- 9. Validación de coherencia entre tipo de atributo y valor de observación
-- --------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION app_private.validate_observation_value()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = ''
AS $$
DECLARE
    v_data_type text;
    v_allowed_values jsonb;
    v_count integer;
BEGIN
    SELECT aa.data_type, aa.allowed_values
      INTO v_data_type, v_allowed_values
      FROM public.accessibility_attributes aa
     WHERE aa.id = NEW.attribute_id;

    IF v_data_type IS NULL THEN
        RAISE EXCEPTION 'El atributo de accesibilidad no existe.';
    END IF;

    v_count :=
        (CASE WHEN NEW.value_boolean IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN NEW.value_number IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN NEW.value_text IS NOT NULL THEN 1 ELSE 0 END);

    IF NEW.result IN ('not_evaluated', 'insufficient_information') THEN
        IF v_count <> 0 THEN
            RAISE EXCEPTION 'Una observación no evaluada o con información insuficiente no debe contener un valor medido.';
        END IF;
        RETURN NEW;
    END IF;

    IF v_data_type = 'boolean' AND
       (NEW.value_boolean IS NULL OR NEW.value_number IS NOT NULL OR NEW.value_text IS NOT NULL) THEN
        RAISE EXCEPTION 'El atributo requiere exactamente un valor booleano.';
    ELSIF v_data_type = 'number' AND
       (NEW.value_number IS NULL OR NEW.value_boolean IS NOT NULL OR NEW.value_text IS NOT NULL) THEN
        RAISE EXCEPTION 'El atributo requiere exactamente un valor numérico.';
    ELSIF v_data_type IN ('text', 'choice') AND
       (NEW.value_text IS NULL OR NEW.value_boolean IS NOT NULL OR NEW.value_number IS NOT NULL) THEN
        RAISE EXCEPTION 'El atributo requiere exactamente un valor de texto.';
    END IF;

    IF v_data_type = 'choice'
       AND NOT EXISTS (
           SELECT 1
             FROM jsonb_array_elements_text(v_allowed_values) AS allowed(value)
            WHERE allowed.value = NEW.value_text
       ) THEN
        RAISE EXCEPTION 'El valor indicado no está incluido en allowed_values para este atributo.';
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER observations_validate_value
BEFORE INSERT OR UPDATE OF attribute_id, result, value_boolean, value_number, value_text
ON public.observations
FOR EACH ROW
EXECUTE FUNCTION app_private.validate_observation_value();

REVOKE ALL ON FUNCTION app_private.prevent_inconsistent_route_city_change() FROM PUBLIC;
REVOKE ALL ON FUNCTION app_private.prevent_inconsistent_segment_route_change() FROM PUBLIC;
REVOKE ALL ON FUNCTION app_private.validate_service_location() FROM PUBLIC;
REVOKE ALL ON FUNCTION app_private.validate_alternative_segment() FROM PUBLIC;
REVOKE ALL ON FUNCTION app_private.valid_allowed_values(text, jsonb) FROM PUBLIC;

REVOKE ALL ON FUNCTION app_private.validate_observation_value() FROM PUBLIC;

-- --------------------------------------------------------------------------
-- 10. updated_at automático en tablas con ese campo
-- --------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION app_private.set_updated_at()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = ''
AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

REVOKE ALL ON FUNCTION app_private.set_updated_at() FROM PUBLIC;

CREATE TRIGGER cities_set_updated_at
BEFORE UPDATE ON public.cities
FOR EACH ROW EXECUTE FUNCTION app_private.set_updated_at();

CREATE TRIGGER routes_set_updated_at
BEFORE UPDATE ON public.routes
FOR EACH ROW EXECUTE FUNCTION app_private.set_updated_at();

CREATE TRIGGER segments_set_updated_at
BEFORE UPDATE ON public.segments
FOR EACH ROW EXECUTE FUNCTION app_private.set_updated_at();

CREATE TRIGGER places_set_updated_at
BEFORE UPDATE ON public.places
FOR EACH ROW EXECUTE FUNCTION app_private.set_updated_at();

CREATE TRIGGER observations_set_updated_at
BEFORE UPDATE ON public.observations
FOR EACH ROW EXECUTE FUNCTION app_private.set_updated_at();

CREATE TRIGGER barriers_set_updated_at
BEFORE UPDATE ON public.barriers
FOR EACH ROW EXECUTE FUNCTION app_private.set_updated_at();

CREATE TRIGGER services_set_updated_at
BEFORE UPDATE ON public.services
FOR EACH ROW EXECUTE FUNCTION app_private.set_updated_at();

CREATE TRIGGER alternatives_set_updated_at
BEFORE UPDATE ON public.alternatives
FOR EACH ROW EXECUTE FUNCTION app_private.set_updated_at();

-- --------------------------------------------------------------------------
-- 11. Comentarios de alcance y seguridad
-- --------------------------------------------------------------------------

COMMENT ON TABLE public.verification_records IS
'Historial append-only de verificaciones de observaciones. En migración 001 no registra verificaciones de rutas, lugares, servicios ni barreras.';

COMMENT ON TABLE public.evidences IS
'Metadatos de evidencias. Los archivos deben almacenarse en un bucket privado de Supabase Storage; esta migración no crea ni configura buckets.';

COMMENT ON TABLE public.access_needs IS
'Catálogo de necesidades de accesibilidad. No almacenar diagnósticos médicos ni datos de salud identificables.';

COMMENT ON TABLE public.observations IS
'Observaciones de accesibilidad con resultado, valores tipados, estado de verificación y estado de publicación separados.';

COMMIT;

-- ============================================================================
-- 12. PASOS POSTERIORES A LA MIGRACIÓN (NO AUTOMÁTICOS)
-- ============================================================================
--
-- A) Crear o confirmar el usuario en Supabase Authentication.
--
-- B) Asignar el primer administrador desde SQL Editor, sustituyendo el UUID
--    por el ID real del usuario. Ejecutar solo tras verificarlo:
--
-- INSERT INTO public.user_roles (user_id, role)
-- VALUES ('UUID_REAL_DEL_USUARIO', 'admin');
--
-- No se crea un administrador automáticamente. No se debe adivinar el UUID.
--
-- C) Comprobar RLS:
--
-- SELECT schemaname, tablename, rowsecurity
-- FROM pg_tables
-- WHERE schemaname = 'public'
-- ORDER BY tablename;
--
-- D) Comprobar políticas:
--
-- SELECT schemaname, tablename, policyname, roles, cmd, qual, with_check
-- FROM pg_policies
-- WHERE schemaname = 'public'
-- ORDER BY tablename, policyname;
--
-- E) Storage:
-- Crear en una fase separada un bucket privado y políticas Storage que
-- permitan leer/escribir únicamente a usuarios editoriales autorizados.
--
-- F) Esta migración es de instalación inicial. No volver a ejecutarla sobre
-- una base ya migrada: no es un script de actualización ni de repetición.
--
-- G) Antes de producción, probar con sesiones reales anon, authenticated
-- sin rol, editor y admin. No basta con inspeccionar las políticas.
-- ============================================================================
