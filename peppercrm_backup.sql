--
-- PostgreSQL database dump
--

\restrict RsYbcl1jXdWZjb35Va0cF4ol0EDu3M29n0p3s2WMjRh7bcTlNtKYbSme3QcMDGL

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: auth; Type: SCHEMA; Schema: -; Owner: supabase_admin
--

CREATE SCHEMA auth;


ALTER SCHEMA auth OWNER TO supabase_admin;

--
-- Name: extensions; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA extensions;


ALTER SCHEMA extensions OWNER TO postgres;

--
-- Name: graphql; Type: SCHEMA; Schema: -; Owner: supabase_admin
--

CREATE SCHEMA graphql;


ALTER SCHEMA graphql OWNER TO supabase_admin;

--
-- Name: graphql_public; Type: SCHEMA; Schema: -; Owner: supabase_admin
--

CREATE SCHEMA graphql_public;


ALTER SCHEMA graphql_public OWNER TO supabase_admin;

--
-- Name: pgbouncer; Type: SCHEMA; Schema: -; Owner: pgbouncer
--

CREATE SCHEMA pgbouncer;


ALTER SCHEMA pgbouncer OWNER TO pgbouncer;

--
-- Name: realtime; Type: SCHEMA; Schema: -; Owner: supabase_admin
--

CREATE SCHEMA realtime;


ALTER SCHEMA realtime OWNER TO supabase_admin;

--
-- Name: storage; Type: SCHEMA; Schema: -; Owner: supabase_admin
--

CREATE SCHEMA storage;


ALTER SCHEMA storage OWNER TO supabase_admin;

--
-- Name: vault; Type: SCHEMA; Schema: -; Owner: supabase_admin
--

CREATE SCHEMA vault;


ALTER SCHEMA vault OWNER TO supabase_admin;

--
-- Name: pg_stat_statements; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_stat_statements WITH SCHEMA extensions;


--
-- Name: EXTENSION pg_stat_statements; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_stat_statements IS 'track planning and execution statistics of all SQL statements executed';


--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA extensions;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: supabase_vault; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS supabase_vault WITH SCHEMA vault;


--
-- Name: EXTENSION supabase_vault; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION supabase_vault IS 'Supabase Vault Extension';


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA extensions;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: aal_level; Type: TYPE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TYPE auth.aal_level AS ENUM (
    'aal1',
    'aal2',
    'aal3'
);


ALTER TYPE auth.aal_level OWNER TO supabase_auth_admin;

--
-- Name: code_challenge_method; Type: TYPE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TYPE auth.code_challenge_method AS ENUM (
    's256',
    'plain'
);


ALTER TYPE auth.code_challenge_method OWNER TO supabase_auth_admin;

--
-- Name: factor_status; Type: TYPE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TYPE auth.factor_status AS ENUM (
    'unverified',
    'verified'
);


ALTER TYPE auth.factor_status OWNER TO supabase_auth_admin;

--
-- Name: factor_type; Type: TYPE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TYPE auth.factor_type AS ENUM (
    'totp',
    'webauthn',
    'phone'
);


ALTER TYPE auth.factor_type OWNER TO supabase_auth_admin;

--
-- Name: oauth_authorization_status; Type: TYPE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TYPE auth.oauth_authorization_status AS ENUM (
    'pending',
    'approved',
    'denied',
    'expired'
);


ALTER TYPE auth.oauth_authorization_status OWNER TO supabase_auth_admin;

--
-- Name: oauth_client_type; Type: TYPE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TYPE auth.oauth_client_type AS ENUM (
    'public',
    'confidential'
);


ALTER TYPE auth.oauth_client_type OWNER TO supabase_auth_admin;

--
-- Name: oauth_registration_type; Type: TYPE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TYPE auth.oauth_registration_type AS ENUM (
    'dynamic',
    'manual'
);


ALTER TYPE auth.oauth_registration_type OWNER TO supabase_auth_admin;

--
-- Name: oauth_response_type; Type: TYPE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TYPE auth.oauth_response_type AS ENUM (
    'code'
);


ALTER TYPE auth.oauth_response_type OWNER TO supabase_auth_admin;

--
-- Name: one_time_token_type; Type: TYPE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TYPE auth.one_time_token_type AS ENUM (
    'confirmation_token',
    'reauthentication_token',
    'recovery_token',
    'email_change_token_new',
    'email_change_token_current',
    'phone_change_token'
);


ALTER TYPE auth.one_time_token_type OWNER TO supabase_auth_admin;

--
-- Name: action; Type: TYPE; Schema: realtime; Owner: supabase_admin
--

CREATE TYPE realtime.action AS ENUM (
    'INSERT',
    'UPDATE',
    'DELETE',
    'TRUNCATE',
    'ERROR'
);


ALTER TYPE realtime.action OWNER TO supabase_admin;

--
-- Name: equality_op; Type: TYPE; Schema: realtime; Owner: supabase_admin
--

CREATE TYPE realtime.equality_op AS ENUM (
    'eq',
    'neq',
    'lt',
    'lte',
    'gt',
    'gte',
    'in'
);


ALTER TYPE realtime.equality_op OWNER TO supabase_admin;

--
-- Name: user_defined_filter; Type: TYPE; Schema: realtime; Owner: supabase_admin
--

CREATE TYPE realtime.user_defined_filter AS (
	column_name text,
	op realtime.equality_op,
	value text
);


ALTER TYPE realtime.user_defined_filter OWNER TO supabase_admin;

--
-- Name: wal_column; Type: TYPE; Schema: realtime; Owner: supabase_admin
--

CREATE TYPE realtime.wal_column AS (
	name text,
	type_name text,
	type_oid oid,
	value jsonb,
	is_pkey boolean,
	is_selectable boolean
);


ALTER TYPE realtime.wal_column OWNER TO supabase_admin;

--
-- Name: wal_rls; Type: TYPE; Schema: realtime; Owner: supabase_admin
--

CREATE TYPE realtime.wal_rls AS (
	wal jsonb,
	is_rls_enabled boolean,
	subscription_ids uuid[],
	errors text[]
);


ALTER TYPE realtime.wal_rls OWNER TO supabase_admin;

--
-- Name: buckettype; Type: TYPE; Schema: storage; Owner: supabase_storage_admin
--

CREATE TYPE storage.buckettype AS ENUM (
    'STANDARD',
    'ANALYTICS',
    'VECTOR'
);


ALTER TYPE storage.buckettype OWNER TO supabase_storage_admin;

--
-- Name: email(); Type: FUNCTION; Schema: auth; Owner: supabase_auth_admin
--

CREATE FUNCTION auth.email() RETURNS text
    LANGUAGE sql STABLE
    AS $$
  select 
  coalesce(
    nullif(current_setting('request.jwt.claim.email', true), ''),
    (nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'email')
  )::text
$$;


ALTER FUNCTION auth.email() OWNER TO supabase_auth_admin;

--
-- Name: FUNCTION email(); Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON FUNCTION auth.email() IS 'Deprecated. Use auth.jwt() -> ''email'' instead.';


--
-- Name: jwt(); Type: FUNCTION; Schema: auth; Owner: supabase_auth_admin
--

CREATE FUNCTION auth.jwt() RETURNS jsonb
    LANGUAGE sql STABLE
    AS $$
  select 
    coalesce(
        nullif(current_setting('request.jwt.claim', true), ''),
        nullif(current_setting('request.jwt.claims', true), '')
    )::jsonb
$$;


ALTER FUNCTION auth.jwt() OWNER TO supabase_auth_admin;

--
-- Name: role(); Type: FUNCTION; Schema: auth; Owner: supabase_auth_admin
--

CREATE FUNCTION auth.role() RETURNS text
    LANGUAGE sql STABLE
    AS $$
  select 
  coalesce(
    nullif(current_setting('request.jwt.claim.role', true), ''),
    (nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'role')
  )::text
$$;


ALTER FUNCTION auth.role() OWNER TO supabase_auth_admin;

--
-- Name: FUNCTION role(); Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON FUNCTION auth.role() IS 'Deprecated. Use auth.jwt() -> ''role'' instead.';


--
-- Name: uid(); Type: FUNCTION; Schema: auth; Owner: supabase_auth_admin
--

CREATE FUNCTION auth.uid() RETURNS uuid
    LANGUAGE sql STABLE
    AS $$
  select 
  coalesce(
    nullif(current_setting('request.jwt.claim.sub', true), ''),
    (nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'sub')
  )::uuid
$$;


ALTER FUNCTION auth.uid() OWNER TO supabase_auth_admin;

--
-- Name: FUNCTION uid(); Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON FUNCTION auth.uid() IS 'Deprecated. Use auth.jwt() -> ''sub'' instead.';


--
-- Name: grant_pg_cron_access(); Type: FUNCTION; Schema: extensions; Owner: supabase_admin
--

CREATE FUNCTION extensions.grant_pg_cron_access() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF EXISTS (
    SELECT
    FROM pg_event_trigger_ddl_commands() AS ev
    JOIN pg_extension AS ext
    ON ev.objid = ext.oid
    WHERE ext.extname = 'pg_cron'
  )
  THEN
    grant usage on schema cron to postgres with grant option;

    alter default privileges in schema cron grant all on tables to postgres with grant option;
    alter default privileges in schema cron grant all on functions to postgres with grant option;
    alter default privileges in schema cron grant all on sequences to postgres with grant option;

    alter default privileges for user supabase_admin in schema cron grant all
        on sequences to postgres with grant option;
    alter default privileges for user supabase_admin in schema cron grant all
        on tables to postgres with grant option;
    alter default privileges for user supabase_admin in schema cron grant all
        on functions to postgres with grant option;

    grant all privileges on all tables in schema cron to postgres with grant option;
    revoke all on table cron.job from postgres;
    grant select on table cron.job to postgres with grant option;
  END IF;
END;
$$;


ALTER FUNCTION extensions.grant_pg_cron_access() OWNER TO supabase_admin;

--
-- Name: FUNCTION grant_pg_cron_access(); Type: COMMENT; Schema: extensions; Owner: supabase_admin
--

COMMENT ON FUNCTION extensions.grant_pg_cron_access() IS 'Grants access to pg_cron';


--
-- Name: grant_pg_graphql_access(); Type: FUNCTION; Schema: extensions; Owner: supabase_admin
--

CREATE FUNCTION extensions.grant_pg_graphql_access() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $_$
DECLARE
    func_is_graphql_resolve bool;
BEGIN
    func_is_graphql_resolve = (
        SELECT n.proname = 'resolve'
        FROM pg_event_trigger_ddl_commands() AS ev
        LEFT JOIN pg_catalog.pg_proc AS n
        ON ev.objid = n.oid
    );

    IF func_is_graphql_resolve
    THEN
        -- Update public wrapper to pass all arguments through to the pg_graphql resolve func
        DROP FUNCTION IF EXISTS graphql_public.graphql;
        create or replace function graphql_public.graphql(
            "operationName" text default null,
            query text default null,
            variables jsonb default null,
            extensions jsonb default null
        )
            returns jsonb
            language sql
        as $$
            select graphql.resolve(
                query := query,
                variables := coalesce(variables, '{}'),
                "operationName" := "operationName",
                extensions := extensions
            );
        $$;

        -- This hook executes when `graphql.resolve` is created. That is not necessarily the last
        -- function in the extension so we need to grant permissions on existing entities AND
        -- update default permissions to any others that are created after `graphql.resolve`
        grant usage on schema graphql to postgres, anon, authenticated, service_role;
        grant select on all tables in schema graphql to postgres, anon, authenticated, service_role;
        grant execute on all functions in schema graphql to postgres, anon, authenticated, service_role;
        grant all on all sequences in schema graphql to postgres, anon, authenticated, service_role;
        alter default privileges in schema graphql grant all on tables to postgres, anon, authenticated, service_role;
        alter default privileges in schema graphql grant all on functions to postgres, anon, authenticated, service_role;
        alter default privileges in schema graphql grant all on sequences to postgres, anon, authenticated, service_role;

        -- Allow postgres role to allow granting usage on graphql and graphql_public schemas to custom roles
        grant usage on schema graphql_public to postgres with grant option;
        grant usage on schema graphql to postgres with grant option;
    END IF;

END;
$_$;


ALTER FUNCTION extensions.grant_pg_graphql_access() OWNER TO supabase_admin;

--
-- Name: FUNCTION grant_pg_graphql_access(); Type: COMMENT; Schema: extensions; Owner: supabase_admin
--

COMMENT ON FUNCTION extensions.grant_pg_graphql_access() IS 'Grants access to pg_graphql';


--
-- Name: grant_pg_net_access(); Type: FUNCTION; Schema: extensions; Owner: supabase_admin
--

CREATE FUNCTION extensions.grant_pg_net_access() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM pg_event_trigger_ddl_commands() AS ev
    JOIN pg_extension AS ext
    ON ev.objid = ext.oid
    WHERE ext.extname = 'pg_net'
  )
  THEN
    IF NOT EXISTS (
      SELECT 1
      FROM pg_roles
      WHERE rolname = 'supabase_functions_admin'
    )
    THEN
      CREATE USER supabase_functions_admin NOINHERIT CREATEROLE LOGIN NOREPLICATION;
    END IF;

    GRANT USAGE ON SCHEMA net TO supabase_functions_admin, postgres, anon, authenticated, service_role;

    IF EXISTS (
      SELECT FROM pg_extension
      WHERE extname = 'pg_net'
      -- all versions in use on existing projects as of 2025-02-20
      -- version 0.12.0 onwards don't need these applied
      AND extversion IN ('0.2', '0.6', '0.7', '0.7.1', '0.8', '0.10.0', '0.11.0')
    ) THEN
      ALTER function net.http_get(url text, params jsonb, headers jsonb, timeout_milliseconds integer) SECURITY DEFINER;
      ALTER function net.http_post(url text, body jsonb, params jsonb, headers jsonb, timeout_milliseconds integer) SECURITY DEFINER;

      ALTER function net.http_get(url text, params jsonb, headers jsonb, timeout_milliseconds integer) SET search_path = net;
      ALTER function net.http_post(url text, body jsonb, params jsonb, headers jsonb, timeout_milliseconds integer) SET search_path = net;

      REVOKE ALL ON FUNCTION net.http_get(url text, params jsonb, headers jsonb, timeout_milliseconds integer) FROM PUBLIC;
      REVOKE ALL ON FUNCTION net.http_post(url text, body jsonb, params jsonb, headers jsonb, timeout_milliseconds integer) FROM PUBLIC;

      GRANT EXECUTE ON FUNCTION net.http_get(url text, params jsonb, headers jsonb, timeout_milliseconds integer) TO supabase_functions_admin, postgres, anon, authenticated, service_role;
      GRANT EXECUTE ON FUNCTION net.http_post(url text, body jsonb, params jsonb, headers jsonb, timeout_milliseconds integer) TO supabase_functions_admin, postgres, anon, authenticated, service_role;
    END IF;
  END IF;
END;
$$;


ALTER FUNCTION extensions.grant_pg_net_access() OWNER TO supabase_admin;

--
-- Name: FUNCTION grant_pg_net_access(); Type: COMMENT; Schema: extensions; Owner: supabase_admin
--

COMMENT ON FUNCTION extensions.grant_pg_net_access() IS 'Grants access to pg_net';


--
-- Name: pgrst_ddl_watch(); Type: FUNCTION; Schema: extensions; Owner: supabase_admin
--

CREATE FUNCTION extensions.pgrst_ddl_watch() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  cmd record;
BEGIN
  FOR cmd IN SELECT * FROM pg_event_trigger_ddl_commands()
  LOOP
    IF cmd.command_tag IN (
      'CREATE SCHEMA', 'ALTER SCHEMA'
    , 'CREATE TABLE', 'CREATE TABLE AS', 'SELECT INTO', 'ALTER TABLE'
    , 'CREATE FOREIGN TABLE', 'ALTER FOREIGN TABLE'
    , 'CREATE VIEW', 'ALTER VIEW'
    , 'CREATE MATERIALIZED VIEW', 'ALTER MATERIALIZED VIEW'
    , 'CREATE FUNCTION', 'ALTER FUNCTION'
    , 'CREATE TRIGGER'
    , 'CREATE TYPE', 'ALTER TYPE'
    , 'CREATE RULE'
    , 'COMMENT'
    )
    -- don't notify in case of CREATE TEMP table or other objects created on pg_temp
    AND cmd.schema_name is distinct from 'pg_temp'
    THEN
      NOTIFY pgrst, 'reload schema';
    END IF;
  END LOOP;
END; $$;


ALTER FUNCTION extensions.pgrst_ddl_watch() OWNER TO supabase_admin;

--
-- Name: pgrst_drop_watch(); Type: FUNCTION; Schema: extensions; Owner: supabase_admin
--

CREATE FUNCTION extensions.pgrst_drop_watch() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  obj record;
BEGIN
  FOR obj IN SELECT * FROM pg_event_trigger_dropped_objects()
  LOOP
    IF obj.object_type IN (
      'schema'
    , 'table'
    , 'foreign table'
    , 'view'
    , 'materialized view'
    , 'function'
    , 'trigger'
    , 'type'
    , 'rule'
    )
    AND obj.is_temporary IS false -- no pg_temp objects
    THEN
      NOTIFY pgrst, 'reload schema';
    END IF;
  END LOOP;
END; $$;


ALTER FUNCTION extensions.pgrst_drop_watch() OWNER TO supabase_admin;

--
-- Name: set_graphql_placeholder(); Type: FUNCTION; Schema: extensions; Owner: supabase_admin
--

CREATE FUNCTION extensions.set_graphql_placeholder() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $_$
    DECLARE
    graphql_is_dropped bool;
    BEGIN
    graphql_is_dropped = (
        SELECT ev.schema_name = 'graphql_public'
        FROM pg_event_trigger_dropped_objects() AS ev
        WHERE ev.schema_name = 'graphql_public'
    );

    IF graphql_is_dropped
    THEN
        create or replace function graphql_public.graphql(
            "operationName" text default null,
            query text default null,
            variables jsonb default null,
            extensions jsonb default null
        )
            returns jsonb
            language plpgsql
        as $$
            DECLARE
                server_version float;
            BEGIN
                server_version = (SELECT (SPLIT_PART((select version()), ' ', 2))::float);

                IF server_version >= 14 THEN
                    RETURN jsonb_build_object(
                        'errors', jsonb_build_array(
                            jsonb_build_object(
                                'message', 'pg_graphql extension is not enabled.'
                            )
                        )
                    );
                ELSE
                    RETURN jsonb_build_object(
                        'errors', jsonb_build_array(
                            jsonb_build_object(
                                'message', 'pg_graphql is only available on projects running Postgres 14 onwards.'
                            )
                        )
                    );
                END IF;
            END;
        $$;
    END IF;

    END;
$_$;


ALTER FUNCTION extensions.set_graphql_placeholder() OWNER TO supabase_admin;

--
-- Name: FUNCTION set_graphql_placeholder(); Type: COMMENT; Schema: extensions; Owner: supabase_admin
--

COMMENT ON FUNCTION extensions.set_graphql_placeholder() IS 'Reintroduces placeholder function for graphql_public.graphql';


--
-- Name: graphql(text, text, jsonb, jsonb); Type: FUNCTION; Schema: graphql_public; Owner: supabase_admin
--

CREATE FUNCTION graphql_public.graphql("operationName" text DEFAULT NULL::text, query text DEFAULT NULL::text, variables jsonb DEFAULT NULL::jsonb, extensions jsonb DEFAULT NULL::jsonb) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
            DECLARE
                server_version float;
            BEGIN
                server_version = (SELECT (SPLIT_PART((select version()), ' ', 2))::float);

                IF server_version >= 14 THEN
                    RETURN jsonb_build_object(
                        'errors', jsonb_build_array(
                            jsonb_build_object(
                                'message', 'pg_graphql extension is not enabled.'
                            )
                        )
                    );
                ELSE
                    RETURN jsonb_build_object(
                        'errors', jsonb_build_array(
                            jsonb_build_object(
                                'message', 'pg_graphql is only available on projects running Postgres 14 onwards.'
                            )
                        )
                    );
                END IF;
            END;
        $$;


ALTER FUNCTION graphql_public.graphql("operationName" text, query text, variables jsonb, extensions jsonb) OWNER TO supabase_admin;

--
-- Name: get_auth(text); Type: FUNCTION; Schema: pgbouncer; Owner: supabase_admin
--

CREATE FUNCTION pgbouncer.get_auth(p_usename text) RETURNS TABLE(username text, password text)
    LANGUAGE plpgsql SECURITY DEFINER
    SET search_path TO ''
    AS $_$
  BEGIN
      RAISE DEBUG 'PgBouncer auth request: %', p_usename;

      RETURN QUERY
      SELECT
          rolname::text,
          CASE WHEN rolvaliduntil < now()
              THEN null
              ELSE rolpassword::text
          END
      FROM pg_authid
      WHERE rolname=$1 and rolcanlogin;
  END;
  $_$;


ALTER FUNCTION pgbouncer.get_auth(p_usename text) OWNER TO supabase_admin;

--
-- Name: apply_rls(jsonb, integer); Type: FUNCTION; Schema: realtime; Owner: supabase_admin
--

CREATE FUNCTION realtime.apply_rls(wal jsonb, max_record_bytes integer DEFAULT (1024 * 1024)) RETURNS SETOF realtime.wal_rls
    LANGUAGE plpgsql
    AS $$
declare
-- Regclass of the table e.g. public.notes
entity_ regclass = (quote_ident(wal ->> 'schema') || '.' || quote_ident(wal ->> 'table'))::regclass;

-- I, U, D, T: insert, update ...
action realtime.action = (
    case wal ->> 'action'
        when 'I' then 'INSERT'
        when 'U' then 'UPDATE'
        when 'D' then 'DELETE'
        else 'ERROR'
    end
);

-- Is row level security enabled for the table
is_rls_enabled bool = relrowsecurity from pg_class where oid = entity_;

subscriptions realtime.subscription[] = array_agg(subs)
    from
        realtime.subscription subs
    where
        subs.entity = entity_
        -- Filter by action early - only get subscriptions interested in this action
        -- action_filter column can be: '*' (all), 'INSERT', 'UPDATE', or 'DELETE'
        and (subs.action_filter = '*' or subs.action_filter = action::text);

-- Subscription vars
roles regrole[] = array_agg(distinct us.claims_role::text)
    from
        unnest(subscriptions) us;

working_role regrole;
claimed_role regrole;
claims jsonb;

subscription_id uuid;
subscription_has_access bool;
visible_to_subscription_ids uuid[] = '{}';

-- structured info for wal's columns
columns realtime.wal_column[];
-- previous identity values for update/delete
old_columns realtime.wal_column[];

error_record_exceeds_max_size boolean = octet_length(wal::text) > max_record_bytes;

-- Primary jsonb output for record
output jsonb;

begin
perform set_config('role', null, true);

columns =
    array_agg(
        (
            x->>'name',
            x->>'type',
            x->>'typeoid',
            realtime.cast(
                (x->'value') #>> '{}',
                coalesce(
                    (x->>'typeoid')::regtype, -- null when wal2json version <= 2.4
                    (x->>'type')::regtype
                )
            ),
            (pks ->> 'name') is not null,
            true
        )::realtime.wal_column
    )
    from
        jsonb_array_elements(wal -> 'columns') x
        left join jsonb_array_elements(wal -> 'pk') pks
            on (x ->> 'name') = (pks ->> 'name');

old_columns =
    array_agg(
        (
            x->>'name',
            x->>'type',
            x->>'typeoid',
            realtime.cast(
                (x->'value') #>> '{}',
                coalesce(
                    (x->>'typeoid')::regtype, -- null when wal2json version <= 2.4
                    (x->>'type')::regtype
                )
            ),
            (pks ->> 'name') is not null,
            true
        )::realtime.wal_column
    )
    from
        jsonb_array_elements(wal -> 'identity') x
        left join jsonb_array_elements(wal -> 'pk') pks
            on (x ->> 'name') = (pks ->> 'name');

for working_role in select * from unnest(roles) loop

    -- Update `is_selectable` for columns and old_columns
    columns =
        array_agg(
            (
                c.name,
                c.type_name,
                c.type_oid,
                c.value,
                c.is_pkey,
                pg_catalog.has_column_privilege(working_role, entity_, c.name, 'SELECT')
            )::realtime.wal_column
        )
        from
            unnest(columns) c;

    old_columns =
            array_agg(
                (
                    c.name,
                    c.type_name,
                    c.type_oid,
                    c.value,
                    c.is_pkey,
                    pg_catalog.has_column_privilege(working_role, entity_, c.name, 'SELECT')
                )::realtime.wal_column
            )
            from
                unnest(old_columns) c;

    if action <> 'DELETE' and count(1) = 0 from unnest(columns) c where c.is_pkey then
        return next (
            jsonb_build_object(
                'schema', wal ->> 'schema',
                'table', wal ->> 'table',
                'type', action
            ),
            is_rls_enabled,
            -- subscriptions is already filtered by entity
            (select array_agg(s.subscription_id) from unnest(subscriptions) as s where claims_role = working_role),
            array['Error 400: Bad Request, no primary key']
        )::realtime.wal_rls;

    -- The claims role does not have SELECT permission to the primary key of entity
    elsif action <> 'DELETE' and sum(c.is_selectable::int) <> count(1) from unnest(columns) c where c.is_pkey then
        return next (
            jsonb_build_object(
                'schema', wal ->> 'schema',
                'table', wal ->> 'table',
                'type', action
            ),
            is_rls_enabled,
            (select array_agg(s.subscription_id) from unnest(subscriptions) as s where claims_role = working_role),
            array['Error 401: Unauthorized']
        )::realtime.wal_rls;

    else
        output = jsonb_build_object(
            'schema', wal ->> 'schema',
            'table', wal ->> 'table',
            'type', action,
            'commit_timestamp', to_char(
                ((wal ->> 'timestamp')::timestamptz at time zone 'utc'),
                'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"'
            ),
            'columns', (
                select
                    jsonb_agg(
                        jsonb_build_object(
                            'name', pa.attname,
                            'type', pt.typname
                        )
                        order by pa.attnum asc
                    )
                from
                    pg_attribute pa
                    join pg_type pt
                        on pa.atttypid = pt.oid
                where
                    attrelid = entity_
                    and attnum > 0
                    and pg_catalog.has_column_privilege(working_role, entity_, pa.attname, 'SELECT')
            )
        )
        -- Add "record" key for insert and update
        || case
            when action in ('INSERT', 'UPDATE') then
                jsonb_build_object(
                    'record',
                    (
                        select
                            jsonb_object_agg(
                                -- if unchanged toast, get column name and value from old record
                                coalesce((c).name, (oc).name),
                                case
                                    when (c).name is null then (oc).value
                                    else (c).value
                                end
                            )
                        from
                            unnest(columns) c
                            full outer join unnest(old_columns) oc
                                on (c).name = (oc).name
                        where
                            coalesce((c).is_selectable, (oc).is_selectable)
                            and ( not error_record_exceeds_max_size or (octet_length((c).value::text) <= 64))
                    )
                )
            else '{}'::jsonb
        end
        -- Add "old_record" key for update and delete
        || case
            when action = 'UPDATE' then
                jsonb_build_object(
                        'old_record',
                        (
                            select jsonb_object_agg((c).name, (c).value)
                            from unnest(old_columns) c
                            where
                                (c).is_selectable
                                and ( not error_record_exceeds_max_size or (octet_length((c).value::text) <= 64))
                        )
                    )
            when action = 'DELETE' then
                jsonb_build_object(
                    'old_record',
                    (
                        select jsonb_object_agg((c).name, (c).value)
                        from unnest(old_columns) c
                        where
                            (c).is_selectable
                            and ( not error_record_exceeds_max_size or (octet_length((c).value::text) <= 64))
                            and ( not is_rls_enabled or (c).is_pkey ) -- if RLS enabled, we can't secure deletes so filter to pkey
                    )
                )
            else '{}'::jsonb
        end;

        -- Create the prepared statement
        if is_rls_enabled and action <> 'DELETE' then
            if (select 1 from pg_prepared_statements where name = 'walrus_rls_stmt' limit 1) > 0 then
                deallocate walrus_rls_stmt;
            end if;
            execute realtime.build_prepared_statement_sql('walrus_rls_stmt', entity_, columns);
        end if;

        visible_to_subscription_ids = '{}';

        for subscription_id, claims in (
                select
                    subs.subscription_id,
                    subs.claims
                from
                    unnest(subscriptions) subs
                where
                    subs.entity = entity_
                    and subs.claims_role = working_role
                    and (
                        realtime.is_visible_through_filters(columns, subs.filters)
                        or (
                          action = 'DELETE'
                          and realtime.is_visible_through_filters(old_columns, subs.filters)
                        )
                    )
        ) loop

            if not is_rls_enabled or action = 'DELETE' then
                visible_to_subscription_ids = visible_to_subscription_ids || subscription_id;
            else
                -- Check if RLS allows the role to see the record
                perform
                    -- Trim leading and trailing quotes from working_role because set_config
                    -- doesn't recognize the role as valid if they are included
                    set_config('role', trim(both '"' from working_role::text), true),
                    set_config('request.jwt.claims', claims::text, true);

                execute 'execute walrus_rls_stmt' into subscription_has_access;

                if subscription_has_access then
                    visible_to_subscription_ids = visible_to_subscription_ids || subscription_id;
                end if;
            end if;
        end loop;

        perform set_config('role', null, true);

        return next (
            output,
            is_rls_enabled,
            visible_to_subscription_ids,
            case
                when error_record_exceeds_max_size then array['Error 413: Payload Too Large']
                else '{}'
            end
        )::realtime.wal_rls;

    end if;
end loop;

perform set_config('role', null, true);
end;
$$;


ALTER FUNCTION realtime.apply_rls(wal jsonb, max_record_bytes integer) OWNER TO supabase_admin;

--
-- Name: broadcast_changes(text, text, text, text, text, record, record, text); Type: FUNCTION; Schema: realtime; Owner: supabase_admin
--

CREATE FUNCTION realtime.broadcast_changes(topic_name text, event_name text, operation text, table_name text, table_schema text, new record, old record, level text DEFAULT 'ROW'::text) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
    -- Declare a variable to hold the JSONB representation of the row
    row_data jsonb := '{}'::jsonb;
BEGIN
    IF level = 'STATEMENT' THEN
        RAISE EXCEPTION 'function can only be triggered for each row, not for each statement';
    END IF;
    -- Check the operation type and handle accordingly
    IF operation = 'INSERT' OR operation = 'UPDATE' OR operation = 'DELETE' THEN
        row_data := jsonb_build_object('old_record', OLD, 'record', NEW, 'operation', operation, 'table', table_name, 'schema', table_schema);
        PERFORM realtime.send (row_data, event_name, topic_name);
    ELSE
        RAISE EXCEPTION 'Unexpected operation type: %', operation;
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Failed to process the row: %', SQLERRM;
END;

$$;


ALTER FUNCTION realtime.broadcast_changes(topic_name text, event_name text, operation text, table_name text, table_schema text, new record, old record, level text) OWNER TO supabase_admin;

--
-- Name: build_prepared_statement_sql(text, regclass, realtime.wal_column[]); Type: FUNCTION; Schema: realtime; Owner: supabase_admin
--

CREATE FUNCTION realtime.build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]) RETURNS text
    LANGUAGE sql
    AS $$
      /*
      Builds a sql string that, if executed, creates a prepared statement to
      tests retrive a row from *entity* by its primary key columns.
      Example
          select realtime.build_prepared_statement_sql('public.notes', '{"id"}'::text[], '{"bigint"}'::text[])
      */
          select
      'prepare ' || prepared_statement_name || ' as
          select
              exists(
                  select
                      1
                  from
                      ' || entity || '
                  where
                      ' || string_agg(quote_ident(pkc.name) || '=' || quote_nullable(pkc.value #>> '{}') , ' and ') || '
              )'
          from
              unnest(columns) pkc
          where
              pkc.is_pkey
          group by
              entity
      $$;


ALTER FUNCTION realtime.build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]) OWNER TO supabase_admin;

--
-- Name: cast(text, regtype); Type: FUNCTION; Schema: realtime; Owner: supabase_admin
--

CREATE FUNCTION realtime."cast"(val text, type_ regtype) RETURNS jsonb
    LANGUAGE plpgsql IMMUTABLE
    AS $$
declare
  res jsonb;
begin
  if type_::text = 'bytea' then
    return to_jsonb(val);
  end if;
  execute format('select to_jsonb(%L::'|| type_::text || ')', val) into res;
  return res;
end
$$;


ALTER FUNCTION realtime."cast"(val text, type_ regtype) OWNER TO supabase_admin;

--
-- Name: check_equality_op(realtime.equality_op, regtype, text, text); Type: FUNCTION; Schema: realtime; Owner: supabase_admin
--

CREATE FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text) RETURNS boolean
    LANGUAGE plpgsql IMMUTABLE
    AS $$
      /*
      Casts *val_1* and *val_2* as type *type_* and check the *op* condition for truthiness
      */
      declare
          op_symbol text = (
              case
                  when op = 'eq' then '='
                  when op = 'neq' then '!='
                  when op = 'lt' then '<'
                  when op = 'lte' then '<='
                  when op = 'gt' then '>'
                  when op = 'gte' then '>='
                  when op = 'in' then '= any'
                  else 'UNKNOWN OP'
              end
          );
          res boolean;
      begin
          execute format(
              'select %L::'|| type_::text || ' ' || op_symbol
              || ' ( %L::'
              || (
                  case
                      when op = 'in' then type_::text || '[]'
                      else type_::text end
              )
              || ')', val_1, val_2) into res;
          return res;
      end;
      $$;


ALTER FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text) OWNER TO supabase_admin;

--
-- Name: is_visible_through_filters(realtime.wal_column[], realtime.user_defined_filter[]); Type: FUNCTION; Schema: realtime; Owner: supabase_admin
--

CREATE FUNCTION realtime.is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]) RETURNS boolean
    LANGUAGE sql IMMUTABLE
    AS $_$
    /*
    Should the record be visible (true) or filtered out (false) after *filters* are applied
    */
        select
            -- Default to allowed when no filters present
            $2 is null -- no filters. this should not happen because subscriptions has a default
            or array_length($2, 1) is null -- array length of an empty array is null
            or bool_and(
                coalesce(
                    realtime.check_equality_op(
                        op:=f.op,
                        type_:=coalesce(
                            col.type_oid::regtype, -- null when wal2json version <= 2.4
                            col.type_name::regtype
                        ),
                        -- cast jsonb to text
                        val_1:=col.value #>> '{}',
                        val_2:=f.value
                    ),
                    false -- if null, filter does not match
                )
            )
        from
            unnest(filters) f
            join unnest(columns) col
                on f.column_name = col.name;
    $_$;


ALTER FUNCTION realtime.is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]) OWNER TO supabase_admin;

--
-- Name: list_changes(name, name, integer, integer); Type: FUNCTION; Schema: realtime; Owner: supabase_admin
--

CREATE FUNCTION realtime.list_changes(publication name, slot_name name, max_changes integer, max_record_bytes integer) RETURNS TABLE(wal jsonb, is_rls_enabled boolean, subscription_ids uuid[], errors text[], slot_changes_count bigint)
    LANGUAGE sql
    SET log_min_messages TO 'fatal'
    AS $$
  WITH pub AS (
    SELECT
      concat_ws(
        ',',
        CASE WHEN bool_or(pubinsert) THEN 'insert' ELSE NULL END,
        CASE WHEN bool_or(pubupdate) THEN 'update' ELSE NULL END,
        CASE WHEN bool_or(pubdelete) THEN 'delete' ELSE NULL END
      ) AS w2j_actions,
      coalesce(
        string_agg(
          realtime.quote_wal2json(format('%I.%I', schemaname, tablename)::regclass),
          ','
        ) filter (WHERE ppt.tablename IS NOT NULL AND ppt.tablename NOT LIKE '% %'),
        ''
      ) AS w2j_add_tables
    FROM pg_publication pp
    LEFT JOIN pg_publication_tables ppt ON pp.pubname = ppt.pubname
    WHERE pp.pubname = publication
    GROUP BY pp.pubname
    LIMIT 1
  ),
  -- MATERIALIZED ensures pg_logical_slot_get_changes is called exactly once
  w2j AS MATERIALIZED (
    SELECT x.*, pub.w2j_add_tables
    FROM pub,
         pg_logical_slot_get_changes(
           slot_name, null, max_changes,
           'include-pk', 'true',
           'include-transaction', 'false',
           'include-timestamp', 'true',
           'include-type-oids', 'true',
           'format-version', '2',
           'actions', pub.w2j_actions,
           'add-tables', pub.w2j_add_tables
         ) x
  ),
  -- Count raw slot entries before apply_rls/subscription filter
  slot_count AS (
    SELECT count(*)::bigint AS cnt
    FROM w2j
    WHERE w2j.w2j_add_tables <> ''
  ),
  -- Apply RLS and filter as before
  rls_filtered AS (
    SELECT xyz.wal, xyz.is_rls_enabled, xyz.subscription_ids, xyz.errors
    FROM w2j,
         realtime.apply_rls(
           wal := w2j.data::jsonb,
           max_record_bytes := max_record_bytes
         ) xyz(wal, is_rls_enabled, subscription_ids, errors)
    WHERE w2j.w2j_add_tables <> ''
      AND xyz.subscription_ids[1] IS NOT NULL
  )
  -- Real rows with slot count attached
  SELECT rf.wal, rf.is_rls_enabled, rf.subscription_ids, rf.errors, sc.cnt
  FROM rls_filtered rf, slot_count sc

  UNION ALL

  -- Sentinel row: always returned when no real rows exist so Elixir can
  -- always read slot_changes_count. Identified by wal IS NULL.
  SELECT null, null, null, null, sc.cnt
  FROM slot_count sc
  WHERE NOT EXISTS (SELECT 1 FROM rls_filtered)
$$;


ALTER FUNCTION realtime.list_changes(publication name, slot_name name, max_changes integer, max_record_bytes integer) OWNER TO supabase_admin;

--
-- Name: quote_wal2json(regclass); Type: FUNCTION; Schema: realtime; Owner: supabase_admin
--

CREATE FUNCTION realtime.quote_wal2json(entity regclass) RETURNS text
    LANGUAGE sql IMMUTABLE STRICT
    AS $$
      select
        (
          select string_agg('' || ch,'')
          from unnest(string_to_array(nsp.nspname::text, null)) with ordinality x(ch, idx)
          where
            not (x.idx = 1 and x.ch = '"')
            and not (
              x.idx = array_length(string_to_array(nsp.nspname::text, null), 1)
              and x.ch = '"'
            )
        )
        || '.'
        || (
          select string_agg('' || ch,'')
          from unnest(string_to_array(pc.relname::text, null)) with ordinality x(ch, idx)
          where
            not (x.idx = 1 and x.ch = '"')
            and not (
              x.idx = array_length(string_to_array(nsp.nspname::text, null), 1)
              and x.ch = '"'
            )
          )
      from
        pg_class pc
        join pg_namespace nsp
          on pc.relnamespace = nsp.oid
      where
        pc.oid = entity
    $$;


ALTER FUNCTION realtime.quote_wal2json(entity regclass) OWNER TO supabase_admin;

--
-- Name: send(jsonb, text, text, boolean); Type: FUNCTION; Schema: realtime; Owner: supabase_admin
--

CREATE FUNCTION realtime.send(payload jsonb, event text, topic text, private boolean DEFAULT true) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
  generated_id uuid;
  final_payload jsonb;
BEGIN
  BEGIN
    -- Generate a new UUID for the id
    generated_id := gen_random_uuid();

    -- Check if payload has an 'id' key, if not, add the generated UUID
    IF payload ? 'id' THEN
      final_payload := payload;
    ELSE
      final_payload := jsonb_set(payload, '{id}', to_jsonb(generated_id));
    END IF;

    -- Set the topic configuration
    EXECUTE format('SET LOCAL realtime.topic TO %L', topic);

    -- Attempt to insert the message
    INSERT INTO realtime.messages (id, payload, event, topic, private, extension)
    VALUES (generated_id, final_payload, event, topic, private, 'broadcast');
  EXCEPTION
    WHEN OTHERS THEN
      -- Capture and notify the error
      RAISE WARNING 'ErrorSendingBroadcastMessage: %', SQLERRM;
  END;
END;
$$;


ALTER FUNCTION realtime.send(payload jsonb, event text, topic text, private boolean) OWNER TO supabase_admin;

--
-- Name: subscription_check_filters(); Type: FUNCTION; Schema: realtime; Owner: supabase_admin
--

CREATE FUNCTION realtime.subscription_check_filters() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    /*
    Validates that the user defined filters for a subscription:
    - refer to valid columns that the claimed role may access
    - values are coercable to the correct column type
    */
    declare
        col_names text[] = coalesce(
                array_agg(c.column_name order by c.ordinal_position),
                '{}'::text[]
            )
            from
                information_schema.columns c
            where
                format('%I.%I', c.table_schema, c.table_name)::regclass = new.entity
                and pg_catalog.has_column_privilege(
                    (new.claims ->> 'role'),
                    format('%I.%I', c.table_schema, c.table_name)::regclass,
                    c.column_name,
                    'SELECT'
                );
        filter realtime.user_defined_filter;
        col_type regtype;

        in_val jsonb;
    begin
        for filter in select * from unnest(new.filters) loop
            -- Filtered column is valid
            if not filter.column_name = any(col_names) then
                raise exception 'invalid column for filter %', filter.column_name;
            end if;

            -- Type is sanitized and safe for string interpolation
            col_type = (
                select atttypid::regtype
                from pg_catalog.pg_attribute
                where attrelid = new.entity
                      and attname = filter.column_name
            );
            if col_type is null then
                raise exception 'failed to lookup type for column %', filter.column_name;
            end if;

            -- Set maximum number of entries for in filter
            if filter.op = 'in'::realtime.equality_op then
                in_val = realtime.cast(filter.value, (col_type::text || '[]')::regtype);
                if coalesce(jsonb_array_length(in_val), 0) > 100 then
                    raise exception 'too many values for `in` filter. Maximum 100';
                end if;
            else
                -- raises an exception if value is not coercable to type
                perform realtime.cast(filter.value, col_type);
            end if;

        end loop;

        -- Apply consistent order to filters so the unique constraint on
        -- (subscription_id, entity, filters) can't be tricked by a different filter order
        new.filters = coalesce(
            array_agg(f order by f.column_name, f.op, f.value),
            '{}'
        ) from unnest(new.filters) f;

        return new;
    end;
    $$;


ALTER FUNCTION realtime.subscription_check_filters() OWNER TO supabase_admin;

--
-- Name: to_regrole(text); Type: FUNCTION; Schema: realtime; Owner: supabase_admin
--

CREATE FUNCTION realtime.to_regrole(role_name text) RETURNS regrole
    LANGUAGE sql IMMUTABLE
    AS $$ select role_name::regrole $$;


ALTER FUNCTION realtime.to_regrole(role_name text) OWNER TO supabase_admin;

--
-- Name: topic(); Type: FUNCTION; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE FUNCTION realtime.topic() RETURNS text
    LANGUAGE sql STABLE
    AS $$
select nullif(current_setting('realtime.topic', true), '')::text;
$$;


ALTER FUNCTION realtime.topic() OWNER TO supabase_realtime_admin;

--
-- Name: allow_any_operation(text[]); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.allow_any_operation(expected_operations text[]) RETURNS boolean
    LANGUAGE sql STABLE
    AS $$
  WITH current_operation AS (
    SELECT storage.operation() AS raw_operation
  ),
  normalized AS (
    SELECT CASE
      WHEN raw_operation LIKE 'storage.%' THEN substr(raw_operation, 9)
      ELSE raw_operation
    END AS current_operation
    FROM current_operation
  )
  SELECT EXISTS (
    SELECT 1
    FROM normalized n
    CROSS JOIN LATERAL unnest(expected_operations) AS expected_operation
    WHERE expected_operation IS NOT NULL
      AND expected_operation <> ''
      AND n.current_operation = CASE
        WHEN expected_operation LIKE 'storage.%' THEN substr(expected_operation, 9)
        ELSE expected_operation
      END
  );
$$;


ALTER FUNCTION storage.allow_any_operation(expected_operations text[]) OWNER TO supabase_storage_admin;

--
-- Name: allow_only_operation(text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.allow_only_operation(expected_operation text) RETURNS boolean
    LANGUAGE sql STABLE
    AS $$
  WITH current_operation AS (
    SELECT storage.operation() AS raw_operation
  ),
  normalized AS (
    SELECT
      CASE
        WHEN raw_operation LIKE 'storage.%' THEN substr(raw_operation, 9)
        ELSE raw_operation
      END AS current_operation,
      CASE
        WHEN expected_operation LIKE 'storage.%' THEN substr(expected_operation, 9)
        ELSE expected_operation
      END AS requested_operation
    FROM current_operation
  )
  SELECT CASE
    WHEN requested_operation IS NULL OR requested_operation = '' THEN FALSE
    ELSE COALESCE(current_operation = requested_operation, FALSE)
  END
  FROM normalized;
$$;


ALTER FUNCTION storage.allow_only_operation(expected_operation text) OWNER TO supabase_storage_admin;

--
-- Name: can_insert_object(text, text, uuid, jsonb); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.can_insert_object(bucketid text, name text, owner uuid, metadata jsonb) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
  INSERT INTO "storage"."objects" ("bucket_id", "name", "owner", "metadata") VALUES (bucketid, name, owner, metadata);
  -- hack to rollback the successful insert
  RAISE sqlstate 'PT200' using
  message = 'ROLLBACK',
  detail = 'rollback successful insert';
END
$$;


ALTER FUNCTION storage.can_insert_object(bucketid text, name text, owner uuid, metadata jsonb) OWNER TO supabase_storage_admin;

--
-- Name: enforce_bucket_name_length(); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.enforce_bucket_name_length() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
    if length(new.name) > 100 then
        raise exception 'bucket name "%" is too long (% characters). Max is 100.', new.name, length(new.name);
    end if;
    return new;
end;
$$;


ALTER FUNCTION storage.enforce_bucket_name_length() OWNER TO supabase_storage_admin;

--
-- Name: extension(text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.extension(name text) RETURNS text
    LANGUAGE plpgsql IMMUTABLE
    AS $$
DECLARE
    _parts text[];
    _filename text;
BEGIN
    -- Split on "/" to get path segments
    SELECT string_to_array(name, '/') INTO _parts;
    -- Get the last path segment (the actual filename)
    SELECT _parts[array_length(_parts, 1)] INTO _filename;
    -- Extract extension: reverse, split on '.', then reverse again
    RETURN reverse(split_part(reverse(_filename), '.', 1));
END
$$;


ALTER FUNCTION storage.extension(name text) OWNER TO supabase_storage_admin;

--
-- Name: filename(text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.filename(name text) RETURNS text
    LANGUAGE plpgsql
    AS $$
DECLARE
_parts text[];
BEGIN
	select string_to_array(name, '/') into _parts;
	return _parts[array_length(_parts,1)];
END
$$;


ALTER FUNCTION storage.filename(name text) OWNER TO supabase_storage_admin;

--
-- Name: foldername(text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.foldername(name text) RETURNS text[]
    LANGUAGE plpgsql IMMUTABLE
    AS $$
DECLARE
    _parts text[];
BEGIN
    -- Split on "/" to get path segments
    SELECT string_to_array(name, '/') INTO _parts;
    -- Return everything except the last segment
    RETURN _parts[1 : array_length(_parts,1) - 1];
END
$$;


ALTER FUNCTION storage.foldername(name text) OWNER TO supabase_storage_admin;

--
-- Name: get_common_prefix(text, text, text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.get_common_prefix(p_key text, p_prefix text, p_delimiter text) RETURNS text
    LANGUAGE sql IMMUTABLE
    AS $$
SELECT CASE
    WHEN position(p_delimiter IN substring(p_key FROM length(p_prefix) + 1)) > 0
    THEN left(p_key, length(p_prefix) + position(p_delimiter IN substring(p_key FROM length(p_prefix) + 1)))
    ELSE NULL
END;
$$;


ALTER FUNCTION storage.get_common_prefix(p_key text, p_prefix text, p_delimiter text) OWNER TO supabase_storage_admin;

--
-- Name: get_size_by_bucket(); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.get_size_by_bucket() RETURNS TABLE(size bigint, bucket_id text)
    LANGUAGE plpgsql STABLE
    AS $$
BEGIN
    return query
        select sum((metadata->>'size')::bigint)::bigint as size, obj.bucket_id
        from "storage".objects as obj
        group by obj.bucket_id;
END
$$;


ALTER FUNCTION storage.get_size_by_bucket() OWNER TO supabase_storage_admin;

--
-- Name: list_multipart_uploads_with_delimiter(text, text, text, integer, text, text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.list_multipart_uploads_with_delimiter(bucket_id text, prefix_param text, delimiter_param text, max_keys integer DEFAULT 100, next_key_token text DEFAULT ''::text, next_upload_token text DEFAULT ''::text) RETURNS TABLE(key text, id text, created_at timestamp with time zone)
    LANGUAGE plpgsql
    AS $_$
BEGIN
    RETURN QUERY EXECUTE
        'SELECT DISTINCT ON(key COLLATE "C") * from (
            SELECT
                CASE
                    WHEN position($2 IN substring(key from length($1) + 1)) > 0 THEN
                        substring(key from 1 for length($1) + position($2 IN substring(key from length($1) + 1)))
                    ELSE
                        key
                END AS key, id, created_at
            FROM
                storage.s3_multipart_uploads
            WHERE
                bucket_id = $5 AND
                key ILIKE $1 || ''%'' AND
                CASE
                    WHEN $4 != '''' AND $6 = '''' THEN
                        CASE
                            WHEN position($2 IN substring(key from length($1) + 1)) > 0 THEN
                                substring(key from 1 for length($1) + position($2 IN substring(key from length($1) + 1))) COLLATE "C" > $4
                            ELSE
                                key COLLATE "C" > $4
                            END
                    ELSE
                        true
                END AND
                CASE
                    WHEN $6 != '''' THEN
                        id COLLATE "C" > $6
                    ELSE
                        true
                    END
            ORDER BY
                key COLLATE "C" ASC, created_at ASC) as e order by key COLLATE "C" LIMIT $3'
        USING prefix_param, delimiter_param, max_keys, next_key_token, bucket_id, next_upload_token;
END;
$_$;


ALTER FUNCTION storage.list_multipart_uploads_with_delimiter(bucket_id text, prefix_param text, delimiter_param text, max_keys integer, next_key_token text, next_upload_token text) OWNER TO supabase_storage_admin;

--
-- Name: list_objects_with_delimiter(text, text, text, integer, text, text, text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.list_objects_with_delimiter(_bucket_id text, prefix_param text, delimiter_param text, max_keys integer DEFAULT 100, start_after text DEFAULT ''::text, next_token text DEFAULT ''::text, sort_order text DEFAULT 'asc'::text) RETURNS TABLE(name text, id uuid, metadata jsonb, updated_at timestamp with time zone, created_at timestamp with time zone, last_accessed_at timestamp with time zone)
    LANGUAGE plpgsql STABLE
    AS $_$
DECLARE
    v_peek_name TEXT;
    v_current RECORD;
    v_common_prefix TEXT;

    -- Configuration
    v_is_asc BOOLEAN;
    v_prefix TEXT;
    v_start TEXT;
    v_upper_bound TEXT;
    v_file_batch_size INT;

    -- Seek state
    v_next_seek TEXT;
    v_count INT := 0;

    -- Dynamic SQL for batch query only
    v_batch_query TEXT;

BEGIN
    -- ========================================================================
    -- INITIALIZATION
    -- ========================================================================
    v_is_asc := lower(coalesce(sort_order, 'asc')) = 'asc';
    v_prefix := coalesce(prefix_param, '');
    v_start := CASE WHEN coalesce(next_token, '') <> '' THEN next_token ELSE coalesce(start_after, '') END;
    v_file_batch_size := LEAST(GREATEST(max_keys * 2, 100), 1000);

    -- Calculate upper bound for prefix filtering (bytewise, using COLLATE "C")
    IF v_prefix = '' THEN
        v_upper_bound := NULL;
    ELSIF right(v_prefix, 1) = delimiter_param THEN
        v_upper_bound := left(v_prefix, -1) || chr(ascii(delimiter_param) + 1);
    ELSE
        v_upper_bound := left(v_prefix, -1) || chr(ascii(right(v_prefix, 1)) + 1);
    END IF;

    -- Build batch query (dynamic SQL - called infrequently, amortized over many rows)
    IF v_is_asc THEN
        IF v_upper_bound IS NOT NULL THEN
            v_batch_query := 'SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata ' ||
                'FROM storage.objects o WHERE o.bucket_id = $1 AND o.name COLLATE "C" >= $2 ' ||
                'AND o.name COLLATE "C" < $3 ORDER BY o.name COLLATE "C" ASC LIMIT $4';
        ELSE
            v_batch_query := 'SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata ' ||
                'FROM storage.objects o WHERE o.bucket_id = $1 AND o.name COLLATE "C" >= $2 ' ||
                'ORDER BY o.name COLLATE "C" ASC LIMIT $4';
        END IF;
    ELSE
        IF v_upper_bound IS NOT NULL THEN
            v_batch_query := 'SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata ' ||
                'FROM storage.objects o WHERE o.bucket_id = $1 AND o.name COLLATE "C" < $2 ' ||
                'AND o.name COLLATE "C" >= $3 ORDER BY o.name COLLATE "C" DESC LIMIT $4';
        ELSE
            v_batch_query := 'SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata ' ||
                'FROM storage.objects o WHERE o.bucket_id = $1 AND o.name COLLATE "C" < $2 ' ||
                'ORDER BY o.name COLLATE "C" DESC LIMIT $4';
        END IF;
    END IF;

    -- ========================================================================
    -- SEEK INITIALIZATION: Determine starting position
    -- ========================================================================
    IF v_start = '' THEN
        IF v_is_asc THEN
            v_next_seek := v_prefix;
        ELSE
            -- DESC without cursor: find the last item in range
            IF v_upper_bound IS NOT NULL THEN
                SELECT o.name INTO v_next_seek FROM storage.objects o
                WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" >= v_prefix AND o.name COLLATE "C" < v_upper_bound
                ORDER BY o.name COLLATE "C" DESC LIMIT 1;
            ELSIF v_prefix <> '' THEN
                SELECT o.name INTO v_next_seek FROM storage.objects o
                WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" >= v_prefix
                ORDER BY o.name COLLATE "C" DESC LIMIT 1;
            ELSE
                SELECT o.name INTO v_next_seek FROM storage.objects o
                WHERE o.bucket_id = _bucket_id
                ORDER BY o.name COLLATE "C" DESC LIMIT 1;
            END IF;

            IF v_next_seek IS NOT NULL THEN
                v_next_seek := v_next_seek || delimiter_param;
            ELSE
                RETURN;
            END IF;
        END IF;
    ELSE
        -- Cursor provided: determine if it refers to a folder or leaf
        IF EXISTS (
            SELECT 1 FROM storage.objects o
            WHERE o.bucket_id = _bucket_id
              AND o.name COLLATE "C" LIKE v_start || delimiter_param || '%'
            LIMIT 1
        ) THEN
            -- Cursor refers to a folder
            IF v_is_asc THEN
                v_next_seek := v_start || chr(ascii(delimiter_param) + 1);
            ELSE
                v_next_seek := v_start || delimiter_param;
            END IF;
        ELSE
            -- Cursor refers to a leaf object
            IF v_is_asc THEN
                v_next_seek := v_start || delimiter_param;
            ELSE
                v_next_seek := v_start;
            END IF;
        END IF;
    END IF;

    -- ========================================================================
    -- MAIN LOOP: Hybrid peek-then-batch algorithm
    -- Uses STATIC SQL for peek (hot path) and DYNAMIC SQL for batch
    -- ========================================================================
    LOOP
        EXIT WHEN v_count >= max_keys;

        -- STEP 1: PEEK using STATIC SQL (plan cached, very fast)
        IF v_is_asc THEN
            IF v_upper_bound IS NOT NULL THEN
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" >= v_next_seek AND o.name COLLATE "C" < v_upper_bound
                ORDER BY o.name COLLATE "C" ASC LIMIT 1;
            ELSE
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" >= v_next_seek
                ORDER BY o.name COLLATE "C" ASC LIMIT 1;
            END IF;
        ELSE
            IF v_upper_bound IS NOT NULL THEN
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" < v_next_seek AND o.name COLLATE "C" >= v_prefix
                ORDER BY o.name COLLATE "C" DESC LIMIT 1;
            ELSIF v_prefix <> '' THEN
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" < v_next_seek AND o.name COLLATE "C" >= v_prefix
                ORDER BY o.name COLLATE "C" DESC LIMIT 1;
            ELSE
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" < v_next_seek
                ORDER BY o.name COLLATE "C" DESC LIMIT 1;
            END IF;
        END IF;

        EXIT WHEN v_peek_name IS NULL;

        -- STEP 2: Check if this is a FOLDER or FILE
        v_common_prefix := storage.get_common_prefix(v_peek_name, v_prefix, delimiter_param);

        IF v_common_prefix IS NOT NULL THEN
            -- FOLDER: Emit and skip to next folder (no heap access needed)
            name := rtrim(v_common_prefix, delimiter_param);
            id := NULL;
            updated_at := NULL;
            created_at := NULL;
            last_accessed_at := NULL;
            metadata := NULL;
            RETURN NEXT;
            v_count := v_count + 1;

            -- Advance seek past the folder range
            IF v_is_asc THEN
                v_next_seek := left(v_common_prefix, -1) || chr(ascii(delimiter_param) + 1);
            ELSE
                v_next_seek := v_common_prefix;
            END IF;
        ELSE
            -- FILE: Batch fetch using DYNAMIC SQL (overhead amortized over many rows)
            -- For ASC: upper_bound is the exclusive upper limit (< condition)
            -- For DESC: prefix is the inclusive lower limit (>= condition)
            FOR v_current IN EXECUTE v_batch_query USING _bucket_id, v_next_seek,
                CASE WHEN v_is_asc THEN COALESCE(v_upper_bound, v_prefix) ELSE v_prefix END, v_file_batch_size
            LOOP
                v_common_prefix := storage.get_common_prefix(v_current.name, v_prefix, delimiter_param);

                IF v_common_prefix IS NOT NULL THEN
                    -- Hit a folder: exit batch, let peek handle it
                    v_next_seek := v_current.name;
                    EXIT;
                END IF;

                -- Emit file
                name := v_current.name;
                id := v_current.id;
                updated_at := v_current.updated_at;
                created_at := v_current.created_at;
                last_accessed_at := v_current.last_accessed_at;
                metadata := v_current.metadata;
                RETURN NEXT;
                v_count := v_count + 1;

                -- Advance seek past this file
                IF v_is_asc THEN
                    v_next_seek := v_current.name || delimiter_param;
                ELSE
                    v_next_seek := v_current.name;
                END IF;

                EXIT WHEN v_count >= max_keys;
            END LOOP;
        END IF;
    END LOOP;
END;
$_$;


ALTER FUNCTION storage.list_objects_with_delimiter(_bucket_id text, prefix_param text, delimiter_param text, max_keys integer, start_after text, next_token text, sort_order text) OWNER TO supabase_storage_admin;

--
-- Name: operation(); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.operation() RETURNS text
    LANGUAGE plpgsql STABLE
    AS $$
BEGIN
    RETURN current_setting('storage.operation', true);
END;
$$;


ALTER FUNCTION storage.operation() OWNER TO supabase_storage_admin;

--
-- Name: protect_delete(); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.protect_delete() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Check if storage.allow_delete_query is set to 'true'
    IF COALESCE(current_setting('storage.allow_delete_query', true), 'false') != 'true' THEN
        RAISE EXCEPTION 'Direct deletion from storage tables is not allowed. Use the Storage API instead.'
            USING HINT = 'This prevents accidental data loss from orphaned objects.',
                  ERRCODE = '42501';
    END IF;
    RETURN NULL;
END;
$$;


ALTER FUNCTION storage.protect_delete() OWNER TO supabase_storage_admin;

--
-- Name: search(text, text, integer, integer, integer, text, text, text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.search(prefix text, bucketname text, limits integer DEFAULT 100, levels integer DEFAULT 1, offsets integer DEFAULT 0, search text DEFAULT ''::text, sortcolumn text DEFAULT 'name'::text, sortorder text DEFAULT 'asc'::text) RETURNS TABLE(name text, id uuid, updated_at timestamp with time zone, created_at timestamp with time zone, last_accessed_at timestamp with time zone, metadata jsonb)
    LANGUAGE plpgsql STABLE
    AS $_$
DECLARE
    v_peek_name TEXT;
    v_current RECORD;
    v_common_prefix TEXT;
    v_delimiter CONSTANT TEXT := '/';

    -- Configuration
    v_limit INT;
    v_prefix TEXT;
    v_prefix_lower TEXT;
    v_is_asc BOOLEAN;
    v_order_by TEXT;
    v_sort_order TEXT;
    v_upper_bound TEXT;
    v_file_batch_size INT;

    -- Dynamic SQL for batch query only
    v_batch_query TEXT;

    -- Seek state
    v_next_seek TEXT;
    v_count INT := 0;
    v_skipped INT := 0;
BEGIN
    -- ========================================================================
    -- INITIALIZATION
    -- ========================================================================
    v_limit := LEAST(coalesce(limits, 100), 1500);
    v_prefix := coalesce(prefix, '') || coalesce(search, '');
    v_prefix_lower := lower(v_prefix);
    v_is_asc := lower(coalesce(sortorder, 'asc')) = 'asc';
    v_file_batch_size := LEAST(GREATEST(v_limit * 2, 100), 1000);

    -- Validate sort column
    CASE lower(coalesce(sortcolumn, 'name'))
        WHEN 'name' THEN v_order_by := 'name';
        WHEN 'updated_at' THEN v_order_by := 'updated_at';
        WHEN 'created_at' THEN v_order_by := 'created_at';
        WHEN 'last_accessed_at' THEN v_order_by := 'last_accessed_at';
        ELSE v_order_by := 'name';
    END CASE;

    v_sort_order := CASE WHEN v_is_asc THEN 'asc' ELSE 'desc' END;

    -- ========================================================================
    -- NON-NAME SORTING: Use path_tokens approach (unchanged)
    -- ========================================================================
    IF v_order_by != 'name' THEN
        RETURN QUERY EXECUTE format(
            $sql$
            WITH folders AS (
                SELECT path_tokens[$1] AS folder
                FROM storage.objects
                WHERE objects.name ILIKE $2 || '%%'
                  AND bucket_id = $3
                  AND array_length(objects.path_tokens, 1) <> $1
                GROUP BY folder
                ORDER BY folder %s
            )
            (SELECT folder AS "name",
                   NULL::uuid AS id,
                   NULL::timestamptz AS updated_at,
                   NULL::timestamptz AS created_at,
                   NULL::timestamptz AS last_accessed_at,
                   NULL::jsonb AS metadata FROM folders)
            UNION ALL
            (SELECT path_tokens[$1] AS "name",
                   id, updated_at, created_at, last_accessed_at, metadata
             FROM storage.objects
             WHERE objects.name ILIKE $2 || '%%'
               AND bucket_id = $3
               AND array_length(objects.path_tokens, 1) = $1
             ORDER BY %I %s)
            LIMIT $4 OFFSET $5
            $sql$, v_sort_order, v_order_by, v_sort_order
        ) USING levels, v_prefix, bucketname, v_limit, offsets;
        RETURN;
    END IF;

    -- ========================================================================
    -- NAME SORTING: Hybrid skip-scan with batch optimization
    -- ========================================================================

    -- Calculate upper bound for prefix filtering
    IF v_prefix_lower = '' THEN
        v_upper_bound := NULL;
    ELSIF right(v_prefix_lower, 1) = v_delimiter THEN
        v_upper_bound := left(v_prefix_lower, -1) || chr(ascii(v_delimiter) + 1);
    ELSE
        v_upper_bound := left(v_prefix_lower, -1) || chr(ascii(right(v_prefix_lower, 1)) + 1);
    END IF;

    -- Build batch query (dynamic SQL - called infrequently, amortized over many rows)
    IF v_is_asc THEN
        IF v_upper_bound IS NOT NULL THEN
            v_batch_query := 'SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata ' ||
                'FROM storage.objects o WHERE o.bucket_id = $1 AND lower(o.name) COLLATE "C" >= $2 ' ||
                'AND lower(o.name) COLLATE "C" < $3 ORDER BY lower(o.name) COLLATE "C" ASC LIMIT $4';
        ELSE
            v_batch_query := 'SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata ' ||
                'FROM storage.objects o WHERE o.bucket_id = $1 AND lower(o.name) COLLATE "C" >= $2 ' ||
                'ORDER BY lower(o.name) COLLATE "C" ASC LIMIT $4';
        END IF;
    ELSE
        IF v_upper_bound IS NOT NULL THEN
            v_batch_query := 'SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata ' ||
                'FROM storage.objects o WHERE o.bucket_id = $1 AND lower(o.name) COLLATE "C" < $2 ' ||
                'AND lower(o.name) COLLATE "C" >= $3 ORDER BY lower(o.name) COLLATE "C" DESC LIMIT $4';
        ELSE
            v_batch_query := 'SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata ' ||
                'FROM storage.objects o WHERE o.bucket_id = $1 AND lower(o.name) COLLATE "C" < $2 ' ||
                'ORDER BY lower(o.name) COLLATE "C" DESC LIMIT $4';
        END IF;
    END IF;

    -- Initialize seek position
    IF v_is_asc THEN
        v_next_seek := v_prefix_lower;
    ELSE
        -- DESC: find the last item in range first (static SQL)
        IF v_upper_bound IS NOT NULL THEN
            SELECT o.name INTO v_peek_name FROM storage.objects o
            WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" >= v_prefix_lower AND lower(o.name) COLLATE "C" < v_upper_bound
            ORDER BY lower(o.name) COLLATE "C" DESC LIMIT 1;
        ELSIF v_prefix_lower <> '' THEN
            SELECT o.name INTO v_peek_name FROM storage.objects o
            WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" >= v_prefix_lower
            ORDER BY lower(o.name) COLLATE "C" DESC LIMIT 1;
        ELSE
            SELECT o.name INTO v_peek_name FROM storage.objects o
            WHERE o.bucket_id = bucketname
            ORDER BY lower(o.name) COLLATE "C" DESC LIMIT 1;
        END IF;

        IF v_peek_name IS NOT NULL THEN
            v_next_seek := lower(v_peek_name) || v_delimiter;
        ELSE
            RETURN;
        END IF;
    END IF;

    -- ========================================================================
    -- MAIN LOOP: Hybrid peek-then-batch algorithm
    -- Uses STATIC SQL for peek (hot path) and DYNAMIC SQL for batch
    -- ========================================================================
    LOOP
        EXIT WHEN v_count >= v_limit;

        -- STEP 1: PEEK using STATIC SQL (plan cached, very fast)
        IF v_is_asc THEN
            IF v_upper_bound IS NOT NULL THEN
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" >= v_next_seek AND lower(o.name) COLLATE "C" < v_upper_bound
                ORDER BY lower(o.name) COLLATE "C" ASC LIMIT 1;
            ELSE
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" >= v_next_seek
                ORDER BY lower(o.name) COLLATE "C" ASC LIMIT 1;
            END IF;
        ELSE
            IF v_upper_bound IS NOT NULL THEN
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" < v_next_seek AND lower(o.name) COLLATE "C" >= v_prefix_lower
                ORDER BY lower(o.name) COLLATE "C" DESC LIMIT 1;
            ELSIF v_prefix_lower <> '' THEN
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" < v_next_seek AND lower(o.name) COLLATE "C" >= v_prefix_lower
                ORDER BY lower(o.name) COLLATE "C" DESC LIMIT 1;
            ELSE
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" < v_next_seek
                ORDER BY lower(o.name) COLLATE "C" DESC LIMIT 1;
            END IF;
        END IF;

        EXIT WHEN v_peek_name IS NULL;

        -- STEP 2: Check if this is a FOLDER or FILE
        v_common_prefix := storage.get_common_prefix(lower(v_peek_name), v_prefix_lower, v_delimiter);

        IF v_common_prefix IS NOT NULL THEN
            -- FOLDER: Handle offset, emit if needed, skip to next folder
            IF v_skipped < offsets THEN
                v_skipped := v_skipped + 1;
            ELSE
                name := split_part(rtrim(storage.get_common_prefix(v_peek_name, v_prefix, v_delimiter), v_delimiter), v_delimiter, levels);
                id := NULL;
                updated_at := NULL;
                created_at := NULL;
                last_accessed_at := NULL;
                metadata := NULL;
                RETURN NEXT;
                v_count := v_count + 1;
            END IF;

            -- Advance seek past the folder range
            IF v_is_asc THEN
                v_next_seek := lower(left(v_common_prefix, -1)) || chr(ascii(v_delimiter) + 1);
            ELSE
                v_next_seek := lower(v_common_prefix);
            END IF;
        ELSE
            -- FILE: Batch fetch using DYNAMIC SQL (overhead amortized over many rows)
            -- For ASC: upper_bound is the exclusive upper limit (< condition)
            -- For DESC: prefix_lower is the inclusive lower limit (>= condition)
            FOR v_current IN EXECUTE v_batch_query
                USING bucketname, v_next_seek,
                    CASE WHEN v_is_asc THEN COALESCE(v_upper_bound, v_prefix_lower) ELSE v_prefix_lower END, v_file_batch_size
            LOOP
                v_common_prefix := storage.get_common_prefix(lower(v_current.name), v_prefix_lower, v_delimiter);

                IF v_common_prefix IS NOT NULL THEN
                    -- Hit a folder: exit batch, let peek handle it
                    v_next_seek := lower(v_current.name);
                    EXIT;
                END IF;

                -- Handle offset skipping
                IF v_skipped < offsets THEN
                    v_skipped := v_skipped + 1;
                ELSE
                    -- Emit file
                    name := split_part(v_current.name, v_delimiter, levels);
                    id := v_current.id;
                    updated_at := v_current.updated_at;
                    created_at := v_current.created_at;
                    last_accessed_at := v_current.last_accessed_at;
                    metadata := v_current.metadata;
                    RETURN NEXT;
                    v_count := v_count + 1;
                END IF;

                -- Advance seek past this file
                IF v_is_asc THEN
                    v_next_seek := lower(v_current.name) || v_delimiter;
                ELSE
                    v_next_seek := lower(v_current.name);
                END IF;

                EXIT WHEN v_count >= v_limit;
            END LOOP;
        END IF;
    END LOOP;
END;
$_$;


ALTER FUNCTION storage.search(prefix text, bucketname text, limits integer, levels integer, offsets integer, search text, sortcolumn text, sortorder text) OWNER TO supabase_storage_admin;

--
-- Name: search_by_timestamp(text, text, integer, integer, text, text, text, text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.search_by_timestamp(p_prefix text, p_bucket_id text, p_limit integer, p_level integer, p_start_after text, p_sort_order text, p_sort_column text, p_sort_column_after text) RETURNS TABLE(key text, name text, id uuid, updated_at timestamp with time zone, created_at timestamp with time zone, last_accessed_at timestamp with time zone, metadata jsonb)
    LANGUAGE plpgsql STABLE
    AS $_$
DECLARE
    v_cursor_op text;
    v_query text;
    v_prefix text;
BEGIN
    v_prefix := coalesce(p_prefix, '');

    IF p_sort_order = 'asc' THEN
        v_cursor_op := '>';
    ELSE
        v_cursor_op := '<';
    END IF;

    v_query := format($sql$
        WITH raw_objects AS (
            SELECT
                o.name AS obj_name,
                o.id AS obj_id,
                o.updated_at AS obj_updated_at,
                o.created_at AS obj_created_at,
                o.last_accessed_at AS obj_last_accessed_at,
                o.metadata AS obj_metadata,
                storage.get_common_prefix(o.name, $1, '/') AS common_prefix
            FROM storage.objects o
            WHERE o.bucket_id = $2
              AND o.name COLLATE "C" LIKE $1 || '%%'
        ),
        -- Aggregate common prefixes (folders)
        -- Both created_at and updated_at use MIN(obj_created_at) to match the old prefixes table behavior
        aggregated_prefixes AS (
            SELECT
                rtrim(common_prefix, '/') AS name,
                NULL::uuid AS id,
                MIN(obj_created_at) AS updated_at,
                MIN(obj_created_at) AS created_at,
                NULL::timestamptz AS last_accessed_at,
                NULL::jsonb AS metadata,
                TRUE AS is_prefix
            FROM raw_objects
            WHERE common_prefix IS NOT NULL
            GROUP BY common_prefix
        ),
        leaf_objects AS (
            SELECT
                obj_name AS name,
                obj_id AS id,
                obj_updated_at AS updated_at,
                obj_created_at AS created_at,
                obj_last_accessed_at AS last_accessed_at,
                obj_metadata AS metadata,
                FALSE AS is_prefix
            FROM raw_objects
            WHERE common_prefix IS NULL
        ),
        combined AS (
            SELECT * FROM aggregated_prefixes
            UNION ALL
            SELECT * FROM leaf_objects
        ),
        filtered AS (
            SELECT *
            FROM combined
            WHERE (
                $5 = ''
                OR ROW(
                    date_trunc('milliseconds', %I),
                    name COLLATE "C"
                ) %s ROW(
                    COALESCE(NULLIF($6, '')::timestamptz, 'epoch'::timestamptz),
                    $5
                )
            )
        )
        SELECT
            split_part(name, '/', $3) AS key,
            name,
            id,
            updated_at,
            created_at,
            last_accessed_at,
            metadata
        FROM filtered
        ORDER BY
            COALESCE(date_trunc('milliseconds', %I), 'epoch'::timestamptz) %s,
            name COLLATE "C" %s
        LIMIT $4
    $sql$,
        p_sort_column,
        v_cursor_op,
        p_sort_column,
        p_sort_order,
        p_sort_order
    );

    RETURN QUERY EXECUTE v_query
    USING v_prefix, p_bucket_id, p_level, p_limit, p_start_after, p_sort_column_after;
END;
$_$;


ALTER FUNCTION storage.search_by_timestamp(p_prefix text, p_bucket_id text, p_limit integer, p_level integer, p_start_after text, p_sort_order text, p_sort_column text, p_sort_column_after text) OWNER TO supabase_storage_admin;

--
-- Name: search_v2(text, text, integer, integer, text, text, text, text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.search_v2(prefix text, bucket_name text, limits integer DEFAULT 100, levels integer DEFAULT 1, start_after text DEFAULT ''::text, sort_order text DEFAULT 'asc'::text, sort_column text DEFAULT 'name'::text, sort_column_after text DEFAULT ''::text) RETURNS TABLE(key text, name text, id uuid, updated_at timestamp with time zone, created_at timestamp with time zone, last_accessed_at timestamp with time zone, metadata jsonb)
    LANGUAGE plpgsql STABLE
    AS $$
DECLARE
    v_sort_col text;
    v_sort_ord text;
    v_limit int;
BEGIN
    -- Cap limit to maximum of 1500 records
    v_limit := LEAST(coalesce(limits, 100), 1500);

    -- Validate and normalize sort_order
    v_sort_ord := lower(coalesce(sort_order, 'asc'));
    IF v_sort_ord NOT IN ('asc', 'desc') THEN
        v_sort_ord := 'asc';
    END IF;

    -- Validate and normalize sort_column
    v_sort_col := lower(coalesce(sort_column, 'name'));
    IF v_sort_col NOT IN ('name', 'updated_at', 'created_at') THEN
        v_sort_col := 'name';
    END IF;

    -- Route to appropriate implementation
    IF v_sort_col = 'name' THEN
        -- Use list_objects_with_delimiter for name sorting (most efficient: O(k * log n))
        RETURN QUERY
        SELECT
            split_part(l.name, '/', levels) AS key,
            l.name AS name,
            l.id,
            l.updated_at,
            l.created_at,
            l.last_accessed_at,
            l.metadata
        FROM storage.list_objects_with_delimiter(
            bucket_name,
            coalesce(prefix, ''),
            '/',
            v_limit,
            start_after,
            '',
            v_sort_ord
        ) l;
    ELSE
        -- Use aggregation approach for timestamp sorting
        -- Not efficient for large datasets but supports correct pagination
        RETURN QUERY SELECT * FROM storage.search_by_timestamp(
            prefix, bucket_name, v_limit, levels, start_after,
            v_sort_ord, v_sort_col, sort_column_after
        );
    END IF;
END;
$$;


ALTER FUNCTION storage.search_v2(prefix text, bucket_name text, limits integer, levels integer, start_after text, sort_order text, sort_column text, sort_column_after text) OWNER TO supabase_storage_admin;

--
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW; 
END;
$$;


ALTER FUNCTION storage.update_updated_at_column() OWNER TO supabase_storage_admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: audit_log_entries; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.audit_log_entries (
    instance_id uuid,
    id uuid NOT NULL,
    payload json,
    created_at timestamp with time zone,
    ip_address character varying(64) DEFAULT ''::character varying NOT NULL
);


ALTER TABLE auth.audit_log_entries OWNER TO supabase_auth_admin;

--
-- Name: TABLE audit_log_entries; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.audit_log_entries IS 'Auth: Audit trail for user actions.';


--
-- Name: custom_oauth_providers; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.custom_oauth_providers (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    provider_type text NOT NULL,
    identifier text NOT NULL,
    name text NOT NULL,
    client_id text NOT NULL,
    client_secret text NOT NULL,
    acceptable_client_ids text[] DEFAULT '{}'::text[] NOT NULL,
    scopes text[] DEFAULT '{}'::text[] NOT NULL,
    pkce_enabled boolean DEFAULT true NOT NULL,
    attribute_mapping jsonb DEFAULT '{}'::jsonb NOT NULL,
    authorization_params jsonb DEFAULT '{}'::jsonb NOT NULL,
    enabled boolean DEFAULT true NOT NULL,
    email_optional boolean DEFAULT false NOT NULL,
    issuer text,
    discovery_url text,
    skip_nonce_check boolean DEFAULT false NOT NULL,
    cached_discovery jsonb,
    discovery_cached_at timestamp with time zone,
    authorization_url text,
    token_url text,
    userinfo_url text,
    jwks_uri text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT custom_oauth_providers_authorization_url_https CHECK (((authorization_url IS NULL) OR (authorization_url ~~ 'https://%'::text))),
    CONSTRAINT custom_oauth_providers_authorization_url_length CHECK (((authorization_url IS NULL) OR (char_length(authorization_url) <= 2048))),
    CONSTRAINT custom_oauth_providers_client_id_length CHECK (((char_length(client_id) >= 1) AND (char_length(client_id) <= 512))),
    CONSTRAINT custom_oauth_providers_discovery_url_length CHECK (((discovery_url IS NULL) OR (char_length(discovery_url) <= 2048))),
    CONSTRAINT custom_oauth_providers_identifier_format CHECK ((identifier ~ '^[a-z0-9][a-z0-9:-]{0,48}[a-z0-9]$'::text)),
    CONSTRAINT custom_oauth_providers_issuer_length CHECK (((issuer IS NULL) OR ((char_length(issuer) >= 1) AND (char_length(issuer) <= 2048)))),
    CONSTRAINT custom_oauth_providers_jwks_uri_https CHECK (((jwks_uri IS NULL) OR (jwks_uri ~~ 'https://%'::text))),
    CONSTRAINT custom_oauth_providers_jwks_uri_length CHECK (((jwks_uri IS NULL) OR (char_length(jwks_uri) <= 2048))),
    CONSTRAINT custom_oauth_providers_name_length CHECK (((char_length(name) >= 1) AND (char_length(name) <= 100))),
    CONSTRAINT custom_oauth_providers_oauth2_requires_endpoints CHECK (((provider_type <> 'oauth2'::text) OR ((authorization_url IS NOT NULL) AND (token_url IS NOT NULL) AND (userinfo_url IS NOT NULL)))),
    CONSTRAINT custom_oauth_providers_oidc_discovery_url_https CHECK (((provider_type <> 'oidc'::text) OR (discovery_url IS NULL) OR (discovery_url ~~ 'https://%'::text))),
    CONSTRAINT custom_oauth_providers_oidc_issuer_https CHECK (((provider_type <> 'oidc'::text) OR (issuer IS NULL) OR (issuer ~~ 'https://%'::text))),
    CONSTRAINT custom_oauth_providers_oidc_requires_issuer CHECK (((provider_type <> 'oidc'::text) OR (issuer IS NOT NULL))),
    CONSTRAINT custom_oauth_providers_provider_type_check CHECK ((provider_type = ANY (ARRAY['oauth2'::text, 'oidc'::text]))),
    CONSTRAINT custom_oauth_providers_token_url_https CHECK (((token_url IS NULL) OR (token_url ~~ 'https://%'::text))),
    CONSTRAINT custom_oauth_providers_token_url_length CHECK (((token_url IS NULL) OR (char_length(token_url) <= 2048))),
    CONSTRAINT custom_oauth_providers_userinfo_url_https CHECK (((userinfo_url IS NULL) OR (userinfo_url ~~ 'https://%'::text))),
    CONSTRAINT custom_oauth_providers_userinfo_url_length CHECK (((userinfo_url IS NULL) OR (char_length(userinfo_url) <= 2048)))
);


ALTER TABLE auth.custom_oauth_providers OWNER TO supabase_auth_admin;

--
-- Name: flow_state; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.flow_state (
    id uuid NOT NULL,
    user_id uuid,
    auth_code text,
    code_challenge_method auth.code_challenge_method,
    code_challenge text,
    provider_type text NOT NULL,
    provider_access_token text,
    provider_refresh_token text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    authentication_method text NOT NULL,
    auth_code_issued_at timestamp with time zone,
    invite_token text,
    referrer text,
    oauth_client_state_id uuid,
    linking_target_id uuid,
    email_optional boolean DEFAULT false NOT NULL
);


ALTER TABLE auth.flow_state OWNER TO supabase_auth_admin;

--
-- Name: TABLE flow_state; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.flow_state IS 'Stores metadata for all OAuth/SSO login flows';


--
-- Name: identities; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.identities (
    provider_id text NOT NULL,
    user_id uuid NOT NULL,
    identity_data jsonb NOT NULL,
    provider text NOT NULL,
    last_sign_in_at timestamp with time zone,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    email text GENERATED ALWAYS AS (lower((identity_data ->> 'email'::text))) STORED,
    id uuid DEFAULT gen_random_uuid() NOT NULL
);


ALTER TABLE auth.identities OWNER TO supabase_auth_admin;

--
-- Name: TABLE identities; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.identities IS 'Auth: Stores identities associated to a user.';


--
-- Name: COLUMN identities.email; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON COLUMN auth.identities.email IS 'Auth: Email is a generated column that references the optional email property in the identity_data';


--
-- Name: instances; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.instances (
    id uuid NOT NULL,
    uuid uuid,
    raw_base_config text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);


ALTER TABLE auth.instances OWNER TO supabase_auth_admin;

--
-- Name: TABLE instances; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.instances IS 'Auth: Manages users across multiple sites.';


--
-- Name: mfa_amr_claims; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.mfa_amr_claims (
    session_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    authentication_method text NOT NULL,
    id uuid NOT NULL
);


ALTER TABLE auth.mfa_amr_claims OWNER TO supabase_auth_admin;

--
-- Name: TABLE mfa_amr_claims; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.mfa_amr_claims IS 'auth: stores authenticator method reference claims for multi factor authentication';


--
-- Name: mfa_challenges; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.mfa_challenges (
    id uuid NOT NULL,
    factor_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    verified_at timestamp with time zone,
    ip_address inet NOT NULL,
    otp_code text,
    web_authn_session_data jsonb
);


ALTER TABLE auth.mfa_challenges OWNER TO supabase_auth_admin;

--
-- Name: TABLE mfa_challenges; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.mfa_challenges IS 'auth: stores metadata about challenge requests made';


--
-- Name: mfa_factors; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.mfa_factors (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    friendly_name text,
    factor_type auth.factor_type NOT NULL,
    status auth.factor_status NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    secret text,
    phone text,
    last_challenged_at timestamp with time zone,
    web_authn_credential jsonb,
    web_authn_aaguid uuid,
    last_webauthn_challenge_data jsonb
);


ALTER TABLE auth.mfa_factors OWNER TO supabase_auth_admin;

--
-- Name: TABLE mfa_factors; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.mfa_factors IS 'auth: stores metadata about factors';


--
-- Name: COLUMN mfa_factors.last_webauthn_challenge_data; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON COLUMN auth.mfa_factors.last_webauthn_challenge_data IS 'Stores the latest WebAuthn challenge data including attestation/assertion for customer verification';


--
-- Name: oauth_authorizations; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.oauth_authorizations (
    id uuid NOT NULL,
    authorization_id text NOT NULL,
    client_id uuid NOT NULL,
    user_id uuid,
    redirect_uri text NOT NULL,
    scope text NOT NULL,
    state text,
    resource text,
    code_challenge text,
    code_challenge_method auth.code_challenge_method,
    response_type auth.oauth_response_type DEFAULT 'code'::auth.oauth_response_type NOT NULL,
    status auth.oauth_authorization_status DEFAULT 'pending'::auth.oauth_authorization_status NOT NULL,
    authorization_code text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    expires_at timestamp with time zone DEFAULT (now() + '00:03:00'::interval) NOT NULL,
    approved_at timestamp with time zone,
    nonce text,
    CONSTRAINT oauth_authorizations_authorization_code_length CHECK ((char_length(authorization_code) <= 255)),
    CONSTRAINT oauth_authorizations_code_challenge_length CHECK ((char_length(code_challenge) <= 128)),
    CONSTRAINT oauth_authorizations_expires_at_future CHECK ((expires_at > created_at)),
    CONSTRAINT oauth_authorizations_nonce_length CHECK ((char_length(nonce) <= 255)),
    CONSTRAINT oauth_authorizations_redirect_uri_length CHECK ((char_length(redirect_uri) <= 2048)),
    CONSTRAINT oauth_authorizations_resource_length CHECK ((char_length(resource) <= 2048)),
    CONSTRAINT oauth_authorizations_scope_length CHECK ((char_length(scope) <= 4096)),
    CONSTRAINT oauth_authorizations_state_length CHECK ((char_length(state) <= 4096))
);


ALTER TABLE auth.oauth_authorizations OWNER TO supabase_auth_admin;

--
-- Name: oauth_client_states; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.oauth_client_states (
    id uuid NOT NULL,
    provider_type text NOT NULL,
    code_verifier text,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE auth.oauth_client_states OWNER TO supabase_auth_admin;

--
-- Name: TABLE oauth_client_states; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.oauth_client_states IS 'Stores OAuth states for third-party provider authentication flows where Supabase acts as the OAuth client.';


--
-- Name: oauth_clients; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.oauth_clients (
    id uuid NOT NULL,
    client_secret_hash text,
    registration_type auth.oauth_registration_type NOT NULL,
    redirect_uris text NOT NULL,
    grant_types text NOT NULL,
    client_name text,
    client_uri text,
    logo_uri text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    deleted_at timestamp with time zone,
    client_type auth.oauth_client_type DEFAULT 'confidential'::auth.oauth_client_type NOT NULL,
    token_endpoint_auth_method text NOT NULL,
    CONSTRAINT oauth_clients_client_name_length CHECK ((char_length(client_name) <= 1024)),
    CONSTRAINT oauth_clients_client_uri_length CHECK ((char_length(client_uri) <= 2048)),
    CONSTRAINT oauth_clients_logo_uri_length CHECK ((char_length(logo_uri) <= 2048)),
    CONSTRAINT oauth_clients_token_endpoint_auth_method_check CHECK ((token_endpoint_auth_method = ANY (ARRAY['client_secret_basic'::text, 'client_secret_post'::text, 'none'::text])))
);


ALTER TABLE auth.oauth_clients OWNER TO supabase_auth_admin;

--
-- Name: oauth_consents; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.oauth_consents (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    client_id uuid NOT NULL,
    scopes text NOT NULL,
    granted_at timestamp with time zone DEFAULT now() NOT NULL,
    revoked_at timestamp with time zone,
    CONSTRAINT oauth_consents_revoked_after_granted CHECK (((revoked_at IS NULL) OR (revoked_at >= granted_at))),
    CONSTRAINT oauth_consents_scopes_length CHECK ((char_length(scopes) <= 2048)),
    CONSTRAINT oauth_consents_scopes_not_empty CHECK ((char_length(TRIM(BOTH FROM scopes)) > 0))
);


ALTER TABLE auth.oauth_consents OWNER TO supabase_auth_admin;

--
-- Name: one_time_tokens; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.one_time_tokens (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    token_type auth.one_time_token_type NOT NULL,
    token_hash text NOT NULL,
    relates_to text NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT one_time_tokens_token_hash_check CHECK ((char_length(token_hash) > 0))
);


ALTER TABLE auth.one_time_tokens OWNER TO supabase_auth_admin;

--
-- Name: refresh_tokens; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.refresh_tokens (
    instance_id uuid,
    id bigint NOT NULL,
    token character varying(255),
    user_id character varying(255),
    revoked boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    parent character varying(255),
    session_id uuid
);


ALTER TABLE auth.refresh_tokens OWNER TO supabase_auth_admin;

--
-- Name: TABLE refresh_tokens; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.refresh_tokens IS 'Auth: Store of tokens used to refresh JWT tokens once they expire.';


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE; Schema: auth; Owner: supabase_auth_admin
--

CREATE SEQUENCE auth.refresh_tokens_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE auth.refresh_tokens_id_seq OWNER TO supabase_auth_admin;

--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: auth; Owner: supabase_auth_admin
--

ALTER SEQUENCE auth.refresh_tokens_id_seq OWNED BY auth.refresh_tokens.id;


--
-- Name: saml_providers; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.saml_providers (
    id uuid NOT NULL,
    sso_provider_id uuid NOT NULL,
    entity_id text NOT NULL,
    metadata_xml text NOT NULL,
    metadata_url text,
    attribute_mapping jsonb,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    name_id_format text,
    CONSTRAINT "entity_id not empty" CHECK ((char_length(entity_id) > 0)),
    CONSTRAINT "metadata_url not empty" CHECK (((metadata_url = NULL::text) OR (char_length(metadata_url) > 0))),
    CONSTRAINT "metadata_xml not empty" CHECK ((char_length(metadata_xml) > 0))
);


ALTER TABLE auth.saml_providers OWNER TO supabase_auth_admin;

--
-- Name: TABLE saml_providers; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.saml_providers IS 'Auth: Manages SAML Identity Provider connections.';


--
-- Name: saml_relay_states; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.saml_relay_states (
    id uuid NOT NULL,
    sso_provider_id uuid NOT NULL,
    request_id text NOT NULL,
    for_email text,
    redirect_to text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    flow_state_id uuid,
    CONSTRAINT "request_id not empty" CHECK ((char_length(request_id) > 0))
);


ALTER TABLE auth.saml_relay_states OWNER TO supabase_auth_admin;

--
-- Name: TABLE saml_relay_states; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.saml_relay_states IS 'Auth: Contains SAML Relay State information for each Service Provider initiated login.';


--
-- Name: schema_migrations; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.schema_migrations (
    version character varying(255) NOT NULL
);


ALTER TABLE auth.schema_migrations OWNER TO supabase_auth_admin;

--
-- Name: TABLE schema_migrations; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.schema_migrations IS 'Auth: Manages updates to the auth system.';


--
-- Name: sessions; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.sessions (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    factor_id uuid,
    aal auth.aal_level,
    not_after timestamp with time zone,
    refreshed_at timestamp without time zone,
    user_agent text,
    ip inet,
    tag text,
    oauth_client_id uuid,
    refresh_token_hmac_key text,
    refresh_token_counter bigint,
    scopes text,
    CONSTRAINT sessions_scopes_length CHECK ((char_length(scopes) <= 4096))
);


ALTER TABLE auth.sessions OWNER TO supabase_auth_admin;

--
-- Name: TABLE sessions; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.sessions IS 'Auth: Stores session data associated to a user.';


--
-- Name: COLUMN sessions.not_after; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON COLUMN auth.sessions.not_after IS 'Auth: Not after is a nullable column that contains a timestamp after which the session should be regarded as expired.';


--
-- Name: COLUMN sessions.refresh_token_hmac_key; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON COLUMN auth.sessions.refresh_token_hmac_key IS 'Holds a HMAC-SHA256 key used to sign refresh tokens for this session.';


--
-- Name: COLUMN sessions.refresh_token_counter; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON COLUMN auth.sessions.refresh_token_counter IS 'Holds the ID (counter) of the last issued refresh token.';


--
-- Name: sso_domains; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.sso_domains (
    id uuid NOT NULL,
    sso_provider_id uuid NOT NULL,
    domain text NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    CONSTRAINT "domain not empty" CHECK ((char_length(domain) > 0))
);


ALTER TABLE auth.sso_domains OWNER TO supabase_auth_admin;

--
-- Name: TABLE sso_domains; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.sso_domains IS 'Auth: Manages SSO email address domain mapping to an SSO Identity Provider.';


--
-- Name: sso_providers; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.sso_providers (
    id uuid NOT NULL,
    resource_id text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    disabled boolean,
    CONSTRAINT "resource_id not empty" CHECK (((resource_id = NULL::text) OR (char_length(resource_id) > 0)))
);


ALTER TABLE auth.sso_providers OWNER TO supabase_auth_admin;

--
-- Name: TABLE sso_providers; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.sso_providers IS 'Auth: Manages SSO identity provider information; see saml_providers for SAML.';


--
-- Name: COLUMN sso_providers.resource_id; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON COLUMN auth.sso_providers.resource_id IS 'Auth: Uniquely identifies a SSO provider according to a user-chosen resource ID (case insensitive), useful in infrastructure as code.';


--
-- Name: users; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.users (
    instance_id uuid,
    id uuid NOT NULL,
    aud character varying(255),
    role character varying(255),
    email character varying(255),
    encrypted_password character varying(255),
    email_confirmed_at timestamp with time zone,
    invited_at timestamp with time zone,
    confirmation_token character varying(255),
    confirmation_sent_at timestamp with time zone,
    recovery_token character varying(255),
    recovery_sent_at timestamp with time zone,
    email_change_token_new character varying(255),
    email_change character varying(255),
    email_change_sent_at timestamp with time zone,
    last_sign_in_at timestamp with time zone,
    raw_app_meta_data jsonb,
    raw_user_meta_data jsonb,
    is_super_admin boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    phone text DEFAULT NULL::character varying,
    phone_confirmed_at timestamp with time zone,
    phone_change text DEFAULT ''::character varying,
    phone_change_token character varying(255) DEFAULT ''::character varying,
    phone_change_sent_at timestamp with time zone,
    confirmed_at timestamp with time zone GENERATED ALWAYS AS (LEAST(email_confirmed_at, phone_confirmed_at)) STORED,
    email_change_token_current character varying(255) DEFAULT ''::character varying,
    email_change_confirm_status smallint DEFAULT 0,
    banned_until timestamp with time zone,
    reauthentication_token character varying(255) DEFAULT ''::character varying,
    reauthentication_sent_at timestamp with time zone,
    is_sso_user boolean DEFAULT false NOT NULL,
    deleted_at timestamp with time zone,
    is_anonymous boolean DEFAULT false NOT NULL,
    CONSTRAINT users_email_change_confirm_status_check CHECK (((email_change_confirm_status >= 0) AND (email_change_confirm_status <= 2)))
);


ALTER TABLE auth.users OWNER TO supabase_auth_admin;

--
-- Name: TABLE users; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.users IS 'Auth: Stores user login data within a secure schema.';


--
-- Name: COLUMN users.is_sso_user; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON COLUMN auth.users.is_sso_user IS 'Auth: Set this column to true when the account comes from SSO. These accounts can have duplicate emails.';


--
-- Name: webauthn_challenges; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.webauthn_challenges (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    challenge_type text NOT NULL,
    session_data jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    CONSTRAINT webauthn_challenges_challenge_type_check CHECK ((challenge_type = ANY (ARRAY['signup'::text, 'registration'::text, 'authentication'::text])))
);


ALTER TABLE auth.webauthn_challenges OWNER TO supabase_auth_admin;

--
-- Name: webauthn_credentials; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.webauthn_credentials (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    credential_id bytea NOT NULL,
    public_key bytea NOT NULL,
    attestation_type text DEFAULT ''::text NOT NULL,
    aaguid uuid,
    sign_count bigint DEFAULT 0 NOT NULL,
    transports jsonb DEFAULT '[]'::jsonb NOT NULL,
    backup_eligible boolean DEFAULT false NOT NULL,
    backed_up boolean DEFAULT false NOT NULL,
    friendly_name text DEFAULT ''::text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    last_used_at timestamp with time zone
);


ALTER TABLE auth.webauthn_credentials OWNER TO supabase_auth_admin;

--
-- Name: associacao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.associacao (
    associacao_id integer NOT NULL,
    nome text,
    tipo text,
    cidade text,
    estado text,
    fone text,
    email text,
    contato text,
    observacao text,
    ativo integer DEFAULT 1
);


ALTER TABLE public.associacao OWNER TO postgres;

--
-- Name: associacao_associacao_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.associacao_associacao_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.associacao_associacao_id_seq OWNER TO postgres;

--
-- Name: associacao_associacao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.associacao_associacao_id_seq OWNED BY public.associacao.associacao_id;


--
-- Name: att_promotor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.att_promotor (
    att_promotor_id integer NOT NULL,
    promotor_id integer,
    pdv_id integer,
    dias_visita text,
    frequencia text,
    hora_inicio text,
    hora_fim text,
    observacao text,
    ativo integer DEFAULT 1
);


ALTER TABLE public.att_promotor OWNER TO postgres;

--
-- Name: att_promotor_att_promotor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.att_promotor_att_promotor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.att_promotor_att_promotor_id_seq OWNER TO postgres;

--
-- Name: att_promotor_att_promotor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.att_promotor_att_promotor_id_seq OWNED BY public.att_promotor.att_promotor_id;


--
-- Name: att_vendedor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.att_vendedor (
    att_vendedor_id integer NOT NULL,
    vendedor_id integer,
    pdv_id integer,
    dias_visita text,
    frequencia text,
    observacao text,
    ativo integer DEFAULT 1
);


ALTER TABLE public.att_vendedor OWNER TO postgres;

--
-- Name: att_vendedor_att_vendedor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.att_vendedor_att_vendedor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.att_vendedor_att_vendedor_id_seq OWNER TO postgres;

--
-- Name: att_vendedor_att_vendedor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.att_vendedor_att_vendedor_id_seq OWNED BY public.att_vendedor.att_vendedor_id;


--
-- Name: categoria; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categoria (
    categoria_id integer NOT NULL,
    nome_categoria text NOT NULL,
    ativo integer DEFAULT 1
);


ALTER TABLE public.categoria OWNER TO postgres;

--
-- Name: categoria_categoria_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categoria_categoria_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categoria_categoria_id_seq OWNER TO postgres;

--
-- Name: categoria_categoria_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categoria_categoria_id_seq OWNED BY public.categoria.categoria_id;


--
-- Name: central_compras; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.central_compras (
    central_id integer NOT NULL,
    cliente_id integer,
    nome_central text,
    tipo_entrega text,
    endereco_cd text,
    bairro_cd text,
    cidade_cd text,
    estado_cd text,
    fone text,
    email text,
    contato text,
    observacao text,
    ativo integer DEFAULT 1
);


ALTER TABLE public.central_compras OWNER TO postgres;

--
-- Name: central_compras_central_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.central_compras_central_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.central_compras_central_id_seq OWNER TO postgres;

--
-- Name: central_compras_central_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.central_compras_central_id_seq OWNED BY public.central_compras.central_id;


--
-- Name: cliente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cliente (
    cliente_id integer NOT NULL,
    razao_social text,
    nome_fantasia text NOT NULL,
    endereco text,
    bairro text,
    cidade text,
    estado text,
    cnpj text,
    ie text,
    site text,
    instagram text,
    fone text,
    perfil text,
    associacao_id integer,
    observacao text,
    ativo integer DEFAULT 1,
    status text DEFAULT 'prospecto'::text,
    email character varying(255)
);


ALTER TABLE public.cliente OWNER TO postgres;

--
-- Name: cliente_cliente_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cliente_cliente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cliente_cliente_id_seq OWNER TO postgres;

--
-- Name: cliente_cliente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cliente_cliente_id_seq OWNED BY public.cliente.cliente_id;


--
-- Name: cliente_fornecedor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cliente_fornecedor (
    cliente_fornecedor_id integer NOT NULL,
    cliente_id integer,
    fornecedor_id integer,
    tabela_preco_id integer,
    prazo_pagamento text,
    codigo_cliente text,
    observacao text,
    ativo integer DEFAULT 1
);


ALTER TABLE public.cliente_fornecedor OWNER TO postgres;

--
-- Name: cliente_fornecedor_cliente_fornecedor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cliente_fornecedor_cliente_fornecedor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cliente_fornecedor_cliente_fornecedor_id_seq OWNER TO postgres;

--
-- Name: cliente_fornecedor_cliente_fornecedor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cliente_fornecedor_cliente_fornecedor_id_seq OWNED BY public.cliente_fornecedor.cliente_fornecedor_id;


--
-- Name: comissao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comissao (
    comissao_id integer NOT NULL,
    fornecedor_id integer,
    percentual real,
    observacao text,
    ativo integer DEFAULT 1
);


ALTER TABLE public.comissao OWNER TO postgres;

--
-- Name: comissao_comissao_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.comissao_comissao_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comissao_comissao_id_seq OWNER TO postgres;

--
-- Name: comissao_comissao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.comissao_comissao_id_seq OWNED BY public.comissao.comissao_id;


--
-- Name: comissao_pagamento; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comissao_pagamento (
    pagamento_id integer NOT NULL,
    pedido_id integer,
    data_pagamento text,
    valor_previsto real,
    valor_pago real,
    status_pagamento text,
    observacao text
);


ALTER TABLE public.comissao_pagamento OWNER TO postgres;

--
-- Name: comissao_pagamento_pagamento_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.comissao_pagamento_pagamento_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comissao_pagamento_pagamento_id_seq OWNER TO postgres;

--
-- Name: comissao_pagamento_pagamento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.comissao_pagamento_pagamento_id_seq OWNED BY public.comissao_pagamento.pagamento_id;


--
-- Name: concorrente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.concorrente (
    concorrente_id integer NOT NULL,
    fornecedor_id integer,
    marca_concorrente text NOT NULL,
    origem_cidade text,
    importada integer DEFAULT 0,
    importado_por text,
    observacao text,
    ativo integer DEFAULT 1
);


ALTER TABLE public.concorrente OWNER TO postgres;

--
-- Name: concorrente_concorrente_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.concorrente_concorrente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.concorrente_concorrente_id_seq OWNER TO postgres;

--
-- Name: concorrente_concorrente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.concorrente_concorrente_id_seq OWNED BY public.concorrente.concorrente_id;


--
-- Name: configuracao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.configuracao (
    config_id integer NOT NULL,
    modo_operacao text,
    empresa_nome text,
    data_instalacao text,
    versao_sistema text,
    anthropic_api_key text,
    senha_exclusao text
);


ALTER TABLE public.configuracao OWNER TO postgres;

--
-- Name: configuracao_config_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.configuracao_config_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.configuracao_config_id_seq OWNER TO postgres;

--
-- Name: configuracao_config_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.configuracao_config_id_seq OWNED BY public.configuracao.config_id;


--
-- Name: contato_cliente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contato_cliente (
    contato_cliente_id integer NOT NULL,
    cliente_id integer,
    nome_contato text,
    departamento text,
    fone text,
    whatsapp text,
    email text,
    observacao text,
    ativo integer DEFAULT 1
);


ALTER TABLE public.contato_cliente OWNER TO postgres;

--
-- Name: contato_cliente_contato_cliente_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contato_cliente_contato_cliente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contato_cliente_contato_cliente_id_seq OWNER TO postgres;

--
-- Name: contato_cliente_contato_cliente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contato_cliente_contato_cliente_id_seq OWNED BY public.contato_cliente.contato_cliente_id;


--
-- Name: contato_fornecedor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contato_fornecedor (
    contato_fornecedor_id integer NOT NULL,
    fornecedor_id integer,
    nome_contato text,
    departamento text,
    fone text,
    email text,
    observacao text,
    ativo integer DEFAULT 1
);


ALTER TABLE public.contato_fornecedor OWNER TO postgres;

--
-- Name: contato_fornecedor_contato_fornecedor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contato_fornecedor_contato_fornecedor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contato_fornecedor_contato_fornecedor_id_seq OWNER TO postgres;

--
-- Name: contato_fornecedor_contato_fornecedor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contato_fornecedor_contato_fornecedor_id_seq OWNED BY public.contato_fornecedor.contato_fornecedor_id;


--
-- Name: contato_fornecedor_topico; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contato_fornecedor_topico (
    cft_id integer NOT NULL,
    contato_id integer NOT NULL,
    fornecedor_id integer NOT NULL,
    status character varying(50) DEFAULT 'A contatar'::character varying,
    tipo_topico character varying(30) DEFAULT 'Contato'::character varying,
    data_followup date,
    prioridade character varying(20) DEFAULT 'Média'::character varying,
    observacao text,
    ativo integer DEFAULT 1
);


ALTER TABLE public.contato_fornecedor_topico OWNER TO postgres;

--
-- Name: contato_fornecedor_topico_cft_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contato_fornecedor_topico_cft_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contato_fornecedor_topico_cft_id_seq OWNER TO postgres;

--
-- Name: contato_fornecedor_topico_cft_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contato_fornecedor_topico_cft_id_seq OWNED BY public.contato_fornecedor_topico.cft_id;


--
-- Name: contato_interacao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contato_interacao (
    interacao_id integer NOT NULL,
    contato_id integer,
    data_interacao text,
    via_comunicacao text,
    contato_pessoa text,
    descricao text,
    ativo integer DEFAULT 1,
    contato_cliente_id integer,
    resultado text,
    data_followup text
);


ALTER TABLE public.contato_interacao OWNER TO postgres;

--
-- Name: contato_interacao_interacao_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contato_interacao_interacao_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contato_interacao_interacao_id_seq OWNER TO postgres;

--
-- Name: contato_interacao_interacao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contato_interacao_interacao_id_seq OWNED BY public.contato_interacao.interacao_id;


--
-- Name: contato_registro; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contato_registro (
    contato_id integer NOT NULL,
    data_contato text,
    via_comunicacao text,
    tipo_entidade text,
    cliente_id integer,
    fornecedor_id integer,
    contato_pessoa text,
    assunto text,
    descricao text,
    resultado text,
    proxima_acao text,
    data_followup text,
    previsao_conclusao text,
    status text,
    prioridade text,
    tipo_topico text DEFAULT 'Contato'::text,
    usuario_resp text,
    observacao text,
    ativo integer DEFAULT 1
);


ALTER TABLE public.contato_registro OWNER TO postgres;

--
-- Name: contato_registro_contato_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contato_registro_contato_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contato_registro_contato_id_seq OWNER TO postgres;

--
-- Name: contato_registro_contato_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contato_registro_contato_id_seq OWNED BY public.contato_registro.contato_id;


--
-- Name: contato_x_fornecedor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contato_x_fornecedor (
    id integer NOT NULL,
    contato_id integer,
    fornecedor_id integer,
    cxf_id integer
);


ALTER TABLE public.contato_x_fornecedor OWNER TO postgres;

--
-- Name: contato_x_fornecedor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contato_x_fornecedor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contato_x_fornecedor_id_seq OWNER TO postgres;

--
-- Name: contato_x_fornecedor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contato_x_fornecedor_id_seq OWNED BY public.contato_x_fornecedor.id;


--
-- Name: fornecedor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fornecedor (
    fornecedor_id integer NOT NULL,
    razao_social text,
    nome_fantasia text NOT NULL,
    endereco text,
    bairro text,
    cidade text,
    estado text,
    cnpj text,
    ie text,
    observacao text,
    ativo integer DEFAULT 1,
    pedido_minimo numeric
);


ALTER TABLE public.fornecedor OWNER TO postgres;

--
-- Name: fornecedor_fornecedor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fornecedor_fornecedor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.fornecedor_fornecedor_id_seq OWNER TO postgres;

--
-- Name: fornecedor_fornecedor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fornecedor_fornecedor_id_seq OWNED BY public.fornecedor.fornecedor_id;


--
-- Name: historico_preco; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.historico_preco (
    hist_id integer NOT NULL,
    produto_id integer,
    fornecedor_id integer,
    tabela_id integer,
    nome_tabela text,
    data_vigencia text,
    preco_caixa real,
    preco_kg real,
    data_registro text
);


ALTER TABLE public.historico_preco OWNER TO postgres;

--
-- Name: historico_preco_hist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.historico_preco_hist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.historico_preco_hist_id_seq OWNER TO postgres;

--
-- Name: historico_preco_hist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.historico_preco_hist_id_seq OWNED BY public.historico_preco.hist_id;


--
-- Name: interacao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.interacao (
    interacao_id integer NOT NULL,
    negociacao_id bigint,
    data_interacao text,
    via_comunicacao text,
    contato_pessoa text,
    contato_cliente_id bigint,
    descricao text,
    resultado text,
    data_followup text,
    status_interacao text,
    ativo bigint
);


ALTER TABLE public.interacao OWNER TO postgres;

--
-- Name: interacao_interacao_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.interacao_interacao_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.interacao_interacao_id_seq OWNER TO postgres;

--
-- Name: interacao_interacao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.interacao_interacao_id_seq OWNED BY public.interacao.interacao_id;


--
-- Name: linha; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.linha (
    linha_id integer NOT NULL,
    categoria_id integer,
    nome_linha text NOT NULL,
    ativo integer DEFAULT 1
);


ALTER TABLE public.linha OWNER TO postgres;

--
-- Name: linha_linha_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.linha_linha_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.linha_linha_id_seq OWNER TO postgres;

--
-- Name: linha_linha_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.linha_linha_id_seq OWNED BY public.linha.linha_id;


--
-- Name: marca; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marca (
    marca_id integer NOT NULL,
    fornecedor_id integer,
    nome_marca text NOT NULL,
    ativo integer DEFAULT 1
);


ALTER TABLE public.marca OWNER TO postgres;

--
-- Name: marca_marca_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marca_marca_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.marca_marca_id_seq OWNER TO postgres;

--
-- Name: marca_marca_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marca_marca_id_seq OWNED BY public.marca.marca_id;


--
-- Name: mensagem_modelo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mensagem_modelo (
    mensagem_id integer NOT NULL,
    nome text NOT NULL,
    assunto text,
    corpo text NOT NULL,
    via text DEFAULT 'WhatsApp'::text,
    ativo integer DEFAULT 1
);


ALTER TABLE public.mensagem_modelo OWNER TO postgres;

--
-- Name: mensagem_modelo_mensagem_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mensagem_modelo_mensagem_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mensagem_modelo_mensagem_id_seq OWNER TO postgres;

--
-- Name: mensagem_modelo_mensagem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mensagem_modelo_mensagem_id_seq OWNED BY public.mensagem_modelo.mensagem_id;


--
-- Name: meta_fornecedor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.meta_fornecedor (
    meta_id integer NOT NULL,
    fornecedor_id integer,
    ano integer,
    mes integer,
    meta_valor real,
    meta_pedidos integer,
    observacao text,
    ativo integer DEFAULT 1
);


ALTER TABLE public.meta_fornecedor OWNER TO postgres;

--
-- Name: meta_fornecedor_meta_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.meta_fornecedor_meta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.meta_fornecedor_meta_id_seq OWNER TO postgres;

--
-- Name: meta_fornecedor_meta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.meta_fornecedor_meta_id_seq OWNED BY public.meta_fornecedor.meta_id;


--
-- Name: meta_mix; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.meta_mix (
    meta_mix_id integer NOT NULL,
    fornecedor_id integer,
    tipo text DEFAULT 'produto'::text,
    referencia_id integer,
    descricao text,
    ano integer,
    mes integer,
    meta_qtd integer,
    meta_clientes integer,
    observacao text,
    ativo integer DEFAULT 1
);


ALTER TABLE public.meta_mix OWNER TO postgres;

--
-- Name: meta_mix_meta_mix_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.meta_mix_meta_mix_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.meta_mix_meta_mix_id_seq OWNER TO postgres;

--
-- Name: meta_mix_meta_mix_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.meta_mix_meta_mix_id_seq OWNED BY public.meta_mix.meta_mix_id;


--
-- Name: mix_cliente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mix_cliente (
    mix_id integer NOT NULL,
    cliente_id integer,
    fornecedor_id integer,
    pdv_id integer,
    produto_id integer,
    ativo integer DEFAULT 1,
    observacao text
);


ALTER TABLE public.mix_cliente OWNER TO postgres;

--
-- Name: mix_cliente_mix_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mix_cliente_mix_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mix_cliente_mix_id_seq OWNER TO postgres;

--
-- Name: mix_cliente_mix_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mix_cliente_mix_id_seq OWNED BY public.mix_cliente.mix_id;


--
-- Name: negociacao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.negociacao (
    negociacao_id integer NOT NULL,
    cliente_id bigint,
    fornecedor_id bigint,
    titulo text,
    data_abertura text,
    status text,
    prioridade text,
    previsao_conclusao text,
    observacao text,
    ativo bigint
);


ALTER TABLE public.negociacao OWNER TO postgres;

--
-- Name: negociacao_negociacao_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.negociacao_negociacao_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.negociacao_negociacao_id_seq OWNER TO postgres;

--
-- Name: negociacao_negociacao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.negociacao_negociacao_id_seq OWNED BY public.negociacao.negociacao_id;


--
-- Name: pdv; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pdv (
    pdv_id integer NOT NULL,
    cliente_id integer,
    numero_loja text,
    nome_loja text,
    endereco text,
    bairro text,
    cidade text,
    estado text,
    cnpj text,
    ie text,
    gerente text,
    fone_gerente text,
    encarregado text,
    fone_encarregado text,
    horario_recebimento text,
    tipo_pdv text,
    setor text,
    cluster text,
    tamanho_pdv text,
    latitude text,
    longitude text,
    ordem_roteiro integer,
    dia_visita text,
    frequencia_visita text,
    observacao text,
    ativo integer DEFAULT 1,
    status text DEFAULT 'Ativo'::text
);


ALTER TABLE public.pdv OWNER TO postgres;

--
-- Name: pdv_pdv_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pdv_pdv_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pdv_pdv_id_seq OWNER TO postgres;

--
-- Name: pdv_pdv_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pdv_pdv_id_seq OWNED BY public.pdv.pdv_id;


--
-- Name: pedido; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pedido (
    pedido_id integer NOT NULL,
    nr_pedido_fornecedor text,
    nr_pedido_cliente text,
    cliente_id integer NOT NULL,
    pdv_id integer,
    fornecedor_id integer NOT NULL,
    vendedor_id integer,
    tabela_preco_id integer,
    prazo_pagamento text,
    frete text,
    data_pedido text,
    data_entrega text,
    desconto_geral real DEFAULT 0,
    observacao text,
    status_pedido text DEFAULT 'ABERTO'::text,
    comissao_percentual real,
    data_entrega_realizada text
);


ALTER TABLE public.pedido OWNER TO postgres;

--
-- Name: pedido_historico; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pedido_historico (
    historico_id integer NOT NULL,
    pedido_id integer,
    data_hora text,
    campo text,
    valor_antes text,
    valor_depois text,
    observacao text
);


ALTER TABLE public.pedido_historico OWNER TO postgres;

--
-- Name: pedido_historico_historico_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pedido_historico_historico_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pedido_historico_historico_id_seq OWNER TO postgres;

--
-- Name: pedido_historico_historico_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pedido_historico_historico_id_seq OWNED BY public.pedido_historico.historico_id;


--
-- Name: pedido_item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pedido_item (
    pedido_item_id integer NOT NULL,
    pedido_id integer NOT NULL,
    produto_id integer,
    preco_tabela real,
    desconto real,
    preco_final real,
    quantidade integer,
    status_item text
);


ALTER TABLE public.pedido_item OWNER TO postgres;

--
-- Name: pedido_item_pedido_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pedido_item_pedido_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pedido_item_pedido_item_id_seq OWNER TO postgres;

--
-- Name: pedido_item_pedido_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pedido_item_pedido_item_id_seq OWNED BY public.pedido_item.pedido_item_id;


--
-- Name: pedido_pedido_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pedido_pedido_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pedido_pedido_id_seq OWNER TO postgres;

--
-- Name: pedido_pedido_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pedido_pedido_id_seq OWNED BY public.pedido.pedido_id;


--
-- Name: pesquisa_foto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pesquisa_foto (
    foto_id integer NOT NULL,
    pesquisa_id integer,
    foto_data text,
    nome_arquivo text,
    descricao text,
    data_upload text,
    foto_path text,
    legenda text,
    ativo bigint
);


ALTER TABLE public.pesquisa_foto OWNER TO postgres;

--
-- Name: pesquisa_foto_foto_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pesquisa_foto_foto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pesquisa_foto_foto_id_seq OWNER TO postgres;

--
-- Name: pesquisa_foto_foto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pesquisa_foto_foto_id_seq OWNED BY public.pesquisa_foto.foto_id;


--
-- Name: pesquisa_preco; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pesquisa_preco (
    pesquisa_id integer NOT NULL,
    data_pesquisa text,
    pdv_id integer,
    cliente_id integer,
    fornecedor_id integer,
    observacao text,
    status text DEFAULT 'rascunho'::text,
    foto_path text
);


ALTER TABLE public.pesquisa_preco OWNER TO postgres;

--
-- Name: pesquisa_preco_item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pesquisa_preco_item (
    pesquisa_item_id integer NOT NULL,
    pesquisa_id integer,
    produto_id integer,
    produto_concorrente_id integer,
    preco real,
    em_oferta integer DEFAULT 0,
    frentes integer,
    ruptura integer DEFAULT 0,
    ponto_extra integer DEFAULT 0,
    tipo_ponto_extra text,
    observacao text,
    preco_proprio real,
    facing integer,
    preco_concorrente double precision,
    marca_concorrente_livre text,
    obs_concorrente text,
    foto_path text,
    unidade_coleta text DEFAULT 'UN'::text,
    peso_coleta double precision,
    preco_kg double precision
);


ALTER TABLE public.pesquisa_preco_item OWNER TO postgres;

--
-- Name: pesquisa_preco_item_pesquisa_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pesquisa_preco_item_pesquisa_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pesquisa_preco_item_pesquisa_item_id_seq OWNER TO postgres;

--
-- Name: pesquisa_preco_item_pesquisa_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pesquisa_preco_item_pesquisa_item_id_seq OWNED BY public.pesquisa_preco_item.pesquisa_item_id;


--
-- Name: pesquisa_preco_pesquisa_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pesquisa_preco_pesquisa_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pesquisa_preco_pesquisa_id_seq OWNER TO postgres;

--
-- Name: pesquisa_preco_pesquisa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pesquisa_preco_pesquisa_id_seq OWNED BY public.pesquisa_preco.pesquisa_id;


--
-- Name: produto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.produto (
    produto_id integer NOT NULL,
    fornecedor_id integer,
    marca_id integer,
    categoria_id integer,
    linha_id integer,
    codigo_produto text,
    descricao text NOT NULL,
    descricao_curta text,
    peso real,
    peso_caixa real,
    unidade_medida text,
    unidades_caixa integer,
    caixas_pallet integer,
    ean text,
    dun text,
    ncm text,
    cest text,
    validade_dias integer,
    sub_categoria text,
    grupo text,
    observacao text,
    ativo integer DEFAULT 1,
    shelf_life_resfriado integer,
    shelf_life_congelado integer
);


ALTER TABLE public.produto OWNER TO postgres;

--
-- Name: produto_codigo_cliente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.produto_codigo_cliente (
    produto_codigo_id integer NOT NULL,
    cliente_id integer,
    produto_id integer,
    codigo_cliente text
);


ALTER TABLE public.produto_codigo_cliente OWNER TO postgres;

--
-- Name: produto_codigo_cliente_produto_codigo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.produto_codigo_cliente_produto_codigo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.produto_codigo_cliente_produto_codigo_id_seq OWNER TO postgres;

--
-- Name: produto_codigo_cliente_produto_codigo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.produto_codigo_cliente_produto_codigo_id_seq OWNED BY public.produto_codigo_cliente.produto_codigo_id;


--
-- Name: produto_concorrente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.produto_concorrente (
    produto_concorrente_id integer NOT NULL,
    concorrente_id integer,
    categoria_id integer,
    linha_id integer,
    descricao text NOT NULL,
    descricao_curta text,
    peso real,
    unidade_medida text,
    ean_concorrente text,
    auditavel integer DEFAULT 1,
    validade_dias integer,
    observacao text,
    ativo integer DEFAULT 1,
    unidades_caixa integer,
    ean text,
    preco_referencia double precision
);


ALTER TABLE public.produto_concorrente OWNER TO postgres;

--
-- Name: produto_concorrente_produto_concorrente_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.produto_concorrente_produto_concorrente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.produto_concorrente_produto_concorrente_id_seq OWNER TO postgres;

--
-- Name: produto_concorrente_produto_concorrente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.produto_concorrente_produto_concorrente_id_seq OWNED BY public.produto_concorrente.produto_concorrente_id;


--
-- Name: produto_concorrente_relacao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.produto_concorrente_relacao (
    relacao_id integer NOT NULL,
    produto_id integer,
    produto_concorrente_id integer,
    tipo_relacao text,
    observacao text
);


ALTER TABLE public.produto_concorrente_relacao OWNER TO postgres;

--
-- Name: produto_concorrente_relacao_relacao_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.produto_concorrente_relacao_relacao_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.produto_concorrente_relacao_relacao_id_seq OWNER TO postgres;

--
-- Name: produto_concorrente_relacao_relacao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.produto_concorrente_relacao_relacao_id_seq OWNED BY public.produto_concorrente_relacao.relacao_id;


--
-- Name: produto_produto_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.produto_produto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.produto_produto_id_seq OWNER TO postgres;

--
-- Name: produto_produto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.produto_produto_id_seq OWNED BY public.produto.produto_id;


--
-- Name: promotor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.promotor (
    promotor_id integer NOT NULL,
    nome text,
    fone text,
    email text,
    cpf text,
    cnh text,
    veiculo text,
    cidade text,
    estado text,
    bairro text,
    endereco text,
    observacao text,
    ativo integer DEFAULT 1
);


ALTER TABLE public.promotor OWNER TO postgres;

--
-- Name: promotor_promotor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.promotor_promotor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.promotor_promotor_id_seq OWNER TO postgres;

--
-- Name: promotor_promotor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.promotor_promotor_id_seq OWNED BY public.promotor.promotor_id;


--
-- Name: representante; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.representante (
    representante_id integer NOT NULL,
    razao_social text,
    nome_fantasia text,
    cnpj text,
    endereco text,
    bairro text,
    cidade text,
    estado text,
    fone text,
    whatsapp text,
    email text,
    site text,
    observacao text,
    ativo integer DEFAULT 1
);


ALTER TABLE public.representante OWNER TO postgres;

--
-- Name: representante_representante_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.representante_representante_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.representante_representante_id_seq OWNER TO postgres;

--
-- Name: representante_representante_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.representante_representante_id_seq OWNED BY public.representante.representante_id;


--
-- Name: tabela_preco; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tabela_preco (
    tabela_preco_id integer NOT NULL,
    fornecedor_id integer,
    nome_tabela text NOT NULL,
    tipo_tabela text,
    prazo_pagamento text,
    frete text,
    data_inicio text,
    data_fim text,
    ativo integer DEFAULT 1
);


ALTER TABLE public.tabela_preco OWNER TO postgres;

--
-- Name: tabela_preco_item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tabela_preco_item (
    tabela_preco_item_id integer NOT NULL,
    tabela_preco_id integer,
    produto_id integer,
    preco_caixa real NOT NULL,
    desconto_maximo real DEFAULT 0,
    preco_kg real,
    observacao text,
    peso_unidade real
);


ALTER TABLE public.tabela_preco_item OWNER TO postgres;

--
-- Name: tabela_preco_item_tabela_preco_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tabela_preco_item_tabela_preco_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tabela_preco_item_tabela_preco_item_id_seq OWNER TO postgres;

--
-- Name: tabela_preco_item_tabela_preco_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tabela_preco_item_tabela_preco_item_id_seq OWNED BY public.tabela_preco_item.tabela_preco_item_id;


--
-- Name: tabela_preco_tabela_preco_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tabela_preco_tabela_preco_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tabela_preco_tabela_preco_id_seq OWNER TO postgres;

--
-- Name: tabela_preco_tabela_preco_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tabela_preco_tabela_preco_id_seq OWNED BY public.tabela_preco.tabela_preco_id;


--
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario (
    usuario_id integer NOT NULL,
    nome text,
    email text,
    senha_hash text,
    tipo text,
    vendedor_id integer,
    ativo integer DEFAULT 1
);


ALTER TABLE public.usuario OWNER TO postgres;

--
-- Name: usuario_usuario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuario_usuario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuario_usuario_id_seq OWNER TO postgres;

--
-- Name: usuario_usuario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuario_usuario_id_seq OWNED BY public.usuario.usuario_id;


--
-- Name: vendedor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vendedor (
    vendedor_id integer NOT NULL,
    representante_id integer,
    nome text,
    fone text,
    whatsapp text,
    email text,
    cpf text,
    chave_pix text,
    data_aniversario text,
    observacao text,
    ativo integer DEFAULT 1
);


ALTER TABLE public.vendedor OWNER TO postgres;

--
-- Name: vendedor_vendedor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.vendedor_vendedor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.vendedor_vendedor_id_seq OWNER TO postgres;

--
-- Name: vendedor_vendedor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.vendedor_vendedor_id_seq OWNED BY public.vendedor.vendedor_id;


--
-- Name: visita_cliente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.visita_cliente (
    visita_id integer NOT NULL,
    cliente_id integer,
    pdv_id integer,
    local text,
    data_visita text,
    contato text,
    resumo text,
    produtos_tratados text,
    pedido_id integer,
    proxima_acao text,
    data_followup text,
    observacao text,
    pesquisa_preco_id integer,
    latitude text,
    longitude text,
    endereco_gps text,
    duracao_minutos bigint
);


ALTER TABLE public.visita_cliente OWNER TO postgres;

--
-- Name: visita_cliente_visita_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.visita_cliente_visita_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.visita_cliente_visita_id_seq OWNER TO postgres;

--
-- Name: visita_cliente_visita_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.visita_cliente_visita_id_seq OWNED BY public.visita_cliente.visita_id;


--
-- Name: messages; Type: TABLE; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE TABLE realtime.messages (
    topic text NOT NULL,
    extension text NOT NULL,
    payload jsonb,
    event text,
    private boolean DEFAULT false,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    inserted_at timestamp without time zone DEFAULT now() NOT NULL,
    id uuid DEFAULT gen_random_uuid() NOT NULL
)
PARTITION BY RANGE (inserted_at);


ALTER TABLE realtime.messages OWNER TO supabase_realtime_admin;

--
-- Name: schema_migrations; Type: TABLE; Schema: realtime; Owner: supabase_admin
--

CREATE TABLE realtime.schema_migrations (
    version bigint NOT NULL,
    inserted_at timestamp(0) without time zone
);


ALTER TABLE realtime.schema_migrations OWNER TO supabase_admin;

--
-- Name: subscription; Type: TABLE; Schema: realtime; Owner: supabase_admin
--

CREATE TABLE realtime.subscription (
    id bigint NOT NULL,
    subscription_id uuid NOT NULL,
    entity regclass NOT NULL,
    filters realtime.user_defined_filter[] DEFAULT '{}'::realtime.user_defined_filter[] NOT NULL,
    claims jsonb NOT NULL,
    claims_role regrole GENERATED ALWAYS AS (realtime.to_regrole((claims ->> 'role'::text))) STORED NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    action_filter text DEFAULT '*'::text,
    CONSTRAINT subscription_action_filter_check CHECK ((action_filter = ANY (ARRAY['*'::text, 'INSERT'::text, 'UPDATE'::text, 'DELETE'::text])))
);


ALTER TABLE realtime.subscription OWNER TO supabase_admin;

--
-- Name: subscription_id_seq; Type: SEQUENCE; Schema: realtime; Owner: supabase_admin
--

ALTER TABLE realtime.subscription ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME realtime.subscription_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: buckets; Type: TABLE; Schema: storage; Owner: supabase_storage_admin
--

CREATE TABLE storage.buckets (
    id text NOT NULL,
    name text NOT NULL,
    owner uuid,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    public boolean DEFAULT false,
    avif_autodetection boolean DEFAULT false,
    file_size_limit bigint,
    allowed_mime_types text[],
    owner_id text,
    type storage.buckettype DEFAULT 'STANDARD'::storage.buckettype NOT NULL
);


ALTER TABLE storage.buckets OWNER TO supabase_storage_admin;

--
-- Name: COLUMN buckets.owner; Type: COMMENT; Schema: storage; Owner: supabase_storage_admin
--

COMMENT ON COLUMN storage.buckets.owner IS 'Field is deprecated, use owner_id instead';


--
-- Name: buckets_analytics; Type: TABLE; Schema: storage; Owner: supabase_storage_admin
--

CREATE TABLE storage.buckets_analytics (
    name text NOT NULL,
    type storage.buckettype DEFAULT 'ANALYTICS'::storage.buckettype NOT NULL,
    format text DEFAULT 'ICEBERG'::text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE storage.buckets_analytics OWNER TO supabase_storage_admin;

--
-- Name: buckets_vectors; Type: TABLE; Schema: storage; Owner: supabase_storage_admin
--

CREATE TABLE storage.buckets_vectors (
    id text NOT NULL,
    type storage.buckettype DEFAULT 'VECTOR'::storage.buckettype NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE storage.buckets_vectors OWNER TO supabase_storage_admin;

--
-- Name: migrations; Type: TABLE; Schema: storage; Owner: supabase_storage_admin
--

CREATE TABLE storage.migrations (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    hash character varying(40) NOT NULL,
    executed_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE storage.migrations OWNER TO supabase_storage_admin;

--
-- Name: objects; Type: TABLE; Schema: storage; Owner: supabase_storage_admin
--

CREATE TABLE storage.objects (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    bucket_id text,
    name text,
    owner uuid,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    last_accessed_at timestamp with time zone DEFAULT now(),
    metadata jsonb,
    path_tokens text[] GENERATED ALWAYS AS (string_to_array(name, '/'::text)) STORED,
    version text,
    owner_id text,
    user_metadata jsonb
);


ALTER TABLE storage.objects OWNER TO supabase_storage_admin;

--
-- Name: COLUMN objects.owner; Type: COMMENT; Schema: storage; Owner: supabase_storage_admin
--

COMMENT ON COLUMN storage.objects.owner IS 'Field is deprecated, use owner_id instead';


--
-- Name: s3_multipart_uploads; Type: TABLE; Schema: storage; Owner: supabase_storage_admin
--

CREATE TABLE storage.s3_multipart_uploads (
    id text NOT NULL,
    in_progress_size bigint DEFAULT 0 NOT NULL,
    upload_signature text NOT NULL,
    bucket_id text NOT NULL,
    key text NOT NULL COLLATE pg_catalog."C",
    version text NOT NULL,
    owner_id text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    user_metadata jsonb,
    metadata jsonb
);


ALTER TABLE storage.s3_multipart_uploads OWNER TO supabase_storage_admin;

--
-- Name: s3_multipart_uploads_parts; Type: TABLE; Schema: storage; Owner: supabase_storage_admin
--

CREATE TABLE storage.s3_multipart_uploads_parts (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    upload_id text NOT NULL,
    size bigint DEFAULT 0 NOT NULL,
    part_number integer NOT NULL,
    bucket_id text NOT NULL,
    key text NOT NULL COLLATE pg_catalog."C",
    etag text NOT NULL,
    owner_id text,
    version text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE storage.s3_multipart_uploads_parts OWNER TO supabase_storage_admin;

--
-- Name: vector_indexes; Type: TABLE; Schema: storage; Owner: supabase_storage_admin
--

CREATE TABLE storage.vector_indexes (
    id text DEFAULT gen_random_uuid() NOT NULL,
    name text NOT NULL COLLATE pg_catalog."C",
    bucket_id text NOT NULL,
    data_type text NOT NULL,
    dimension integer NOT NULL,
    distance_metric text NOT NULL,
    metadata_configuration jsonb,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE storage.vector_indexes OWNER TO supabase_storage_admin;

--
-- Name: refresh_tokens id; Type: DEFAULT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.refresh_tokens ALTER COLUMN id SET DEFAULT nextval('auth.refresh_tokens_id_seq'::regclass);


--
-- Name: associacao associacao_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.associacao ALTER COLUMN associacao_id SET DEFAULT nextval('public.associacao_associacao_id_seq'::regclass);


--
-- Name: att_promotor att_promotor_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.att_promotor ALTER COLUMN att_promotor_id SET DEFAULT nextval('public.att_promotor_att_promotor_id_seq'::regclass);


--
-- Name: att_vendedor att_vendedor_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.att_vendedor ALTER COLUMN att_vendedor_id SET DEFAULT nextval('public.att_vendedor_att_vendedor_id_seq'::regclass);


--
-- Name: categoria categoria_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categoria ALTER COLUMN categoria_id SET DEFAULT nextval('public.categoria_categoria_id_seq'::regclass);


--
-- Name: central_compras central_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.central_compras ALTER COLUMN central_id SET DEFAULT nextval('public.central_compras_central_id_seq'::regclass);


--
-- Name: cliente cliente_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente ALTER COLUMN cliente_id SET DEFAULT nextval('public.cliente_cliente_id_seq'::regclass);


--
-- Name: cliente_fornecedor cliente_fornecedor_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente_fornecedor ALTER COLUMN cliente_fornecedor_id SET DEFAULT nextval('public.cliente_fornecedor_cliente_fornecedor_id_seq'::regclass);


--
-- Name: comissao comissao_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comissao ALTER COLUMN comissao_id SET DEFAULT nextval('public.comissao_comissao_id_seq'::regclass);


--
-- Name: comissao_pagamento pagamento_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comissao_pagamento ALTER COLUMN pagamento_id SET DEFAULT nextval('public.comissao_pagamento_pagamento_id_seq'::regclass);


--
-- Name: concorrente concorrente_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.concorrente ALTER COLUMN concorrente_id SET DEFAULT nextval('public.concorrente_concorrente_id_seq'::regclass);


--
-- Name: configuracao config_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.configuracao ALTER COLUMN config_id SET DEFAULT nextval('public.configuracao_config_id_seq'::regclass);


--
-- Name: contato_cliente contato_cliente_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contato_cliente ALTER COLUMN contato_cliente_id SET DEFAULT nextval('public.contato_cliente_contato_cliente_id_seq'::regclass);


--
-- Name: contato_fornecedor contato_fornecedor_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contato_fornecedor ALTER COLUMN contato_fornecedor_id SET DEFAULT nextval('public.contato_fornecedor_contato_fornecedor_id_seq'::regclass);


--
-- Name: contato_fornecedor_topico cft_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contato_fornecedor_topico ALTER COLUMN cft_id SET DEFAULT nextval('public.contato_fornecedor_topico_cft_id_seq'::regclass);


--
-- Name: contato_interacao interacao_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contato_interacao ALTER COLUMN interacao_id SET DEFAULT nextval('public.contato_interacao_interacao_id_seq'::regclass);


--
-- Name: contato_registro contato_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contato_registro ALTER COLUMN contato_id SET DEFAULT nextval('public.contato_registro_contato_id_seq'::regclass);


--
-- Name: contato_x_fornecedor id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contato_x_fornecedor ALTER COLUMN id SET DEFAULT nextval('public.contato_x_fornecedor_id_seq'::regclass);


--
-- Name: fornecedor fornecedor_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fornecedor ALTER COLUMN fornecedor_id SET DEFAULT nextval('public.fornecedor_fornecedor_id_seq'::regclass);


--
-- Name: historico_preco hist_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.historico_preco ALTER COLUMN hist_id SET DEFAULT nextval('public.historico_preco_hist_id_seq'::regclass);


--
-- Name: interacao interacao_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.interacao ALTER COLUMN interacao_id SET DEFAULT nextval('public.interacao_interacao_id_seq'::regclass);


--
-- Name: linha linha_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.linha ALTER COLUMN linha_id SET DEFAULT nextval('public.linha_linha_id_seq'::regclass);


--
-- Name: marca marca_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marca ALTER COLUMN marca_id SET DEFAULT nextval('public.marca_marca_id_seq'::regclass);


--
-- Name: mensagem_modelo mensagem_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mensagem_modelo ALTER COLUMN mensagem_id SET DEFAULT nextval('public.mensagem_modelo_mensagem_id_seq'::regclass);


--
-- Name: meta_fornecedor meta_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meta_fornecedor ALTER COLUMN meta_id SET DEFAULT nextval('public.meta_fornecedor_meta_id_seq'::regclass);


--
-- Name: meta_mix meta_mix_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meta_mix ALTER COLUMN meta_mix_id SET DEFAULT nextval('public.meta_mix_meta_mix_id_seq'::regclass);


--
-- Name: mix_cliente mix_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mix_cliente ALTER COLUMN mix_id SET DEFAULT nextval('public.mix_cliente_mix_id_seq'::regclass);


--
-- Name: negociacao negociacao_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.negociacao ALTER COLUMN negociacao_id SET DEFAULT nextval('public.negociacao_negociacao_id_seq'::regclass);


--
-- Name: pdv pdv_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pdv ALTER COLUMN pdv_id SET DEFAULT nextval('public.pdv_pdv_id_seq'::regclass);


--
-- Name: pedido pedido_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedido ALTER COLUMN pedido_id SET DEFAULT nextval('public.pedido_pedido_id_seq'::regclass);


--
-- Name: pedido_historico historico_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedido_historico ALTER COLUMN historico_id SET DEFAULT nextval('public.pedido_historico_historico_id_seq'::regclass);


--
-- Name: pedido_item pedido_item_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedido_item ALTER COLUMN pedido_item_id SET DEFAULT nextval('public.pedido_item_pedido_item_id_seq'::regclass);


--
-- Name: pesquisa_foto foto_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pesquisa_foto ALTER COLUMN foto_id SET DEFAULT nextval('public.pesquisa_foto_foto_id_seq'::regclass);


--
-- Name: pesquisa_preco pesquisa_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pesquisa_preco ALTER COLUMN pesquisa_id SET DEFAULT nextval('public.pesquisa_preco_pesquisa_id_seq'::regclass);


--
-- Name: pesquisa_preco_item pesquisa_item_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pesquisa_preco_item ALTER COLUMN pesquisa_item_id SET DEFAULT nextval('public.pesquisa_preco_item_pesquisa_item_id_seq'::regclass);


--
-- Name: produto produto_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produto ALTER COLUMN produto_id SET DEFAULT nextval('public.produto_produto_id_seq'::regclass);


--
-- Name: produto_codigo_cliente produto_codigo_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produto_codigo_cliente ALTER COLUMN produto_codigo_id SET DEFAULT nextval('public.produto_codigo_cliente_produto_codigo_id_seq'::regclass);


--
-- Name: produto_concorrente produto_concorrente_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produto_concorrente ALTER COLUMN produto_concorrente_id SET DEFAULT nextval('public.produto_concorrente_produto_concorrente_id_seq'::regclass);


--
-- Name: produto_concorrente_relacao relacao_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produto_concorrente_relacao ALTER COLUMN relacao_id SET DEFAULT nextval('public.produto_concorrente_relacao_relacao_id_seq'::regclass);


--
-- Name: promotor promotor_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.promotor ALTER COLUMN promotor_id SET DEFAULT nextval('public.promotor_promotor_id_seq'::regclass);


--
-- Name: representante representante_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.representante ALTER COLUMN representante_id SET DEFAULT nextval('public.representante_representante_id_seq'::regclass);


--
-- Name: tabela_preco tabela_preco_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tabela_preco ALTER COLUMN tabela_preco_id SET DEFAULT nextval('public.tabela_preco_tabela_preco_id_seq'::regclass);


--
-- Name: tabela_preco_item tabela_preco_item_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tabela_preco_item ALTER COLUMN tabela_preco_item_id SET DEFAULT nextval('public.tabela_preco_item_tabela_preco_item_id_seq'::regclass);


--
-- Name: usuario usuario_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario ALTER COLUMN usuario_id SET DEFAULT nextval('public.usuario_usuario_id_seq'::regclass);


--
-- Name: vendedor vendedor_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vendedor ALTER COLUMN vendedor_id SET DEFAULT nextval('public.vendedor_vendedor_id_seq'::regclass);


--
-- Name: visita_cliente visita_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visita_cliente ALTER COLUMN visita_id SET DEFAULT nextval('public.visita_cliente_visita_id_seq'::regclass);


--
-- Data for Name: audit_log_entries; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.audit_log_entries (instance_id, id, payload, created_at, ip_address) FROM stdin;
\.


--
-- Data for Name: custom_oauth_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.custom_oauth_providers (id, provider_type, identifier, name, client_id, client_secret, acceptable_client_ids, scopes, pkce_enabled, attribute_mapping, authorization_params, enabled, email_optional, issuer, discovery_url, skip_nonce_check, cached_discovery, discovery_cached_at, authorization_url, token_url, userinfo_url, jwks_uri, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: flow_state; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.flow_state (id, user_id, auth_code, code_challenge_method, code_challenge, provider_type, provider_access_token, provider_refresh_token, created_at, updated_at, authentication_method, auth_code_issued_at, invite_token, referrer, oauth_client_state_id, linking_target_id, email_optional) FROM stdin;
\.


--
-- Data for Name: identities; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.identities (provider_id, user_id, identity_data, provider, last_sign_in_at, created_at, updated_at, id) FROM stdin;
\.


--
-- Data for Name: instances; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.instances (id, uuid, raw_base_config, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: mfa_amr_claims; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.mfa_amr_claims (session_id, created_at, updated_at, authentication_method, id) FROM stdin;
\.


--
-- Data for Name: mfa_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.mfa_challenges (id, factor_id, created_at, verified_at, ip_address, otp_code, web_authn_session_data) FROM stdin;
\.


--
-- Data for Name: mfa_factors; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.mfa_factors (id, user_id, friendly_name, factor_type, status, created_at, updated_at, secret, phone, last_challenged_at, web_authn_credential, web_authn_aaguid, last_webauthn_challenge_data) FROM stdin;
\.


--
-- Data for Name: oauth_authorizations; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.oauth_authorizations (id, authorization_id, client_id, user_id, redirect_uri, scope, state, resource, code_challenge, code_challenge_method, response_type, status, authorization_code, created_at, expires_at, approved_at, nonce) FROM stdin;
\.


--
-- Data for Name: oauth_client_states; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.oauth_client_states (id, provider_type, code_verifier, created_at) FROM stdin;
\.


--
-- Data for Name: oauth_clients; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.oauth_clients (id, client_secret_hash, registration_type, redirect_uris, grant_types, client_name, client_uri, logo_uri, created_at, updated_at, deleted_at, client_type, token_endpoint_auth_method) FROM stdin;
\.


--
-- Data for Name: oauth_consents; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.oauth_consents (id, user_id, client_id, scopes, granted_at, revoked_at) FROM stdin;
\.


--
-- Data for Name: one_time_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.one_time_tokens (id, user_id, token_type, token_hash, relates_to, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.refresh_tokens (instance_id, id, token, user_id, revoked, created_at, updated_at, parent, session_id) FROM stdin;
\.


--
-- Data for Name: saml_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.saml_providers (id, sso_provider_id, entity_id, metadata_xml, metadata_url, attribute_mapping, created_at, updated_at, name_id_format) FROM stdin;
\.


--
-- Data for Name: saml_relay_states; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.saml_relay_states (id, sso_provider_id, request_id, for_email, redirect_to, created_at, updated_at, flow_state_id) FROM stdin;
\.


--
-- Data for Name: schema_migrations; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.schema_migrations (version) FROM stdin;
20171026211738
20171026211808
20171026211834
20180103212743
20180108183307
20180119214651
20180125194653
00
20210710035447
20210722035447
20210730183235
20210909172000
20210927181326
20211122151130
20211124214934
20211202183645
20220114185221
20220114185340
20220224000811
20220323170000
20220429102000
20220531120530
20220614074223
20220811173540
20221003041349
20221003041400
20221011041400
20221020193600
20221021073300
20221021082433
20221027105023
20221114143122
20221114143410
20221125140132
20221208132122
20221215195500
20221215195800
20221215195900
20230116124310
20230116124412
20230131181311
20230322519590
20230402418590
20230411005111
20230508135423
20230523124323
20230818113222
20230914180801
20231027141322
20231114161723
20231117164230
20240115144230
20240214120130
20240306115329
20240314092811
20240427152123
20240612123726
20240729123726
20240802193726
20240806073726
20241009103726
20250717082212
20250731150234
20250804100000
20250901200500
20250903112500
20250904133000
20250925093508
20251007112900
20251104100000
20251111201300
20251201000000
20260115000000
20260121000000
20260219120000
20260302000000
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.sessions (id, user_id, created_at, updated_at, factor_id, aal, not_after, refreshed_at, user_agent, ip, tag, oauth_client_id, refresh_token_hmac_key, refresh_token_counter, scopes) FROM stdin;
\.


--
-- Data for Name: sso_domains; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.sso_domains (id, sso_provider_id, domain, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: sso_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.sso_providers (id, resource_id, created_at, updated_at, disabled) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.users (instance_id, id, aud, role, email, encrypted_password, email_confirmed_at, invited_at, confirmation_token, confirmation_sent_at, recovery_token, recovery_sent_at, email_change_token_new, email_change, email_change_sent_at, last_sign_in_at, raw_app_meta_data, raw_user_meta_data, is_super_admin, created_at, updated_at, phone, phone_confirmed_at, phone_change, phone_change_token, phone_change_sent_at, email_change_token_current, email_change_confirm_status, banned_until, reauthentication_token, reauthentication_sent_at, is_sso_user, deleted_at, is_anonymous) FROM stdin;
\.


--
-- Data for Name: webauthn_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.webauthn_challenges (id, user_id, challenge_type, session_data, created_at, expires_at) FROM stdin;
\.


--
-- Data for Name: webauthn_credentials; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.webauthn_credentials (id, user_id, credential_id, public_key, attestation_type, aaguid, sign_count, transports, backup_eligible, backed_up, friendly_name, created_at, updated_at, last_used_at) FROM stdin;
\.


--
-- Data for Name: associacao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.associacao (associacao_id, nome, tipo, cidade, estado, fone, email, contato, observacao, ativo) FROM stdin;
1	Rede Litoral	Associacao de compras	São Vicente	SP	\N	\N	\N	\N	1
\.


--
-- Data for Name: att_promotor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.att_promotor (att_promotor_id, promotor_id, pdv_id, dias_visita, frequencia, hora_inicio, hora_fim, observacao, ativo) FROM stdin;
\.


--
-- Data for Name: att_vendedor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.att_vendedor (att_vendedor_id, vendedor_id, pdv_id, dias_visita, frequencia, observacao, ativo) FROM stdin;
\.


--
-- Data for Name: categoria; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categoria (categoria_id, nome_categoria, ativo) FROM stdin;
1	Limpeza	1
2	Vinagre	1
3	Óleo	1
4	Palmito	1
5	Tempero	1
7	Doce	1
8	Geleia	1
9	Fondant	1
10	Linguiças Grossas Suínas	1
11	Linguiças Grossas Bovinas	1
12	Linguiças Finas	1
13	Linguiças Defumadas	1
14	Salsichas	1
15	Fatiados	1
16	Molhos	1
17	Mortadela E Pastrami	1
18	Caixas Compostas / Kits	1
20	Talharim	1
21	Ninho	1
22	Gravata	1
23	Lasanha	1
24	Yakissoba	1
25	Pappardelle	1
27	Macarrão	1
28	Salada	1
26	Lasagne	0
6	Molho	0
19	Massa Linguiça	1
\.


--
-- Data for Name: central_compras; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.central_compras (central_id, cliente_id, nome_central, tipo_entrega, endereco_cd, bairro_cd, cidade_cd, estado_cd, fone, email, contato, observacao, ativo) FROM stdin;
\.


--
-- Data for Name: cliente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cliente (cliente_id, razao_social, nome_fantasia, endereco, bairro, cidade, estado, cnpj, ie, site, instagram, fone, perfil, associacao_id, observacao, ativo, status, email) FROM stdin;
102	\N	Padaria Pamer	R. Fumio Miyazi, 1001	Guilhermina	Praia Grande	SP	\N	\N	\N	padariapamer	13 3591-3539	Padaria	\N	\N	0	Prospecto	\N
103	\N	Padaria Boa Praça	Av. Pres. Castelo Branco, 4222	Aviação	Praia Grande	SP	\N	\N	\N	padaria.boapraca1	(13) 3481-5233	Padaria	\N	Rede	0	Prospecto	\N
104	\N	Padaria Nova Charm	Av. Pres. Costa e Silva, 988	Boqueirão	Praia Grande	SP	\N	\N	\N	novacharm.pg	13 95549-2701	Padaria	\N	\N	0	Prospecto	\N
105	\N	Padaria Canto do Forte	Av. Mal. Mallet, 594	Canto do Forte	Praia Grande	SP	\N	\N	\N	padariacantodoforte	13 3491-4032	Padaria	\N	\N	0	Prospecto	\N
96	carrefour	Carrefour	\N	\N	Praia Grande	SP	\N	\N	\N	\N	\N	Supermercado	\N	\N	0	Inativo	\N
101		Central de Carnes Boi Nobre	Av. Pres. Kennedy, 5420	Vila Tupi	Praia Grande	SP	\N	\N	\N	\N	13 99688-3922	Casa de Carnes	\N	\N	0	Prospecto	\N
94	\N	COOP	\N	\N	Santo André	SP	\N	\N	\N	\N	\N	Supermercado	\N	\N	0	visitado	\N
3	Super Cake Choperia & Restaurante Ltda	Cuca Supermercados	Av. Presidente Kennedy, 13601	Vila Caiçara	Praia Grande	SP	44.658.438/0001-37	558.685.687.114	\N	\N	\N	Supermercado	\N	\N	0	Suspenso	\N
39	\N	Empório Bolshoi	Rua Carvalho De Mendonça, 336	Campo Grande	Santos	SP	\N	\N	\N	\N	(13) 3203-3362/3299-3941	Supermercado	1	\N	0	Prospecto	\N
32	\N	Empório Casa Porto	Av. Dr. Epitácio Pessoa, 651	Ponta da Praia	Santos	SP	\N	\N	\N	@emporio_casaporto	13 99121-5056	Empório	\N	Empório gourmet	0	Prospecto	\N
30	\N	Empório Grãos da Vila	R. Dr Carvalho de Mendonça, 377	Vila Belmiro	Santos	SP	\N	\N	\N	@emporiograosdavila	13 3321-5000	Empório	\N	Loja de produtos naturais	0	Prospecto	\N
29	\N	Empório Haydar	Av. Mal. Floriano Peixoto, 67, loja 35	Gonzaga	Santos	SP	\N	\N	\N	@emporiohaydar	13 99723-9556	Empório	\N	Loja de frutas secas	0	Prospecto	\N
22	\N	Empório Luar do Sertão	R. Expedicionários Vicentinos, 70	Centro	São Vicente	SP	\N	\N	\N	@emporio.luardosertao	13 99102-1482	Empório	\N	Loja de produtos naturais	0	Prospecto	\N
31		Empório Natural Bem Viver	R. Pereira Barreto, 5	Gonzaga	Santos	SP	\N	\N	\N	@emporionaturalbemviver	13 97811-1000	Empório	\N	Loja de produtos naturais	0	Inativo	\N
24	\N	Empório Padaria José Menino	Av Presidente Wilson, 192	José Menino	Santos	SP	\N	\N	\N	@emporiojosemeninosantos	13 3225-6115	Empório	\N	Empório gourmet	0	Prospecto	\N
26	\N	Empório Pinguim	Rua Carvalho de Mendonça, 411	Campo Grande	Santos	SP	\N	\N	\N	emporiopinguim	13 99763-2057	Empório	\N	Empório gourmet	0	Prospecto	\N
23		Empório Porãozinho	R. Dr. Carvalho de Mendonça, 256	Vila Belmiro	Santos	SP	\N	\N	www.emporioporaozinho.com.br	\N	13 98138-5209	Empório	\N	Empório gourmet	0	Prospecto	\N
34	\N	Empório Santista Produtos Naturais	Av. Senador Dantas, 428	Estuário	Santos	SP	\N	\N	\N	@emporiosantista	13 99200-6972	Empório	\N	Loja de produtos naturais	0	Prospecto	\N
27	\N	Empório Santo Antônio	R. Cunha Moreira, 37	Encruzilhada	Santos	SP	\N	\N	\N	@stoantonioemporio	13 97420-6699	Empório	\N	Empório gourmet	0	Prospecto	\N
40	\N	Forte Da Barra	Av. Dos Bancarios, 85	Ponta Da Praia	Santos	SP	\N	\N	\N	\N	(13) 3269-4080	Supermercado	1	\N	0	Prospecto	\N
44	\N	Supermercado Barros	Praça José Oliveira Lopes, 86	Jd. Castelo	Santos	SP	\N	\N	\N	\N	(13)3203-3362/3299-3941	Supermercado	1	\N	0	Prospecto	\N
45	\N	Supermercado Bonsucesso	Av. Nossa Senhora Da Lapa, 1400	Vila Nova	Cubatão	SP	\N	\N	\N	\N	(13) 3361-1889	Supermercado	1	\N	0	Prospecto	\N
46	\N	Supermercado Casa Luanda	Av. Antônio Emmerick, 335/373	Vila Cascatinha	São Vicente	SP	\N	\N	\N	\N	(13) 3569-1900	Supermercado	1	\N	0	Prospecto	\N
47	\N	Supermercado D’pinho	Rua Onze De Junho, 180	Boa Vista	São Vicente	SP	\N	\N	\N	\N	(13) 3469- 3554	Supermercado	1	\N	0	Prospecto	\N
48	\N	Supermercado Figueroa	Av. Marechal Mallet, 532	Canto Do Forte	Praia Grande	SP	\N	\N	\N	\N	(13) 3491-2849/3473-5816	Supermercado	1	\N	0	Prospecto	\N
49	\N	Supermercado Forte Itapema	Av. Santos Dumont, 474/494	Vicente De Carvalho	Guarujá	SP	\N	\N	\N	\N	(13) 3269-4080	Supermercado	1	\N	0	Prospecto	\N
50	\N	Supermercado Fransue	R. Domingos José Martins, 170	Vl. São Jorge	Santos	SP	\N	\N	\N	\N	(13) 3209-8110	Supermercado	1	\N	0	Prospecto	\N
51	\N	Supermercado Jóia	Av. Adhemar De Barros, 3255	Vila Ligya	Guarujá	SP	\N	\N	\N	\N	(13)3269-4060	Supermercado	1	\N	0	Prospecto	\N
52	\N	Supermercado Litoral	Av. Presidente Wilson, 187/188	José Menino	Santos	SP	\N	\N	\N	\N	(13)3225-9200	Supermercado	1	\N	0	Prospecto	\N
53	\N	Supermercado Martinho Rodrigues	R. Dois, 947	Morro Do S. Bento	Santos	SP	\N	\N	\N	\N	(13)3258-6407	Supermercado	1	\N	0	Prospecto	\N
54	\N	Supermercado Saito	Rua João Mariano, 193 Loja 4	Centro	Itanhaém	SP	\N	\N	\N	\N	(13) 3421-4448/4316	Supermercado	1	\N	0	Prospecto	\N
55	\N	Supermercado Talismã	R. Monte Belvedere, 610	Vila Margarida	São Vicente	SP	\N	\N	\N	\N	(13) 3465-5454	Supermercado	1	\N	0	Prospecto	\N
56	\N	Supermercado Varandas	Av. Sen. Pinheiro Machado, 643	Campo Grande	Santos	SP	\N	\N	\N	\N	(13) 2102-5153/5159	Supermercado	1	\N	0	Prospecto	\N
106	\N	Padaria Santa Terezinha	Av. Pres. Kennedy, 5799	Vila Tupi	Praia Grande	SP	\N	\N	\N	santaterezinhapadaria	(13) 99680-6489	Padaria	\N	\N	0	Prospecto	\N
108	\N	Panificadora e Confeitaria 2 Corações	Av. João André Quintale, 695	Maracanã	Praia Grande	SP	\N	\N	\N	padariadoiscoracoes	(13) 99798-4140	Padaria	\N	\N	0	Prospecto	\N
109	\N	Nova Balneária - Padaria & Restaurante	R. Caribas	Vila Tupi	Praia Grande	SP	\N	\N	\N	novabalnearia	(13) 99606-9898	Padaria	\N	\N	0	Prospecto	\N
110	\N	Padaria Balneária	Av. Min. Marcos Freire, 4948	Vila Antartica	Praia Grande	SP	\N	\N	\N	\N	(13) 3596-6376	Padaria	\N	\N	0	Prospecto	\N
111	\N	Empório Dom José	R. Conselheiro Lafayette, 3	Embaré	Santos	SP	\N	\N	\N	domjoseemporio	13 99601-9021	Padaria	\N	\N	0	Prospecto	\N
113	\N	Panificadora Washington Luiz	Av. Washington Luís, 449	Boqueirão	Santos	SP	\N	\N	\N	\N	(13) 3232-4067	Padaria	\N	\N	0	Prospecto	\N
114	\N	Padaria Bella Villa	R. Goiás, 44	Boqueirão	Santos	SP	\N	\N	\N	bellavillasantos	(13) 3221-3737	Padaria	\N	\N	0	Prospecto	\N
115	\N	Empório Nova Era	Rua Dr. Cunha Moreira, 210	Encruzilhada	Santos	SP	\N	\N	\N	novaeraemporio	13 97405-0358	Padaria	\N	\N	0	Prospecto	\N
116	\N	Panificadora Nova Itararé	Av. Presidente Wilson, 88/96	Itararé	São Vicente	SP	\N	\N	\N	padarianovaitarare	(13) 99661-0033	Padaria	\N	\N	0	Prospecto	\N
117	\N	Padaria & Confeitaria Bella São Vicente	R. Marquês de São Vicente, 91	Centro	São Vicente	SP	\N	\N	\N	bellasaovicente	(13) 99633-6621	Padaria	\N	\N	0	Prospecto	\N
107		Padaria Peg Pão do Forte	Av. Mal. Mallet, 422	Canto do Forte	Praia Grande	SP	\N	\N	https://padariapegpao.com.br/	pegpaodoforteoficial	13 97600-1949	Padaria	\N	\N	0	Prospecto	\N
61	\N	Bacana Burguer	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/bacana.burguer/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
118		Rede Padaria Peg Pão	\N	\N	SP	SP	\N	\N	\N	pegpaooficial	\N	Padaria	\N	\N	0	Prospecto	\N
62	\N	Barba Burger	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/barbaburger013/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
59		Bella Caiçara Padaria e Pizzaria	Av. Pres. Kennedy, 12707	Vila Caiçara	Praia Grande	SP	\N	\N	\N	@bellacaicarapadaria	(13) 99678-7221	Padaria	\N	\N	0	Prospecto	\N
63	\N	BROW Hamburgueria	\N	\N	\N	SP	\N	\N	https://www.facebook.com/browhamburgueria013/	https://www.instagram.com/browrangoeburger_/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
64	\N	Burger Company Santos	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/burgercompanysantos/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
65	\N	Burgman Santos	\N	\N	\N	SP	\N	\N	https://www.burgman.com.br	https://www.instagram.com/quiosquesburgmansantos/?hl=pt	\N	Hamburgueria	\N	\N	0	Prospecto	\N
66	\N	C3 Burguer	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/c3.burguer/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
67	\N	Cabalera Burguer	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/cabaleraburguer/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
28	\N	Cantin Empório Mineiro	Av. Pres. Wilson, 26, Loja 30E	Gonzaga	Santos	SP	\N	\N	\N	@cantinemporiomineiro	13 98212-3123	Empório	\N	Empório gourmet	0	Prospecto	\N
68	\N	Casa Cinza	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/cinza.company	\N	Hamburgueria	\N	\N	0	Prospecto	\N
69		Casa de Carnes Boi do Litoral	\N	\N	Praia Grande	SP	\N	\N	\N	https://www.instagram.com/boi.do.litoral/	\N	Casa de Carnes	\N	\N	0	Prospecto	\N
21		Cruzeiro Carnes	\N	\N	Praia Grande	SP	\N	\N	\N	\N	\N	Casa de Carnes	\N	\N	0	Prospecto	\N
1	Cristina Junqueira Franco Menezes Eireli	Diet House	R. Plinio Salgado, 1017	Jardim Maracanã	São José do Rio Preto	SP	08.848.560/0001-02	647503477111	https://diethouse.com.br/	https://www.instagram.com/diethousebr/	\N	Outro	\N	\N	1	Ativo	\N
58		Dona Manuela Padaria	Dona Manuela Padaria	Canto do Forte	Praia Grande	SP	\N	\N	\N	@donamanuelapadaria	(13) 3473-5992	Padaria	\N	\N	0	Prospecto	\N
33	\N	Empório Casa dos 7 grãos	Av. Mal. Floriano Peixoto, 98	Gonzaga	Santos	SP	\N	\N	\N	@emporiocasados7graos	13 98132-0137	Empório	\N	Loja de produtos naturais	0	Prospecto	\N
16		Empório Lapilli	\N	\N	Praia Grande	SP	\N	\N	\N	\N	\N	Empório	\N	\N	0	Prospecto	\N
57	\N	Supermercado Vip	Av. Afonso Pena, 336	Embaré	Santos	SP	\N	\N	\N	\N	(13) 3236-5930	Supermercado	1	\N	0	Prospecto	\N
2		Supermercados Fácil	\N	\N	Praia Grande	SP	\N	\N	\N	\N	\N	Supermercado	\N	\N	0	Visitado	\N
14	\N	Supermercados Krill	\N	\N	Praia Grande	SP	\N	\N	\N	\N	\N	Supermercado	\N	\N	0	Prospecto	\N
12	\N	Supermercados Pompéia	\N	\N	Praia Grande	SP	\N	\N	\N	\N	\N	Supermercado	\N	\N	0	Prospecto	\N
13		Supermercados Prático			Mongaguá	SP					\N	Supermercado	\N		0	Prospecto	\N
90	\N	Uncle Black Burger	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/uncleblackburger/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
91	\N	Yank Burgers & Beers	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/yankburger/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
119		Gualchi Padaria e Conveniência	R. Honduras, 195	Guilhermina	Praia Grande	SP	\N	\N	\N	gualchipadaria	55 13 98225-4073	Padaria	\N	\N	0	Prospecto	\N
60	\N	Amorim Burger Mongagua	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/amorimburguer/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
37	\N	Empório Villa Borghese	R. Azevedo Sodré, 144	Gonzaga	Santos	SP	\N	\N	\N	@villaborgheseemporio	13 3226-9501	Empório	\N	Empório gourmet	0	Prospecto	\N
25	\N	Empório Villa Natural	R. Goytacazes, 20	Gonzaga	Santos	SP	\N	\N	\N	@emporiovillanatural	13 99751-1990	Empório	\N	Loja de alimentos orgânicos	0	Prospecto	\N
93		Grupo Pão de Açúcar - GPA	\N	Jardim Paulista	São Paulo	SP	\N	\N	\N	\N	\N	Supermercado	\N	\N	0	Prospecto	\N
97	Hortifruti Akira	Hortifruti Akira	Av. Irmãos Adorno,170	Sítio do Campo	Praia Grande	SP	\N	\N	\N	https://www.instagram.com/hortifruti_akira/	13 97409-1768	Hortifruti	\N	\N	0	Visitado	\N
100	Supermercado Los Hermanos Ltda	Los Hermanos (Ge Pires)	Av. Yervant kKissajikian, 1666	Vila Joaniza	São Paulo	SP	60.354.596/0001-50	\N	\N	\N	11 99932-1896	Supermercado	\N	\N	1	Ativo	\N
17	\N	MDV Supermercados	\N	\N	Praia Grande	SP	\N	\N	\N	\N	\N	Supermercado	\N	\N	0	Prospecto	\N
15	\N	MegaStock Atacado	\N	\N	Praia Grande	SP	\N	\N	\N	\N	\N	Atacadista	\N	\N	0	Prospecto	\N
20	\N	Mercadão Atacadista	\N	\N	Praia Grande	SP	\N	\N	\N	\N	\N	Atacadista	\N	\N	0	Prospecto	\N
11	\N	Nova Esmeralda	\N	\N	Praia Grande	SP	\N	\N	\N	\N	\N	Supermercado	\N	\N	0	Prospecto	\N
18	\N	PAM Sacolão e Mercado	\N	\N	Praia Grande	SP	\N	\N	\N	\N	\N	Supermercado	\N	\N	0	Prospecto	\N
36	\N	Paulistana Empório Cerealista	R. Euclides da Cunha, 63	Gonzaga	Santos	SP	\N	\N	\N	@paulistanaemporio	13 98881-3922	Empório	\N	Empório gourmet	0	Prospecto	\N
19	\N	Proplastik	\N	\N	Praia Grande	SP	\N	\N	\N	\N	\N	Outro	\N	\N	0	Prospecto	\N
10	\N	Raizeiro	\N	\N	Praia Grande	SP	\N	\N	\N	\N	\N	Empório	\N	\N	0	Prospecto	\N
41	\N	Supermercado Aldeias	Av. Marechal Floriano Peixoto, 92	Gonzaga	Santos	SP	\N	\N	\N	\N	(13) 3289-1160	Supermercado	1	\N	0	Prospecto	\N
42	\N	Supermercado Ao Fiel Barateiro	R. Quinze De Novembro, 537 / R. João Ramalho, 950	Centro	São Vicente	SP	\N	\N	\N	\N	(13) 3468-0614/1781	Supermercado	1	\N	0	Prospecto	\N
43	\N	Supermercado Baba	Av. Xxiv De Dezembro, 560	Estação	Peruíbe	SP	\N	\N	\N	\N	(13) 3455-2004	Supermercado	1	\N	0	Prospecto	\N
70		Casa de Carnes Boi Nobre	\N	\N		SP	\N	\N	contato@carnesboinobre.com.br	https://www.instagram.com/carnesboinobre/	13 97405-6394	Casa de Carnes	\N	\N	0	Prospecto	contato@carnesboinobre.com.br
71		Casa de Carnes Vila Rica	\N	\N		SP	\N	\N	https://www.carnesvilarica.com.br	https://www.instagram.com/vilaricasantos/	(13) 99649-2340	Casa de Carnes	\N	\N	0	Prospecto	contato@carnesvilarica.com.br
72	\N	Cola na Base Burger	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/colanabase/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
73	\N	Dags Burger	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/dagsfc/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
98	KB Supermercado Ltda	DaVila	Av. Miami, 689	Vila Caiçara	Praia Grande	SP	62.837.293/0001-13	\N	\N	https://www.instagram.com/supermercado_kb/	\N	Hortifruti	\N	\N	0	Prospecto	\N
74	\N	Dunk Duni Hamburgueria	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/dunkduni/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
38	\N	Empório Rodrigues	Av. Mal. Humberto de Alencar Castelo Branco, 217	Cidade Náutica	São Vicente	SP	\N	\N	\N	@emporiorodrigues466	(13) 3043-6006	Padaria	\N	Padaria	0	Prospecto	\N
35	\N	Empório Santa Helena	R. Silva Jardim, 299	Macuco	Santos	SP	\N	\N	\N	@santahelenaemporio	(13) 3232-3051	Padaria	\N	Padaria	0	Prospecto	\N
75	\N	Fucking Burger	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/fuckingburgeroficial/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
76	\N	Gold Burger	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/goldburgerbr/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
77	\N	Goma Barbecue Hamburgueria	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/gomabbq/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
95		Good Times Burger	Av. Mal. Mallet, 1619	Canto do Forte	Praia Grande	SP	\N	\N	\N	https://www.instagram.com/goodtimesburger/reels/	(13) 99649-1619	Hamburgueria	\N	\N	0	Prospecto	\N
78	\N	Hamburgueria do Fusca	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/hamburgueriadofusca/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
79	\N	Hangar 55	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/hangar.55/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
80	\N	Heisenburg Burger	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/heisenburgbr/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
81	\N	Herois Burger	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/heroisburgersantos/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
82	\N	Kasa Burguer	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/kasaburguer_santos/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
83	\N	Magnatas	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/magnatasburguer013/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
84	\N	Mangue Pub & Burger	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/manguesteakpub/?hl=pt-br	\N	Hamburgueria	\N	\N	0	Prospecto	\N
85	\N	O Armazem Burger & Shake	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/oarmazemlanchesbar/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
86	\N	Original Co. Burger & Steak	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/originalcosantos	\N	Hamburgueria	\N	\N	0	Prospecto	\N
87	\N	Quero Burgers	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/queroburgers/?hl=pt-br	\N	Hamburgueria	\N	\N	0	Prospecto	\N
92		Rede Litoral Supermercados	R. Paulo Horneaux de Moura, 381	Esplanada dos Barreiros	São Vicente	SP	\N	\N	\N	\N	(13) 3465-4200	Supermercado	1	\N	0	Prospecto	\N
88	\N	Save Point Santos	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/savepointsantos/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
89	\N	Stand Ipa Burger Bar	\N	\N	\N	SP	\N	\N	\N	https://www.instagram.com/standipa/	\N	Hamburgueria	\N	\N	0	Prospecto	\N
\.


--
-- Data for Name: cliente_fornecedor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cliente_fornecedor (cliente_fornecedor_id, cliente_id, fornecedor_id, tabela_preco_id, prazo_pagamento, codigo_cliente, observacao, ativo) FROM stdin;
1	1	1	2	\N	\N		1
2	3	1	2	\N	\N	\N	1
3	100	1	20	\N	\N	\N	1
\.


--
-- Data for Name: comissao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.comissao (comissao_id, fornecedor_id, percentual, observacao, ativo) FROM stdin;
2	2	5	\N	1
8	3	6	\N	1
1	1	5	\N	1
3	4	5	\N	1
\.


--
-- Data for Name: comissao_pagamento; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.comissao_pagamento (pagamento_id, pedido_id, data_pagamento, valor_previsto, valor_pago, status_pagamento, observacao) FROM stdin;
\.


--
-- Data for Name: concorrente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.concorrente (concorrente_id, fornecedor_id, marca_concorrente, origem_cidade, importada, importado_por, observacao, ativo) FROM stdin;
80	3	Prieto	Cajamar/SP	0	\N	\N	1
81	3	Kassel	\N	0	\N	\N	1
1	1	Castelo	Jundiaí/SP	0	\N	Marca Líder	1
2	\N	Vitalia	\N	0	\N	\N	1
3	1	Vitalia	Jundiaí/SP	0	\N	\N	1
4	1	Neval	Valinhos/SP	0	\N	\N	1
5	1	Palladio	Várzea Paulista/SP	0	\N	Fabricados pela empresa Vinagre Toscano	1
6	1	Almaromi	Indaiatuba/SP	0	\N	\N	1
7	1	Fortaleza	Jundiaí/SP	0	\N	Pertence à Castelo	1
8	1	Kodilar	São José do Rio Preto/SP	0	\N	\N	1
9	1	Palhinha	Jundiaí/SP	0	\N	\N	1
10	1	Puro Pomar	\N	0	\N	\N	1
11	1	Rosani	Garibaldi/RS	0	\N	\N	1
13	1	São Francisco	Caxias do Sul/RS	0	\N	\N	1
14	1	São Roque	Caxias do Sul/RS	0	\N	\N	1
15	1	Toscano	Várzea Paulista/SP	0	\N	\N	1
17	1	Maratá	Maruim/SE	0	\N	\N	1
18	1	Dai Alimentos	São Paulo/SP	0	\N	\N	1
19	1	Marca Própria	\N	0	\N	\N	1
20	1	Viccino	Indaiatuba/SP	0	\N	\N	1
21	1	Cepêra	\N	0	\N	\N	1
22	2	Bom Princípio	\N	0	\N	\N	1
23	2	Reserva de Minas	\N	0	\N	\N	1
24	2	Queensberry	\N	0	\N	\N	1
25	2	Vitao	\N	0	\N	\N	1
26	2	Amore	\N	0	\N	\N	1
27	2	Colina Verde	\N	0	\N	\N	1
28	1	La Pastina	\N	0	\N	\N	1
30	1	Ponti	Itália	1	Aurora	\N	1
32	1	Colavita	Itália	1	Colavita Brasil	\N	1
33	1	Beaufor	França	1	La Pastina	\N	1
34	1	Mastroiani	Itália	1	La Violetera	\N	1
35	3	Swift	\N	0	\N	\N	1
36	3	Seara	\N	0	\N	\N	1
37	3	Rezende	\N	0	\N	\N	1
38	3	Seara Gourmet	\N	0	\N	\N	1
39	3	Ceratti	\N	0	\N	\N	1
40	3	Sadia	\N	0	\N	\N	1
41	3	Berna	\N	0	\N	\N	1
42	3	Hans	\N	0	\N	\N	1
43	3	F.A. Defumados	\N	0	\N	\N	1
57	4	Renata	\N	0	\N	\N	1
58	4	Petybon	\N	0	\N	\N	1
59	4	Dona Benta	\N	0	\N	\N	1
60	4	Romanha	\N	0	\N	\N	1
61	4	Nissin	\N	0	\N	\N	1
62	4	Kirin	\N	0	\N	\N	1
63	4	Barilla	\N	0	\N	\N	1
64	4	Adria	\N	0	\N	\N	1
65	4	San Vito Speciale	\N	0	\N	\N	1
66	4	Sacciali	\N	0	\N	\N	1
67	4	Qualitá	\N	0	\N	\N	1
68	4	Floriani	\N	0	\N	\N	1
69	4	Native	\N	0	\N	\N	1
70	2	Linea	\N	0	\N	\N	1
71	2	Flormel	\N	0	\N	\N	1
72	1	KiSabor	\N	0	\N	\N	1
73	1	Knorr	\N	0	\N	\N	1
74	1	Kenko	\N	0	\N	\N	1
77	4	Galla	\N	0	\N	\N	1
78	4	Orquídea	\N	0	\N	\N	1
\.


--
-- Data for Name: configuracao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.configuracao (config_id, modo_operacao, empresa_nome, data_instalacao, versao_sistema, anthropic_api_key, senha_exclusao) FROM stdin;
1	REPRESENTANTE	Azevedo e Filhos Representações	2026-03-27	1.0	\N	EXCLUIR123
\.


--
-- Data for Name: contato_cliente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contato_cliente (contato_cliente_id, cliente_id, nome_contato, departamento, fone, whatsapp, email, observacao, ativo) FROM stdin;
1	3	Carlos	Compras	13 99629-1692	\N	balcao.caicara@cucasupermercados.com.br'		1
2	10	Michele	Compradora	\N	13 99181-2679	\N	\N	1
3	58	Ed Carlo	Comprador	\N	13 99712-6471	\N	\N	1
4	93	Tatiana Gomes	Compradora / Salsicharia	\N	11 94235-4598	\N	\N	1
5	59	Luiz	Compras	\N	13 99646-1150	\N	\N	1
6	94	Renato de Oliveira Antunes	comprador	\N	11 91774-6209	renato.antunes@coopsp.coop.br	\N	1
7	97	Akira	Proprietário/Comprador	\N	13 97409-1768	\N	\N	1
8	97	Akira	Proprietário/Comprador	\N	13 97409-1768	\N	\N	1
9	98	Alisson	Comprador	\N	13 97424-4080	\N	\N	1
10	94	Daniela Mendonça	Gestora Marcas Próprias	\N	\N	daniela.mendonca@coopsp.coop.br	\N	1
11	94	Daniela Mendonça	Gestora Marcas Próprias	\N	\N	daniela.mendonca@coopsp.coop.br	\N	0
12	94	Daniela Mendonça	Gestora de Marcas Próprias	\N	\N	daniela.mendonca@coopsp.coop.br	\N	0
13	94	Daniela Mendonça	Gestora de Marcas Próprias	\N	\N	daniela.mendonca@coopsp.coop.br	\N	0
14	94	Daniela Mendonça	Gestora Marcas Próprias	\N	\N	daniela.mendonca@coopsp.coop.br	\N	0
15	21	Loja Boqueirão	\N	13 3591-5707	13 99670-0300	contato@cruzeirocarnes.com.br	\N	1
16	14	Moisés	comprador	\N	\N	moises@redekrill.com	\N	1
17	93	Alcides Borges	Comprador / Mercearia Complementar II	\N	(11) 97273-7461	alcides.neto@gpabr.com	\N	1
18	29	Ana Paula	Irmã da compradora	\N	13 99723-9556	\N	\N	1
19	34	Renato	Comprador	\N	\N	compras@emporiosantista.com.br	\N	1
20	28	Fátima Belani	\N	Compradora	13 98212-3123	comercial.cantindiminas@gmail.com	\N	1
\.


--
-- Data for Name: contato_fornecedor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contato_fornecedor (contato_fornecedor_id, fornecedor_id, nome_contato, departamento, fone, email, observacao, ativo) FROM stdin;
\.


--
-- Data for Name: contato_fornecedor_topico; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contato_fornecedor_topico (cft_id, contato_id, fornecedor_id, status, tipo_topico, data_followup, prioridade, observacao, ativo) FROM stdin;
\.


--
-- Data for Name: contato_interacao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contato_interacao (interacao_id, contato_id, data_interacao, via_comunicacao, contato_pessoa, descricao, ativo, contato_cliente_id, resultado, data_followup) FROM stdin;
1	1	2026-04-13	WhatsApp	Ed Carlo	Boa tarde, Ed Carlos! Tudo bem?\n\nA Padaria Dona Manuela me passou seu contato e fico feliz em poder falar diretamente com você. \n\nSou o *Fernando Azevedo Jr*, da *Azevedo e Filhos Representações*, e represento na Baixada Santista dois fornecedores que acredito terem muito a agregar ao mix da padaria:\n\n🍓 *Diet House* — empresa familiar com 30 anos de estrada, produz doces, compotas e fondants diet e light com sabores que surpreendem na primeira colherada.\n\n🥩 *Charcutaria Specialli* — 20 anos entregando qualidade, técnica e exclusividade em linguiças artesanais, salsichas, salame, copa, pastrami e mortadela.\n\nGostaria muito de agendar uma visita para me apresentar pessoalmente e mostrar o trabalho desses fornecedores — se possível, levar algumas amostras para sua avaliação.\n\nQual seria o melhor dia e horário para eu passar?\n\nDesde já agradeço a atenção! 🤝\n\n*Fernando Azevedo Jr* — Azevedo e Filhos Representações\n11 98833-4747	1	\N	\N	2026-04-16
2	2	2026-04-13	WhatsApp	Michele	Boa tarde, Michele! Tudo bem?\n\nSei como o varejo tem seu próprio ritmo — meu pai trabalhou a vida toda no Grupo Pão de Açúcar e nós, os filhos, crescemos entendendo bem essa rotina. Por isso não quero que se sinta pressionada de forma alguma.\n\nSó retorno ao meu contato do dia 07 justamente porque acredito muito na sinergia da *Diet House* com o perfil do Raizeiro, e gostaria de lhe pedir que *me permita entregar, aos seus cuidados, algumas amostras da linha na loja da Guilhermina.* \n\nÉ uma empresa familiar que acompanho há décadas, com produtos diet de verdade — doces, compotas e fondants sem adição de açúcar, com ótima aceitação no varejo.\n\nFico no aguardo de sua autorização e desde já grato,\n\n*Fernando Azevedo Jr* — Azevedo e Filhos Representações\n11 98833-4747	1	\N	\N	2026-04-21
3	3	2026-04-13	E-mail	Recepção	De: fernandojr@azevedoefilhos.com.br <fernandojr@azevedoefilhos.com.br> \nEnviada em: segunda-feira, 13 de abril de 2026 14:42\nPara: 'recepcao@redelitoral.com' <recepcao@redelitoral.com>\nAssunto: Contato Comercial | Belmont Alimentos, Diet House e Charcutaria Specialli\n\nBoa tarde,\n\nMeu nome é Fernando Azevedo Jr e represento na Baixada Santista três fornecedores que acredito terem forte sinergia com o perfil e o mix da Rede Litoral:\n\n• Belmont Alimentos — mais de 50 anos de tradição, com destaque para a linha de vinagres de excelente qualidade e giro comprovado no varejo.\n\n• Diet House — empresa familiar com 30 anos de estrada, especializada em doces, compotas e fondants diet e light, com crescente demanda dos consumidores que buscam opções sem adição de açúcar.\n\n• Charcutaria Specialli — 20 anos entregando qualidade, técnica e exclusividade em linguiças artesanais, salsichas, salame, copa, pastrami e mortadela.\n\nUma única reunião pode abrir três oportunidades de negócio para a rede — e estou à disposição para apresentar cada uma delas no formato e momento que melhor se encaixar na rotina de vocês.\n\nGostaria de solicitar o contato do responsável pela área de compras ou a orientação sobre a forma correta de atendimento comercial da rede.\n\nAgradeço a atenção e fico no aguardo de um retorno.\n\nAtenciosamente,\n\nFernando Azevedo Jr . 11 98833-4747	1	\N	Caso não haja retorno, visitar pessoalmente a central em São Vicente.	2026-04-21
4	4	2026-04-13	WhatsApp	Tatiana Gomes	Boa tarde, Tatiana! Tudo bem?\n\nMeu nome é *Fernando Azevedo Jr*, da *Azevedo e Filhos Representações*. Me permita uma breve apresentação antes do motivo do contato.\n\nSou filho do Fernando Azevedo, que dedicou *32 anos de carreira ao Grupo Pão de Açúcar*, aposentando-se na área de Marcas Próprias. Cresci dentro dessa cultura e hoje, dando continuidade ao trabalho da família, atuo como representante comercial com foco em grandes redes de varejo.\n\nO motivo do meu contato, Tatiana, é apresentar uma oportunidade que acredito ter muito a ver com a sua categoria: a *Charcutaria Specialli*.\n\nUma charcutaria artesanal com 20 anos de história, que une qualidade, técnica e sabor. E o primeiro produto que gostaria de apresentar ao GPA é a *Mortadela Peça de 3,1 kg* — produzida 100% com carne suína, textura macia, aroma marcante e toque artesanal. Um produto com enorme potencial para operação de *fatiados no balcão*.\n\nGostaria muito de agendar uma visita presencial para me apresentar e apresentar a Specialli com mais detalhes.\n\nQual seria a melhor forma e o melhor momento para conversarmos?\n\nFernando Azevedo Jr — Azevedo e Filhos Representações\n📱 11 98833-4747\n📧 fernandojr@azevedoefilhos.com.br	1	\N	Tatiana respondeu em 14/04/2026: Ola \nBom dia,\nTudo bem!\nAcredito que na próxima semana, assim que surgir agenda te informo.	2026-04-21
5	5	2026-04-14	WhatsApp	Luiz	Boa tarde, Luiz! Tudo bem?\n\nO Felipe me passou seu contato hoje quando estive na Bella Caiçara. Sou o *Fernando Azevedo Jr*, moro aqui no Caiçara e sou cliente da padaria — e agora tambem venho bater à porta como representante comercial. 😊\n\nRepresento na Baixada Santista três fornecedores que acredito terem muito a agregar ao mix da Bella Caiçara:\n\n🥩 *Charcutaria Specialli* — 20 anos de qualidade, técnica e exclusividade em linguiças artesanais, salsichas, salame, copa, pastrami e mortadela.\n\n🍓 *Diet House* — empresa familiar com 30 anos, especializada em doces, compotas e fondants diet e light com sabores que surpreendem na primeira colherada.\n\n🥫 *Belmont Alimentos* — mais de 50 anos de tradição, com destaque para a linha de vinagres de excelente qualidade e giro comprovado no varejo.\n\nGostaria muito de saber se teria um espaço na sua agenda para que eu passe pessoalmente, me apresente e mostre o trabalho desses fornecedores.\n\nFico no aguardo e desde já grato,\n\n*Fernando Azevedo Jr* — Azevedo e Filhos Representações\n📱 11 98833-4747	0	\N	\N	2026-04-22
6	6	2026-04-15	Visita presencial	Renato de Oliveira Antunes	Ambrosio, bom dia!\n\nVenho compartilhar uma excelente notícia: ontem concluí uma reunião muito promissora com o comprador Renato de Oliveira Antunes, da Coop — rede líder no ABC paulista com 32 lojas —, e saio dela com uma janela concreta de oportunidade para a Belmont.\n\nÉ importante esclarecer desde já o contexto: a Coop passou por uma reformulação estratégica em sua política comercial e adota hoje um modelo enxuto de categorias — apenas uma marca para o segmento líder, uma para o primeiro preço e uma para o premium. Por isso, neste momento, não há espaço para entrada de uma nova marca de vinagre em linha. No entanto, abre-se uma oportunidade distinta e muito relevante: a Coop encerrou recentemente o contrato de fornecimento de vinagres marca própria com a Toscano, e o comprador demonstrou abertura real para avaliar a Belmont como novo fornecedor neste segmento.\n\nO mix discutido e bem recebido — inclusive com entrega de amostras — foi:\n\n• Vinagre de Maçã 750ml\n• Vinagre de Álcool 750ml\n• Vinagre de Álcool Colorido 750ml\n• Vinagre de Vinho Tinto 380ml\n• Vinagre de Vinho Branco 380ml\n• Vinagre Balsâmico 380ml\n\nAs condições comerciais praticadas pela Coop são: entrega no CD (com distribuição para 32 lojas via cross-docking), desconto contratual de 2% sobre logística e prazo de pagamento padrão de 90 dias. Um ponto importante: o comprador foi transparente ao informar que a Coop não trabalha com prazo inferior a 70 dias — o que nos abre uma margem de negociação. Caso a Belmont consiga operar com um prazo entre 70 e 90 dias, isso pode ser um elemento valioso para compor uma proposta de preço mais competitiva e diferenciada.\n\nAlém da tabela de preços, o comprador solicitou que sinalizemos as quantidades mínimas de pedido para o fornecimento de marca própria por SKU. Esta informação será fundamental para que a Coop avalie a viabilidade operacional do fornecimento, por isso peço que nos indiquem esses volumes junto à proposta.\n\nO Renato solicitou celeridade no retorno e a Coop já iniciou internamente o processo de validação da Belmont como fornecedora de marca própria. A janela é real, mas tem prazo.\n\nSabendo da história, da qualidade e da capacidade produtiva da Belmont, estou certo de que temos condições de surpreender positivamente. Conto com a sua prioridade no envio da tabela e das quantidades mínimas para que possamos responder com a agilidade que esta oportunidade exige.\n\nFico à disposição para alinhar qualquer detalhe.\n\nGrato pela parceria e confiança!\n\nFernando Azevedo Jr . 11 98833-4747\n------------------------------------------------------\n[08:32, 17/04/2026] Ambrósio Galvão Belmont: Bom dia Fernando tudo bem tomei conhecimento da ata coop vou montar a proposta. Temos possibilidades de fazer a marca própria deles sim. Precisamos saber se eles estão com a Amicci ou se irão negociar direto conosco.\n[08:33, 17/04/2026] Ambrósio Galvão Belmont: Amicci e uma multinacional direcionada a gerenciar marcas próprias trabalha interagindo com redes e fornecedores\n[08:34, 17/04/2026] Ambrósio Galvão Belmont: Nesse trabalho eles exigem 3% de comissão\n[08:36, 17/04/2026] Ambrósio Galvão Belmont: Se for negociação direta será muito mais produtivo para nós e menor riscos de sermos substituídos por outros fornecedores uma vez que eles procuram sempre maior benefício aos clientes não se posicionando de forma fiel a fornecedores.\n---------------------------------------------------\n[10:58, 17/04/2026] Fernando Azevedo Jr: Bom dia, Renato! Tudo bem?\n\nPreciso confirmar um ponto importante com você antes de avançarmos com a proposta da Belmont para a Coop.\n\nVocê mencionou na reunião que havia uma consultoria envolvida nos projetos de marca própria, mas que a Coop optou por não mais manter este serviço. Correto?\n\nO motivo da pergunta é prático: se não há consultoria intermediando, a negociação será direta entre Coop e Belmont — o que elimina custos adicionais da proposta e nos permite chegar a um preço mais competitivo e vantajoso para a rede.\n\nPoderia confirmar esse ponto para que eu possa orientar corretamente a Belmont na elaboração da proposta?\n\nAgradeço e fico no aguardo! 🤝\n\nFernando Azevedo Jr — Azevedo e Filhos Representações\n📱 11 98833-4747\n[15:55, 17/04/2026] Fernando Azevedo Jr: Renato, boa tarde. Permaneço no aguardo da informação para solicitar celeridade à Belmont. Obrigado.\n[17:10, 17/04/2026] Renato Antunes COOP: Boa tarde\n[17:10, 17/04/2026] Renato Antunes COOP: Isso mesmo\n[17:10, 17/04/2026] Renato Antunes COOP: Negociação direta\n-----------------------------------------------------------------------	1	\N	Aguardar envio proposta de preços e volume Belmont para enviar para a COOP.	2026-04-23
8	8	2026-04-19	WhatsApp	Luiz	\N	0	5	\N	\N
9	8	2026-04-14	WhatsApp	Luiz	Boa tarde, Luiz! Tudo bem?\n\nO Felipe me passou seu contato hoje quando estive na Bella Caiçara. Sou o *Fernando Azevedo Jr*, moro aqui no Caiçara e sou cliente da padaria — e agora tambem venho bater à porta como representante comercial. 😊\n\nRepresento na Baixada Santista três fornecedores que acredito terem muito a agregar ao mix da Bella Caiçara:\n\n🥩 *Charcutaria Specialli* — 20 anos de qualidade, técnica e exclusividade em linguiças artesanais, salsichas, salame, copa, pastrami e mortadela.\n\n🍓 *Diet House* — empresa familiar com 30 anos, especializada em doces, compotas e fondants diet e light com sabores que surpreendem na primeira colherada.\n\n🥫 *Belmont Alimentos* — mais de 50 anos de tradição, com destaque para a linha de vinagres de excelente qualidade e giro comprovado no varejo.\n\nGostaria muito de saber se teria um espaço na sua agenda para que eu passe pessoalmente, me apresente e mostre o trabalho desses fornecedores.\n\nFico no aguardo e desde já grato,\n\n*Fernando Azevedo Jr* — Azevedo e Filhos Representações\n📱 11 98833-4747	1	5	\N	2026-04-23
7	7	2026-04-22	WhatsApp	\N	\N	0	\N	\N	\N
45	4	2026-05-18	WhatsApp	Tatiana Gomes	Boa tarde, Tatiana! Tudo bem?\n\nPassando apenas para reforçar que permanecerei atento aguardando a confirmação da data conforme sua disponibilidade nesta semana.\n\nFico à disposição e agradeço novamente pela atenção.\n\nFernando Azevedo Jr	1	4	\N	\N
10	4	2026-04-22	WhatsApp	Tatiana Gomes	Bom dia, Tatiana! Tudo bem?\n\nPermaneço atento ao agendamento e à disposição assim que surgir um espaço na sua agenda. 😊\n\nEnquanto isso, gostaria de compartilhar um diferencial da *Mortadela Specialli* que acredito vai despertar ainda mais seu interesse:\n\né produzida com *100% pernil suíno*, *zero CMS*, *sem adição de proteína vegetal* e com *baixo teor de gordura* — resultando em um produto com equilíbrio excepcional de paladar, gordura, água e proteína cárnea. Um padrão que poucos produtos no mercado conseguem entregar.\n\nTenho certeza que na prática, na prova, isso fala por si. Fico no aguardo! 🤝\n\n*Fernando Azevedo Jr* — Azevedo e Filhos Representações\n📱 11 98833-4747	1	4	\N	2026-04-27
11	6	2026-04-22	E-mail	Renato de Oliveira Antunes	Renato, Daniela e Letícia, boa tarde!\n\nConforme alinhado em nossa reunião, encaminho em anexo a proposta comercial da Belmont Alimentos para o desenvolvimento dos vinagres marca própria da Coop.\n\nO arquivo apresenta toda a linha de produtos Belmont, com destaque — em grifo — para os 5 SKUs que sugiro para o projeto de marca própria, todos na embalagem de 750ml:\n\n• Vinagre de Álcool 750ml\n• Vinagre de Álcool Colorido 750ml\n• Vinagre de Maçã 750ml\n• Vinagre de Vinho Tinto 750ml\n• Vinagre de Vinho Branco 750ml\n\nQuero ser transparente quanto a uma decisão estratégica que tomei na construção desta proposta: inicialmente havia vislumbrado a possibilidade de oferecer os vinagres de Vinho Tinto, Vinho Branco e Balsâmico na embalagem de 380ml, uma vez que não identifiquei produtos neste volume na gôndola da Coop, o que geraria uma linha de acesso com percepção de menor preço para produtos que são, por natureza, premium. No entanto, ao analisar os requisitos de volume mínimo da Belmont para desenvolvimento de marca própria, optei por não seguir este caminho neste momento. Explico: o pedido mínimo total é de 16 paletes, com mínimo de 3 paletes por sabor. Na linha de 750ml, cada palete contém 85 caixas de 12 unidades (1.020 unidades); já na linha de 380ml, o palete é composto por 256 caixas de 6 unidades (1.536 unidades) — um volume consideravelmente superior, historicamente associado a um giro mais lento. Sendo assim, entendo que iniciar o projeto com a linha de 750ml é a decisão mais equilibrada e segura para a operação da Coop, evitando formação de estoque desproporcional ao potencial de venda.\n\nA proposta em anexo contempla:\n\n• Preços apresentados por caixa e por unidade\n• Simulação com progressividade de prazo de pagamento: 60, 70, 80 e 90 dias\n• Simulação de pedido mínimo em paletes e caixas, atendendo os requisitos de desenvolvimento de marca própria pela Belmont\n• Média de caixas recebidas por loja, considerando a distribuição para as 32 unidades da rede\n\nA inclusão da simulação por prazo de pagamento tem o objetivo de facilitar a análise e evidenciar que há espaço para encontrarmos juntos o ponto de equilíbrio ideal entre preço e prazo, sempre buscando a melhor condição para a Coop.\n\nColoco-me à disposição para apresentar, detalhar ou ajustar qualquer ponto da proposta. Fico no aguardo do seu retorno e permaneço comprometido em viabilizar este projeto com a seriedade e o respeito que a Coop merece.\n\nAtenciosamente,\n\nFernando Azevedo Jr . 11 98833-4747	1	6	\N	2026-04-24
12	8	2026-04-23	WhatsApp	Luiz	Bom dia, Luiz! Tudo bem?\n\nSou o Fernando, passei aqui rapidinho só para renovar o contato. Sei que a rotina de quem está à frente de uma operação como a Bella Caiçara é intensa, então não quero tomar seu tempo agora — apenas reforçar meu interesse em apresentar pessoalmente os fornecedores que represento.\n\nQuando tiver um espaço na agenda, mesmo que rápido, fico à disposição para passar aí. Tenho certeza de que vale a visita! \n\nFernando Azevedo Jr — Azevedo e Filhos Representações\n📱 11 98833-4747	1	5	\N	2026-04-29
13	1	2026-04-23	WhatsApp	Ed Carlo	Sou o Fernando, da Azevedo e Filhos Representações — passei aqui rapidinho apenas para renovar o contato e reforçar meu interesse em apresentar a Diet House e a Charcutaria Specialli pessoalmente, até com algumas amostras para você avaliar.\n\nSei que a agenda aperta, mas quando tiver um espaçinho, é só me falar! \n\nFernando Azevedo Jr — 11 98833-4747	1	3	\N	2026-04-29
14	3	2026-04-23	E-mail	\N	De: fernandojr@azevedoefilhos.com.br <fernandojr@azevedoefilhos.com.br> \nEnviada em: quinta-feira, 23 de abril de 2026 11:18\nPara: 'recepcao@redelitoral.com' <recepcao@redelitoral.com>\nAssunto: RES: Contato Comercial | Belmont Alimentos, Diet House e Charcutaria Specialli\n\nBoa tarde!\n\nPermito-me retomar contato, pois acredito genuinamente que os fornecedores que represento têm muito a agregar ao mix da Rede Litoral e seus associados.\n\nEm 13 de abril encaminhei um e-mail apresentando Belmont Alimentos, Diet House e Charcutaria Specialli — três empresas com histórias sólidas, produtos de qualidade comprovada e perfil alinhado ao consumidor da Baixada Santista. Como não obtive retorno, imagino que a mensagem possa ter se perdido no volume de e-mails, e por isso reforço o contato.\n\nMeu objetivo é simples: identificar a pessoa certa na área de compras e agendar uma conversa, no formato e momento que melhor se encaixar na rotina da rede. Uma única reunião pode abrir três oportunidades concretas de negócio para os associados.\n\nCaso este não seja o canal adequado, agradeceria imensamente a orientação sobre a forma correta de contato comercial com a Rede Litoral.\n\nFico à disposição e agradeço a atenção.\n\nAtenciosamente,\n\nFernando Azevedo Jr . 11 98833-4747	1	\N	\N	2026-04-29
15	10	2026-05-04	WhatsApp	Akira	\N	1	\N	Akira, boa tarde! Tudo bem?\n\nSou o Fernando, passei aí com meu pai há uma semana e tivemos uma ótima conversa. Fiquei feliz com a receptividade e aproveito para perguntar: teve oportunidade de experimentar as amostras da Diet House que deixei? Se sim, gostaria de saber a sua impressão!\n\nComo combinado, estou enviando a tabela de preços. Nela há uma aba com simulação de pedido, onde tomei a liberdade de sugerir alguns produtos — o pedido mínimo é de R$ 1.000,00, algo em torno de 5 a 6 caixas.\n\nA Diet House nasceu em 1990: seu fundador, ao ser diagnosticado com diabetes, decidiu criar doces sem açúcar que realmente encantassem o paladar. Mais de 30 anos depois, a marca é referência em compotas e doces diet e light, com produção artesanal, frutas selecionadas e adоçantes importados.\n\nCaso prefira receber o arquivo Excel por e-mail, é só me passar o endereço e encaminho imediatamente.\n\nFico no aguardo e à disposição!\n\nFernando Azevedo Jr\n11 98833-4747	2026-05-07
41	1	2026-05-13	WhatsApp	\N	Boa tarde, Ed Carlo! Tudo bem?\nPrimeiramente, gostaria de agradecer pela receptividade de ontem, pela atenção e pelo tempo que dedicou para me atender na Dona Manuela. \nConforme combinamos, estou lhe encaminhando a tabela de preços da Diet House, que conta inclusive com uma aba de simulação de pedido para facilitar a análise da linha.\nO pedido mínimo é de R$ 1.000,00 (em média 5 a 6 caixas de produtos), com entrega CIF e prazo de pagamento de 30 dias.\nDeixei destacados em negrito alguns dos itens carro-chefe para lhe auxiliar na avaliação. Pensando em uma seleção inicial de aproximadamente 6 sabores, acredito bastante no potencial de:\n\n• Frutas Vermelhas\n• Abóbora com Coco\n• Doce de Leite\n• Goiabada Cascão\n• Figo\n• Pimenta com Abacaxi\n• Pé de Moça ou Cocada\nFico totalmente à disposição para qualquer dúvida.	1	\N	\N	\N
22	11	2026-05-05	WhatsApp	\N	Boa tarde,\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e estou desenvolvendo a marca Diet House na região.\nGostaria de saber, por gentileza, quem é o responsável pelas compras do Empório Lapilli e qual a melhor forma de agendar uma visita rápida para apresentação da linha.\nA Diet House é uma marca com mais de 30 anos de mercado, especializada em doces sem açúcar e sem glúten, com produção artesanal e foco em sabor e qualidade — um mix bastante alinhado ao público que busca saúde e bem-estar, como o perfil do Empório.\nA ideia é levar algumas amostras para avaliação, sem compromisso, e entender se faz sentido para o portfólio de vocês.\nFico à disposição e agradeço desde já pela atenção!\nFernando Azevedo Jr\n11 98833-4747	1	\N	\N	\N
26	7	2026-05-05	WhatsApp	Loja Boqueirão	Boa tarde,\nMeu nome é Fernando Azevedo Jr., atuo como representante comercial na Baixada Santista.\nPoderia, por gentileza, me informar quem é o responsável pelas compras da Cruzeiro Carnes e qual a melhor forma de agendar uma visita rápida para apresentação da linha?\nTrabalho com a Charcutaria Specialli, de Jundiaí (SP), especializada em embutidos artesanais de alta qualidade, com linguiças e salsichas 100% carne, desenvolvidas por chef charcutier e com excelente desempenho para churrasco — um mix que pode agregar valor ao portfólio de vocês.\nPosso também encaminhar algumas imagens do portfólio para uma avaliação inicial.\nFico à disposição e agradeço desde já pela atenção.\nFernando Azevedo Jr\n(11) 9 8833-4747	1	15	\N	2026-05-07
42	1	2026-05-14	WhatsApp	\N	Segue também a tabela de preços da Charcutaria Specialli, com os itens que conversamos destacados em negrito para facilitar sua avaliação.\n\nO pedido mínimo também é de R$ 1.000,00, com frete FOB.\n\nConforme alinhamos ontem, na próxima semana estarei em reunião com o pessoal da Charcutaria e já vou providenciar as amostras solicitadas para que vocês possam avaliar os produtos na prática.\n\nMais uma vez, muito obrigado pela atenção e oportunidade, Ed Carlo!\n\nFernando Azevedo Jr\n11 98833-4747	1	\N	\N	2026-05-20
65	27	2026-05-20	WhatsApp	\N	Prezado(a), este canal é EXCLUSIVO para atendimento ao cliente final, assuntos relacionados a compras devem  ser encaminhados EXCLUSIVAMENTE para o e-mail compras@emporiosantista.com.br aos cuidados de Renato. Obrigado	1	\N	\N	2026-05-25
27	6	2026-05-05	WhatsApp	Daniela Mendonça	De: fernandojr@azevedoefilhos.com.br <fernandojr@azevedoefilhos.com.br> Enviada em: terça-feira, 5 de maio de 2026 10:49 Para: 'Daniela Cristina Mendonca da Silva' <daniela.mendonca@coopsp.coop.br> Cc: 'Renato de Oliveira Antunes' <renato.antunes@coopsp.coop.br>; 'Letícia Brito Galves' <leticia.galves@coopsp.coop.br>; 'comercial@vinagrebelmont.com.br' <comercial@vinagrebelmont.com.br> Assunto: RES: Projeto Vinagre - Marca própria - Belmont Daniela, bom dia! Permita-me me apresentar: sou Fernando Azevedo Jr, da Azevedo e Filhos Representações, representante comercial da Belmont Alimentos. Em 22 de abril encaminhei ao Renato, a você e à Letícia, a proposta comercial da Belmont para o desenvolvimento dos vinagres marca própria da Coop. Ao contatar o Renato o recebimento, ele me orientou que a condução da negociação de marca própria está sob sua gestão. Por isso, venho diretamente até você dar continuidade ao processo. Gostaríamos de receber um posicionamento sobre a análise da proposta, e coloco-me inteiramente à disposição para apresentar, detalhar ou ajustar qualquer ponto que facilite sua avaliação. Aproveito para reforçar brevemente o contexto: a Belmont Alimentos é uma indústria com mais de 50 anos de história, reconhecida pela tradição e qualidade de sua linha de vinagres — uma marca que, inclusive, já teve passagens relevantes de fornecimento à Coop. Tenho grande carinho e respeito pela rede, algo que tive a oportunidade de compartilhar com o Renato em nossa reunião, e que torna este projeto ainda mais especial para mim. Agradeço a atenção e fico no aguardo do seu retorno. Atenciosamente, Fernando Azevedo Jr . 11 98833-4747	1	10	\N	2026-05-07
28	7	2026-05-12	E-mail	\N	De: fernandojr@azevedoefilhos.com.br <fernandojr@azevedoefilhos.com.br> \nEnviada em: terça-feira, 12 de maio de 2026 10:25\nPara: 'contato@cruzeirocarnes.com.br' <contato@cruzeirocarnes.com.br>\nAssunto: Contato Charcutaria Specialli na Baixada\n\nBom dia,\n\nMeu nome é Fernando Azevedo Jr. e atuo como representante comercial da Charcutaria Specialli na Baixada Santista.\n\nPoderia, por gentileza, me informar quem é o responsável pelas compras da Cruzeiro Carnes e qual a melhor forma de agendar uma breve visita para apresentação da linha?\n\nA Charcutaria Specialli, de Jundiaí (SP), é especializada em embutidos artesanais de alta qualidade, com linguiças e salsichas 100% carne, desenvolvidas por chef charcutier e com excelente desempenho para churrasco — um mix diferenciado que pode agregar valor à linha de produtos da empresa.\n\nCaso seja de interesse, posso também encaminhar algumas imagens e materiais de apresentação para uma avaliação inicial.\n\nFico à disposição e agradeço desde já pela atenção.\n\nFernando Azevedo Jr  (11) 9 8833-4747	1	\N	\N	2026-05-14
29	7	2026-05-12	E-mail	\N	De: fernandojr@azevedoefilhos.com.br <fernandojr@azevedoefilhos.com.br> \nEnviada em: terça-feira, 12 de maio de 2026 10:25\nPara: 'contato@cruzeirocarnes.com.br' <contato@cruzeirocarnes.com.br>\nAssunto: Contato Charcutaria Specialli na Baixada\n\nBom dia,\n\nMeu nome é Fernando Azevedo Jr. e atuo como representante comercial da Charcutaria Specialli na Baixada Santista.\n\nPoderia, por gentileza, me informar quem é o responsável pelas compras da Cruzeiro Carnes e qual a melhor forma de agendar uma breve visita para apresentação da linha?\n\nA Charcutaria Specialli, de Jundiaí (SP), é especializada em embutidos artesanais de alta qualidade, com linguiças e salsichas 100% carne, desenvolvidas por chef charcutier e com excelente desempenho para churrasco — um mix diferenciado que pode agregar valor à linha de produtos da empresa.\n\nCaso seja de interesse, posso também encaminhar algumas imagens e materiais de apresentação para uma avaliação inicial.\n\nFico à disposição e agradeço desde já pela atenção.\n\nFernando Azevedo Jr  (11) 9 8833-4747	0	\N	\N	2026-05-14
30	10	2026-05-12	WhatsApp	Akira	Akira, bom dia! Tudo bem?\n\nTenho acompanhado o Instagram do Hortifruti e dá para perceber o cuidado de vocês em trabalhar um mix realmente diferenciado e de qualidade.\n\nPor isso lembrei novamente da Diet House e queria ouvir sua sincera opinião: você acredita que os doces Diet e Light da marca façam sentido dentro da proposta do Hortifruti Akira?\n\nAcredito que possa ser uma linha interessante para complementar o mix, principalmente pela qualidade dos produtos e pelo público que busca opções mais saudáveis e sem açúcar.\n\nFico à disposição e agradeço novamente pela atenção e receptividade que teve conosco naquele dia.\n\nFernando Azevedo Jr\n11 98833-4747	1	8	\N	2026-05-18
31	4	2026-05-12	WhatsApp	Tatiana Gomes	Bom dia, Tatiana! Tudo bem?\n\nEspero que tenha passado bem por este período de feriados. \n\nRetomo meu contato apenas para reforçar meu interesse em apresentar a Charcutaria Specialli ao GPA quando houver uma oportunidade na sua agenda.\n\nAcredito sinceramente que a linha tenha potencial para agregar valor à categoria, especialmente pela proposta artesanal e pelo padrão de qualidade dos produtos.\n\nPosso me adaptar ao melhor formato para você — seja uma visita rápida presencial, apresentação inicial por vídeo ou envio de material e amostras para avaliação.\n\nFico à disposição e agradeço novamente pela atenção desde nosso primeiro contato.\n\nFernando Azevedo Jr\n📱 11 98833-4747	1	4	\N	2026-05-15
43	12	2026-05-14	WhatsApp	Camila e Isabelle	Olá, Camila e Isabelle! Tudo bem?\n\nConforme alinhado, seguem em anexo o catálogo de produtos e a tabela de preços da Massas DE.\n\nHá mais de 50 anos no mercado, a Massas DE é referência na produção de massas com característica verdadeiramente caseira, preservando sabor, qualidade e tradição, sem utilização de aditivos químicos, através de um rigoroso controle em todas as etapas de produção.\n\nDados da empresa:\n\n• Razão Social: *Indústria de Massas Alimentícias DE Ltda.*\n• CNPJ: *48.657.860/0001-29*\n\nFico à disposição para quaisquer esclarecimentos, envio de informações complementares ou alinhamento de uma futura apresentação da linha.\n\nFernando Azevedo Jr.\nRepresentante Comercial Massas DE\n📞 11 98833-4747\n✉️ [fernandojr@azevedoefilhos.com.br](e-mail:fernandojr@azevedoefilhos.com.br)	1	\N	\N	2026-05-19
32	6	2026-05-12	E-mail	Daniela Mendonça	De: fernandojr@azevedoefilhos.com.br <fernandojr@azevedoefilhos.com.br> \nEnviada em: terça-feira, 5 de maio de 2026 10:49\nPara: 'Daniela Cristina Mendonca da Silva' <daniela.mendonca@coopsp.coop.br>\nCc: 'Renato de Oliveira Antunes' <renato.antunes@coopsp.coop.br>; 'Letícia Brito Galves' <leticia.galves@coopsp.coop.br>; 'comercial@vinagrebelmont.com.br' <comercial@vinagrebelmont.com.br>\nAssunto: RES: Projeto Vinagre - Marca própria - Belmont \n\nDaniela, bom dia!\n\nPermita-me me apresentar: sou Fernando Azevedo Jr, da Azevedo e Filhos Representações, representante comercial da Belmont Alimentos.\n\nEm 22 de abril encaminhei ao Renato, a você e à Letícia, a proposta comercial da Belmont para o desenvolvimento dos vinagres marca própria da Coop. Ao contatar o Renato o recebimento, ele me orientou que a condução da negociação de marca própria está sob sua gestão. Por isso, venho diretamente até você dar continuidade ao processo.\n\nGostaríamos de receber um posicionamento sobre a análise da proposta, e coloco-me inteiramente à disposição para apresentar, detalhar ou ajustar qualquer ponto que facilite sua avaliação.\n\nAproveito para reforçar brevemente o contexto: a Belmont Alimentos é uma indústria com mais de 50 anos de história, reconhecida pela tradição e qualidade de sua linha de vinagres — uma marca que, inclusive, já teve passagens relevantes de fornecimento à Coop. Tenho grande carinho e respeito pela rede, algo que tive a oportunidade de compartilhar com o Renato em nossa reunião, e que torna este projeto ainda mais especial para mim.\n\nAgradeço a atenção e fico no aguardo do seu retorno.\n\nAtenciosamente,\n\nFernando Azevedo Jr . 11 98833-4747	1	10	\N	2026-05-15
33	11	2026-05-12	E-mail	\N	De: fernandojr@azevedoefilhos.com.br <fernandojr@azevedoefilhos.com.br> \nEnviada em: terça-feira, 12 de maio de 2026 13:36\nPara: 'contato@emporiolapilli.com.br' <contato@emporiolapilli.com.br>\nAssunto: Doces Diet Light DIET HOUSE - Contato compras\n\nBoa tarde,\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e estou desenvolvendo a marca Diet House na região.\n\nGostaria de saber, por gentileza, quem é o responsável pelas compras do Empório Lapilli e qual a melhor forma de agendar uma visita rápida para apresentação da linha.\n\nA Diet House é uma marca com mais de 30 anos de mercado, especializada em doces sem açúcar e sem glúten, com produção artesanal e foco em sabor e qualidade — um mix bastante alinhado ao público que busca saúde e bem-estar, como o perfil do Empório.\n\nA ideia é levar algumas amostras para avaliação, sem compromisso, e entender se faz sentido para o portfólio de vocês.\n\nFico à disposição e agradeço desde já pela atenção!\n\nFernando Azevedo Jr . 11 98833-4747	1	\N	\N	2026-05-15
34	1	2026-05-12	WhatsApp	Ed Carlo	Boa tarde, Ed Carlo! Tudo bem?\n\nRetomo o contato apenas porque acredito sinceramente que tanto a Diet House quanto a Charcutaria Specialli possam fazer sentido dentro da proposta da Dona Manuela, especialmente pelo cuidado e perfil diferenciado que a padaria transmite ao público.\n\nEntendo perfeitamente a correria do dia a dia, então queria apenas saber se faz sentido seguirmos a conversa para que eu possa, em um momento oportuno, apresentar os produtos pessoalmente e levar algumas amostras para sua avaliação.\n\nFico à disposição e agradeço pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	1	3	\N	2026-05-15
35	8	2026-05-12	WhatsApp	Luiz	Boa tarde, Luiz! Tudo bem?\n\nResolvi renovar meu contato porque, além de representante comercial, sou cliente e vizinho da Bella Caiçara — moro aqui na Rua São Domingos — e confesso que para mim seria uma satisfação muito grande ter a oportunidade de apresentar produtos que acredito combinar com o padrão e a proposta da padaria.\n\nA Bella Caiçara, na minha opinião, é a referência diferenciada na Praia Grande, e justamente por isso acredito que algumas linhas que represento possam fazer bastante sentido aí dentro.\n\nQuando surgir uma oportunidade, mesmo que para uma conversa rápida, fico totalmente à disposição para passar pessoalmente e apresentar tudo com calma.\n\nObrigado pela atenção, Luiz!\n\nFernando Azevedo Jr\n11 98833-4747	1	5	\N	2026-05-19
36	2	2026-04-07	WhatsApp	\N	Michele, boa tarde! Tudo bem?\n\nRetomando nosso contato, desta vez para te apresentar uma linha diferente, que acredito ter bastante sinergia com o perfil das lojas do Raizeiro.\n\nEstou trabalhando também com a *Diet House*, uma empresa com forte atuação em *produtos diet*, especialmente *doces, compotas e fondants*, com ótima aceitação no varejo e foco em consumidores que buscam opções sem adição de açúcar.\n\nRecentemente estive na unidade da Guilhermina e acredito que essa linha pode complementar muito bem o mix atual da categoria.\n\nGostaria muito de poder te apresentar melhor os produtos e, se possível, levar algumas amostras para sua avaliação.\n\nVocê teria um momento nos próximos dias para uma conversa rápida ou poderia me orientar sobre o melhor dia e horário para uma visita?\n\nAgradeço desde já a atenção e fico à disposição.	1	\N	\N	\N
37	2	2026-05-12	WhatsApp	Michele	Boa tarde, Michele! Tudo bem?\n\nResolvi renovar meu contato porque continuo acreditando que a linha da Diet House tenha bastante sinergia com a proposta do Raizeiro, especialmente pelo perfil de consumidores que buscam produtos de qualidade e opções sem adição de açúcar.\n\nNas visitas que fiz às lojas, percebi que a categoria diet e light ainda pode ter espaço para itens diferenciados, e justamente por isso gostaria muito de lhe apresentar a linha com mais profundidade e deixar algumas amostras para avaliação.\n\nQuando surgir uma oportunidade, mesmo que rápida, fico totalmente à disposição para passar na unidade que for mais conveniente para você.\n\nObrigado pela atenção, Michele!\n\nFernando Azevedo Jr\n11 98833-4747	1	2	\N	2026-05-15
38	1	2026-05-12	WhatsApp	Ed Carlo	[13:49, 12/05/2026] +55 13 99712-6471: BOA TARDE FERNANDO\n[13:49, 12/05/2026] +55 13 99712-6471: TUDO BEM\n[13:50, 12/05/2026] +55 13 99712-6471: QUANDO QUISER PODE PASSAR AQUI NA PADARIA DONA MANUELA ´RA CONVERSARMOS E QUEM SABE CONHECERMOS SEUS ´PRODUTOS	1	3	\N	\N
39	1	2026-05-12	WhatsApp	Ed Carlo	Boa tarde, Ed Carlo! Tudo ótimo, graças a Deus — espero que com você também!\n\nFico muito feliz pelo retorno e agradeço pela receptividade. 😊\n\nAmanhã mesmo vou me organizar para passar aí na Dona Manuela, conversar pessoalmente com você e apresentar os produtos.\n\nMuito obrigado pela oportunidade!\n\nFernando Azevedo Jr	1	3	\N	2026-05-13
40	2	2026-05-12	WhatsApp	Michele	Muito obrigado pelo retorno e atenção. \n\nEstou lhe encaminhando o portfólio da Diet House para uma avaliação inicial e também a tabela de preços em Excel, que contém uma aba com simulação de pedido, caso lhe auxilie na análise da linha.\n\nO pedido mínimo é de R$ 1.000,00 (5 a 6 caixas), com prazo de pagamento de 30 dias e entrega CIF.\n\nFico à disposição para qualquer dúvida ou, se fizer sentido para vocês, para apresentar a linha pessoalmente.\n\nObrigado novamente!	1	2	\N	2026-05-15
44	4	2026-05-13	WhatsApp	Tatiana Gomes	Bom dia, Fernando \nTudo bem!\nEsta semana agenda esta bem cheia, vamos marcar para semana que vem!\nJa te passo a data	1	4	\N	\N
46	13	2026-05-18	WhatsApp	Elzio	Aproveitando também para compartilhar uma oportunidade bastante interessante: na semana passada fui recebido pela Padaria Dona Manuela, na Praia Grande — eleita Top 1 no ranking das padarias da Baixada Santista em 2025 — e também pela operação ligada à Padaria Casaria, de Santos, quinta colocada no ranking.\n\nConversei com o comprador Ed Carlo sobre possível introdução da linha Specialli, tanto para revenda quanto para utilização nas operações de lanches e refeições. Houve boa receptividade principalmente para salsichas Viena e Frankfurter, linguiças, copa, salame, pastrami fatiado e mortadela peça.\n\nSegundo ele, os preços foram considerados viáveis, porém o proprietário costuma validar novos produtos apenas após experimentar e avaliar aceitação dos clientes — processo semelhante ao que ocorreu com a linha Diet House que também represento.\n\n\nPara avaliação inicial, solicitaram:\n• Mortadela para teste de fatiamento e aceitação dos clientes\n• 1 pct Viena e Frankfurter\n• Copa ou salame 100g\n• Pastrami 100g\n• Linguiça toscana 400g\n\nNo caso específico da mortadela, o pedido inicial mencionado foi de uma peça de 3,1 kg para avaliarem o comportamento no fatiamento e aceitação no balcão. Porém, caso você considere excessivo para uma primeira aproximação, acredito que eu consiga administrar bem a situação inicialmente com uma apresentação menor, como a embalagem de 100g para degustação e percepção de qualidade do produto.\n\nAs duas padarias trabalham atualmente com Ceratti Tradicional e Perdigão Ouro, inclusive com campanhas de cashback por volume (Perdigão Ouro), mas o Ed Carlo comentou que o giro para nossa mortadela teria potencial tranquilo para ao menos uma caixa mensal por unidade.\n\nComo vejo as duas operações como possíveis vitrines e grandes formadoras de opinião para a Specialli na Baixada, gostaria de alinharmos também o envio das minhas amostras de salsichas e da massa de linguiça. Talvez possamos aproveitar inclusive quando nos encontrarmos na reunião do GPA.	1	\N	\N	\N
47	11	2026-05-18	WhatsApp	Loja Aviação: 13 99753-1236	Boa tarde,\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e estou desenvolvendo a marca Diet House na região.\nGostaria de saber, por gentileza, quem é o responsável pelas compras do Empório Lapilli e qual a melhor forma de agendar uma visita rápida para apresentação da linha.\n\nA Diet House é uma marca com mais de 30 anos de mercado, especializada em doces sem açúcar e sem glúten, com produção artesanal e foco em sabor e qualidade — um mix bastante alinhado ao público que busca saúde e bem-estar, como o perfil do Empório.\n\nA ideia é levar algumas amostras para avaliação, sem compromisso, e entender se faz sentido para o portfólio de vocês.\n\nFico à disposição e agradeço desde já pela atenção!\n\nFernando Azevedo Jr\n11 98833-4747	1	\N	\N	2026-05-21
48	3	2026-05-18	WhatsApp	\N	[09:04, 18/05/2026] +55 13 99679-5383: Obrigada pelas informações.\n\nIremos encaminhá-las à Gerente Comercial para verificação da disponibilidade em sua agenda. Assim que houver a aprovação, informarei o dia e o horário da reunião.\n\nAté breve.\n[10:11, 18/05/2026] Fernando Azevedo Jr: Bom dia,\n\nEu que agradeço pela atenção e pelo retorno.\n\nFico à disposição para quaisquer informações complementares e aguardarei o contato de vocês para alinharmos a reunião no melhor dia e horário para a gerente comercial.\n\nSerá um prazer apresentar melhor a linha Massas DE.\n\nAté breve!\n\nFernando Azevedo Jr.\n11 98833-4747	1	\N	\N	2026-05-25
49	11	2026-05-18	WhatsApp	Loja Aviação	[16:34, 18/05/2026] Lapilli Empório - Aviação: Boa tarde Fernando\n[16:35, 18/05/2026] Lapilli Empório - Aviação: envia a tabela de preços para que encaminhar ao responsavel\n[16:37, 18/05/2026] Fernando Azevedo Jr: Boa tarde!\n\nPerfeito, muito obrigado pelo retorno e pela atenção.\n\nEstou encaminhando em anexo o portfólio da Diet House juntamente com a tabela de preços para avaliação.\n\nFico totalmente à disposição para quaisquer dúvidas e, caso faça sentido posteriormente, também para uma apresentação rápida da linha com algumas amostras para avaliação.\n\nFernando Azevedo Jr\n11 98833-4747	1	\N	\N	2026-05-21
50	11	2026-05-18	WhatsApp	Loja Aviação	[16:41, 18/05/2026] Lapilli Empório - Aviação: quais os 5 mais vendidos?\n[16:43, 18/05/2026] Fernando Azevedo Jr: Obrigado por perguntar.\n\nDeixei destacados em negrito na planilha alguns dos itens carro-chefe para lhe auxiliar na avaliação. Pensando em uma seleção inicial de aproximadamente 6 sabores, acredito bastante no potencial de:\n\n* Frutas Vermelhas\n* Abóbora com Coco\n* Doce de Leite\n* Goiabada Cascão\n* Figo\n* Pimenta com Abacaxi\n* Pé de Moça ou Cocada\n\nO pedido mínimo é de R$ 1.000,00 (em média 5 a 6 caixas de produtos), com entrega CIF e prazo de pagamento de 30 dias.\n[16:44, 18/05/2026] Fernando Azevedo Jr: Aqui na baixada por enquanto apenas o Pão de Açúcar comercializa Diet House (há 15 anos), revendendo a R$ 30,99.	1	\N	\N	\N
51	14	2026-05-19	E-mail	Moisés	De: fernandojr@azevedoefilhos.com.br <fernandojr@azevedoefilhos.com.br> \nEnviada em: terça-feira, 19 de maio de 2026 11:45\nPara: 'moises@redekrill.com' <moises@redekrill.com>\nAssunto: Massas DE | Apresentação da Linha para Rede Krill\n\nPrezado Moisés, bom dia.\n\nMeu nome é Fernando Azevedo Jr e gostaria de apresentar à Rede Krill a linha de produtos da Massas DE, indústria com mais de 50 anos de tradição na produção de massas com características autenticamente caseiras, reconhecida pelo cuidado na seleção de matérias-primas, rigoroso controle de qualidade e por preservar o sabor e a textura típicos das massas artesanais, sem utilização de aditivos químicos.\n\nVejo uma boa sinergia entre a proposta da Massas DE e o perfil de qualidade da Rede Krill e, por isso, gostaria de verificar a possibilidade de uma breve visita presencial, no melhor dia e horário conforme sua disponibilidade, para apresentação da empresa, da linha de produtos e entendimento das necessidades da categoria.\n\nAproveitando a oportunidade, encaminho em anexo o catálogo de produtos Massas DE.\n\nPermaneço à disposição e agradeço desde já pela atenção.	1	\N	\N	2026-05-26
52	15	2026-05-19	WhatsApp	\N	Boa tarde,\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial na Baixada Santista.\nPoderia, por gentileza, me informar quem é o responsável pelas compras do Boi Nobre e qual a melhor forma de agendar uma visita rápida para apresentação da linha da Charcutaria Specialli?\n\nA Specialli é uma charcutaria de Jundiaí (SP), especializada em embutidos artesanais de alta qualidade, com linguiças e salsichas 100% carne, desenvolvidas por chef charcutier e com excelente padrão de sabor, textura e apresentação — uma linha bastante alinhada a operações que valorizam diferenciação e qualidade.\n\nAproveito também para encaminhar o catálogo da Specialli para uma avaliação inicial.\n\nFico à disposição e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n(11) 9 8833-4747	1	\N	\N	2026-05-22
53	16	2026-05-19	WhatsApp	13 99688-3922	Boa tarde,\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial na Baixada Santista.\nPoderia, por gentileza, me informar quem é o responsável pelas compras da Central de Carnes Boi Nobre e qual a melhor forma de agendar uma visita rápida para apresentação da linha da Charcutaria Specialli?\n\nA Specialli é uma charcutaria de Jundiaí (SP), especializada em embutidos artesanais de alta qualidade, com linguiças e salsichas 100% carne, desenvolvidas por chef charcutier e com excelente padrão de sabor, textura e apresentação — uma linha bastante alinhada a operações que valorizam diferenciação e qualidade.\n\nAproveito também para encaminhar o catálogo da Specialli para uma avaliação inicial.\n\nFico à disposição e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n(11) 9 8833-4747	1	\N	\N	\N
54	17	2026-05-19	WhatsApp	Alcides Borges	De: fernandojr@azevedoefilhos.com.br <fernandojr@azevedoefilhos.com.br> \nEnviada em: terça-feira, 19 de maio de 2026 16:28\nPara: 'alcides.neto@gpabr.com' <alcides.neto@gpabr.com>\nCc: 'fernando@azevedoefilhos.com.br' <fernando@azevedoefilhos.com.br>; 'Ambrosio Galvão' <comercial@vinagrebelmont.com.br>; 'J L Toledo' <jl@vinagrebelmont.com.br>\nAssunto: Belmont Alimentos | Retomada de Contato\n\nPrezado Alcides, boa tarde.\n\nEspero que esteja bem.\n\nRetomo nosso contato de maneira bastante tranquila e respeitosa, apenas para reforçar que permanecemos à disposição sempre que houver oportunidade para uma nova avaliação da linha de Vinagres Belmont junto ao GPA.\n\nDesde nossa última troca de mensagens, entendemos ser importante respeitar o momento e o ritmo das demandas da companhia, razão pela qual aguardamos o tempo adequado antes de voltar a lhe escrever.\n\nA Belmont segue com sua estrutura comercial e industrial fortalecida, mantendo o compromisso de qualidade que historicamente sempre caracterizou a marca e sua relação com o varejo brasileiro.\n\nPara mim, de forma muito particular, existe também um carinho genuíno pelo Grupo Pão de Açúcar, em razão da longa trajetória profissional do meu pai junto à companhia, o que naturalmente aumenta nosso respeito e interesse em construir uma relação sólida e de longo prazo com o GPA.\n\nFico à disposição sempre que julgar oportuno retomarmos essa conversa.\n\nAgradeço novamente pela atenção e cordialidade de sempre.\n\nAtenciosamente,\n\nFernando Azevedo Jr . 11 98833-4747\n \n\nDe: Ambrosio Galvão <comercial@vinagrebelmont.com.br> \nEnviada em: quarta-feira, 25 de março de 2026 12:30\nPara: alcides.neto@gpabr.com\nCc: fernandojr@azevedoefilhos.com.br; fernando@azevedoefilhos.com.br; Odair Martini <controladoria@vinagrebelmont.com.br>; J L Toledo <jl@vinagrebelmont.com.br>\nAssunto: Alteração de Representação Comercial\n\nBoa tarde  Sr. Alcides  tudo bem\n\nAnexo encaminho comunicado de alteração da representação comercial ora sendo atendida pelo sr. Carlos Ramhold.\nque estará assumindo novo setor também como nosso representante comercial.\n\nmuito obrigado\n\nAmbrosio Galvão\n--Gerente Nacional de Vendas\nVinagre Belmont S/A\n11 99914-20-78	1	17	\N	2026-05-21
55	18	2026-05-19	WhatsApp	13 99649-2340	Boa tarde,\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial na Baixada Santista.\nPoderia, por gentileza, me informar quem é o responsável pelas compras da Casa de Carnes Vila Rica e qual a melhor forma de agendar uma visita rápida para apresentação da linha da Charcutaria Specialli?\n\nA Specialli é uma charcutaria de Jundiaí (SP), especializada em embutidos artesanais de alta qualidade, com linguiças e salsichas 100% carne, desenvolvidas por chef charcutier e com excelente padrão de sabor, textura e apresentação — uma linha bastante alinhada a operações que valorizam diferenciação e qualidade.\n\nAproveito também para encaminhar o catálogo da Specialli para uma avaliação inicial.\n\nFico à disposição e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n(11) 9 8833-4747	1	\N	\N	2026-05-21
56	19	2026-05-20	WhatsApp	\N	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	1	\N	\N	\N
57	20	2026-05-20	WhatsApp	\N	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	1	\N	\N	\N
58	21	2026-05-20	WhatsApp	\N	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	1	\N	\N	\N
59	22	2026-05-20	WhatsApp	\N	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	1	\N	\N	\N
60	23	2026-05-20	WhatsApp	\N	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.	1	\N	\N	\N
61	24	2026-05-20	WhatsApp	\N	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	1	\N	\N	\N
62	25	2026-05-20	WhatsApp	\N	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.	1	\N	\N	\N
63	26	2026-05-20	WhatsApp	\N	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	1	\N	\N	\N
64	27	2026-05-20	WhatsApp	\N	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	1	\N	\N	\N
66	28	2026-05-20	WhatsApp	\N	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	1	\N	\N	\N
68	30	2026-05-20	WhatsApp	\N	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	1	\N	\N	\N
69	31	2026-05-20	WhatsApp	\N	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.	1	\N	\N	\N
70	32	2026-05-20	WhatsApp	Ana Paula	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	1	\N	\N	2026-05-25
67	29	2026-05-20	WhatsApp	\N	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	0	\N	\N	\N
71	27	2026-05-20	E-mail	Renato	De: fernandojr@azevedoefilhos.com.br <fernandojr@azevedoefilhos.com.br> \nEnviada em: quarta-feira, 20 de maio de 2026 16:44\nPara: 'compras@emporiosantista.com.br' <compras@emporiosantista.com.br>\nAssunto: Apresentação Comercial | Diet House\n\nPrezado Renato, boa tarde.\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial na Baixada Santista e estou desenvolvendo a marca Diet House na região.\n\nRecebi do atendimento do Empório Santista a orientação para encaminhar diretamente a você a apresentação da linha.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma proposta bastante alinhada ao perfil de consumidores que buscam qualidade, saudabilidade e alimentação funcional.\n\nEm anexo encaminho o portfólio da linha e também a tabela de preços para uma avaliação inicial. Para facilitar uma análise mais rápida da proposta, destaquei em negrito na tabela 8 itens carro-chefe da linha, com maior potencial de giro e aceitação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, com itens revendidos na faixa de R$ 30,99 ao consumidor final.\n\nA operação trabalha atualmente com pedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), entrega CIF e prazo de pagamento de 30 dias.\n\nFico à disposição para quaisquer dúvidas ou informações complementares e agradeço desde já pela atenção.\n\nAtenciosamente,\n\nFernando Azevedo Jr . 11 98833-4747	1	19	\N	2026-05-25
72	19	2026-05-21	WhatsApp	\N	[11:13, 21/05/2026] Cantin Empório Mineiro: Meu nome é Fátima Belani\n[11:13, 21/05/2026] Cantin Empório Mineiro: Bom dia\n[11:14, 21/05/2026] Cantin Empório Mineiro: Como poderíamos provar algum desses itens?\n[11:14, 21/05/2026] Cantin Empório Mineiro: Costumamos participar de festivais para conhecermos produtor e produto antes de incluir em nosso negócio\n[11:15, 21/05/2026] Cantin Empório Mineiro: E trabalhamos c produtos de Minas Gerais\n[11:15, 21/05/2026] Cantin Empório Mineiro: Como vcs nos localizaram ?\n[11:19, 21/05/2026] Fernando Azevedo Jr: Bom dia. Obrigado pela atenção, Fátima. Sim, é possível, posso levar uma amostra até vocês. Me mudei de São Paulo há 6 meses para a Praia Grande, para estar mais próximo aos meus pais, então estou realizando levantamento de diversos tipos de estabelecimentos, pois trouxe em minha carteira de representadas: 4 marcas: Massas De macarrão caseiro, a Diet House com os doces diet, a charcutaria Specialli de Jundiaí, linguiças, salsichas e curados, todos artesanais e os vinagres Belmont, por isso estou prospectando inicialmente por contato telefônico e e-mail para buscar me apresentar e às marcas. Assim os localizei via pesquisas de Google e Instagram da Baixada Santista.\n[11:20, 21/05/2026] Fernando Azevedo Jr: Qual seria para vocês o melhor dia e horário para eu  levar amostra?	1	\N	\N	2026-05-25
\.


--
-- Data for Name: contato_registro; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contato_registro (contato_id, data_contato, via_comunicacao, tipo_entidade, cliente_id, fornecedor_id, contato_pessoa, assunto, descricao, resultado, proxima_acao, data_followup, previsao_conclusao, status, prioridade, tipo_topico, usuario_resp, observacao, ativo) FROM stdin;
11	2026-05-05	WhatsApp	cliente	16	\N	\N	Apresentação Diet House	Boa tarde,\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e estou desenvolvendo a marca Diet House na região.\nGostaria de saber, por gentileza, quem é o responsável pelas compras do Empório Lapilli e qual a melhor forma de agendar uma visita rápida para apresentação da linha.\nA Diet House é uma marca com mais de 30 anos de mercado, especializada em doces sem açúcar e sem glúten, com produção artesanal e foco em sabor e qualidade — um mix bastante alinhado ao público que busca saúde e bem-estar, como o perfil do Empório.\nA ideia é levar algumas amostras para avaliação, sem compromisso, e entender se faz sentido para o portfólio de vocês.\nFico à disposição e agradeço desde já pela atenção!\nFernando Azevedo Jr\n11 98833-4747	\N	\N	2026-05-21	\N	Aguardando retorno	Média	Contato	\N	\N	1
5	2026-04-14	WhatsApp	cliente	59	\N	Luiz	Aprsentação Specialli, Diet House e Belmont	Boa tarde, Luiz! Tudo bem?\n\nO Felipe me passou seu contato hoje quando estive na Bella Caiçara. Sou o *Fernando Azevedo Jr*, moro aqui no Caiçara e sou cliente da padaria — e agora tambem venho bater à porta como representante comercial. 😊\n\nRepresento na Baixada Santista três fornecedores que acredito terem muito a agregar ao mix da Bella Caiçara:\n\n🥩 *Charcutaria Specialli* — 20 anos de qualidade, técnica e exclusividade em linguiças artesanais, salsichas, salame, copa, pastrami e mortadela.\n\n🍓 *Diet House* — empresa familiar com 30 anos, especializada em doces, compotas e fondants diet e light com sabores que surpreendem na primeira colherada.\n\n🥫 *Belmont Alimentos* — mais de 50 anos de tradição, com destaque para a linha de vinagres de excelente qualidade e giro comprovado no varejo.\n\nGostaria muito de saber se teria um espaço na sua agenda para que eu passe pessoalmente, me apresente e mostre o trabalho desses fornecedores.\n\nFico no aguardo e desde já grato,\n\n*Fernando Azevedo Jr* — Azevedo e Filhos Representações\n📱 11 98833-4747	\N	\N	2026-04-22	\N	A contatar	Alta	Contato	\N	\N	0
8	2026-04-19	WhatsApp	cliente	59	\N	Luiz	Apresentação Specialli e Diet House	\N	\N	\N	2026-05-19	\N	A contatar	Alta	Contato	\N	1	1
6	2026-04-15	Visita presencial	cliente	94	\N	Renato de Oliveira Antunes	Fornecimento Marca Própria Coop	Ambrosio, bom dia!\n\nVenho compartilhar uma excelente notícia: ontem concluí uma reunião muito promissora com o comprador Renato de Oliveira Antunes, da Coop — rede líder no ABC paulista com 32 lojas —, e saio dela com uma janela concreta de oportunidade para a Belmont.\n\nÉ importante esclarecer desde já o contexto: a Coop passou por uma reformulação estratégica em sua política comercial e adota hoje um modelo enxuto de categorias — apenas uma marca para o segmento líder, uma para o primeiro preço e uma para o premium. Por isso, neste momento, não há espaço para entrada de uma nova marca de vinagre em linha. No entanto, abre-se uma oportunidade distinta e muito relevante: a Coop encerrou recentemente o contrato de fornecimento de vinagres marca própria com a Toscano, e o comprador demonstrou abertura real para avaliar a Belmont como novo fornecedor neste segmento.\n\nO mix discutido e bem recebido — inclusive com entrega de amostras — foi:\n\n• Vinagre de Maçã 750ml\n• Vinagre de Álcool 750ml\n• Vinagre de Álcool Colorido 750ml\n• Vinagre de Vinho Tinto 380ml\n• Vinagre de Vinho Branco 380ml\n• Vinagre Balsâmico 380ml\n\nAs condições comerciais praticadas pela Coop são: entrega no CD (com distribuição para 32 lojas via cross-docking), desconto contratual de 2% sobre logística e prazo de pagamento padrão de 90 dias. Um ponto importante: o comprador foi transparente ao informar que a Coop não trabalha com prazo inferior a 70 dias — o que nos abre uma margem de negociação. Caso a Belmont consiga operar com um prazo entre 70 e 90 dias, isso pode ser um elemento valioso para compor uma proposta de preço mais competitiva e diferenciada.\n\nAlém da tabela de preços, o comprador solicitou que sinalizemos as quantidades mínimas de pedido para o fornecimento de marca própria por SKU. Esta informação será fundamental para que a Coop avalie a viabilidade operacional do fornecimento, por isso peço que nos indiquem esses volumes junto à proposta.\n\nO Renato solicitou celeridade no retorno e a Coop já iniciou internamente o processo de validação da Belmont como fornecedora de marca própria. A janela é real, mas tem prazo.\n\nSabendo da história, da qualidade e da capacidade produtiva da Belmont, estou certo de que temos condições de surpreender positivamente. Conto com a sua prioridade no envio da tabela e das quantidades mínimas para que possamos responder com a agilidade que esta oportunidade exige.\n\nFico à disposição para alinhar qualquer detalhe.\n\nGrato pela parceria e confiança!\n\nFernando Azevedo Jr . 11 98833-4747\n------------------------------------------------------\n[08:32, 17/04/2026] Ambrósio Galvão Belmont: Bom dia Fernando tudo bem tomei conhecimento da ata coop vou montar a proposta. Temos possibilidades de fazer a marca própria deles sim. Precisamos saber se eles estão com a Amicci ou se irão negociar direto conosco.\n[08:33, 17/04/2026] Ambrósio Galvão Belmont: Amicci e uma multinacional direcionada a gerenciar marcas próprias trabalha interagindo com redes e fornecedores\n[08:34, 17/04/2026] Ambrósio Galvão Belmont: Nesse trabalho eles exigem 3% de comissão\n[08:36, 17/04/2026] Ambrósio Galvão Belmont: Se for negociação direta será muito mais produtivo para nós e menor riscos de sermos substituídos por outros fornecedores uma vez que eles procuram sempre maior benefício aos clientes não se posicionando de forma fiel a fornecedores.\n---------------------------------------------------\n[10:58, 17/04/2026] Fernando Azevedo Jr: Bom dia, Renato! Tudo bem?\n\nPreciso confirmar um ponto importante com você antes de avançarmos com a proposta da Belmont para a Coop.\n\nVocê mencionou na reunião que havia uma consultoria envolvida nos projetos de marca própria, mas que a Coop optou por não mais manter este serviço. Correto?\n\nO motivo da pergunta é prático: se não há consultoria intermediando, a negociação será direta entre Coop e Belmont — o que elimina custos adicionais da proposta e nos permite chegar a um preço mais competitivo e vantajoso para a rede.\n\nPoderia confirmar esse ponto para que eu possa orientar corretamente a Belmont na elaboração da proposta?\n\nAgradeço e fico no aguardo! 🤝\n\nFernando Azevedo Jr — Azevedo e Filhos Representações\n📱 11 98833-4747\n[15:55, 17/04/2026] Fernando Azevedo Jr: Renato, boa tarde. Permaneço no aguardo da informação para solicitar celeridade à Belmont. Obrigado.\n[17:10, 17/04/2026] Renato Antunes COOP: Boa tarde\n[17:10, 17/04/2026] Renato Antunes COOP: Isso mesmo\n[17:10, 17/04/2026] Renato Antunes COOP: Negociação direta\n-----------------------------------------------------------------------	Aguardar envio proposta de preços e volume Belmont para enviar para a COOP.	\N	2026-05-15	\N	Aguardando retorno	Alta	Negociação	\N	\N	1
2	2026-04-13	WhatsApp	cliente	10	\N	Michele	Apresentação Diet House	Boa tarde, Michele! Tudo bem?\n\nSei como o varejo tem seu próprio ritmo — meu pai trabalhou a vida toda no Grupo Pão de Açúcar e nós, os filhos, crescemos entendendo bem essa rotina. Por isso não quero que se sinta pressionada de forma alguma.\n\nSó retorno ao meu contato do dia 07 justamente porque acredito muito na sinergia da *Diet House* com o perfil do Raizeiro, e gostaria de lhe pedir que *me permita entregar, aos seus cuidados, algumas amostras da linha na loja da Guilhermina.* \n\nÉ uma empresa familiar que acompanho há décadas, com produtos diet de verdade — doces, compotas e fondants sem adição de açúcar, com ótima aceitação no varejo.\n\nFico no aguardo de sua autorização e desde já grato,\n\n*Fernando Azevedo Jr* — Azevedo e Filhos Representações\n11 98833-4747	\N	\N	2026-05-15	\N	Proposta enviada	Média	Contato	\N	\N	1
7	2026-04-22	WhatsApp	cliente	21	\N	\N	Apresentação Specialli	\N	\N	\N	2026-05-14	\N	Aguardando retorno	Alta	Contato	\N	\N	1
16	2026-05-19	WhatsApp	cliente	101	\N	13 99688-3922	Contato Specialli	Boa tarde,\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial na Baixada Santista.\nPoderia, por gentileza, me informar quem é o responsável pelas compras da Central de Carnes Boi Nobre e qual a melhor forma de agendar uma visita rápida para apresentação da linha da Charcutaria Specialli?\n\nA Specialli é uma charcutaria de Jundiaí (SP), especializada em embutidos artesanais de alta qualidade, com linguiças e salsichas 100% carne, desenvolvidas por chef charcutier e com excelente padrão de sabor, textura e apresentação — uma linha bastante alinhada a operações que valorizam diferenciação e qualidade.\n\nAproveito também para encaminhar o catálogo da Specialli para uma avaliação inicial.\n\nFico à disposição e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n(11) 9 8833-4747	\N	\N	\N	\N	Aguardando retorno	Média	Contato	\N	\N	1
1	2026-04-13	WhatsApp	cliente	58	\N	Ed Carlo	Apreesentação Diet House e Specialli	Boa tarde, Ed Carlos! Tudo bem?\n\nA Padaria Dona Manuela me passou seu contato e fico feliz em poder falar diretamente com você. \n\nSou o *Fernando Azevedo Jr*, da *Azevedo e Filhos Representações*, e represento na Baixada Santista dois fornecedores que acredito terem muito a agregar ao mix da padaria:\n\n🍓 *Diet House* — empresa familiar com 30 anos de estrada, produz doces, compotas e fondants diet e light com sabores que surpreendem na primeira colherada.\n\n🥩 *Charcutaria Specialli* — 20 anos entregando qualidade, técnica e exclusividade em linguiças artesanais, salsichas, salame, copa, pastrami e mortadela.\n\nGostaria muito de agendar uma visita para me apresentar pessoalmente e mostrar o trabalho desses fornecedores — se possível, levar algumas amostras para sua avaliação.\n\nQual seria o melhor dia e horário para eu passar?\n\nDesde já agradeço a atenção! 🤝\n\n*Fernando Azevedo Jr* — Azevedo e Filhos Representações\n11 98833-4747	\N	\N	2026-05-20	\N	Em andamento	Média	Contato	\N	\N	1
3	2026-04-13	E-mail	cliente	92	\N	Recepção	Contato Comercial | Belmont Alimentos, Diet House e Charcutaria Specialli	De: fernandojr@azevedoefilhos.com.br <fernandojr@azevedoefilhos.com.br> \nEnviada em: segunda-feira, 13 de abril de 2026 14:42\nPara: 'recepcao@redelitoral.com' <recepcao@redelitoral.com>\nAssunto: Contato Comercial | Belmont Alimentos, Diet House e Charcutaria Specialli\n\nBoa tarde,\n\nMeu nome é Fernando Azevedo Jr e represento na Baixada Santista três fornecedores que acredito terem forte sinergia com o perfil e o mix da Rede Litoral:\n\n• Belmont Alimentos — mais de 50 anos de tradição, com destaque para a linha de vinagres de excelente qualidade e giro comprovado no varejo.\n\n• Diet House — empresa familiar com 30 anos de estrada, especializada em doces, compotas e fondants diet e light, com crescente demanda dos consumidores que buscam opções sem adição de açúcar.\n\n• Charcutaria Specialli — 20 anos entregando qualidade, técnica e exclusividade em linguiças artesanais, salsichas, salame, copa, pastrami e mortadela.\n\nUma única reunião pode abrir três oportunidades de negócio para a rede — e estou à disposição para apresentar cada uma delas no formato e momento que melhor se encaixar na rotina de vocês.\n\nGostaria de solicitar o contato do responsável pela área de compras ou a orientação sobre a forma correta de atendimento comercial da rede.\n\nAgradeço a atenção e fico no aguardo de um retorno.\n\nAtenciosamente,\n\nFernando Azevedo Jr . 11 98833-4747	Caso não haja retorno, visitar pessoalmente a central em São Vicente.	\N	2026-05-25	\N	Cancelado	Média	Contato	\N	\N	1
10	2026-05-04	WhatsApp	cliente	97	\N	Akira	Envio Tabela Diet House	\N	Akira, boa tarde! Tudo bem?\n\nSou o Fernando, passei aí com meu pai há uma semana e tivemos uma ótima conversa. Fiquei feliz com a receptividade e aproveito para perguntar: teve oportunidade de experimentar as amostras da Diet House que deixei? Se sim, gostaria de saber a sua impressão!\n\nComo combinado, estou enviando a tabela de preços. Nela há uma aba com simulação de pedido, onde tomei a liberdade de sugerir alguns produtos — o pedido mínimo é de R$ 1.000,00, algo em torno de 5 a 6 caixas.\n\nA Diet House nasceu em 1990: seu fundador, ao ser diagnosticado com diabetes, decidiu criar doces sem açúcar que realmente encantassem o paladar. Mais de 30 anos depois, a marca é referência em compotas e doces diet e light, com produção artesanal, frutas selecionadas e adоçantes importados.\n\nCaso prefira receber o arquivo Excel por e-mail, é só me passar o endereço e encaminho imediatamente.\n\nFico no aguardo e à disposição!\n\nFernando Azevedo Jr\n11 98833-4747	\N	2026-05-18	\N	Aguardando retorno	Média	Contato	\N	\N	1
14	2026-05-19	E-mail	cliente	14	\N	Moisés	Massas DE | Apresentação da Linha para Rede Krill	De: fernandojr@azevedoefilhos.com.br <fernandojr@azevedoefilhos.com.br> \nEnviada em: terça-feira, 19 de maio de 2026 11:45\nPara: 'moises@redekrill.com' <moises@redekrill.com>\nAssunto: Massas DE | Apresentação da Linha para Rede Krill\n\nPrezado Moisés, bom dia.\n\nMeu nome é Fernando Azevedo Jr e gostaria de apresentar à Rede Krill a linha de produtos da Massas DE, indústria com mais de 50 anos de tradição na produção de massas com características autenticamente caseiras, reconhecida pelo cuidado na seleção de matérias-primas, rigoroso controle de qualidade e por preservar o sabor e a textura típicos das massas artesanais, sem utilização de aditivos químicos.\n\nVejo uma boa sinergia entre a proposta da Massas DE e o perfil de qualidade da Rede Krill e, por isso, gostaria de verificar a possibilidade de uma breve visita presencial, no melhor dia e horário conforme sua disponibilidade, para apresentação da empresa, da linha de produtos e entendimento das necessidades da categoria.\n\nAproveitando a oportunidade, encaminho em anexo o catálogo de produtos Massas DE.\n\nPermaneço à disposição e agradeço desde já pela atenção.	\N	\N	2026-05-26	\N	Aguardando retorno	Alta	Contato	\N	\N	1
12	2026-05-14	WhatsApp	cliente	92	\N	Camila e Isabelle	Apresentação Massas DE	Olá, Camila e Isabelle! Tudo bem?\n\nConforme alinhado, seguem em anexo o catálogo de produtos e a tabela de preços da Massas DE.\n\nHá mais de 50 anos no mercado, a Massas DE é referência na produção de massas com característica verdadeiramente caseira, preservando sabor, qualidade e tradição, sem utilização de aditivos químicos, através de um rigoroso controle em todas as etapas de produção.\n\nDados da empresa:\n\n• Razão Social: *Indústria de Massas Alimentícias DE Ltda.*\n• CNPJ: *48.657.860/0001-29*\n\nFico à disposição para quaisquer esclarecimentos, envio de informações complementares ou alinhamento de uma futura apresentação da linha.\n\nFernando Azevedo Jr.\nRepresentante Comercial Massas DE\n📞 11 98833-4747\n✉️ [fernandojr@azevedoefilhos.com.br](e-mail:fernandojr@azevedoefilhos.com.br)	\N	\N	2026-05-19	\N	Aguardando retorno	Alta	Contato	\N	\N	1
13	2026-05-18	WhatsApp	fornecedor	\N	3	Elzio	Padaria Dona Manuella	Aproveitando também para compartilhar uma oportunidade bastante interessante: na semana passada fui recebido pela Padaria Dona Manuela, na Praia Grande — eleita Top 1 no ranking das padarias da Baixada Santista em 2025 — e também pela operação ligada à Padaria Casaria, de Santos, quinta colocada no ranking.\n\nConversei com o comprador Ed Carlo sobre possível introdução da linha Specialli, tanto para revenda quanto para utilização nas operações de lanches e refeições. Houve boa receptividade principalmente para salsichas Viena e Frankfurter, linguiças, copa, salame, pastrami fatiado e mortadela peça.\n\nSegundo ele, os preços foram considerados viáveis, porém o proprietário costuma validar novos produtos apenas após experimentar e avaliar aceitação dos clientes — processo semelhante ao que ocorreu com a linha Diet House que também represento.\n\n\nPara avaliação inicial, solicitaram:\n• Mortadela para teste de fatiamento e aceitação dos clientes\n• 1 pct Viena e Frankfurter\n• Copa ou salame 100g\n• Pastrami 100g\n• Linguiça toscana 400g\n\nNo caso específico da mortadela, o pedido inicial mencionado foi de uma peça de 3,1 kg para avaliarem o comportamento no fatiamento e aceitação no balcão. Porém, caso você considere excessivo para uma primeira aproximação, acredito que eu consiga administrar bem a situação inicialmente com uma apresentação menor, como a embalagem de 100g para degustação e percepção de qualidade do produto.\n\nAs duas padarias trabalham atualmente com Ceratti Tradicional e Perdigão Ouro, inclusive com campanhas de cashback por volume (Perdigão Ouro), mas o Ed Carlo comentou que o giro para nossa mortadela teria potencial tranquilo para ao menos uma caixa mensal por unidade.\n\nComo vejo as duas operações como possíveis vitrines e grandes formadoras de opinião para a Specialli na Baixada, gostaria de alinharmos também o envio das minhas amostras de salsichas e da massa de linguiça. Talvez possamos aproveitar inclusive quando nos encontrarmos na reunião do GPA.	\N	\N	\N	\N	Aguardando retorno	Média	Contato	\N	\N	1
4	2026-04-13	WhatsApp	cliente	93	\N	Tatiana Gomes	Apresentação Mortadela Specialli	Boa tarde, Tatiana! Tudo bem?\n\nMeu nome é *Fernando Azevedo Jr*, da *Azevedo e Filhos Representações*. Me permita uma breve apresentação antes do motivo do contato.\n\nSou filho do Fernando Azevedo, que dedicou *32 anos de carreira ao Grupo Pão de Açúcar*, aposentando-se na área de Marcas Próprias. Cresci dentro dessa cultura e hoje, dando continuidade ao trabalho da família, atuo como representante comercial com foco em grandes redes de varejo.\n\nO motivo do meu contato, Tatiana, é apresentar uma oportunidade que acredito ter muito a ver com a sua categoria: a *Charcutaria Specialli*.\n\nUma charcutaria artesanal com 20 anos de história, que une qualidade, técnica e sabor. E o primeiro produto que gostaria de apresentar ao GPA é a *Mortadela Peça de 3,1 kg* — produzida 100% com carne suína, textura macia, aroma marcante e toque artesanal. Um produto com enorme potencial para operação de *fatiados no balcão*.\n\nGostaria muito de agendar uma visita presencial para me apresentar e apresentar a Specialli com mais detalhes.\n\nQual seria a melhor forma e o melhor momento para conversarmos?\n\nFernando Azevedo Jr — Azevedo e Filhos Representações\n📱 11 98833-4747\n📧 fernandojr@azevedoefilhos.com.br	Tatiana respondeu em 14/04/2026: Ola \nBom dia,\nTudo bem!\nAcredito que na próxima semana, assim que surgir agenda te informo.	\N	2026-05-15	\N	Aguardando retorno	Alta	Contato	\N	\N	1
15	2026-05-19	WhatsApp	cliente	70	\N	\N	Contato Specialli	Boa tarde,\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial na Baixada Santista.\nPoderia, por gentileza, me informar quem é o responsável pelas compras do Boi Nobre e qual a melhor forma de agendar uma visita rápida para apresentação da linha da Charcutaria Specialli?\n\nA Specialli é uma charcutaria de Jundiaí (SP), especializada em embutidos artesanais de alta qualidade, com linguiças e salsichas 100% carne, desenvolvidas por chef charcutier e com excelente padrão de sabor, textura e apresentação — uma linha bastante alinhada a operações que valorizam diferenciação e qualidade.\n\nAproveito também para encaminhar o catálogo da Specialli para uma avaliação inicial.\n\nFico à disposição e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n(11) 9 8833-4747	\N	\N	2026-05-22	\N	Aguardando retorno	Média	Contato	\N	\N	1
17	2026-05-19	WhatsApp	cliente	93	\N	Alcides Borges	Belmont Alimentos | Retomada de Contato	De: fernandojr@azevedoefilhos.com.br <fernandojr@azevedoefilhos.com.br> \nEnviada em: terça-feira, 19 de maio de 2026 16:28\nPara: 'alcides.neto@gpabr.com' <alcides.neto@gpabr.com>\nCc: 'fernando@azevedoefilhos.com.br' <fernando@azevedoefilhos.com.br>; 'Ambrosio Galvão' <comercial@vinagrebelmont.com.br>; 'J L Toledo' <jl@vinagrebelmont.com.br>\nAssunto: Belmont Alimentos | Retomada de Contato\n\nPrezado Alcides, boa tarde.\n\nEspero que esteja bem.\n\nRetomo nosso contato de maneira bastante tranquila e respeitosa, apenas para reforçar que permanecemos à disposição sempre que houver oportunidade para uma nova avaliação da linha de Vinagres Belmont junto ao GPA.\n\nDesde nossa última troca de mensagens, entendemos ser importante respeitar o momento e o ritmo das demandas da companhia, razão pela qual aguardamos o tempo adequado antes de voltar a lhe escrever.\n\nA Belmont segue com sua estrutura comercial e industrial fortalecida, mantendo o compromisso de qualidade que historicamente sempre caracterizou a marca e sua relação com o varejo brasileiro.\n\nPara mim, de forma muito particular, existe também um carinho genuíno pelo Grupo Pão de Açúcar, em razão da longa trajetória profissional do meu pai junto à companhia, o que naturalmente aumenta nosso respeito e interesse em construir uma relação sólida e de longo prazo com o GPA.\n\nFico à disposição sempre que julgar oportuno retomarmos essa conversa.\n\nAgradeço novamente pela atenção e cordialidade de sempre.\n\nAtenciosamente,\n\nFernando Azevedo Jr . 11 98833-4747\n \n\nDe: Ambrosio Galvão <comercial@vinagrebelmont.com.br> \nEnviada em: quarta-feira, 25 de março de 2026 12:30\nPara: alcides.neto@gpabr.com\nCc: fernandojr@azevedoefilhos.com.br; fernando@azevedoefilhos.com.br; Odair Martini <controladoria@vinagrebelmont.com.br>; J L Toledo <jl@vinagrebelmont.com.br>\nAssunto: Alteração de Representação Comercial\n\nBoa tarde  Sr. Alcides  tudo bem\n\nAnexo encaminho comunicado de alteração da representação comercial ora sendo atendida pelo sr. Carlos Ramhold.\nque estará assumindo novo setor também como nosso representante comercial.\n\nmuito obrigado\n\nAmbrosio Galvão\n--Gerente Nacional de Vendas\nVinagre Belmont S/A\n11 99914-20-78	\N	\N	2026-05-21	\N	Aguardando retorno	Alta	Contato	\N	\N	1
18	2026-05-19	WhatsApp	cliente	71	\N	13 99649-2340	Contato Specialli	Boa tarde,\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial na Baixada Santista.\nPoderia, por gentileza, me informar quem é o responsável pelas compras da Casa de Carnes Vila Rica e qual a melhor forma de agendar uma visita rápida para apresentação da linha da Charcutaria Specialli?\n\nA Specialli é uma charcutaria de Jundiaí (SP), especializada em embutidos artesanais de alta qualidade, com linguiças e salsichas 100% carne, desenvolvidas por chef charcutier e com excelente padrão de sabor, textura e apresentação — uma linha bastante alinhada a operações que valorizam diferenciação e qualidade.\n\nAproveito também para encaminhar o catálogo da Specialli para uma avaliação inicial.\n\nFico à disposição e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n(11) 9 8833-4747	\N	\N	2026-05-21	\N	Aguardando retorno	Média	Contato	\N	\N	1
20	2026-05-20	WhatsApp	cliente	33	\N	\N	Contato Diet House	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	\N	\N	\N	\N	Em andamento	Média	Contato	\N	\N	1
21	2026-05-20	WhatsApp	cliente	32	\N	\N	Contato Diet House	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	\N	\N	\N	\N	Em andamento	Média	Contato	\N	\N	1
22	2026-05-20	WhatsApp	cliente	30	\N	\N	Contato Diet House	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	\N	\N	\N	\N	Em andamento	Média	Contato	\N	\N	1
23	2026-05-20	WhatsApp	cliente	22	\N	\N	Contato Diet House	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.	\N	\N	\N	\N	Em andamento	Média	Contato	\N	\N	1
24	2026-05-20	WhatsApp	cliente	31	\N	\N	Contato Diet House	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	\N	\N	\N	\N	Em andamento	Média	Contato	\N	\N	1
25	2026-05-20	WhatsApp	cliente	24	\N	\N	Contato Diet House	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.	\N	\N	\N	\N	Em andamento	Média	Contato	\N	\N	1
26	2026-05-20	WhatsApp	cliente	26	\N	\N	Contato Diet House	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	\N	\N	\N	\N	Em andamento	Média	Contato	\N	\N	1
28	2026-05-20	WhatsApp	cliente	27	\N	\N	Contato Diet House	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	\N	\N	\N	\N	Em andamento	Média	Contato	\N	\N	1
27	2026-05-20	WhatsApp	cliente	34	\N	\N	Contato Diet House	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	\N	\N	2026-05-25	\N	Proposta enviada	Média	Contato	\N	\N	1
30	2026-05-20	WhatsApp	cliente	25	\N	\N	Contato Diet House	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	\N	\N	\N	\N	Em andamento	Média	Contato	\N	\N	1
31	2026-05-20	WhatsApp	cliente	36	\N	\N	Contato Diet House	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.	\N	\N	\N	\N	Em andamento	Média	Contato	\N	\N	1
32	2026-05-20	WhatsApp	cliente	29	\N	Ana Paula	Contato Diet House	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	\N	\N	2026-05-25	\N	Proposta enviada	Média	Contato	\N	\N	1
29	2026-05-20	WhatsApp	cliente	37	\N	\N	Contato Diet House	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	\N	\N	\N	\N	Em andamento	Média	Contato	\N	\N	0
19	2026-05-20	WhatsApp	cliente	28	\N	\N	Contato Diet House	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.\n\n------------------------\n\nPara facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	\N	\N	2026-05-25	\N	Em andamento	Média	Contato	\N	\N	1
\.


--
-- Data for Name: contato_x_fornecedor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contato_x_fornecedor (id, contato_id, fornecedor_id, cxf_id) FROM stdin;
16	1	3	5
17	1	2	6
18	2	2	7
22	6	1	11
23	4	3	12
24	7	3	13
25	5	1	14
26	5	3	15
27	5	2	16
28	8	3	19
29	8	2	20
30	8	1	21
31	10	2	\N
32	11	2	\N
33	12	4	\N
34	13	3	\N
35	14	4	\N
36	15	3	\N
37	16	3	\N
38	17	1	\N
39	18	3	\N
40	19	2	\N
41	20	2	\N
42	21	2	\N
43	22	2	\N
44	23	2	\N
45	24	2	\N
46	25	2	\N
47	26	2	\N
48	27	2	\N
49	28	2	\N
50	29	2	\N
51	30	2	\N
52	31	2	\N
53	32	2	\N
\.


--
-- Data for Name: fornecedor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fornecedor (fornecedor_id, razao_social, nome_fantasia, endereco, bairro, cidade, estado, cnpj, ie, observacao, ativo, pedido_minimo) FROM stdin;
3	Embutidos Specialli Ltda	Charcutaria Specialli	Av. Caetano Gornati, 267, Galpão A2	Engordadouro	Jundiaí	SP	27.470.795/0001-58			1	\N
1	VINAGRE BELMONT S/A	Belmont	RODOVIA OSNY MATEHEUS  KM  116	LAGOA BONITA	Lençóis Paulista	SP	44.806.784/0001-15	416007003118		1	\N
2	CRISTINA JUNQUEIRA FRANCO MENEZES LTDA - ME	Diet House	R. PLINIO SALGADO, 1017	Jd Maracanã	São José do Rio Preto	SP	08.848.560/0001-02	647503477111		1	1000.0
4	Indústria de Massas Alimenticias De Ltda	Massas De	Rua Alexandre H Moleta, 782	Loteamento Ana Carolina	Valinhos	SP	48.657.860/0001-29	708010340119		1	1000.0
\.


--
-- Data for Name: historico_preco; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.historico_preco (hist_id, produto_id, fornecedor_id, tabela_id, nome_tabela, data_vigencia, preco_caixa, preco_kg, data_registro) FROM stdin;
438	380	4	19	Tabela 28d (2026)	2026-01-01	232.8	\N	2026-05-14
439	371	4	19	Tabela 28d (2026)	2026-01-01	220.8	\N	2026-05-14
440	372	4	19	Tabela 28d (2026)	2026-01-01	164.6	\N	2026-05-14
441	378	4	19	Tabela 28d (2026)	2026-01-01	155.88	\N	2026-05-14
442	370	4	19	Tabela 28d (2026)	2026-01-01	206.88	\N	2026-05-14
443	373	4	19	Tabela 28d (2026)	2026-01-01	245.28	\N	2026-05-14
444	377	4	19	Tabela 28d (2026)	2026-01-01	82.3	\N	2026-05-14
445	365	4	19	Tabela 28d (2026)	2026-01-01	164.6	\N	2026-05-14
446	366	4	19	Tabela 28d (2026)	2026-01-01	164.6	\N	2026-05-14
447	367	4	19	Tabela 28d (2026)	2026-01-01	164.6	\N	2026-05-14
448	368	4	19	Tabela 28d (2026)	2026-01-01	164.6	\N	2026-05-14
449	369	4	19	Tabela 28d (2026)	2026-01-01	164.6	\N	2026-05-14
450	376	4	19	Tabela 28d (2026)	2026-01-01	108.25	\N	2026-05-14
451	387	4	19	Tabela 28d (2026)	2026-01-01	184	\N	2026-05-14
452	375	4	19	Tabela 28d (2026)	2026-01-01	179.8	\N	2026-05-14
453	379	4	19	Tabela 28d (2026)	2026-01-01	87.8	\N	2026-05-14
454	374	4	19	Tabela 28d (2026)	2026-01-01	204.4	\N	2026-05-14
455	381	4	19	Tabela 28d (2026)	2026-01-01	125.6	\N	2026-05-14
456	2	1	20	Varejo 28D (2026)	2026-05-01	23.217392	\N	2026-05-14
457	3	1	20	Varejo 28D (2026)	2026-05-01	23.217392	\N	2026-05-14
458	1	1	20	Varejo 28D (2026)	2026-05-01	41.5	\N	2026-05-14
459	382	1	20	Varejo 28D (2026)	2026-05-01	18.438095	\N	2026-05-14
460	383	1	20	Varejo 28D (2026)	2026-05-01	18.438095	\N	2026-05-14
461	4	1	20	Varejo 28D (2026)	2026-05-01	28.125	\N	2026-05-14
462	5	1	20	Varejo 28D (2026)	2026-05-01	28.125	\N	2026-05-14
463	6	1	20	Varejo 28D (2026)	2026-05-01	70.17544	\N	2026-05-14
464	7	1	20	Varejo 28D (2026)	2026-05-01	65.37288	\N	2026-05-14
465	8	1	20	Varejo 28D (2026)	2026-05-01	65.37288	\N	2026-05-14
466	9	1	20	Varejo 28D (2026)	2026-05-01	44.188282	\N	2026-05-14
467	10	1	20	Varejo 28D (2026)	2026-05-01	44.188282	\N	2026-05-14
468	16	1	20	Varejo 28D (2026)	2026-05-01	115	\N	2026-05-14
469	13	1	20	Varejo 28D (2026)	2026-05-01	30.51	\N	2026-05-14
470	14	1	20	Varejo 28D (2026)	2026-05-01	30.51	\N	2026-05-14
471	15	1	20	Varejo 28D (2026)	2026-05-01	33.09	\N	2026-05-14
472	12	1	20	Varejo 28D (2026)	2026-05-01	35.9	\N	2026-05-14
473	11	1	20	Varejo 28D (2026)	2026-05-01	36.5	\N	2026-05-14
474	18	1	20	Varejo 28D (2026)	2026-05-01	10.045455	\N	2026-05-14
475	17	1	20	Varejo 28D (2026)	2026-05-01	10.045455	\N	2026-05-14
476	19	1	20	Varejo 28D (2026)	2026-05-01	12.272727	\N	2026-05-14
477	20	1	20	Varejo 28D (2026)	2026-05-01	12.272727	\N	2026-05-14
478	27	1	20	Varejo 28D (2026)	2026-05-01	41.5	\N	2026-05-14
479	29	1	20	Varejo 28D (2026)	2026-05-01	43.2	\N	2026-05-14
480	31	1	20	Varejo 28D (2026)	2026-05-01	40.5	\N	2026-05-14
481	2	1	21	Rede 28D (2026)	2026-05-01	23.565653	\N	2026-05-14
482	3	1	21	Rede 28D (2026)	2026-05-01	23.565653	\N	2026-05-14
483	1	1	21	Rede 28D (2026)	2026-05-01	42.5375	\N	2026-05-14
484	382	1	21	Rede 28D (2026)	2026-05-01	18.714666	\N	2026-05-14
485	383	1	21	Rede 28D (2026)	2026-05-01	18.714666	\N	2026-05-14
486	4	1	21	Rede 28D (2026)	2026-05-01	28.546875	\N	2026-05-14
487	5	1	21	Rede 28D (2026)	2026-05-01	28.546875	\N	2026-05-14
488	6	1	21	Rede 28D (2026)	2026-05-01	70.87719	\N	2026-05-14
489	7	1	21	Rede 28D (2026)	2026-05-01	66.02661	\N	2026-05-14
490	8	1	21	Rede 28D (2026)	2026-05-01	66.02661	\N	2026-05-14
491	9	1	21	Rede 28D (2026)	2026-05-01	44.630165	\N	2026-05-14
492	10	1	21	Rede 28D (2026)	2026-05-01	44.630165	\N	2026-05-14
493	16	1	21	Rede 28D (2026)	2026-05-01	117.3	\N	2026-05-14
494	13	1	21	Rede 28D (2026)	2026-05-01	30.8151	\N	2026-05-14
495	14	1	21	Rede 28D (2026)	2026-05-01	30.8151	\N	2026-05-14
496	15	1	21	Rede 28D (2026)	2026-05-01	33.7518	\N	2026-05-14
497	12	1	21	Rede 28D (2026)	2026-05-01	36.259	\N	2026-05-14
498	11	1	21	Rede 28D (2026)	2026-05-01	36.865	\N	2026-05-14
499	18	1	21	Rede 28D (2026)	2026-05-01	10.246364	\N	2026-05-14
500	17	1	21	Rede 28D (2026)	2026-05-01	10.246364	\N	2026-05-14
501	19	1	21	Rede 28D (2026)	2026-05-01	12.518182	\N	2026-05-14
502	20	1	21	Rede 28D (2026)	2026-05-01	12.518182	\N	2026-05-14
503	27	1	21	Rede 28D (2026)	2026-05-01	42.33	\N	2026-05-14
504	29	1	21	Rede 28D (2026)	2026-05-01	44.064	\N	2026-05-14
505	31	1	21	Rede 28D (2026)	2026-05-01	41.31	\N	2026-05-14
506	2	1	22	Rede 42D (2026)	2026-05-01	23.89557	\N	2026-05-14
507	3	1	22	Rede 42D (2026)	2026-05-01	23.89557	\N	2026-05-14
508	1	1	22	Rede 42D (2026)	2026-05-01	43.133026	\N	2026-05-14
509	382	1	22	Rede 42D (2026)	2026-05-01	18.976671	\N	2026-05-14
510	383	1	22	Rede 42D (2026)	2026-05-01	18.976671	\N	2026-05-14
511	4	1	22	Rede 42D (2026)	2026-05-01	28.946531	\N	2026-05-14
512	5	1	22	Rede 42D (2026)	2026-05-01	28.946531	\N	2026-05-14
513	6	1	22	Rede 42D (2026)	2026-05-01	71.58597	\N	2026-05-14
514	7	1	22	Rede 42D (2026)	2026-05-01	66.686874	\N	2026-05-14
515	8	1	22	Rede 42D (2026)	2026-05-01	66.686874	\N	2026-05-14
516	9	1	22	Rede 42D (2026)	2026-05-01	45.076466	\N	2026-05-14
517	10	1	22	Rede 42D (2026)	2026-05-01	45.076466	\N	2026-05-14
518	16	1	22	Rede 42D (2026)	2026-05-01	118.9422	\N	2026-05-14
519	13	1	22	Rede 42D (2026)	2026-05-01	31.123251	\N	2026-05-14
520	14	1	22	Rede 42D (2026)	2026-05-01	31.123251	\N	2026-05-14
521	15	1	22	Rede 42D (2026)	2026-05-01	34.224327	\N	2026-05-14
522	12	1	22	Rede 42D (2026)	2026-05-01	36.62159	\N	2026-05-14
523	11	1	22	Rede 42D (2026)	2026-05-01	37.23365	\N	2026-05-14
524	18	1	22	Rede 42D (2026)	2026-05-01	10.389812	\N	2026-05-14
525	17	1	22	Rede 42D (2026)	2026-05-01	10.389812	\N	2026-05-14
526	19	1	22	Rede 42D (2026)	2026-05-01	12.693437	\N	2026-05-14
527	20	1	22	Rede 42D (2026)	2026-05-01	12.693437	\N	2026-05-14
528	27	1	22	Rede 42D (2026)	2026-05-01	42.92262	\N	2026-05-14
529	29	1	22	Rede 42D (2026)	2026-05-01	44.680897	\N	2026-05-14
530	31	1	22	Rede 42D (2026)	2026-05-01	41.88834	\N	2026-05-14
531	2	1	23	Atacado 7D (2026)	2026-05-01	20.961027	\N	2026-05-14
532	3	1	23	Atacado 7D (2026)	2026-05-01	20.961027	\N	2026-05-14
533	1	1	23	Atacado 7D (2026)	2026-05-01	36.04873	\N	2026-05-14
534	382	1	23	Atacado 7D (2026)	2026-05-01	16.561651	\N	2026-05-14
535	383	1	23	Atacado 7D (2026)	2026-05-01	16.561651	\N	2026-05-14
536	4	1	23	Atacado 7D (2026)	2026-05-01	25.041119	\N	2026-05-14
537	5	1	23	Atacado 7D (2026)	2026-05-01	25.041119	\N	2026-05-14
538	6	1	23	Atacado 7D (2026)	2026-05-01	62.172977	\N	2026-05-14
539	7	1	23	Atacado 7D (2026)	2026-05-01	57.91808	\N	2026-05-14
540	8	1	23	Atacado 7D (2026)	2026-05-01	57.91808	\N	2026-05-14
541	9	1	23	Atacado 7D (2026)	2026-05-01	39.149265	\N	2026-05-14
542	10	1	23	Atacado 7D (2026)	2026-05-01	39.149265	\N	2026-05-14
543	16	1	23	Atacado 7D (2026)	2026-05-01	108.611115	\N	2026-05-14
544	13	1	23	Atacado 7D (2026)	2026-05-01	26.795738	\N	2026-05-14
545	14	1	23	Atacado 7D (2026)	2026-05-01	26.795738	\N	2026-05-14
546	15	1	23	Atacado 7D (2026)	2026-05-01	29.349392	\N	2026-05-14
547	12	1	23	Atacado 7D (2026)	2026-05-01	31.529566	\N	2026-05-14
548	11	1	23	Atacado 7D (2026)	2026-05-01	32.056522	\N	2026-05-14
549	18	1	23	Atacado 7D (2026)	2026-05-01	9.487373	\N	2026-05-14
550	17	1	23	Atacado 7D (2026)	2026-05-01	9.487373	\N	2026-05-14
551	19	1	23	Atacado 7D (2026)	2026-05-01	11.590909	\N	2026-05-14
552	20	1	23	Atacado 7D (2026)	2026-05-01	11.590909	\N	2026-05-14
553	27	1	23	Atacado 7D (2026)	2026-05-01	39.194443	\N	2026-05-14
554	29	1	23	Atacado 7D (2026)	2026-05-01	40.8	\N	2026-05-14
555	31	1	23	Atacado 7D (2026)	2026-05-01	38.25	\N	2026-05-14
556	2	1	24	Atacado 28D (2026)	2026-05-01	18.632025	\N	2026-05-14
557	3	1	24	Atacado 28D (2026)	2026-05-01	18.632025	\N	2026-05-14
558	1	1	24	Atacado 28D (2026)	2026-05-01	32.043316	\N	2026-05-14
559	382	1	24	Atacado 28D (2026)	2026-05-01	14.721468	\N	2026-05-14
560	383	1	24	Atacado 28D (2026)	2026-05-01	14.721468	\N	2026-05-14
561	4	1	24	Atacado 28D (2026)	2026-05-01	22.258772	\N	2026-05-14
562	5	1	24	Atacado 28D (2026)	2026-05-01	22.258772	\N	2026-05-14
563	6	1	24	Atacado 28D (2026)	2026-05-01	55.26487	\N	2026-05-14
564	7	1	24	Atacado 28D (2026)	2026-05-01	51.48274	\N	2026-05-14
565	8	1	24	Atacado 28D (2026)	2026-05-01	51.48274	\N	2026-05-14
566	9	1	24	Atacado 28D (2026)	2026-05-01	34.799347	\N	2026-05-14
567	10	1	24	Atacado 28D (2026)	2026-05-01	34.799347	\N	2026-05-14
568	16	1	24	Atacado 28D (2026)	2026-05-01	100.56584	\N	2026-05-14
569	13	1	24	Atacado 28D (2026)	2026-05-01	23.818436	\N	2026-05-14
570	14	1	24	Atacado 28D (2026)	2026-05-01	23.818436	\N	2026-05-14
571	15	1	24	Atacado 28D (2026)	2026-05-01	26.088348	\N	2026-05-14
572	12	1	24	Atacado 28D (2026)	2026-05-01	28.02628	\N	2026-05-14
573	11	1	24	Atacado 28D (2026)	2026-05-01	28.494686	\N	2026-05-14
574	18	1	24	Atacado 28D (2026)	2026-05-01	8.433221	\N	2026-05-14
575	17	1	24	Atacado 28D (2026)	2026-05-01	8.433221	\N	2026-05-14
576	19	1	24	Atacado 28D (2026)	2026-05-01	10.30303	\N	2026-05-14
577	20	1	24	Atacado 28D (2026)	2026-05-01	10.30303	\N	2026-05-14
578	27	1	24	Atacado 28D (2026)	2026-05-01	34.839508	\N	2026-05-14
579	29	1	24	Atacado 28D (2026)	2026-05-01	36.266666	\N	2026-05-14
580	31	1	24	Atacado 28D (2026)	2026-05-01	34	\N	2026-05-14
581	2	1	20	Varejo 28D (2026)	2026-05-01	23.22	\N	2026-05-16
582	3	1	20	Varejo 28D (2026)	2026-05-01	23.22	\N	2026-05-16
583	1	1	20	Varejo 28D (2026)	2026-05-01	41.5	\N	2026-05-16
584	382	1	20	Varejo 28D (2026)	2026-05-01	18.44	\N	2026-05-16
585	383	1	20	Varejo 28D (2026)	2026-05-01	18.44	\N	2026-05-16
586	4	1	20	Varejo 28D (2026)	2026-05-01	28.13	\N	2026-05-16
587	5	1	20	Varejo 28D (2026)	2026-05-01	28.13	\N	2026-05-16
588	6	1	20	Varejo 28D (2026)	2026-05-01	70.18	\N	2026-05-16
589	7	1	20	Varejo 28D (2026)	2026-05-01	65.37	\N	2026-05-16
590	8	1	20	Varejo 28D (2026)	2026-05-01	65.37	\N	2026-05-16
591	9	1	20	Varejo 28D (2026)	2026-05-01	44.19	\N	2026-05-16
592	10	1	20	Varejo 28D (2026)	2026-05-01	44.19	\N	2026-05-16
593	16	1	20	Varejo 28D (2026)	2026-05-01	115	\N	2026-05-16
594	13	1	20	Varejo 28D (2026)	2026-05-01	30.51	\N	2026-05-16
595	14	1	20	Varejo 28D (2026)	2026-05-01	30.51	\N	2026-05-16
596	15	1	20	Varejo 28D (2026)	2026-05-01	33.09	\N	2026-05-16
597	12	1	20	Varejo 28D (2026)	2026-05-01	35.9	\N	2026-05-16
598	11	1	20	Varejo 28D (2026)	2026-05-01	36.5	\N	2026-05-16
599	18	1	20	Varejo 28D (2026)	2026-05-01	10.05	\N	2026-05-16
600	17	1	20	Varejo 28D (2026)	2026-05-01	10.05	\N	2026-05-16
601	19	1	20	Varejo 28D (2026)	2026-05-01	12.27	\N	2026-05-16
602	20	1	20	Varejo 28D (2026)	2026-05-01	12.27	\N	2026-05-16
603	27	1	20	Varejo 28D (2026)	2026-05-01	41.5	\N	2026-05-16
604	29	1	20	Varejo 28D (2026)	2026-05-01	43.2	\N	2026-05-16
605	31	1	20	Varejo 28D (2026)	2026-05-01	40.5	\N	2026-05-16
606	2	1	21	Rede 28D (2026)	2026-05-01	23.57	\N	2026-05-16
607	3	1	21	Rede 28D (2026)	2026-05-01	23.57	\N	2026-05-16
608	1	1	21	Rede 28D (2026)	2026-05-01	42.54	\N	2026-05-16
609	382	1	21	Rede 28D (2026)	2026-05-01	18.71	\N	2026-05-16
610	383	1	21	Rede 28D (2026)	2026-05-01	18.71	\N	2026-05-16
611	4	1	21	Rede 28D (2026)	2026-05-01	28.55	\N	2026-05-16
612	5	1	21	Rede 28D (2026)	2026-05-01	28.55	\N	2026-05-16
613	6	1	21	Rede 28D (2026)	2026-05-01	70.88	\N	2026-05-16
614	7	1	21	Rede 28D (2026)	2026-05-01	66.03	\N	2026-05-16
615	8	1	21	Rede 28D (2026)	2026-05-01	66.03	\N	2026-05-16
616	9	1	21	Rede 28D (2026)	2026-05-01	44.63	\N	2026-05-16
617	10	1	21	Rede 28D (2026)	2026-05-01	44.63	\N	2026-05-16
618	16	1	21	Rede 28D (2026)	2026-05-01	117.3	\N	2026-05-16
619	13	1	21	Rede 28D (2026)	2026-05-01	30.82	\N	2026-05-16
620	14	1	21	Rede 28D (2026)	2026-05-01	30.82	\N	2026-05-16
621	15	1	21	Rede 28D (2026)	2026-05-01	33.75	\N	2026-05-16
622	12	1	21	Rede 28D (2026)	2026-05-01	36.26	\N	2026-05-16
623	11	1	21	Rede 28D (2026)	2026-05-01	36.87	\N	2026-05-16
624	18	1	21	Rede 28D (2026)	2026-05-01	10.25	\N	2026-05-16
625	17	1	21	Rede 28D (2026)	2026-05-01	10.25	\N	2026-05-16
626	19	1	21	Rede 28D (2026)	2026-05-01	12.52	\N	2026-05-16
627	20	1	21	Rede 28D (2026)	2026-05-01	12.52	\N	2026-05-16
628	27	1	21	Rede 28D (2026)	2026-05-01	42.33	\N	2026-05-16
629	29	1	21	Rede 28D (2026)	2026-05-01	44.06	\N	2026-05-16
630	31	1	21	Rede 28D (2026)	2026-05-01	41.31	\N	2026-05-16
631	2	1	22	Rede 42D (2026)	2026-05-01	23.9	\N	2026-05-16
632	3	1	22	Rede 42D (2026)	2026-05-01	23.9	\N	2026-05-16
633	1	1	22	Rede 42D (2026)	2026-05-01	43.13	\N	2026-05-16
634	382	1	22	Rede 42D (2026)	2026-05-01	18.98	\N	2026-05-16
635	383	1	22	Rede 42D (2026)	2026-05-01	18.98	\N	2026-05-16
636	4	1	22	Rede 42D (2026)	2026-05-01	28.95	\N	2026-05-16
637	5	1	22	Rede 42D (2026)	2026-05-01	28.95	\N	2026-05-16
638	6	1	22	Rede 42D (2026)	2026-05-01	71.59	\N	2026-05-16
639	7	1	22	Rede 42D (2026)	2026-05-01	66.69	\N	2026-05-16
640	8	1	22	Rede 42D (2026)	2026-05-01	66.69	\N	2026-05-16
641	9	1	22	Rede 42D (2026)	2026-05-01	45.08	\N	2026-05-16
642	10	1	22	Rede 42D (2026)	2026-05-01	45.08	\N	2026-05-16
643	16	1	22	Rede 42D (2026)	2026-05-01	118.94	\N	2026-05-16
644	13	1	22	Rede 42D (2026)	2026-05-01	31.12	\N	2026-05-16
645	14	1	22	Rede 42D (2026)	2026-05-01	31.12	\N	2026-05-16
646	15	1	22	Rede 42D (2026)	2026-05-01	34.22	\N	2026-05-16
647	12	1	22	Rede 42D (2026)	2026-05-01	36.62	\N	2026-05-16
648	11	1	22	Rede 42D (2026)	2026-05-01	37.23	\N	2026-05-16
649	18	1	22	Rede 42D (2026)	2026-05-01	10.39	\N	2026-05-16
650	17	1	22	Rede 42D (2026)	2026-05-01	10.39	\N	2026-05-16
651	19	1	22	Rede 42D (2026)	2026-05-01	12.69	\N	2026-05-16
652	20	1	22	Rede 42D (2026)	2026-05-01	12.69	\N	2026-05-16
653	27	1	22	Rede 42D (2026)	2026-05-01	42.92	\N	2026-05-16
654	29	1	22	Rede 42D (2026)	2026-05-01	44.68	\N	2026-05-16
655	31	1	22	Rede 42D (2026)	2026-05-01	41.89	\N	2026-05-16
656	2	1	23	Atacado 7D (2026)	2026-05-01	20.96	\N	2026-05-16
657	3	1	23	Atacado 7D (2026)	2026-05-01	20.96	\N	2026-05-16
658	1	1	23	Atacado 7D (2026)	2026-05-01	36.05	\N	2026-05-16
659	382	1	23	Atacado 7D (2026)	2026-05-01	16.56	\N	2026-05-16
660	383	1	23	Atacado 7D (2026)	2026-05-01	16.56	\N	2026-05-16
661	4	1	23	Atacado 7D (2026)	2026-05-01	25.04	\N	2026-05-16
662	5	1	23	Atacado 7D (2026)	2026-05-01	25.04	\N	2026-05-16
663	6	1	23	Atacado 7D (2026)	2026-05-01	62.17	\N	2026-05-16
664	7	1	23	Atacado 7D (2026)	2026-05-01	57.92	\N	2026-05-16
665	8	1	23	Atacado 7D (2026)	2026-05-01	57.92	\N	2026-05-16
666	9	1	23	Atacado 7D (2026)	2026-05-01	39.15	\N	2026-05-16
667	10	1	23	Atacado 7D (2026)	2026-05-01	39.15	\N	2026-05-16
668	16	1	23	Atacado 7D (2026)	2026-05-01	108.61	\N	2026-05-16
669	13	1	23	Atacado 7D (2026)	2026-05-01	26.8	\N	2026-05-16
670	14	1	23	Atacado 7D (2026)	2026-05-01	26.8	\N	2026-05-16
671	15	1	23	Atacado 7D (2026)	2026-05-01	29.35	\N	2026-05-16
672	12	1	23	Atacado 7D (2026)	2026-05-01	31.53	\N	2026-05-16
673	11	1	23	Atacado 7D (2026)	2026-05-01	32.06	\N	2026-05-16
674	18	1	23	Atacado 7D (2026)	2026-05-01	9.49	\N	2026-05-16
675	17	1	23	Atacado 7D (2026)	2026-05-01	9.49	\N	2026-05-16
676	19	1	23	Atacado 7D (2026)	2026-05-01	11.59	\N	2026-05-16
677	20	1	23	Atacado 7D (2026)	2026-05-01	11.59	\N	2026-05-16
678	27	1	23	Atacado 7D (2026)	2026-05-01	39.19	\N	2026-05-16
679	29	1	23	Atacado 7D (2026)	2026-05-01	40.8	\N	2026-05-16
680	31	1	23	Atacado 7D (2026)	2026-05-01	38.25	\N	2026-05-16
681	2	1	24	Atacado 28D (2026)	2026-05-01	18.63	\N	2026-05-16
682	3	1	24	Atacado 28D (2026)	2026-05-01	18.63	\N	2026-05-16
683	1	1	24	Atacado 28D (2026)	2026-05-01	32.04	\N	2026-05-16
684	382	1	24	Atacado 28D (2026)	2026-05-01	14.72	\N	2026-05-16
685	383	1	24	Atacado 28D (2026)	2026-05-01	14.72	\N	2026-05-16
686	4	1	24	Atacado 28D (2026)	2026-05-01	22.26	\N	2026-05-16
687	5	1	24	Atacado 28D (2026)	2026-05-01	22.26	\N	2026-05-16
688	6	1	24	Atacado 28D (2026)	2026-05-01	55.26	\N	2026-05-16
689	7	1	24	Atacado 28D (2026)	2026-05-01	51.48	\N	2026-05-16
690	8	1	24	Atacado 28D (2026)	2026-05-01	51.48	\N	2026-05-16
691	9	1	24	Atacado 28D (2026)	2026-05-01	34.8	\N	2026-05-16
692	10	1	24	Atacado 28D (2026)	2026-05-01	34.8	\N	2026-05-16
693	16	1	24	Atacado 28D (2026)	2026-05-01	100.57	\N	2026-05-16
694	13	1	24	Atacado 28D (2026)	2026-05-01	23.82	\N	2026-05-16
695	14	1	24	Atacado 28D (2026)	2026-05-01	23.82	\N	2026-05-16
696	15	1	24	Atacado 28D (2026)	2026-05-01	26.09	\N	2026-05-16
697	12	1	24	Atacado 28D (2026)	2026-05-01	28.03	\N	2026-05-16
698	11	1	24	Atacado 28D (2026)	2026-05-01	28.49	\N	2026-05-16
699	18	1	24	Atacado 28D (2026)	2026-05-01	8.43	\N	2026-05-16
700	17	1	24	Atacado 28D (2026)	2026-05-01	8.43	\N	2026-05-16
701	19	1	24	Atacado 28D (2026)	2026-05-01	10.3	\N	2026-05-16
702	20	1	24	Atacado 28D (2026)	2026-05-01	10.3	\N	2026-05-16
703	27	1	24	Atacado 28D (2026)	2026-05-01	34.84	\N	2026-05-16
704	29	1	24	Atacado 28D (2026)	2026-05-01	36.27	\N	2026-05-16
705	31	1	24	Atacado 28D (2026)	2026-05-01	34	\N	2026-05-16
1	1	1	1	Varejo 28d (2025)	2025-02-01	41.2	\N	2025-02-01
2	2	1	1	Varejo 28d (2025)	2025-02-01	24.35	\N	2025-02-01
3	3	1	1	Varejo 28d (2025)	2025-02-01	24.35	\N	2025-02-01
4	4	1	1	Varejo 28d (2025)	2025-02-01	28.13	\N	2025-02-01
5	5	1	1	Varejo 28d (2025)	2025-02-01	27.59	\N	2025-02-01
6	6	1	1	Varejo 28d (2025)	2025-02-01	74.91	\N	2025-02-01
7	7	1	1	Varejo 28d (2025)	2025-02-01	69.07	\N	2025-02-01
8	8	1	1	Varejo 28d (2025)	2025-02-01	69.07	\N	2025-02-01
9	9	1	1	Varejo 28d (2025)	2025-02-01	46.35	\N	2025-02-01
10	10	1	1	Varejo 28d (2025)	2025-02-01	46.35	\N	2025-02-01
11	11	1	1	Varejo 28d (2025)	2025-02-01	30.39	\N	2025-02-01
12	12	1	1	Varejo 28d (2025)	2025-02-01	20.87	\N	2025-02-01
13	13	1	1	Varejo 28d (2025)	2025-02-01	19.6	\N	2025-02-01
14	14	1	1	Varejo 28d (2025)	2025-02-01	19.6	\N	2025-02-01
15	15	1	1	Varejo 28d (2025)	2025-02-01	22.76	\N	2025-02-01
16	16	1	1	Varejo 28d (2025)	2025-02-01	108.15	\N	2025-02-01
17	17	1	1	Varejo 28d (2025)	2025-02-01	10.2	\N	2025-02-01
18	18	1	1	Varejo 28d (2025)	2025-02-01	10.2	\N	2025-02-01
19	19	1	1	Varejo 28d (2025)	2025-02-01	12.83	\N	2025-02-01
20	20	1	1	Varejo 28d (2025)	2025-02-01	12.83	\N	2025-02-01
21	21	1	1	Varejo 28d (2025)	2025-02-01	29.15	\N	2025-02-01
22	22	1	1	Varejo 28d (2025)	2025-02-01	27.21	\N	2025-02-01
23	23	1	1	Varejo 28d (2025)	2025-02-01	27.21	\N	2025-02-01
24	24	1	1	Varejo 28d (2025)	2025-02-01	272.54	\N	2025-02-01
25	25	1	1	Varejo 28d (2025)	2025-02-01	229.28	\N	2025-02-01
26	26	1	1	Varejo 28d (2025)	2025-02-01	172.61	\N	2025-02-01
27	27	1	1	Varejo 28d (2025)	2025-02-01	42.64	\N	2025-02-01
28	28	1	1	Varejo 28d (2025)	2025-02-01	50.06	\N	2025-02-01
29	29	1	1	Varejo 28d (2025)	2025-02-01	46.35	\N	2025-02-01
30	30	1	1	Varejo 28d (2025)	2025-02-01	39.55	\N	2025-02-01
31	31	1	1	Varejo 28d (2025)	2025-02-01	41.15	\N	2025-02-01
32	1	1	2	Rede 28d (2025)	2025-02-01	40	\N	2025-02-01
33	2	1	2	Rede 28d (2025)	2025-02-01	23.64	\N	2025-02-01
34	3	1	2	Rede 28d (2025)	2025-02-01	23.64	\N	2025-02-01
35	4	1	2	Rede 28d (2025)	2025-02-01	26.79	\N	2025-02-01
36	5	1	2	Rede 28d (2025)	2025-02-01	26.79	\N	2025-02-01
37	6	1	2	Rede 28d (2025)	2025-02-01	72.73	\N	2025-02-01
38	7	1	2	Rede 28d (2025)	2025-02-01	67.05	\N	2025-02-01
39	8	1	2	Rede 28d (2025)	2025-02-01	67.05	\N	2025-02-01
40	9	1	2	Rede 28d (2025)	2025-02-01	45	\N	2025-02-01
41	10	1	2	Rede 28d (2025)	2025-02-01	45	\N	2025-02-01
42	11	1	2	Rede 28d (2025)	2025-02-01	29.5	\N	2025-02-01
43	12	1	2	Rede 28d (2025)	2025-02-01	20.27	\N	2025-02-01
44	13	1	2	Rede 28d (2025)	2025-02-01	19.03	\N	2025-02-01
45	14	1	2	Rede 28d (2025)	2025-02-01	19.03	\N	2025-02-01
46	15	1	2	Rede 28d (2025)	2025-02-01	22.1	\N	2025-02-01
47	16	1	2	Rede 28d (2025)	2025-02-01	105	\N	2025-02-01
48	17	1	2	Rede 28d (2025)	2025-02-01	9.91	\N	2025-02-01
49	18	1	2	Rede 28d (2025)	2025-02-01	9.91	\N	2025-02-01
50	19	1	2	Rede 28d (2025)	2025-02-01	12.45	\N	2025-02-01
51	20	1	2	Rede 28d (2025)	2025-02-01	12.45	\N	2025-02-01
52	21	1	2	Rede 28d (2025)	2025-02-01	28.3	\N	2025-02-01
53	22	1	2	Rede 28d (2025)	2025-02-01	26.42	\N	2025-02-01
54	23	1	2	Rede 28d (2025)	2025-02-01	26.42	\N	2025-02-01
55	24	1	2	Rede 28d (2025)	2025-02-01	264.6	\N	2025-02-01
56	25	1	2	Rede 28d (2025)	2025-02-01	222.6	\N	2025-02-01
57	26	1	2	Rede 28d (2025)	2025-02-01	167.58	\N	2025-02-01
58	27	1	2	Rede 28d (2025)	2025-02-01	41.4	\N	2025-02-01
59	28	1	2	Rede 28d (2025)	2025-02-01	48.6	\N	2025-02-01
60	29	1	2	Rede 28d (2025)	2025-02-01	45	\N	2025-02-01
61	30	1	2	Rede 28d (2025)	2025-02-01	38.4	\N	2025-02-01
62	31	1	2	Rede 28d (2025)	2025-02-01	39.95	\N	2025-02-01
63	1	1	3	Rede 42d (2025)	2025-02-01	42.06	\N	2025-02-01
64	2	1	3	Rede 42d (2025)	2025-02-01	24.85	\N	2025-02-01
65	3	1	3	Rede 42d (2025)	2025-02-01	24.85	\N	2025-02-01
66	4	1	3	Rede 42d (2025)	2025-02-01	28.17	\N	2025-02-01
67	5	1	3	Rede 42d (2025)	2025-02-01	28.17	\N	2025-02-01
68	6	1	3	Rede 42d (2025)	2025-02-01	76.47	\N	2025-02-01
69	7	1	3	Rede 42d (2025)	2025-02-01	70.51	\N	2025-02-01
70	8	1	3	Rede 42d (2025)	2025-02-01	70.51	\N	2025-02-01
71	9	1	3	Rede 42d (2025)	2025-02-01	47.32	\N	2025-02-01
72	10	1	3	Rede 42d (2025)	2025-02-01	47.32	\N	2025-02-01
73	11	1	3	Rede 42d (2025)	2025-02-01	31.02	\N	2025-02-01
74	12	1	3	Rede 42d (2025)	2025-02-01	21.31	\N	2025-02-01
75	13	1	3	Rede 42d (2025)	2025-02-01	20.01	\N	2025-02-01
76	14	1	3	Rede 42d (2025)	2025-02-01	20.01	\N	2025-02-01
77	15	1	3	Rede 42d (2025)	2025-02-01	23.24	\N	2025-02-01
78	16	1	3	Rede 42d (2025)	2025-02-01	110.82	\N	2025-02-01
79	17	1	3	Rede 42d (2025)	2025-02-01	10.42	\N	2025-02-01
80	18	1	3	Rede 42d (2025)	2025-02-01	10.42	\N	2025-02-01
81	19	1	3	Rede 42d (2025)	2025-02-01	13.09	\N	2025-02-01
82	20	1	3	Rede 42d (2025)	2025-02-01	13.09	\N	2025-02-01
83	21	1	3	Rede 42d (2025)	2025-02-01	29.76	\N	2025-02-01
84	22	1	3	Rede 42d (2025)	2025-02-01	27.78	\N	2025-02-01
85	23	1	3	Rede 42d (2025)	2025-02-01	27.78	\N	2025-02-01
86	24	1	3	Rede 42d (2025)	2025-02-01	278.23	\N	2025-02-01
87	25	1	3	Rede 42d (2025)	2025-02-01	234.07	\N	2025-02-01
88	26	1	3	Rede 42d (2025)	2025-02-01	176.21	\N	2025-02-01
89	27	1	3	Rede 42d (2025)	2025-02-01	43.53	\N	2025-02-01
90	28	1	3	Rede 42d (2025)	2025-02-01	51.1	\N	2025-02-01
91	29	1	3	Rede 42d (2025)	2025-02-01	47.32	\N	2025-02-01
92	30	1	3	Rede 42d (2025)	2025-02-01	40.38	\N	2025-02-01
93	31	1	3	Rede 42d (2025)	2025-02-01	42.01	\N	2025-02-01
94	1	1	4	Atacado à vista (2025)	2025-02-01	32	\N	2025-02-01
95	2	1	4	Atacado à vista (2025)	2025-02-01	18.91	\N	2025-02-01
96	3	1	4	Atacado à vista (2025)	2025-02-01	18.91	\N	2025-02-01
97	4	1	4	Atacado à vista (2025)	2025-02-01	21.43	\N	2025-02-01
98	5	1	4	Atacado à vista (2025)	2025-02-01	21.43	\N	2025-02-01
99	6	1	4	Atacado à vista (2025)	2025-02-01	66.12	\N	2025-02-01
100	7	1	4	Atacado à vista (2025)	2025-02-01	60.96	\N	2025-02-01
101	8	1	4	Atacado à vista (2025)	2025-02-01	60.96	\N	2025-02-01
102	9	1	4	Atacado à vista (2025)	2025-02-01	45	\N	2025-02-01
103	10	1	4	Atacado à vista (2025)	2025-02-01	45	\N	2025-02-01
104	11	1	4	Atacado à vista (2025)	2025-02-01	28.1	\N	2025-02-01
105	12	1	4	Atacado à vista (2025)	2025-02-01	19.3	\N	2025-02-01
106	13	1	4	Atacado à vista (2025)	2025-02-01	18.12	\N	2025-02-01
107	14	1	4	Atacado à vista (2025)	2025-02-01	18.12	\N	2025-02-01
108	15	1	4	Atacado à vista (2025)	2025-02-01	21.05	\N	2025-02-01
109	16	1	4	Atacado à vista (2025)	2025-02-01	105	\N	2025-02-01
110	17	1	4	Atacado à vista (2025)	2025-02-01	8.25	\N	2025-02-01
111	18	1	4	Atacado à vista (2025)	2025-02-01	8.25	\N	2025-02-01
112	19	1	4	Atacado à vista (2025)	2025-02-01	10.38	\N	2025-02-01
113	20	1	4	Atacado à vista (2025)	2025-02-01	10.38	\N	2025-02-01
114	21	1	4	Atacado à vista (2025)	2025-02-01	23.58	\N	2025-02-01
115	22	1	4	Atacado à vista (2025)	2025-02-01	22.01	\N	2025-02-01
116	23	1	4	Atacado à vista (2025)	2025-02-01	22.01	\N	2025-02-01
117	24	1	4	Atacado à vista (2025)	2025-02-01	264.6	\N	2025-02-01
118	25	1	4	Atacado à vista (2025)	2025-02-01	222.6	\N	2025-02-01
119	26	1	4	Atacado à vista (2025)	2025-02-01	167.58	\N	2025-02-01
120	27	1	4	Atacado à vista (2025)	2025-02-01	37.64	\N	2025-02-01
121	28	1	4	Atacado à vista (2025)	2025-02-01	44.18	\N	2025-02-01
122	29	1	4	Atacado à vista (2025)	2025-02-01	40.91	\N	2025-02-01
123	30	1	4	Atacado à vista (2025)	2025-02-01	34.91	\N	2025-02-01
124	31	1	4	Atacado à vista (2025)	2025-02-01	36.32	\N	2025-02-01
125	1	1	5	Atacado 28d (2025)	2025-02-01	33.08	\N	2025-02-01
126	2	1	5	Atacado 28d (2025)	2025-02-01	19.55	\N	2025-02-01
127	3	1	5	Atacado 28d (2025)	2025-02-01	19.55	\N	2025-02-01
128	4	1	5	Atacado 28d (2025)	2025-02-01	22.15	\N	2025-02-01
129	5	1	5	Atacado 28d (2025)	2025-02-01	22.15	\N	2025-02-01
130	6	1	5	Atacado 28d (2025)	2025-02-01	68.35	\N	2025-02-01
131	7	1	5	Atacado 28d (2025)	2025-02-01	63.02	\N	2025-02-01
132	8	1	5	Atacado 28d (2025)	2025-02-01	63.02	\N	2025-02-01
133	9	1	5	Atacado 28d (2025)	2025-02-01	46.52	\N	2025-02-01
134	10	1	5	Atacado 28d (2025)	2025-02-01	46.52	\N	2025-02-01
135	11	1	5	Atacado 28d (2025)	2025-02-01	29.05	\N	2025-02-01
136	12	1	5	Atacado 28d (2025)	2025-02-01	19.95	\N	2025-02-01
137	13	1	5	Atacado 28d (2025)	2025-02-01	18.73	\N	2025-02-01
138	14	1	5	Atacado 28d (2025)	2025-02-01	18.73	\N	2025-02-01
139	15	1	5	Atacado 28d (2025)	2025-02-01	21.76	\N	2025-02-01
140	16	1	5	Atacado 28d (2025)	2025-02-01	105	\N	2025-02-01
141	17	1	5	Atacado 28d (2025)	2025-02-01	8.53	\N	2025-02-01
142	18	1	5	Atacado 28d (2025)	2025-02-01	8.53	\N	2025-02-01
143	19	1	5	Atacado 28d (2025)	2025-02-01	10.73	\N	2025-02-01
144	20	1	5	Atacado 28d (2025)	2025-02-01	10.73	\N	2025-02-01
145	21	1	5	Atacado 28d (2025)	2025-02-01	24.38	\N	2025-02-01
146	22	1	5	Atacado 28d (2025)	2025-02-01	22.76	\N	2025-02-01
147	23	1	5	Atacado 28d (2025)	2025-02-01	22.76	\N	2025-02-01
148	24	1	5	Atacado 28d (2025)	2025-02-01	273.54	\N	2025-02-01
149	25	1	5	Atacado 28d (2025)	2025-02-01	230.13	\N	2025-02-01
150	26	1	5	Atacado 28d (2025)	2025-02-01	173.25	\N	2025-02-01
151	27	1	5	Atacado 28d (2025)	2025-02-01	38.91	\N	2025-02-01
152	28	1	5	Atacado 28d (2025)	2025-02-01	45.68	\N	2025-02-01
153	29	1	5	Atacado 28d (2025)	2025-02-01	42.29	\N	2025-02-01
154	30	1	5	Atacado 28d (2025)	2025-02-01	36.09	\N	2025-02-01
155	31	1	5	Atacado 28d (2025)	2025-02-01	37.55	\N	2025-02-01
156	32	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
157	33	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
158	34	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
159	35	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
160	36	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
161	37	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
162	38	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
163	39	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
164	40	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
165	41	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
166	42	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
167	43	2	6	Varejo 30d	2026-02-01 00:00:00	248.4	\N	2026-02-01 00:00:00
168	44	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
169	45	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
170	46	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
171	47	2	6	Varejo 30d	2026-02-01 00:00:00	223.2	\N	2026-02-01 00:00:00
172	48	2	6	Varejo 30d	2026-02-01 00:00:00	208.8	\N	2026-02-01 00:00:00
173	49	2	6	Varejo 30d	2026-02-01 00:00:00	208.8	\N	2026-02-01 00:00:00
174	50	2	6	Varejo 30d	2026-02-01 00:00:00	208.8	\N	2026-02-01 00:00:00
175	51	2	6	Varejo 30d	2026-02-01 00:00:00	208.8	\N	2026-02-01 00:00:00
176	52	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
177	53	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
178	54	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
179	55	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
180	56	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
181	57	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
182	58	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
325	249	3	12	Varejo 12d (2026)	2025-12-01	383.84	23.99	2025-12-01
183	59	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
184	60	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
185	61	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
186	62	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
187	63	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
188	64	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
189	65	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
190	66	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
191	67	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
192	68	2	6	Varejo 30d	2026-02-01 00:00:00	208.8	\N	2026-02-01 00:00:00
193	69	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
194	70	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
195	71	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
196	72	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
197	73	2	6	Varejo 30d	2026-02-01 00:00:00	195.6	\N	2026-02-01 00:00:00
198	74	2	6	Varejo 30d	2026-02-01 00:00:00	208.8	\N	2026-02-01 00:00:00
199	75	2	6	Varejo 30d	2026-02-01 00:00:00	208.8	\N	2026-02-01 00:00:00
200	76	2	6	Varejo 30d	2026-02-01 00:00:00	208.8	\N	2026-02-01 00:00:00
201	77	2	6	Varejo 30d	2026-02-01 00:00:00	208.8	\N	2026-02-01 00:00:00
202	78	2	6	Varejo 30d	2026-02-01 00:00:00	208.8	\N	2026-02-01 00:00:00
203	1	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	39.95	\N	2026-04-01 00:00:00
204	2	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	21.1	\N	2026-04-01 00:00:00
205	3	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	21.1	\N	2026-04-01 00:00:00
206	4	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	24.2	\N	2026-04-01 00:00:00
207	5	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	24.2	\N	2026-04-01 00:00:00
208	6	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	64	\N	2026-04-01 00:00:00
209	7	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	59.8	\N	2026-04-01 00:00:00
210	8	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	59.8	\N	2026-04-01 00:00:00
211	9	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	38	\N	2026-04-01 00:00:00
212	10	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	38	\N	2026-04-01 00:00:00
213	11	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	23.181818	\N	2026-04-01 00:00:00
214	12	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	19.772728	\N	2026-04-01 00:00:00
215	13	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	19.5	\N	2026-04-01 00:00:00
216	14	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	19.5	\N	2026-04-01 00:00:00
217	15	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	19.77	\N	2026-04-01 00:00:00
218	16	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	105	\N	2026-04-01 00:00:00
219	17	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	9.1	\N	2026-04-01 00:00:00
220	18	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	9.1	\N	2026-04-01 00:00:00
221	19	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	10.05	\N	2026-04-01 00:00:00
222	20	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	10.05	\N	2026-04-01 00:00:00
223	27	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	34.2	\N	2026-04-01 00:00:00
224	29	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	35.7	\N	2026-04-01 00:00:00
225	31	1	7	Varejo 28d (2026)	2026-04-01 00:00:00	33.5	\N	2026-04-01 00:00:00
226	1	1	8	Rede 28d (2026)	2026-04-01 00:00:00	40.94875	\N	2026-04-01 00:00:00
227	2	1	8	Rede 28d (2026)	2026-04-01 00:00:00	21.4165	\N	2026-04-01 00:00:00
228	3	1	8	Rede 28d (2026)	2026-04-01 00:00:00	21.4165	\N	2026-04-01 00:00:00
229	4	1	8	Rede 28d (2026)	2026-04-01 00:00:00	24.563	\N	2026-04-01 00:00:00
230	5	1	8	Rede 28d (2026)	2026-04-01 00:00:00	24.563	\N	2026-04-01 00:00:00
231	6	1	8	Rede 28d (2026)	2026-04-01 00:00:00	64.96	\N	2026-04-01 00:00:00
232	7	1	8	Rede 28d (2026)	2026-04-01 00:00:00	60.697	\N	2026-04-01 00:00:00
233	8	1	8	Rede 28d (2026)	2026-04-01 00:00:00	60.697	\N	2026-04-01 00:00:00
234	9	1	8	Rede 28d (2026)	2026-04-01 00:00:00	38.57	\N	2026-04-01 00:00:00
235	10	1	8	Rede 28d (2026)	2026-04-01 00:00:00	38.57	\N	2026-04-01 00:00:00
236	11	1	8	Rede 28d (2026)	2026-04-01 00:00:00	23.645454	\N	2026-04-01 00:00:00
237	12	1	8	Rede 28d (2026)	2026-04-01 00:00:00	20.168182	\N	2026-04-01 00:00:00
238	13	1	8	Rede 28d (2026)	2026-04-01 00:00:00	19.89	\N	2026-04-01 00:00:00
239	14	1	8	Rede 28d (2026)	2026-04-01 00:00:00	19.89	\N	2026-04-01 00:00:00
240	15	1	8	Rede 28d (2026)	2026-04-01 00:00:00	20.1654	\N	2026-04-01 00:00:00
241	16	1	8	Rede 28d (2026)	2026-04-01 00:00:00	107.1	\N	2026-04-01 00:00:00
242	17	1	8	Rede 28d (2026)	2026-04-01 00:00:00	9.282	\N	2026-04-01 00:00:00
243	18	1	8	Rede 28d (2026)	2026-04-01 00:00:00	9.282	\N	2026-04-01 00:00:00
244	19	1	8	Rede 28d (2026)	2026-04-01 00:00:00	10.251	\N	2026-04-01 00:00:00
245	20	1	8	Rede 28d (2026)	2026-04-01 00:00:00	10.251	\N	2026-04-01 00:00:00
246	27	1	8	Rede 28d (2026)	2026-04-01 00:00:00	34.884	\N	2026-04-01 00:00:00
247	29	1	8	Rede 28d (2026)	2026-04-01 00:00:00	36.414	\N	2026-04-01 00:00:00
248	31	1	8	Rede 28d (2026)	2026-04-01 00:00:00	34.17	\N	2026-04-01 00:00:00
249	1	1	9	Rede 42d (2026)	2026-04-01 00:00:00	41.96275	\N	2026-04-01 00:00:00
250	2	1	9	Rede 42d (2026)	2026-04-01 00:00:00	22.4305	\N	2026-04-01 00:00:00
251	3	1	9	Rede 42d (2026)	2026-04-01 00:00:00	22.4305	\N	2026-04-01 00:00:00
252	4	1	9	Rede 42d (2026)	2026-04-01 00:00:00	25.577	\N	2026-04-01 00:00:00
253	5	1	9	Rede 42d (2026)	2026-04-01 00:00:00	25.577	\N	2026-04-01 00:00:00
254	6	1	9	Rede 42d (2026)	2026-04-01 00:00:00	65.974	\N	2026-04-01 00:00:00
255	7	1	9	Rede 42d (2026)	2026-04-01 00:00:00	61.711	\N	2026-04-01 00:00:00
256	8	1	9	Rede 42d (2026)	2026-04-01 00:00:00	61.711	\N	2026-04-01 00:00:00
257	9	1	9	Rede 42d (2026)	2026-04-01 00:00:00	39.584	\N	2026-04-01 00:00:00
258	10	1	9	Rede 42d (2026)	2026-04-01 00:00:00	39.584	\N	2026-04-01 00:00:00
259	11	1	9	Rede 42d (2026)	2026-04-01 00:00:00	24.659454	\N	2026-04-01 00:00:00
260	12	1	9	Rede 42d (2026)	2026-04-01 00:00:00	21.182182	\N	2026-04-01 00:00:00
261	13	1	9	Rede 42d (2026)	2026-04-01 00:00:00	20.904	\N	2026-04-01 00:00:00
262	14	1	9	Rede 42d (2026)	2026-04-01 00:00:00	20.904	\N	2026-04-01 00:00:00
263	15	1	9	Rede 42d (2026)	2026-04-01 00:00:00	21.1794	\N	2026-04-01 00:00:00
264	16	1	9	Rede 42d (2026)	2026-04-01 00:00:00	108.114	\N	2026-04-01 00:00:00
265	17	1	9	Rede 42d (2026)	2026-04-01 00:00:00	10.296	\N	2026-04-01 00:00:00
266	18	1	9	Rede 42d (2026)	2026-04-01 00:00:00	10.296	\N	2026-04-01 00:00:00
267	19	1	9	Rede 42d (2026)	2026-04-01 00:00:00	11.265	\N	2026-04-01 00:00:00
268	20	1	9	Rede 42d (2026)	2026-04-01 00:00:00	11.265	\N	2026-04-01 00:00:00
269	27	1	9	Rede 42d (2026)	2026-04-01 00:00:00	35.898	\N	2026-04-01 00:00:00
270	29	1	9	Rede 42d (2026)	2026-04-01 00:00:00	37.428	\N	2026-04-01 00:00:00
271	31	1	9	Rede 42d (2026)	2026-04-01 00:00:00	35.184	\N	2026-04-01 00:00:00
272	1	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	34.70233	\N	2026-04-01 00:00:00
273	2	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	18.149576	\N	2026-04-01 00:00:00
274	3	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	18.149576	\N	2026-04-01 00:00:00
275	4	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	20.816101	\N	2026-04-01 00:00:00
276	5	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	20.816101	\N	2026-04-01 00:00:00
277	6	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	55.050846	\N	2026-04-01 00:00:00
278	7	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	51.438137	\N	2026-04-01 00:00:00
279	8	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	51.438137	\N	2026-04-01 00:00:00
280	9	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	32.68644	\N	2026-04-01 00:00:00
281	10	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	32.68644	\N	2026-04-01 00:00:00
282	11	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	21.495869	\N	2026-04-01 00:00:00
283	12	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	18.334711	\N	2026-04-01 00:00:00
284	13	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	18.081818	\N	2026-04-01 00:00:00
285	14	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	18.081818	\N	2026-04-01 00:00:00
286	15	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	18.332182	\N	2026-04-01 00:00:00
287	16	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	97.36364	\N	2026-04-01 00:00:00
288	17	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	8.438182	\N	2026-04-01 00:00:00
289	18	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	8.438182	\N	2026-04-01 00:00:00
290	19	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	9.319091	\N	2026-04-01 00:00:00
291	20	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	9.319091	\N	2026-04-01 00:00:00
292	27	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	31.712727	\N	2026-04-01 00:00:00
293	29	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	33.103638	\N	2026-04-01 00:00:00
294	31	1	10	Atacado 7D (2026)	2026-04-01 00:00:00	31.063637	\N	2026-04-01 00:00:00
295	1	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	35.43108	\N	2026-04-01 00:00:00
296	2	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	18.530718	\N	2026-04-01 00:00:00
297	3	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	18.530718	\N	2026-04-01 00:00:00
298	4	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	21.25324	\N	2026-04-01 00:00:00
299	5	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	21.25324	\N	2026-04-01 00:00:00
300	6	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	56.206917	\N	2026-04-01 00:00:00
301	7	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	52.518337	\N	2026-04-01 00:00:00
302	8	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	52.518337	\N	2026-04-01 00:00:00
303	9	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	33.372856	\N	2026-04-01 00:00:00
304	10	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	33.372856	\N	2026-04-01 00:00:00
305	11	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	21.94728	\N	2026-04-01 00:00:00
306	12	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	18.71974	\N	2026-04-01 00:00:00
307	13	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	18.461536	\N	2026-04-01 00:00:00
308	14	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	18.461536	\N	2026-04-01 00:00:00
309	15	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	18.717157	\N	2026-04-01 00:00:00
310	16	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	99.40827	\N	2026-04-01 00:00:00
311	17	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	8.615384	\N	2026-04-01 00:00:00
312	18	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	8.615384	\N	2026-04-01 00:00:00
313	19	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	9.5147915	\N	2026-04-01 00:00:00
314	20	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	9.5147915	\N	2026-04-01 00:00:00
315	27	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	32.378696	\N	2026-04-01 00:00:00
316	29	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	33.798813	\N	2026-04-01 00:00:00
317	31	1	11	Atacado 28D (2026)	2026-04-01 00:00:00	31.715973	\N	2026-04-01 00:00:00
318	242	3	12	Varejo 12d (2026)	2025-12-01	404.1	13.47	2025-12-01
319	243	3	12	Varejo 12d (2026)	2025-12-01	459	\N	2025-12-01
320	244	3	12	Varejo 12d (2026)	2025-12-01	522.5	\N	2025-12-01
321	245	3	12	Varejo 12d (2026)	2025-12-01	684	\N	2025-12-01
322	246	3	12	Varejo 12d (2026)	2025-12-01	479.7	15.99	2025-12-01
323	247	3	12	Varejo 12d (2026)	2025-12-01	569.7	18.99	2025-12-01
324	248	3	12	Varejo 12d (2026)	2025-12-01	439.79	21.99	2025-12-01
326	250	3	12	Varejo 12d (2026)	2025-12-01	579.8	28.99	2025-12-01
327	251	3	12	Varejo 12d (2026)	2025-12-01	367.84	22.99	2025-12-01
328	252	3	12	Varejo 12d (2026)	2025-12-01	550	27.5	2025-12-01
329	253	3	12	Varejo 12d (2026)	2025-12-01	512	32	2025-12-01
330	254	3	12	Varejo 12d (2026)	2025-12-01	337.68	67	2025-12-01
331	255	3	12	Varejo 12d (2026)	2025-12-01	352.75	69.99	2025-12-01
332	256	3	12	Varejo 12d (2026)	2025-12-01	322.51	63.99	2025-12-01
333	257	3	12	Varejo 12d (2026)	2025-12-01	410	20.5	2025-12-01
334	258	3	12	Varejo 12d (2026)	2025-12-01	415.84	25.99	2025-12-01
335	259	3	12	Varejo 12d (2026)	2025-12-01	376	23.5	2025-12-01
336	260	3	12	Varejo 12d (2026)	2025-12-01	504	31.5	2025-12-01
337	261	3	12	Varejo 12d (2026)	2025-12-01	519.8	25.99	2025-12-01
338	262	3	12	Varejo 12d (2026)	2025-12-01	383.84	23.99	2025-12-01
339	263	3	12	Varejo 12d (2026)	2025-12-01	670	33.5	2025-12-01
340	264	3	12	Varejo 12d (2026)	2025-12-01	439.79	21.99	2025-12-01
341	265	3	12	Varejo 12d (2026)	2025-12-01	384	24	2025-12-01
342	266	3	12	Varejo 12d (2026)	2025-12-01	424	26.5	2025-12-01
343	267	3	12	Varejo 12d (2026)	2025-12-01	431.84	26.99	2025-12-01
344	268	3	12	Varejo 12d (2026)	2025-12-01	424	26.5	2025-12-01
345	269	3	12	Varejo 12d (2026)	2025-12-01	255.84	15.99	2025-12-01
346	270	3	12	Varejo 12d (2026)	2025-12-01	239.85	15.99	2025-12-01
347	271	3	12	Varejo 12d (2026)	2025-12-01	284.85	18.99	2025-12-01
348	272	3	12	Varejo 12d (2026)	2025-12-01	219.9	21.99	2025-12-01
349	273	3	12	Varejo 12d (2026)	2025-12-01	191.92	23.99	2025-12-01
350	274	3	12	Varejo 12d (2026)	2025-12-01	289.9	28.99	2025-12-01
351	275	3	12	Varejo 12d (2026)	2025-12-01	183.92	22.99	2025-12-01
352	363	3	12	Varejo 12d (2026)	2025-12-01	275	27.5	2025-12-01
353	277	3	12	Varejo 12d (2026)	2025-12-01	256	32	2025-12-01
354	278	3	12	Varejo 12d (2026)	2025-12-01	402	67	2025-12-01
355	279	3	12	Varejo 12d (2026)	2025-12-01	419.94	69.99	2025-12-01
356	280	3	12	Varejo 12d (2026)	2025-12-01	383.94	63.99	2025-12-01
357	281	3	12	Varejo 12d (2026)	2025-12-01	205	20.5	2025-12-01
358	282	3	12	Varejo 12d (2026)	2025-12-01	207.92	25.99	2025-12-01
359	283	3	12	Varejo 12d (2026)	2025-12-01	188	23.5	2025-12-01
360	284	3	12	Varejo 12d (2026)	2025-12-01	252	31.5	2025-12-01
361	285	3	12	Varejo 12d (2026)	2025-12-01	259.9	25.99	2025-12-01
362	286	3	12	Varejo 12d (2026)	2025-12-01	191.92	23.99	2025-12-01
363	287	3	12	Varejo 12d (2026)	2025-12-01	335	33.5	2025-12-01
364	288	3	12	Varejo 12d (2026)	2025-12-01	219.9	21.99	2025-12-01
365	289	3	12	Varejo 12d (2026)	2025-12-01	192	24	2025-12-01
366	290	3	12	Varejo 12d (2026)	2025-12-01	212	26.5	2025-12-01
367	291	3	12	Varejo 12d (2026)	2025-12-01	215.92	26.99	2025-12-01
368	292	3	12	Varejo 12d (2026)	2025-12-01	212	26.5	2025-12-01
369	293	3	12	Varejo 12d (2026)	2025-12-01	127.92	15.99	2025-12-01
370	294	3	12	Varejo 12d (2026)	2025-12-01	449.7	14.99	2025-12-01
371	295	3	12	Varejo 12d (2026)	2025-12-01	149.9	14.99	2025-12-01
372	296	3	12	Varejo 12d (2026)	2025-12-01	449.7	14.99	2025-12-01
373	297	3	12	Varejo 12d (2026)	2025-12-01	149.9	14.99	2025-12-01
374	298	3	12	Varejo 12d (2026)	2025-12-01	449.7	14.99	2025-12-01
375	299	3	12	Varejo 12d (2026)	2025-12-01	149.9	14.99	2025-12-01
376	300	3	12	Varejo 12d (2026)	2025-12-01	209.7	6.99	2025-12-01
377	301	3	12	Varejo 12d (2026)	2025-12-01	69.9	6.99	2025-12-01
378	302	3	12	Varejo 12d (2026)	2025-12-01	185.97	61.99	2025-12-01
379	303	3	12	Varejo 12d (2026)	2025-12-01	600	20	2025-12-01
380	304	3	12	Varejo 12d (2026)	2025-12-01	200	20	2025-12-01
381	305	3	12	Varejo 12d (2026)	2025-12-01	799.96	199.99	2025-12-01
382	306	3	12	Varejo 12d (2026)	2025-12-01	1999.9	199.99	2025-12-01
383	307	3	12	Varejo 12d (2026)	2025-12-01	419.7	13.99	2025-12-01
384	308	3	12	Varejo 12d (2026)	2025-12-01	423	23.5	2025-12-01
385	309	3	12	Varejo 12d (2026)	2025-12-01	341.82	18.99	2025-12-01
386	310	3	12	Varejo 12d (2026)	2025-12-01	225	22.5	2025-12-01
387	311	3	12	Varejo 12d (2026)	2025-12-01	306	17	2025-12-01
388	312	3	12	Varejo 12d (2026)	2025-12-01	279	15.5	2025-12-01
389	313	3	12	Varejo 12d (2026)	2025-12-01	378	21	2025-12-01
390	314	3	12	Varejo 12d (2026)	2025-12-01	209.85	13.99	2025-12-01
391	315	3	12	Varejo 12d (2026)	2025-12-01	211.5	23.5	2025-12-01
392	316	3	12	Varejo 12d (2026)	2025-12-01	170.91	18.99	2025-12-01
393	317	3	12	Varejo 12d (2026)	2025-12-01	135	22.5	2025-12-01
394	318	3	12	Varejo 12d (2026)	2025-12-01	153	17	2025-12-01
395	319	3	12	Varejo 12d (2026)	2025-12-01	139.5	15.5	2025-12-01
396	320	3	12	Varejo 12d (2026)	2025-12-01	189	21	2025-12-01
397	321	3	12	Varejo 12d (2026)	2025-12-01	439.79	21.99	2025-12-01
398	322	3	12	Varejo 12d (2026)	2025-12-01	383.84	23.99	2025-12-01
399	323	3	12	Varejo 12d (2026)	2025-12-01	579.8	28.99	2025-12-01
400	324	3	12	Varejo 12d (2026)	2025-12-01	367.84	22.99	2025-12-01
401	325	3	12	Varejo 12d (2026)	2025-12-01	550	27.5	2025-12-01
402	326	3	12	Varejo 12d (2026)	2025-12-01	512	32	2025-12-01
403	327	3	12	Varejo 12d (2026)	2025-12-01	410	20.5	2025-12-01
404	328	3	12	Varejo 12d (2026)	2025-12-01	415.84	25.99	2025-12-01
405	329	3	12	Varejo 12d (2026)	2025-12-01	376	23.5	2025-12-01
406	330	3	12	Varejo 12d (2026)	2025-12-01	504	31.5	2025-12-01
407	331	3	12	Varejo 12d (2026)	2025-12-01	519.8	25.99	2025-12-01
408	332	3	12	Varejo 12d (2026)	2025-12-01	383.84	23.99	2025-12-01
409	333	3	12	Varejo 12d (2026)	2025-12-01	670	33.5	2025-12-01
410	334	3	12	Varejo 12d (2026)	2025-12-01	439.79	21.99	2025-12-01
411	335	3	12	Varejo 12d (2026)	2025-12-01	384	24	2025-12-01
412	336	3	12	Varejo 12d (2026)	2025-12-01	424	26.5	2025-12-01
413	337	3	12	Varejo 12d (2026)	2025-12-01	431.84	26.99	2025-12-01
414	338	3	12	Varejo 12d (2026)	2025-12-01	424	26.5	2025-12-01
415	339	3	12	Varejo 12d (2026)	2025-12-01	255.84	15.99	2025-12-01
416	340	3	12	Varejo 12d (2026)	2025-12-01	219.9	21.99	2025-12-01
417	341	3	12	Varejo 12d (2026)	2025-12-01	191.92	23.99	2025-12-01
418	342	3	12	Varejo 12d (2026)	2025-12-01	289.9	28.99	2025-12-01
419	343	3	12	Varejo 12d (2026)	2025-12-01	183.92	22.99	2025-12-01
420	276	3	12	Varejo 12d (2026)	2025-12-01	275	27.5	2025-12-01
421	344	3	12	Varejo 12d (2026)	2025-12-01	256	32	2025-12-01
422	345	3	12	Varejo 12d (2026)	2025-12-01	205	20.5	2025-12-01
423	346	3	12	Varejo 12d (2026)	2025-12-01	207.92	25.99	2025-12-01
424	347	3	12	Varejo 12d (2026)	2025-12-01	188	23.5	2025-12-01
425	348	3	12	Varejo 12d (2026)	2025-12-01	252	31.5	2025-12-01
426	349	3	12	Varejo 12d (2026)	2025-12-01	259.9	25.99	2025-12-01
427	350	3	12	Varejo 12d (2026)	2025-12-01	191.92	23.99	2025-12-01
428	351	3	12	Varejo 12d (2026)	2025-12-01	335	33.5	2025-12-01
429	352	3	12	Varejo 12d (2026)	2025-12-01	219.9	21.99	2025-12-01
430	353	3	12	Varejo 12d (2026)	2025-12-01	192	24	2025-12-01
431	354	3	12	Varejo 12d (2026)	2025-12-01	212	26.5	2025-12-01
432	355	3	12	Varejo 12d (2026)	2025-12-01	215.92	26.99	2025-12-01
433	356	3	12	Varejo 12d (2026)	2025-12-01	212	26.5	2025-12-01
434	357	3	12	Varejo 12d (2026)	2025-12-01	127.92	15.99	2025-12-01
435	358	3	12	Varejo 12d (2026)	2025-12-01	23.6	\N	2025-12-01
436	359	3	12	Varejo 12d (2026)	2025-12-01	17.99	\N	2025-12-01
437	360	3	12	Varejo 12d (2026)	2025-12-01	166.5	\N	2025-12-01
\.


--
-- Data for Name: interacao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.interacao (interacao_id, negociacao_id, data_interacao, via_comunicacao, contato_pessoa, contato_cliente_id, descricao, resultado, data_followup, status_interacao, ativo) FROM stdin;
\.


--
-- Data for Name: linha; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.linha (linha_id, categoria_id, nome_linha, ativo) FROM stdin;
1	1	STANDARD	1
2	2	STANDARD	1
3	2	TRADIÇÃO	1
4	2	PREMIO	1
5	2	GOURMET	1
6	3	GOURMET	1
7	2	FOOD	1
8	4	CONSERVAS	1
9	5	TEMPEROS	1
10	6	MOLHOS	1
11	7	DIET/LIGHT	1
12	8	DIET/LIGHT	1
13	9	DIET/LIGHT	1
14	10	Suína	1
15	11	Bovina	1
16	12	Cordeiro	1
17	12	Suína	1
18	12	Frango	1
19	12	Bovina	1
20	13	Suína	1
21	14	Suína	1
22	14	Mista	1
23	14	Bovina	1
24	17	Suína	1
25	17	Bovina	1
26	19	Suína	1
27	18	—	1
28	20	Tradicional	1
29	20	Integral	1
30	24	Oriental	1
31	27	Fast Pasta	1
32	28	Tricolori	1
\.


--
-- Data for Name: marca; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marca (marca_id, fornecedor_id, nome_marca, ativo) FROM stdin;
1	1	Belmont	1
2	1	Vinaro	1
3	2	Diet House	1
4	3	Specialli	1
5	4	Massas De	1
\.


--
-- Data for Name: mensagem_modelo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mensagem_modelo (mensagem_id, nome, assunto, corpo, via, ativo) FROM stdin;
2	Contato Diet House (I)	Contato Diet House	Boa tarde!\n\nMeu nome é Fernando Azevedo Jr, atuo como representante comercial aqui na Baixada Santista e desenvolvo a marca Diet House na região.\n\nA Diet House é uma empresa com mais de 30 anos de mercado, especializada em doces diet sem açúcar e sem glúten, produzidos artesanalmente, sem conservantes e adoçados apenas com xilitol — uma linha bastante alinhada ao público que busca saúde, qualidade e alimentação funcional.\n\nEstou encaminhando em anexo o portfólio da linha e também a tabela de preços para uma avaliação inicial.\n\nHoje a marca já possui presença consolidada em redes importantes, como o Grupo Pão de Açúcar, onde alguns itens são revendidos na faixa de R$ 30,99 ao consumidor final.	WhatsApp	1
3	Contato Diet House (II)	Contato Diet House	Para facilitar uma análise rápida, seguem alguns dos itens com maior potencial de giro e aceitação inicial:\n\n• Geleia de Frutas Vermelhas 250g — R$ 18,60\n• Doce de Abóbora com Coco Diet 250g — R$ 16,30\n• Fondant de Leite Cremoso Diet 250g — R$ 17,40\n• Goiabada Cascão Diet 250g — R$ 16,30\n• Doce de Figo em Calda Diet 250g — R$ 16,30\n• Geleia de Pimenta com Abacaxi Diet 250g — R$ 17,40\n• Cocada Diet 250g — R$ 18,60\n• Pé de Moça Diet 250g — R$ 18,60\n\n(Caixas com 12 unidades por sabor.)\n\nPedido mínimo de R$ 1.000,00 (em média 5 a 6 caixas), com entrega CIF e prazo de pagamento de 30 dias.\n\nFico totalmente à disposição para quaisquer dúvidas e agradeço desde já pela atenção.\n\nFernando Azevedo Jr\n11 98833-4747	WhatsApp	1
\.


--
-- Data for Name: meta_fornecedor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.meta_fornecedor (meta_id, fornecedor_id, ano, mes, meta_valor, meta_pedidos, observacao, ativo) FROM stdin;
\.


--
-- Data for Name: meta_mix; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.meta_mix (meta_mix_id, fornecedor_id, tipo, referencia_id, descricao, ano, mes, meta_qtd, meta_clientes, observacao, ativo) FROM stdin;
1	3	categoria	14	Salsichas	2026	4	20	10	\N	1
2	3	categoria	14	Salsichas	2026	4	20	10	\N	0
\.


--
-- Data for Name: mix_cliente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mix_cliente (mix_id, cliente_id, fornecedor_id, pdv_id, produto_id, ativo, observacao) FROM stdin;
1	1	1	\N	23	1	\N
2	3	1	2	1	1	\N
3	3	1	2	2	1	\N
4	3	1	2	3	1	\N
5	3	1	2	6	1	\N
6	3	1	2	7	1	\N
7	3	1	2	8	1	\N
8	3	1	2	9	1	\N
9	3	1	2	10	1	\N
10	3	1	2	13	1	\N
11	3	1	2	14	1	\N
12	3	1	2	25	1	\N
13	3	1	2	26	1	\N
14	3	1	2	27	1	\N
15	3	1	2	28	1	\N
16	3	1	2	29	1	\N
17	3	1	2	30	1	\N
18	3	1	2	31	1	\N
19	100	1	\N	2	1	\N
20	100	1	\N	3	1	\N
21	100	1	\N	6	1	\N
22	100	1	\N	7	1	\N
23	100	1	\N	8	1	\N
24	100	1	\N	9	1	\N
25	100	1	\N	10	1	\N
\.


--
-- Data for Name: negociacao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.negociacao (negociacao_id, cliente_id, fornecedor_id, titulo, data_abertura, status, prioridade, previsao_conclusao, observacao, ativo) FROM stdin;
\.


--
-- Data for Name: pdv; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pdv (pdv_id, cliente_id, numero_loja, nome_loja, endereco, bairro, cidade, estado, cnpj, ie, gerente, fone_gerente, encarregado, fone_encarregado, horario_recebimento, tipo_pdv, setor, cluster, tamanho_pdv, latitude, longitude, ordem_roteiro, dia_visita, frequencia_visita, observacao, ativo, status) FROM stdin;
161	97	\N	Hortifruti Akira	Av. Irmãos Adorno,170	Sítio do Campo	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Hortifruti	Setor 7A - Praia Grande Orla / Norte	B/C	P	\N	\N	\N	\N	\N	\N	0	Prospecto
156	96	\N	Carrefour Bairro Guilhermina	Av. Pres. Castelo Branco, 1888	Guilhermina	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	\N	B/C	G	\N	\N	\N	\N	\N	\N	0	Inativo
165	102	\N	Padaria Pamer	R. Fumio Miyazi, 1001	Guilhermina	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 7 - Praia Grande	\N	\N	-24.0063	-46.4185	\N	\N	\N	\N	0	Prospecto
166	103	1	Padaria Boa Praça	Av. Pres. Castelo Branco, 4222	Aviação	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 7 - Praia Grande	\N	\N	-24.0145	-46.4272	\N	\N	\N	\N	0	Prospecto
167	103	2	Padaria Boa Praça II	Rua Nicarágua 133	Vila Guilhermina	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 7 - Praia Grande	\N	\N	-24.006	-46.417	\N	\N	\N	\N	0	Prospecto
168	104	\N	Padaria Nova Charm	Av. Pres. Costa e Silva, 988	Boqueirão	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 7 - Praia Grande	\N	\N	-24.0055	-46.402	\N	\N	\N	\N	0	Prospecto
169	105	\N	Padaria Canto do Forte	Av. Mal. Mallet, 594	Canto do Forte	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 7 - Praia Grande	\N	\N	-24.0058	-46.4022	\N	\N	\N	\N	0	Prospecto
170	106	\N	Padaria Santa Terezinha	Av. Pres. Kennedy, 5799	Vila Tupi	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 7 - Praia Grande	\N	\N	-24.0172	-46.4298	\N	\N	\N	\N	0	Prospecto
171	108	\N	Panificadora e Confeitaria 2 Corações	Av. João André Quintale, 695	Maracanã	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 7 - Praia Grande	\N	\N	-24.026	-46.455	\N	\N	\N	\N	0	Prospecto
172	109	\N	Nova Balneária - Padaria & Restaurante	R. Caribas	Vila Tupi	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 7 - Praia Grande	\N	\N	-24.0172	-46.4298	\N	\N	\N	\N	0	Prospecto
173	110	\N	Padaria Balneária	Av. Min. Marcos Freire, 4948	Vila Antartica	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 7 - Praia Grande	\N	\N	-24.095	-46.63	\N	\N	\N	\N	0	Prospecto
174	111	\N	Empório Dom José	R. Conselheiro Lafayette, 3	Embaré	Santos	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 3 - Santos Orla	\N	\N	-23.9765	-46.3122	\N	\N	\N	\N	0	Prospecto
175	58	\N	Casaria Padaria	Av. Conselheiro Nébias, 718	Boqueirão	Santos	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 3 - Santos Orla	\N	\N	-23.9715	-46.3282	\N	\N	\N	\N	0	Prospecto
176	113	\N	Panificadora Washington Luiz	Av. Washington Luís, 449	Boqueirão	Santos	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 3 - Santos Orla	\N	\N	-23.9715	-46.3282	\N	\N	\N	\N	0	Prospecto
177	114	\N	Padaria Bella Villa	R. Goiás, 44	Boqueirão	Santos	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 3 - Santos Orla	\N	\N	-23.9715	-46.3282	\N	\N	\N	\N	0	Prospecto
178	115	\N	Empório Nova Era	Rua Dr. Cunha Moreira, 210	Encruzilhada	Santos	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 2 - Santos Intermediário	\N	\N	-23.9472	-46.3279	\N	\N	\N	\N	0	Prospecto
179	116	\N	Panificadora Nova Itararé	Av. Presidente Wilson, 88/96	Itararé	São Vicente	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 5 - São Vicente	\N	\N	-23.9675	-46.367	\N	\N	\N	\N	0	Prospecto
180	117	\N	Padaria & Confeitaria Bella São Vicente	R. Marquês de São Vicente, 91	Centro	São Vicente	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 5 - São Vicente	\N	\N	-23.9632	-46.3917	\N	\N	\N	\N	0	Prospecto
181	107	\N	Padaria Peg Pão do Forte	Av. Mal. Mallet, 422	Canto do Forte	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 7 - Praia Grande	\N	\N	-24.0058	-46.4022	\N	\N	\N	\N	0	Prospecto
182	118	\N	Padaria Peg Pão São Vicente	R. Frei Gaspar, 128	Centro	São Vicente	SP	\N	\N	\N	13 99652-5124	\N	\N	\N	Padaria	Setor 5 - São Vicente	\N	\N	-23.9632	-46.3917	\N	\N	\N	pegpaosaovicente	0	Prospecto
183	118	\N	Padaria Peg Pão Praia Grande	Av. Paris, 508	Canto do Forte	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 7 - Praia Grande	\N	\N	-24.0058	-46.4022	\N	\N	\N	pegpaopg	0	Prospecto
184	118	\N	Padaria Peg Pão Mongaguá Av.São Paulo	Av. São Paulo, 1904	Centro	Mongaguá	SP	\N	\N	\N	13 99779-1499	\N	\N	\N	Padaria	Setor 8 - Litoral Sul	\N	\N	-24.0965	-46.6205	\N	\N	\N	pegpaomongagua	0	Prospecto
185	118	\N	Padaria Peg Pão Mongaguá Av.Marina	Av. Marina, 215 	Centro	Mongaguá	SP	\N	\N	\N	13 99742-2905	\N	\N	\N	Padaria	Setor 8 - Litoral Sul	\N	\N	-24.0965	-46.6205	\N	\N	\N	pegpaomongagua	0	Prospecto
186	118	\N	Padaria Peg Pão Itanhaém Centro	Praça Carlos Botelho, 159	Centro	Itanhaém	SP	\N	\N	\N	13 99615-3212	\N	\N	\N	Padaria	Setor 8 - Litoral Sul	\N	\N	-24.1833	-46.7882	\N	\N	\N	pegpaoitanhaem	0	Prospecto
187	118	\N	Padaria Peg Pão Itanhaém Belas Artes	R. Rodolfo Amoedo, 98	Belas Artes	Itanhaém	SP	\N	\N	\N	13 99719-9343	\N	\N	\N	Padaria	Setor 8 - Litoral Sul	\N	\N	-24.2045	-46.785	\N	\N	\N	pegpaoitanhaem	0	Prospecto
188	118	\N	Padaria Peg Pão Peruíbe Três Marias	Av. Padre Anchieta, 4973	Balneário Três Marias	Peruíbe	SP	\N	\N	\N	13 99758-3326	\N	\N	\N	Padaria	Setor 8 - Litoral Sul	\N	\N	-24.3205	-47.0018	\N	\N	\N	pegpaoperuibe	0	Prospecto
189	118	\N	Padaria Peg Pão Peruíbe Centro	Av. Padre Anchieta, 924	Centro	Peruíbe	SP	\N	\N	\N	13 99652-9590	\N	\N	\N	Padaria	Setor 8 - Litoral Sul	\N	\N	-24.3202	-47.0015	\N	\N	\N	pegpaoperuibe	0	Prospecto
190	118	\N	Padaria Peg Pão Peruíbe Jangadas	Av. Padre Anchieta, 2273	Jd. Jangadas	Peruíbe	SP	\N	\N	\N	13 97819-4854	\N	\N	\N	Padaria	Setor 8 - Litoral Sul	\N	\N	-24.305	-46.985	\N	\N	\N	pegpaoperuibe	0	Prospecto
115	59	\N	Caiçara	Av. Pres. Kennedy, 12707	Vila Caiçara	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 7B - Praia Grande Interior / Sul	A/B	G	-24.0485	-46.5164	\N	\N	\N	\N	0	Prospecto
191	119	\N	Padaria Gualchi	R. Honduras, 195	Guilhermina	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 7 - Praia Grande	\N	\N	\N	\N	\N	\N	\N	\N	1	Prospecto
163	98	\N	Davila Mercado e Hortifruti	Av. Miami, 689 	Vila Caiçara	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Hortifruti	Setor 7B - Praia Grande Interior / Sul	C/D	P	\N	\N	\N	\N	\N	\N	1	Ativo
1	2	\N	Boqueirão	R. Jaú, 1254	Boqueirão	Praia Grande	SP	\N	\N	Gabriel	\N	\N	\N	\N	Supermercado	Setor 7A - Praia Grande Orla / Norte	\N	\N	-24.0087	-46.3997	\N	\N	\N	\N	0	Visitado
2	3	1	Caiçara	Av. Presidente Kennedy, 13601	Caiçara	Praia Grande	SP	44.658.438/0001-37	558.685.687.114	Carlos	\N	\N	\N	\N	Supermercado	Setor 7B - Praia Grande Interior / Sul	\N	\N	-24.0337	-46.3717	\N	\N	\N	\N	0	Suspenso
4	10	\N	Guilhermina	Av. Pres. Kennedy, 2194	Guilhermina	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 7A - Praia Grande Orla / Norte	\N	\N	-24.0127	-46.3817	\N	\N	\N	\N	0	Visitado
5	11	\N	Balneário Esmeralda	Av. Zélia Giglioli Galves, 02	Balneário Esmeralda	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 7B - Praia Grande Interior / Sul	\N	\N	-24.0557	-46.3577	\N	\N	\N	\N	0	Visitado
6	12	3	Jardim Real	Av. Presidente Kennedy, 16767	Jardim Real	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 7B - Praia Grande Interior / Sul	\N	\N	-24.0617	-46.3507	\N	\N	\N	\N	0	Visitado
7	13	7	Mongaguá - Av.São Paulo	Av. São Paulo, 2304	Centro	Mongaguá	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 8 - Litoral Sul	\N	\N	-24.0887	-46.6237	\N	\N	\N	\N	0	Visitado
8	14	\N	Almeida Rocha III	R. Antônio Cândido da Silva, 57	Vila Sonia	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 7B - Praia Grande Interior / Sul	\N	\N	-24.0677	-46.3417	\N	\N	\N	\N	0	Visitado
9	15	\N	Guilhermina	R. Enseada, 116	Guilhermina	Praia Grande	SP	\N	\N	\N	(13) 3474-6154	\N	\N	\N	Supermercado	Setor 7A - Praia Grande Orla / Norte	\N	\N	-24.0127	-46.3817	\N	\N	\N	\N	0	Visitado
11	17	\N	Jardim Real	Av. Pres. Kennedy, 17145	Real	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 7B - Praia Grande Interior / Sul	\N	\N	-24.0617	-46.3507	\N	\N	\N	\N	0	Visitado
12	18	\N	Aviação	Av. Pres. Kennedy, 3430	Aviação	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 7A - Praia Grande Orla / Norte	\N	\N	-23.9987	-46.4077	\N	\N	\N	\N	0	Visitado
13	19	\N	Ocian	Av. Pres Kennedy, 7137	Cidade Ocian	Praia Grande	SP	\N	\N	\N	(13) 3278 9000	\N	\N	\N	Supermercado	Setor 7A - Praia Grande Orla / Norte	\N	\N	-24.0207	-46.3887	\N	\N	\N	\N	0	Visitado
14	20	\N	Nova Mirim	Av. Dr. Roberto de Almeida Vinhas, 8969	Nova Mirim	Praia Grande	SP	\N	\N	\N	(13) 3494-8610	\N	\N	\N	Supermercado	Setor 7B - Praia Grande Interior / Sul	\N	\N	-24.0437	-46.3667	\N	\N	\N	\N	0	Visitado
15	21	1	Boqueirão	Av. São Paulo, 1078	Boqueirão	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Casa de Carnes	Setor 7A - Praia Grande Orla / Norte	\N	\N	-24.0087	-46.3997	\N	\N	\N	\N	0	Visitado
16	22	\N	Centro	R. Expedicionários Vicentinos, 70	Centro	São Vicente	SP	\N	\N	\N	(13) 99102-1482	\N	\N	\N	Empório	Setor 5 - São Vicente	\N	\N	-23.9632	-46.3917	\N	\N	\N	\N	0	Prospecto
17	23	\N	Vila Belmiro	R. Dr. Carvalho de Mendonça, 256	Vila Belmiro	Santos	SP	\N	\N	\N	(13) 3233-5249	\N	\N	\N	Empório	Setor 2 - Santos Intermediário	\N	\N	-23.9505	-46.3432	\N	\N	\N	\N	0	Prospecto
18	24	\N	José Menino	Av Presidente Wilson, 192	José Menino	Santos	SP	\N	\N	\N	(13) 3237-3600	\N	\N	\N	Empório	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9669	-46.3495	\N	\N	\N	\N	0	Prospecto
19	25	\N	Gonzaga	R. Goytacazes, 20	Gonzaga	Santos	SP	\N	\N	\N	(13) 99751-1990	\N	\N	\N	Empório	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.969	-46.3338	\N	\N	\N	\N	0	Prospecto
20	26	\N	Campo Grande	Rua Carvalho de Mendonça, 411	Campo Grande	Santos	SP	\N	\N	\N	(13) 3221-9232	\N	\N	\N	Empório	Setor 2 - Santos Intermediário	\N	\N	-23.9489	-46.3355	\N	\N	\N	\N	0	Prospecto
21	27	\N	Encruzilhada	R. Cunha Moreira, 37	Encruzilhada	Santos	SP	\N	\N	\N	(13) 3041-3337	\N	\N	\N	Empório	Setor 2 - Santos Intermediário	\N	\N	-23.9472	-46.3279	\N	\N	\N	\N	0	Prospecto
22	28	\N	Gonzaga	Av. Pres. Wilson, 26, Loja 30E	Gonzaga	Santos	SP	\N	\N	\N	(13) 98212-3123	\N	\N	\N	Empório	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9678	-46.3349	\N	\N	\N	\N	0	Prospecto
23	29	\N	Gonzaga	Av. Mal. Floriano Peixoto, 67, loja 35	Gonzaga	Santos	SP	\N	\N	\N	(13) 3289-5762	\N	\N	\N	Empório	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9672	-46.334	\N	\N	\N	\N	0	Prospecto
24	30	\N	Vila Belmiro	R. Dr Carvalho de Mendonça, 377	Vila Belmiro	Santos	SP	\N	\N	\N	(13) 3321-5000	\N	\N	\N	Empório	Setor 2 - Santos Intermediário	\N	\N	-23.9498	-46.3415	\N	\N	\N	\N	0	Prospecto
25	31	\N	Gonzaga	R. Pereira Barreto, 5	Gonzaga	Santos	SP	\N	\N	\N	(13) 97811-1000	\N	\N	\N	Empório	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9695	-46.332	\N	\N	\N	\N	0	Prospecto
26	32	\N	Ponta da Praia	Av. Dr. Epitácio Pessoa, 651	Ponta da Praia	Santos	SP	\N	\N	\N	(13) 3345-0662	\N	\N	\N	Empório	Setor 4 - Ponta da Praia	\N	\N	-23.9815	-46.2998	\N	\N	\N	\N	0	Prospecto
27	33	\N	Gonzaga	Av. Mal. Floriano Peixoto, 98	Gonzaga	Santos	SP	\N	\N	\N	(13) 98132-0137	\N	\N	\N	Empório	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9675	-46.3332	\N	\N	\N	\N	0	Prospecto
28	33	\N	Centro	R. Riachuelo, 86	Centro	Santos	SP	\N	\N	\N	(13) 98132-0137	\N	\N	\N	Empório	Setor 1 - Santos Centro / Porto	\N	\N	-23.9368	-46.3295	\N	\N	\N	\N	0	Prospecto
29	34	\N	Estuário	Av. Senador Dantas, 428	Estuário	Santos	SP	\N	\N	\N	(13) 3227-1508	\N	\N	\N	Empório	Setor 1 - Santos Centro / Porto	\N	\N	-23.9538	-46.3165	\N	\N	\N	\N	0	Prospecto
30	35	\N	Macuco	R. Silva Jardim, 299	Macuco	Santos	SP	\N	\N	\N	(13) 3232-3051	\N	\N	\N	Padaria	Setor 1 - Santos Centro / Porto	\N	\N	-23.9487	-46.3221	\N	\N	\N	\N	0	Prospecto
31	36	\N	Gonzaga	R. Euclides da Cunha, 63	Gonzaga	Santos	SP	\N	\N	\N	(13) 98881-3922	\N	\N	\N	Empório	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9693	-46.3345	\N	\N	\N	\N	0	Prospecto
32	37	\N	Gonzaga	R. Azevedo Sodré, 144	Gonzaga	Santos	SP	\N	\N	\N	(13) 2104-7575	\N	\N	\N	Empório	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.97	-46.3348	\N	\N	\N	\N	0	Prospecto
33	37	\N	Boqueirão	R. Mato Grosso, 404	Boqueirão	Santos	SP	\N	\N	\N	(13) 2104-7575	\N	\N	\N	Empório	Setor 3A - Santos Orla Norte (Boqueirão / Aparecida)	\N	\N	-23.9715	-46.3282	\N	\N	\N	\N	0	Prospecto
34	38	\N	Cidade Náutica	Av. Mal. Humberto de Alencar Castelo Branco, 217	Cidade Náutica	São Vicente	SP	\N	\N	\N	(13) 3043-6006	\N	\N	\N	Padaria	Setor 5 - São Vicente	\N	\N	-23.9578	-46.4042	\N	\N	\N	\N	0	Prospecto
35	39	1	Campo Grande	Rua Carvalho De Mendonça, 336	Campo Grande	Santos	SP	\N	\N	\N	(13) 3203-3362/3299-3941	\N	\N	\N	Supermercado	Setor 2 - Santos Intermediário	\N	\N	-23.9492	-46.337	\N	\N	\N	\N	0	Prospecto
36	39	3	Gonzaga	Rua Tolentino Filgueiras, 70	Gonzaga	Santos	SP	\N	\N	\N	(13) 3284-2005	\N	\N	\N	Supermercado	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9692	-46.3341	\N	\N	\N	\N	0	Prospecto
37	39	2	Pompeia	Rua Praça Benedito Calixto, 15	Pompeia	Santos	SP	\N	\N	\N	(13) 3301-4414	\N	\N	\N	Supermercado	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.967	-46.3452	\N	\N	\N	\N	0	Prospecto
38	40	\N	Ponta Da Praia	Av. Dos Bancarios, 85	Ponta Da Praia	Santos	SP	\N	\N	\N	(13) 3269-4080	\N	\N	\N	Supermercado	Setor 4 - Ponta da Praia	\N	\N	-23.9832	-46.2985	\N	\N	\N	\N	0	Prospecto
39	41	\N	Gonzaga	Av. Marechal Floriano Peixoto, 92	Gonzaga	Santos	SP	\N	\N	\N	(13) 3289-1160	\N	\N	\N	Supermercado	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9676	-46.3343	\N	\N	\N	\N	0	Prospecto
40	42	\N	Centro	R. Quinze De Novembro, 537 / R. João Ramalho, 950	Centro	São Vicente	SP	\N	\N	\N	(13) 3468-0614/1781	\N	\N	\N	Supermercado	Setor 5 - São Vicente	\N	\N	-23.9625	-46.3928	\N	\N	\N	\N	0	Prospecto
41	43	\N	Estação	Av. Xxiv De Dezembro, 560	Estação	Peruíbe	SP	\N	\N	\N	(13) 3455-2004	\N	\N	\N	Supermercado	Setor 8 - Litoral Sul	\N	\N	-24.3202	-47.0015	\N	\N	\N	\N	0	Prospecto
42	44	\N	Jd. Castelo	Praça José Oliveira Lopes, 86	Jd. Castelo	Santos	SP	\N	\N	\N	(13)3203-3362/3299-3941	\N	\N	\N	Supermercado	Setor 2 - Santos Intermediário	\N	\N	-23.9465	-46.336	\N	\N	\N	\N	0	Prospecto
43	45	\N	Vila Nova	Av. Nossa Senhora Da Lapa, 1400	Vila Nova	Cubatão	SP	\N	\N	\N	(13) 3361-1889	\N	\N	\N	Supermercado	Setor 1 - Santos Centro / Porto	\N	\N	-23.8895	-46.4253	\N	\N	\N	\N	0	Prospecto
44	46	\N	Vila Cascatinha	Av. Antônio Emmerick, 335/373	Vila Cascatinha	São Vicente	SP	\N	\N	\N	(13) 3569-1900	\N	\N	\N	Supermercado	Setor 5 - São Vicente	\N	\N	-23.9639	-46.377	\N	\N	\N	\N	0	Prospecto
45	47	\N	Boa Vista	Rua Onze De Junho, 180	Boa Vista	São Vicente	SP	\N	\N	\N	(13) 3469- 3554	\N	\N	\N	Supermercado	Setor 5 - São Vicente	\N	\N	-23.9682	-46.3835	\N	\N	\N	\N	0	Prospecto
46	48	\N	Canto Do Forte	Av. Marechal Mallet, 532	Canto Do Forte	Praia Grande	SP	\N	\N	\N	(13) 3491-2849/3473-5816	\N	\N	\N	Supermercado	Setor 7A - Praia Grande Orla / Norte	\N	\N	-24.0058	-46.4022	\N	\N	\N	\N	0	Prospecto
47	49	\N	Vicente De Carvalho	Av. Santos Dumont, 474/494	Vicente De Carvalho	Guarujá	SP	\N	\N	\N	(13) 3269-4080	\N	\N	\N	Supermercado	Setor 6 - Guarujá	\N	\N	-23.9991	-46.2598	\N	\N	\N	\N	0	Prospecto
48	50	2	Campo Grande	Rua Evaristo Da Veiga, 224	Campo Grande	Santos	SP	\N	\N	\N	(13) 3252-3212/3222-8382	\N	\N	\N	Supermercado	Setor 2 - Santos Intermediário	\N	\N	-23.948	-46.3312	\N	\N	\N	\N	0	Prospecto
49	50	1	Vl. São Jorge	R. Domingos José Martins, 170	Vl. São Jorge	Santos	SP	\N	\N	\N	(13) 3209-8110	\N	\N	\N	Supermercado	Setor 1 - Santos Centro / Porto	\N	\N	-23.944	-46.3205	\N	\N	\N	\N	0	Prospecto
50	51	2	Centro	Rua Petrópolis, 291	Centro	Guarujá	SP	\N	\N	\N	(13) 3358-1070	\N	\N	\N	Supermercado	Setor 6 - Guarujá	\N	\N	-23.9935	-46.256	\N	\N	\N	\N	0	Prospecto
51	51	3	Jardim Primavera	Rua Dos Geranios, 136	Jardim Primavera	Guarujá	SP	\N	\N	\N	(13) 3366-7766	\N	\N	\N	Supermercado	Setor 6 - Guarujá	\N	\N	-23.9702	-46.2425	\N	\N	\N	\N	0	Prospecto
52	51	1	Vila Ligya	Av. Adhemar De Barros, 3255	Vila Ligya	Guarujá	SP	\N	\N	\N	(13)3269-4060	\N	\N	\N	Supermercado	Setor 6 - Guarujá	\N	\N	-23.9825	-46.2563	\N	\N	\N	\N	0	Prospecto
53	51	4	Vila Santa Rosa	Rua Antonio Miguel Dos Santos, 456	Vila Santa Rosa	Guarujá	SP	\N	\N	\N	(13) 3384-6924	\N	\N	\N	Supermercado	Setor 6 - Guarujá	\N	\N	-23.9898	-46.2487	\N	\N	\N	\N	0	Prospecto
54	52	\N	José Menino	Av. Presidente Wilson, 187/188	José Menino	Santos	SP	\N	\N	\N	(13)3225-9200	\N	\N	\N	Supermercado	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9665	-46.3488	\N	\N	\N	\N	0	Prospecto
55	53	1	Morro Do S. Bento	R. Dois, 947	Morro Do S. Bento	Santos	SP	\N	\N	\N	(13)3258-6407	\N	\N	\N	Supermercado	Setor 1 - Santos Centro / Porto	\N	\N	-23.9305	-46.321	\N	\N	\N	\N	0	Prospecto
56	53	2	Morro Nova Cintra	Av. Santista, 623	Morro Nova Cintra	Santos	SP	\N	\N	\N	(13) 3385-0395/0437	\N	\N	\N	Supermercado	Setor 1 - Santos Centro / Porto	\N	\N	-23.9358	-46.3085	\N	\N	\N	\N	0	Prospecto
57	54	5	Belas Artes	Av. Harry Forssell, 856	Belas Artes	Itanhaém	SP	\N	\N	\N	(13) 3426-9929	\N	\N	\N	Supermercado	Setor 8 - Litoral Sul	\N	\N	-24.2045	-46.785	\N	\N	\N	\N	0	Prospecto
58	54	10	Boca Da Barra	Av. João Batista Leal, 345	Boca Da Barra	Itanhaém	SP	\N	\N	\N	(13) 3426-9298	\N	\N	\N	Supermercado	Setor 8 - Litoral Sul	\N	\N	-24.1848	-46.7865	\N	\N	\N	\N	0	Prospecto
59	54	1	Centro	Rua João Mariano, 193	Centro	Itanhaém	SP	\N	\N	\N	(13) 3421-4448/4316	\N	\N	\N	Supermercado	Setor 8 - Litoral Sul	\N	\N	-24.1833	-46.7882	\N	\N	\N	\N	0	Prospecto
60	54	7	Nossa Senhora Do Sion	Av. Cabuçu, 377	Nossa Senhora Do Sion	Itanhaém	SP	\N	\N	\N	(13) 3426-6636	\N	\N	\N	Supermercado	Setor 8 - Litoral Sul	\N	\N	-24.2138	-46.8032	\N	\N	\N	\N	0	Prospecto
61	55	2	Vila Margarida	R. Monte Belvedere, 610	Vila Margarida	São Vicente	SP	\N	\N	\N	(13) 3465-1212	\N	\N	\N	Supermercado	Setor 5 - São Vicente	\N	\N	-23.9712	-46.4015	\N	\N	\N	\N	0	Prospecto
62	56	3	Aparecida	Rua Alexandre Martins, 125	Aparecida	Santos	SP	\N	\N	\N	(13) 3231-2883	\N	\N	\N	Supermercado	Setor 3A - Santos Orla Norte (Boqueirão / Aparecida)	\N	\N	-23.9775	-46.311	\N	\N	\N	\N	0	Prospecto
63	56	1	Campo Grande	Av. Sen. Pinheiro Machado, 643	Campo Grande	Santos	SP	\N	\N	\N	(13) 2102-5153/5159	\N	\N	\N	Supermercado	Setor 2 - Santos Intermediário	\N	\N	-23.9485	-46.3328	\N	\N	\N	\N	0	Prospecto
64	56	4	Marapé	Av. Doutor Moura Ribeiro, 116	Marapé	Santos	SP	\N	\N	\N	(13) 3251-8108	\N	\N	\N	Supermercado	Setor 2 - Santos Intermediário	\N	\N	-23.952	-46.3402	\N	\N	\N	\N	0	Prospecto
65	56	2	Saboó	Rua Pio Xii, 82	Saboó	Santos	SP	\N	\N	\N	(13) 3296-4615	\N	\N	\N	Supermercado	Setor 1 - Santos Centro / Porto	\N	\N	-23.9375	-46.3348	\N	\N	\N	\N	0	Prospecto
66	57	\N	Embaré	Av. Afonso Pena, 336	Embaré	Santos	SP	\N	\N	\N	(13) 3236-5930	\N	\N	\N	Supermercado	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9765	-46.3122	\N	\N	\N	\N	0	Prospecto
67	10	\N	Ocian	Av. Pres. Kennedy, 6767	Ocian	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Empório	Setor 7A - Praia Grande Orla / Norte	\N	\N	-24.0207	-46.3887	\N	\N	\N	\N	0	Prospecto
68	10	\N	Caiçara	Av. Presidente Kennedy, 12747 - Loja 1	Vila Caiçara	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Empório	Setor 7B - Praia Grande Interior / Sul	\N	\N	-24.0337	-46.3717	\N	\N	\N	\N	0	Prospecto
69	10	\N	Centro	Rua Jacob Emmerich, 359	Centro	São Vicente	SP	\N	\N	\N	\N	\N	\N	\N	Empório	Setor 5 - São Vicente	\N	\N	-23.964	-46.3917	\N	\N	\N	\N	0	Prospecto
70	10	\N	Ana Costa	Avenida Ana Costa, 495	Gonzaga	Santos	SP	\N	\N	\N	\N	\N	\N	\N	Empório	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9905	-46.3167	\N	\N	\N	\N	0	Prospecto
71	10	\N	Epitácio Pessoa	Av. Dr. Epitácio Pessoa, 40	BoqueirÃ£o	Santos	SP	\N	\N	\N	\N	\N	\N	\N	Empório	Setor 2 - Santos Intermediário	\N	\N	-23.9618	-46.3322	\N	\N	\N	\N	0	Prospecto
72	10	\N	Pedro Lessa	Avenida Pedro Lessa, 1561	Aparecida	Santos	SP	\N	\N	\N	\N	\N	\N	\N	Empório	Setor 3A - Santos Orla Norte (Boqueirão / Aparecida)	\N	\N	-23.9727	-46.3297	\N	\N	\N	\N	0	Prospecto
73	10	\N	Adhemar de Barros	Av. Ademar de Barros, 2235	Vila Santa	Guarujá	SP	\N	\N	\N	\N	\N	\N	\N	Empório	Setor 6 - Guarujá	\N	\N	-23.9687	-46.2387	\N	\N	\N	\N	0	Prospecto
74	14	\N	Samambaia	R. Benedita Custódio, 175	Samambaia	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 7B - Praia Grande Interior / Sul	\N	\N	-24.0777	-46.3317	\N	\N	\N	\N	0	Prospecto
75	14	\N	Anhanguera	R. Joséfa Alves de Siqueira, 5891	Anhanguera	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 7B - Praia Grande Interior / Sul	\N	\N	-24.0727	-46.3387	\N	\N	\N	\N	0	Prospecto
76	14	\N	Gonzaga	Av. Ana Costa, 364	Gonzaga	Santos	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9905	-46.3167	\N	\N	\N	\N	0	Prospecto
77	14	\N	Rádio Clube	R. Ver. Ávaro Guimarãs, 148	Radio Clube	Santos	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 1 - Santos Centro / Porto	\N	\N	-23.953	-46.3408	\N	\N	\N	\N	0	Prospecto
78	14	\N	Nova Cintra	Av. Santista, 833	Morro Nova Cintra	Santos	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 1 - Santos Centro / Porto	\N	\N	-23.9437	-46.3607	\N	\N	\N	\N	0	Prospecto
79	14	\N	Almeida Rocha I	R. Guilherme Raposo de Almeida, 373	Cidade Náutica	São Vicente	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 5 - São Vicente	\N	\N	-23.9617	-46.4147	\N	\N	\N	\N	0	Prospecto
80	14	\N	Almeida Rocha II	Av. Marcolino Xavier de Carvalho, 325	Conj. Res. Tancredo Neves	São Vicente	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 5 - São Vicente	\N	\N	-23.9687	-46.4217	\N	\N	\N	\N	0	Prospecto
81	14	\N	União	Av. Pref. Prestes Maia, 20	Esplanada dos Barreiros	São Vicente	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 5 - São Vicente	\N	\N	-23.9547	-46.4267	\N	\N	\N	\N	0	Prospecto
82	14	\N	Frei Gaspar	R. Frei Gaspar, 2000	Parque Sao Vicente	São Vicente	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 5 - São Vicente	\N	\N	-23.9577	-46.4337	\N	\N	\N	\N	0	Prospecto
83	14	\N	Caiçara	Av. dos CaiÃ§aras, 1682	Jardim Las Palmas	Guarujá	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 6 - Guarujá	\N	\N	-23.9527	-46.2097	\N	\N	\N	\N	0	Prospecto
84	14	\N	Enseada	R. Ãureo Guenaga de Castro, 476	Parque Enseada	Guarujá	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 6 - Guarujá	\N	\N	-23.9997	-46.2247	\N	\N	\N	\N	0	Prospecto
85	14	\N	Vicente de Carvalho	Av. Santos Dumont, 1503	Paecara	Guarujá	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 6 - Guarujá	\N	\N	-23.9887	-46.2527	\N	\N	\N	\N	0	Prospecto
86	14	\N	Vila Nova	Av. Martins Fontes, 1101	Vila Nova	Cubatão	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 1 - Santos Centro / Porto	\N	\N	-23.8887	-46.4157	\N	\N	\N	\N	0	Prospecto
87	14	\N	Casqueiro	Av. Joaquim Jorge Peralta, 166	Parque Sao Luis	Cubatão	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 1 - Santos Centro / Porto	\N	\N	-23.8757	-46.3887	\N	\N	\N	\N	0	Prospecto
88	14	\N	Peruíbe	Av. Luciano de Bona, 2027	Vila Romar	Peruíbe	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 8 - Litoral Sul	\N	\N	-24.3057	-47.0097	\N	\N	\N	\N	0	Prospecto
89	14	\N	Padre Anchieta	Av. Padre Anchieta, 6193	Parque Balneario Oasis	Peruíbe	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 8 - Litoral Sul	\N	\N	-24.3157	-47.0197	\N	\N	\N	\N	0	Prospecto
90	14	\N	Aresta	Av. Nossa Sra. de Fátima, 430	Balneário Agenor de Campos	Mongaguá	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 8 - Litoral Sul	\N	\N	-24.1157	-46.6457	\N	\N	\N	\N	0	Prospecto
91	14	\N	Krill Meri	Av. Marina, 1081	Centro	Mongaguá	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 8 - Litoral Sul	\N	\N	-24.0887	-46.6237	\N	\N	\N	\N	0	Prospecto
92	14	\N	Itanhaém	R. dos Fundadores, 453	Belas Artes	Itanhaém	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 8 - Litoral Sul	\N	\N	-24.1657	-46.7757	\N	\N	\N	\N	0	Prospecto
93	14	\N	Bertioga	Av. Anchieta, 2300	Jardim Albatroz	Bertioga	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 8 - Litoral Sul	\N	\N	-23.8557	-46.1387	\N	\N	\N	\N	0	Prospecto
94	14	\N	Boracéia	Rod. Dr. Manoel Hyppolito Rego, 775	Caiubura	Boracéia	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 8 - Litoral Sul	\N	\N	-23.8487	-45.8897	\N	\N	\N	\N	0	Prospecto
95	14	\N	Boiçucanga	Estr. do Cascalho, 415	Boiçucanga	São Sebastião	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 8 - Litoral Sul	\N	\N	-23.7687	-45.6897	\N	\N	\N	\N	0	Prospecto
96	12	1	São Vicente	Av. Dr. Esmeraldo Soares Tarquínio de Campos, 760	Parque das Bandeiras	São Vicente	SP	\N	\N	\N	13 3566-0969/13 98855-4861	\N	\N	\N	Supermercado	Setor 5 - São Vicente	\N	\N	-23.9477	-46.4177	\N	\N	\N	\N	0	Prospecto
97	12	2	Praia Grande	Av. Presidente Kennedy, 18049	Balneário Florida	Praia Grande	SP	\N	\N	\N	13 3493-2500/13 99756-2319	\N	\N	\N	Supermercado	Setor 7A - Praia Grande Orla / Norte	\N	\N	-24.0297	-46.3787	\N	\N	\N	\N	0	Prospecto
98	2	\N	Vila Tupi	R. Guaranis, 240	Vila Tupi	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 7A - Praia Grande Orla / Norte	\N	\N	-24.0127	-46.4017	\N	\N	\N	\N	0	Prospecto
99	2	\N	São Vicente	Av. Dep. Ulisses Guimarãs, 472	Jardim Rio Branco	São Vicente	SP	\N	\N	\N	(13) 97406-8105	\N	\N	\N	Supermercado	Setor 5 - São Vicente	\N	\N	-23.9547	-46.4097	\N	\N	\N	\N	0	Prospecto
100	13	\N	Mongaguá-Vl.Antártica	Avenida Doutor Luiz Pereira Barreto, 436	Vila Atlântica	Mongaguá	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 8 - Litoral Sul	\N	\N	-24.1027	-46.6357	\N	\N	\N	\N	0	Prospecto
101	13	\N	Itanhaém	Avenida Rui Barbosa, 420	Centro	Itanhaém	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 8 - Litoral Sul	\N	\N	-24.1837	-46.7897	\N	\N	\N	\N	0	Prospecto
102	15	\N	Nova Mirim	R. Manoel Felíciano de Oliveira, 1340	Nova Mirim	Praia Grande	SP	\N	\N	\N	(13) 98205-1340	\N	\N	\N	Atacadista	Setor 7B - Praia Grande Interior / Sul	\N	\N	-24.0437	-46.3667	\N	\N	\N	\N	0	Prospecto
103	15	\N	Itanhaém	R. Equador, 830	Estância Balnearia	Itanhaém	SP	\N	\N	\N	(13) 99662-7452	\N	\N	\N	Atacadista	Setor 8 - Litoral Sul	\N	\N	-24.1987	-46.8027	\N	\N	\N	\N	0	Prospecto
104	19	\N	Proplastik Embaré	Av. Pedro Lessa, 2259	Embaré	Santos	SP	\N	\N	\N	(13) 3278-9000	\N	\N	\N	Confeitaria	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9871	-46.3247	\N	\N	\N	\N	0	Prospecto
105	19	\N	Proplastik Produtos Naturais	Av. Pedro Lessa, 2327	Embaré	Santos	SP	\N	\N	\N	(13) 3202-0300	\N	\N	\N	Confeitaria	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9871	-46.3247	\N	\N	\N	\N	0	Prospecto
106	19	\N	Proplastik Centro	R. JoÃ£o Pessoa, 10	Centro	Santos	SP	\N	\N	\N	(13) 3213-1444	\N	\N	\N	Confeitaria	Setor 1 - Santos Centro / Porto	\N	\N	-23.9618	-46.3322	\N	\N	\N	\N	0	Prospecto
107	19	\N	Proplastik Gonzaga	R. Floriano Peixoto, 78	Gonzaga	Santos	SP	\N	\N	\N	(13) 3285-9595	\N	\N	\N	Confeitaria	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9905	-46.3167	\N	\N	\N	\N	0	Prospecto
108	19	\N	Proplastik Vicente de Carvalho	Av. Thiago Ferreira, 286	Vic. de Carvalho	Guarujá	SP	\N	\N	\N	(13) 3343-3133	\N	\N	\N	Confeitaria	Setor 6 - Guarujá	\N	\N	-23.9927	-46.2567	\N	\N	\N	\N	0	Prospecto
109	19	\N	Proplastik São Vicente	R. Jacob Emerick, 416	Centro	São Vicente	SP	\N	\N	\N	(13) 3569-6500	\N	\N	\N	Confeitaria	Setor 5 - São Vicente	\N	\N	-23.964	-46.3917	\N	\N	\N	\N	0	Prospecto
110	16	\N	Caiçara	Av. Pres. Kennedy, 12665	Caiçara	Praia Grande	SP	\N	\N	\N	(13) 99160-9768	\N	\N	\N	Empório	Setor 7B - Praia Grande Interior / Sul	\N	\N	-24.0337	-46.3717	\N	\N	\N	\N	0	Prospecto
111	16	\N	Aviação	Av. Pres. Castelo Branco, 4194	Aviação	Praia Grande	SP	\N	\N	\N	(13) 99753-1236	\N	\N	\N	Empório	Setor 7A - Praia Grande Orla / Norte	\N	\N	-23.9987	-46.4077	\N	\N	\N	\N	0	Prospecto
112	16	\N	Brasil	Av. Brasil, 262	Boqueirão	Praia Grande	SP	\N	\N	\N	(13) 99759-7577	\N	\N	\N	Empório	Setor 7A - Praia Grande Orla / Norte	\N	\N	-24.0087	-46.3997	\N	\N	\N	\N	0	Prospecto
113	16	\N	Jaú	R. Jaú, 1281	Boqueirão	Praia Grande	SP	\N	\N	\N	(13) 99772-9352	\N	\N	\N	Empório	Setor 7A - Praia Grande Orla / Norte	\N	\N	-24.0087	-46.3997	\N	\N	\N	\N	0	Visitado
114	58	\N	Canto do Forte	R. Rui Barbosa, 618	Canto do Forte	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Padaria	Setor 7A - Praia Grande Orla / Norte	A/B	G	-24.004975	-46.398018	\N	\N	\N	\N	0	Prospecto
117	61	\N	Centro	R. Benjamin Constant, 441	Centro	Guarujá	SP	\N	\N	\N	\N	\N	\N	\N	Hamburgueria	Setor 6 - Guarujá	\N	\N	-23.996	-46.255	\N	\N	\N	\N	0	Prospecto
118	62	\N	Samambaia	Av. Almeida Junior, 665	Samambaia	Praia Grande	SP	\N	\N	\N	(13) 99653-3018	\N	\N	\N	Hamburgueria	Setor 7B - Praia Grande Interior / Sul	\N	\N	-24.0134	-46.4202	\N	\N	\N	\N	0	Prospecto
119	63	\N	Vila Santa Rosa	R. Luis Felipe Machado, 592	Vila Santa Rosa	Guarujá	SP	\N	\N	\N	(13) 99133-0059	\N	\N	\N	Hamburgueria	Setor 6 - Guarujá	\N	\N	-23.9948	-46.2562	\N	\N	\N	\N	0	Prospecto
120	64	\N	Aparecida	Av. Senador Dantas, 330	Aparecida	Santos	SP	\N	\N	\N	(13) 97424-7729	\N	\N	\N	Hamburgueria	Setor 3A - Santos Orla Norte (Boqueirão / Aparecida)	\N	\N	-23.958	-46.3222	\N	\N	\N	\N	0	Prospecto
121	65	\N	Campo Grande	Av. Ana Costa - Canal 5	Campo Grande	Santos	SP	\N	\N	\N	(13) 99650 9498	\N	\N	\N	Hamburgueria	Setor 2 - Santos Intermediário	\N	\N	-23.9678	-46.3255	\N	\N	\N	\N	0	Prospecto
122	65	\N	Embaré	Av. Siqueira Campos, 675 Canal 4 (Boteco)	Embaré	Santos	SP	\N	\N	\N	(13) 97425-5676	\N	\N	\N	Bar	Setor 3A - Santos Orla Norte (Boqueirão / Aparecida)	\N	\N	-23.9678	-46.3255	\N	\N	\N	\N	0	Prospecto
123	65	\N	Pompeia	Av. Marechal Deodoro, 1 - Canal 2	Pompeia	Santos	SP	\N	\N	\N	(13) 99650 9498	\N	\N	\N	Hamburgueria	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9614	-46.323	\N	\N	\N	\N	0	Prospecto
124	66	\N	Santos	Av. Siqueira Campos, 260	Boqueirao	Santos	SP	\N	\N	\N	(13) 98192-9806	\N	\N	\N	Hamburgueria	Setor 3A - Santos Orla Norte (Boqueirão / Aparecida)	\N	\N	-23.9545	-46.3308	\N	\N	\N	\N	0	Prospecto
125	67	\N	Centro	R. Carlos Gomes, 153	Centro	Santos	SP	\N	\N	\N	(13) 99126-7562	\N	\N	\N	Hamburgueria	Setor 1 - Santos Centro / Porto	\N	\N	-23.9625	-46.3451	\N	\N	\N	\N	0	Prospecto
126	68	\N	Boqueirao	R. da Paz, 51	Boqueirao	Santos	SP	\N	\N	\N	(13) 99680-8180	\N	\N	\N	Hamburgueria	Setor 3A - Santos Orla Norte (Boqueirão / Aparecida)	\N	\N	-23.953	-46.328	\N	\N	\N	\N	0	Prospecto
127	69	\N	Aparecida	Av. Pedro Lessa, 1007	Aparecida	Santos	SP	\N	\N	\N	(13) 99689-4805	\N	\N	\N	Casa de Carnes	Setor 3A - Santos Orla Norte (Boqueirão / Aparecida)	\N	\N	-23.9572	-46.3218	\N	\N	\N	\N	0	Prospecto
128	70	\N	Campo Grande	R. Joao Caetano, 117	Campo Grande	Santos	SP	\N	\N	\N	(13) 97405-6394	\N	\N	\N	Casa de Carnes	Setor 2 - Santos Intermediário	\N	\N	-23.9675	-46.3285	\N	\N	\N	\N	0	Prospecto
116	60	\N	Centro	R. Hermenegildo Barbosa, 200, loja 1	Centro	Mongaguá	SP	\N	\N	\N	(13) 99610-1520	\N	\N	\N	Hamburgueria	Setor 8 - Litoral Sul	\N	\N	-24.086	-46.6198	\N	\N	\N	\N	0	Prospecto
129	71	\N	Boqueirao	R. Vahia Abreu, 85	Boqueirao	Santos	SP	\N	\N	\N	13 996492340	\N	\N	\N	Casa de Carnes	Setor 3A - Santos Orla Norte (Boqueirão / Aparecida)	\N	\N	-23.9562	-46.3295	\N	\N	\N	\N	0	Prospecto
130	72	\N	Gonzaga	R. Alagoas, 6	Gonzaga	Santos	SP	\N	\N	\N	(13) 99144-1440	\N	\N	\N	Hamburgueria	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9694	-46.3362	\N	\N	\N	\N	0	Prospecto
131	21	\N	Jardim Casqueiro	Av. Brasil, 238	Jardim Casqueiro	Cubatão	SP	\N	\N	\N	(13) 9.9659-8334	\N	\N	\N	Casa de Carnes	Setor 1 - Santos Centro / Porto	\N	\N	-23.894	-46.4262	\N	\N	\N	\N	0	Prospecto
132	21	\N	Marape	Av. Pinheiro Machado, 728	Marape	Santos	SP	\N	\N	\N	(13) 9.9753-2601 	\N	\N	\N	Casa de Carnes	Setor 2 - Santos Intermediário	\N	\N	-23.9658	-46.3348	\N	\N	\N	\N	0	Prospecto
133	73	\N	Boqueirao	Av. Siqueira Campos, 554	Boqueirao	Santos	SP	\N	\N	\N	(13) 99107-8874	\N	\N	\N	Hamburgueria	Setor 3A - Santos Orla Norte (Boqueirão / Aparecida)	\N	\N	-23.9548	-46.3301	\N	\N	\N	\N	0	Prospecto
134	74	\N	Centro	R. Cidade de Santos, 821	Centro	Itanhaém	SP	\N	\N	\N	(13) 98124-2664	\N	\N	\N	Hamburgueria	Setor 8 - Litoral Sul	\N	\N	-24.1838	-46.787	\N	\N	\N	\N	0	Prospecto
135	75	\N	Embare	R. Conselheiro Lafayette, 76	Embare	Santos	SP	\N	\N	\N	(13) 99135-4096	\N	\N	\N	Hamburgueria	Setor 3A - Santos Orla Norte (Boqueirão / Aparecida)	\N	\N	-23.965	-46.334	\N	\N	\N	\N	0	Prospecto
136	76	\N	Tupi	Av. Kennedy, 5303	Tupi	Praia Grande	SP	\N	\N	\N	(11) 98747-6935	\N	\N	\N	Hamburgueria	Setor 7A - Praia Grande Orla / Norte	\N	\N	-24.021	-46.435	\N	\N	\N	\N	0	Prospecto
137	77	\N	Jardim Guaramar	Av. do Trabalhador, 456	Jardim Guaramar	Praia Grande	SP	\N	\N	\N	(13) 99677-5035	\N	\N	\N	Hamburgueria	Setor 7A - Praia Grande Orla / Norte	\N	\N	-24.018	-46.4298	\N	\N	\N	\N	0	Prospecto
138	78	\N	Embaré	R. Galeão Coutinho, 454	Embaré	Santos	SP	\N	\N	\N	(13) 99183-8160	\N	\N	\N	Hamburgueria	Setor 3A - Santos Orla Norte (Boqueirão / Aparecida)	\N	\N	-23.9686	-46.3184	\N	\N	\N	\N	0	Prospecto
139	79	\N	Arpoador	Av. Padre Anchieta, 3398	Arpoador	Peruíbe	SP	\N	\N	\N	(13) 99758-4602	\N	\N	\N	Hamburgueria	Setor 8 - Litoral Sul	\N	\N	-24.324	-47.008	\N	\N	\N	\N	0	Prospecto
140	79	\N	Canto do Forte	Av. Marechal Mallet, 1121	Canto do Forte	Praia Grande	SP	\N	\N	\N	(13) 99633-7490	\N	\N	\N	Hamburgueria	Setor 7A - Praia Grande Orla / Norte	\N	\N	-24.01	-46.405	\N	\N	\N	\N	0	Prospecto
141	80	\N	Vila Margarida	R. Monte Castelo, 131	Vila Margarida	São Vicente	SP	\N	\N	\N	(13) 98148-3134	\N	\N	\N	Hamburgueria	Setor 5 - São Vicente	\N	\N	-23.9703	-46.3998	\N	\N	\N	\N	0	Prospecto
142	81	\N	Jose Menino	Av. Pres. Wilson, 167	Jose Menino	Santos	SP	\N	\N	\N	(13) 99146-0734	\N	\N	\N	Hamburgueria	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9773	-46.3421	\N	\N	\N	\N	0	Prospecto
143	82	\N	Ponta da Praia	R. Bassim Nagib Trabulsi, 79	Ponta da Praia	Santos	SP	\N	\N	\N	13 98152-0184	\N	\N	\N	Hamburgueria	Setor 4 - Ponta da Praia	\N	\N	-23.9795	-46.3231	\N	\N	\N	\N	0	Prospecto
144	83	\N	Quietude	R. Eros Emílio Turolla, 32389	Quietude	Praia Grande	SP	\N	\N	\N	(13) 99650-1065	\N	\N	\N	Hamburgueria	Setor 7A - Praia Grande Orla / Norte	\N	\N	-24.0144	-46.4783	\N	\N	\N	\N	0	Prospecto
145	84	\N	Vila Nova	Pça. Januario Estevam de Lara Dantes, 216	Vila Nova	Mongaguá	SP	\N	\N	\N	(13) 97401-2767	\N	\N	\N	Hamburgueria	Setor 8 - Litoral Sul	\N	\N	-24.087	-46.62	\N	\N	\N	\N	0	Prospecto
146	85	\N	Boqueirao	Av. Conselheiro Nebias, 821	Boqueirao	Santos	SP	\N	\N	\N	(13) 3385-8324	\N	\N	\N	Hamburgueria	Setor 3A - Santos Orla Norte (Boqueirão / Aparecida)	\N	\N	-23.9566	-46.3312	\N	\N	\N	\N	0	Prospecto
147	86	\N	Gonzaga	R. Azevedo Sodre, 114	Gonzaga	Santos	SP	\N	\N	\N	(13) 98200-7120	\N	\N	\N	Hamburgueria	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9697	-46.3371	\N	\N	\N	\N	0	Prospecto
148	87	\N	Gonzaga	Av. Washington Luis, 191	Gonzaga	Santos	SP	\N	\N	\N	(13) 99109-1051	\N	\N	\N	Hamburgueria	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.9702	-46.3374	\N	\N	\N	\N	0	Prospecto
149	88	\N	Boqueirao	Av. Dr. Epitacio Pessoa, 117	Boqueirao	Santos	SP	\N	\N	\N	\N	\N	\N	\N	Hamburgueria	Setor 3A - Santos Orla Norte (Boqueirão / Aparecida)	\N	\N	-23.9538	-46.327	\N	\N	\N	\N	0	Prospecto
150	89	\N	Boqueirao	R. Luiza Antonio de Andrade Vieira, 51	Boqueirao	Praia Grande	SP	\N	\N	\N	(13) 99668-2652	\N	\N	\N	Hamburgueria	Setor 7A - Praia Grande Orla / Norte	\N	\N	-24.005	-46.401	\N	\N	\N	\N	0	Prospecto
151	90	\N	Gonzaga	Pça. Fernandes Pacheco, 23	Gonzaga	Santos	SP	\N	\N	\N	(13) 3222-4528	\N	\N	\N	Hamburgueria	Setor 3B - Santos Orla Sul (Gonzaga / José Menino)	\N	\N	-23.97	-46.335	\N	\N	\N	\N	0	Prospecto
152	91	\N	Centro	Av. Oswaldo Cruz, 422	Centro	Guarujá	SP	\N	\N	\N	(13) 98834-4676	\N	\N	\N	Hamburgueria	Setor 6 - Guarujá	\N	\N	-23.9939	-46.2568	\N	\N	\N	\N	0	Prospecto
153	66	\N	São Vicente	Av. Prefeito José Monteiro, 568	Jardim Independência	São Vicente	SP	\N	\N	\N	(13) 98194-0260 	\N	\N	\N	Hamburgueria	Setor 5 - São Vicente	\N	\N	-23.96406	-46.37314	\N	\N	\N	\N	0	Prospecto
154	94	\N	Coop	R. dos Coqueiros, 310	Campestre	Santo André	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	\N	\N	\N	\N	\N	\N	\N	\N	\N	0	visitado
155	95	\N	Good Times Burger	Av. Marechal Mallet, 1619	Canto do Forte	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Hamburgueria	Setor 7A - Praia Grande Orla / Norte	\N	\N	-24.0041	-46.3986	\N	\N	\N	\N	0	Prospecto
160	93	5142	MPA Marechal Mallet	Av. Marechal Mallet, 608	Canto do Forte	Praia Grande	SP	\N	\N	\N	\N	\N	\N	\N	Supermercado	Setor 7A - Praia Grande Orla / Norte	A/B	G	\N	\N	\N	\N	\N	\N	0	Prospecto
164	100	\N	GePires	Av. Yervant Kissajikian, 1666	Vl. Joaniza	São Paulo	SP	60.354.596/0001-50	\N	\N	\N	Thiago	11 99932-1896	\N	Supermercado	\N	C/D	M	\N	\N	\N	\N	\N	\N	1	Ativo
\.


--
-- Data for Name: pedido; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pedido (pedido_id, nr_pedido_fornecedor, nr_pedido_cliente, cliente_id, pdv_id, fornecedor_id, vendedor_id, tabela_preco_id, prazo_pagamento, frete, data_pedido, data_entrega, desconto_geral, observacao, status_pedido, comissao_percentual, data_entrega_realizada) FROM stdin;
1	\N	\N	1	\N	1	\N	2	28 dias	CIF	2026-03-26	\N	0	\N	ENTREGUE	\N	\N
2	\N	\N	3	2	1	\N	2	28 dias	CIF	2026-04-04	2026-04-10	10	Desconto de 10% nos primeiros 3 pedidos. (Pedido 1 de 3)	RECUSADO	\N	\N
4	107541	\N	100	164	1	\N	20	28	CIF	2026-05-11	2026-05-20	0	\N	ABERTO	\N	\N
\.


--
-- Data for Name: pedido_historico; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pedido_historico (historico_id, pedido_id, data_hora, campo, valor_antes, valor_depois, observacao) FROM stdin;
1	2	2026-04-04 19:55:10	status_pedido	ABERTO	RECUSADO	\N
2	1	2026-04-04 20:00:49	status_pedido	ABERTO	FATURADO	\N
3	1	2026-04-07 21:00:11	status_pedido	FATURADO	ENTREGUE	\N
\.


--
-- Data for Name: pedido_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pedido_item (pedido_item_id, pedido_id, produto_id, preco_tabela, desconto, preco_final, quantidade, status_item) FROM stdin;
1	1	23	26.42	0	26.42	16	NORMAL
2	2	1	40	0	36	1	NORMAL
3	2	31	39.95	0	35.955	2	NORMAL
4	2	29	45	0	40.5	2	NORMAL
5	2	27	41.4	0	37.26	1	NORMAL
6	2	10	45	0	40.5	1	NORMAL
7	2	9	45	0	40.5	1	NORMAL
8	2	6	72.73	0	65.457	2	NORMAL
9	2	14	19.03	0	17.127	2	NORMAL
10	2	8	67.05	0	60.345	1	NORMAL
11	2	13	19.03	0	17.127	2	NORMAL
12	2	7	67.05	0	60.345	1	NORMAL
13	2	2	23.64	0	21.276	2	NORMAL
14	2	3	23.64	0	21.276	2	NORMAL
16	4	2	23.22	0	23.22	10	NORMAL
17	4	3	23.22	0	23.22	10	NORMAL
18	4	6	70.18	0	70.18	10	NORMAL
19	4	7	65.37	0	65.37	2	NORMAL
20	4	8	65.37	0	65.37	1	NORMAL
21	4	9	44.19	0	44.19	5	NORMAL
22	4	10	44.19	0	44.19	5	NORMAL
\.


--
-- Data for Name: pesquisa_foto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pesquisa_foto (foto_id, pesquisa_id, foto_data, nome_arquivo, descricao, data_upload, foto_path, legenda, ativo) FROM stdin;
1	28	\N	\N	\N	2026-04-18 17:23	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq28_1776543818514_0_WhatsApp Image 2026-04-18 at 16.59.13.jpeg	\N	1
2	28	\N	\N	\N	2026-04-18 17:23	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq28_1776543818523_1_WhatsApp Image 2026-04-18 at 16.59.12(4).jpeg	\N	1
3	28	\N	\N	\N	2026-04-18 17:23	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq28_1776543818524_2_WhatsApp Image 2026-04-18 at 16.59.12(3).jpeg	\N	1
4	28	\N	\N	\N	2026-04-18 17:23	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq28_1776543818525_3_WhatsApp Image 2026-04-18 at 16.59.12(2).jpeg	\N	1
5	28	\N	\N	\N	2026-04-18 17:23	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq28_1776543818525_4_WhatsApp Image 2026-04-18 at 16.59.12(1).jpeg	\N	1
6	28	\N	\N	\N	2026-04-18 17:23	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq28_1776543818526_5_WhatsApp Image 2026-04-18 at 16.59.12.jpeg	\N	1
7	28	\N	\N	\N	2026-04-18 17:23	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq28_1776543818527_6_WhatsApp Image 2026-04-18 at 16.59.11.jpeg	\N	1
8	29	\N	\N	\N	2026-04-25 19:16	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq29_1777155386943_0_WhatsApp Image 2026-04-23 at 18.40.57.jpeg	\N	1
9	30	\N	\N	\N	2026-04-25 19:42	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq30_1777156958140_0_WhatsApp Image 2026-04-23 at 18.40.58(1).jpeg	\N	1
10	30	\N	\N	\N	2026-04-25 19:42	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq30_1777156958144_1_WhatsApp Image 2026-04-23 at 18.40.58.jpeg	\N	1
11	28	\N	\N	\N	2026-04-25 19:54	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq28_1777157641494_0_WhatsApp Image 2026-04-23 at 18.40.57(2).jpeg	\N	1
13	37	\N	\N	\N	2026-05-10 20:25	/app/fotos_pesquisa/pq37_1778444711424_0_IMG_20260428_160023709_AE.jpg	\N	0
14	37	\N	\N	\N	2026-05-10 20:43	/app/fotos_pesquisa/pq37_1778445809820_0_IMG_20260428_160023709_AE.jpg	\N	0
16	37	\N	\N	\N	2026-05-10 22:38	/app/fotos_pesquisa/pq37_1778452685278_0_IMG_20260428_160023709_AE.jpg	\N	1
\.


--
-- Data for Name: pesquisa_preco; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pesquisa_preco (pesquisa_id, data_pesquisa, pdv_id, cliente_id, fornecedor_id, observacao, status, foto_path) FROM stdin;
35	2026-05-04	160	93	3	\N	finalizado	\N
36	2026-05-04	160	93	2	\N	finalizado	\N
37	2026-04-28	8	14	3	\N	finalizado	\N
44	2026-05-08	2	3	3	\N	finalizado	\N
5	2026-03-31	2	3	1	\N	finalizado	\N
6	2025-11-25	1	2	1	\N	finalizado	\N
7	2025-11-27	2	3	1	\N	finalizado	\N
8	2025-11-25	4	10	1	\N	finalizado	\N
9	2025-11-28	5	11	1	\N	finalizado	\N
10	2025-11-28	6	12	1	\N	finalizado	\N
11	2025-11-28	7	13	1	\N	finalizado	\N
12	2025-11-27	8	14	1	\N	finalizado	\N
14	2025-11-25	9	15	1	\N	finalizado	\N
15	2025-11-25	\N	16	1	\N	finalizado	\N
16	2025-11-28	11	17	1	\N	finalizado	\N
17	2025-11-27	12	18	1	\N	finalizado	\N
19	2025-11-27	14	20	1	\N	finalizado	\N
20	2025-11-27	13	19	1	\N	finalizado	\N
21	2026-04-03	9	15	1	\N	finalizado	\N
25	2026-04-05	15	21	1	\N	finalizado	\N
26	2026-04-07	4	10	2	\N	finalizado	\N
27	2026-04-07	4	10	1	\N	finalizado	\N
28	2026-04-15	154	94	1	\N	finalizado	C:\\Users\\welov\\PycharmProjects\\WebSolution\\peppercrm\\fotos_pesquisa\\pq_28_WhatsApp Image 2026-04-18 at 16.59.12.jpeg
29	2026-04-15	154	94	3	\N	finalizado	\N
31	2026-04-28	8	14	4	Gerente: Diego	finalizado	\N
34	2026-05-03	156	96	3	\N	finalizado	\N
32	2026-04-28	8	14	1	Gerente: Diego	finalizado	\N
30	2026-04-15	154	94	2	\N	finalizado	\N
\.


--
-- Data for Name: pesquisa_preco_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pesquisa_preco_item (pesquisa_item_id, pesquisa_id, produto_id, produto_concorrente_id, preco, em_oferta, frentes, ruptura, ponto_extra, tipo_ponto_extra, observacao, preco_proprio, facing, preco_concorrente, marca_concorrente_livre, obs_concorrente, foto_path, unidade_coleta, peso_coleta, preco_kg) FROM stdin;
7	5	30	27	4.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
8	5	31	28	4.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
11	5	2	9	2.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
12	5	2	5	4.99	0	8	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
13	5	2	7	2.99	0	6	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
14	5	3	10	4.99	0	15	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
15	5	3	13	2.99	0	10	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
16	5	6	1	14.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
17	5	7	17	15.49	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
19	6	6	1	14.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
20	6	2	9	2.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
21	7	3	10	4.99	0	8	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
22	7	3	4	2.99	0	6	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
23	7	8	15	14.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
24	7	6	3	9.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
26	8	13	26	9.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
27	8	12	32	24.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
28	8	12	33	34.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
29	8	12	34	28.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
30	9	2	5	3.15	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
31	9	2	6	2.15	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
32	9	3	10	2.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
33	9	3	11	2.15	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
34	9	3	4	1.75	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
35	9	6	1	11.19	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
36	9	9	21	8.25	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
37	10	10	18	8.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
38	10	2	5	3.99	0	6	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
39	10	2	6	2.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
40	10	2	7	2.59	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
41	10	3	10	4.49	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
42	10	3	11	2.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
43	10	3	13	2.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
44	10	6	1	12.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
45	10	12	25	5.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
46	11	10	18	8.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
47	11	9	21	10.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
48	11	9	22	7.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
49	11	2	6	2.79	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
50	11	10	19	7.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
51	11	8	15	11.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
52	11	12	25	6.79	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
53	11	12	35	13.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
54	12	10	18	7.79	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
55	12	2	5	3.69	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
56	12	2	9	2.49	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
57	12	3	10	3.69	0	6	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
58	12	3	13	2.49	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
59	12	8	15	9.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
60	12	7	17	9.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
61	12	6	36	7.99	0	8	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
62	14	2	8	2.39	0	6	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
63	15	12	25	9.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
64	15	12	37	14.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
65	15	2	38	7.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
66	16	2	5	4.19	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
68	16	2	9	2.69	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
69	16	2	6	2.69	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
70	16	10	18	7.39	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
71	16	10	20	3.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
72	16	3	10	3.39	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
73	16	3	12	2.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
74	16	3	13	2.69	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
75	16	9	21	8.29	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
76	16	9	23	6.45	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
77	16	6	1	12.79	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
78	16	6	14	8.29	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
79	16	12	25	5.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
80	16	12	39	5.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
81	16	12	24	6.19	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
82	16	8	15	9.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
83	16	8	16	7.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
84	17	6	1	12.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
85	17	12	35	12.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
87	19	2	9	2.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
88	19	3	10	4.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
89	19	3	13	2.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
90	19	6	1	14.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
91	20	12	37	13.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
92	21	3	54	2.39	0	5	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
93	21	3	4	1.79	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
94	21	2	7	1.79	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
95	10	2	40	12.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
96	10	10	41	8.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
97	10	9	44	4.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
98	10	9	45	5.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
99	10	12	46	32.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
100	10	12	47	14.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
101	15	12	50	46.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
102	12	10	41	7.79	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
103	12	9	43	8.19	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
104	9	9	42	8.15	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
105	20	12	53	36.5	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
106	20	12	55	44.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
107	20	9	56	6.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
108	16	9	42	7.39	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
109	16	9	45	5.19	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
110	16	9	44	4.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
111	16	12	46	44.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
112	16	12	48	24.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
113	16	12	49	17.79	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
114	16	12	52	16.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
115	11	10	41	9.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
116	11	9	44	6.79	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
117	11	9	42	10.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
118	11	9	45	6.79	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
119	11	12	46	34.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
120	11	12	47	16.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
121	11	12	50	29.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
122	8	12	49	27.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
123	25	12	25	19.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
124	25	2	5	3.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
125	25	31	28	3.98	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
126	25	31	57	5.9	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
127	26	47	58	22.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
128	26	47	59	36.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
129	26	47	60	39.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
130	26	47	61	36.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
131	26	47	62	36.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
132	26	47	63	36.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
133	26	75	64	34.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
134	26	47	65	39.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
135	26	75	66	35.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
136	27	11	67	11.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
137	27	11	68	14.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
138	27	13	26	14.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
139	27	9	43	19.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
140	27	12	49	22.99	0	10	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
141	27	12	25	7.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
142	27	12	33	34.99	0	11	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
143	27	12	34	28.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
145	28	7	17	13.99	0	5	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
146	28	6	1	14.49	0	5	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
147	28	3	10	4.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
148	28	2	5	4.99	0	10	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
149	28	7	69	10.99	0	5	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
150	28	8	16	10.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
151	28	2	8	2.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
152	28	2	9	2.99	0	16	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
153	28	3	13	2.99	0	8	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
154	28	2	40	14.99	0	5	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
155	28	2	70	14.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
156	28	2	71	17.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
157	28	12	47	38.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
158	28	11	72	33.19	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
159	28	14	73	21.29	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
160	28	9	21	9.99	0	9	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
163	28	11	75	30.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
165	28	11	77	40.49	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
166	28	11	78	34.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
167	28	11	79	68.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
168	28	14	80	43.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
169	28	11	81	18.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
170	29	248	85	20.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
171	29	269	238	22.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
172	29	264	239	20.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
173	29	254	97	8.49	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
174	29	257	92	17.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
175	30	47	62	32.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
176	30	47	63	32.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
177	30	47	240	26.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
178	30	52	241	30.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
179	28	31	28	3.99	0	5	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
180	28	31	242	3.79	0	6	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
181	28	31	243	9.19	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
182	28	31	244	6.99	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
183	28	31	245	5.89	0	5	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
184	31	373	214	8.49	0	6	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
185	31	373	\N	9.29	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
186	31	373	248	9.29	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
187	31	373	204	8.69	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
188	31	373	249	8.99	0	5	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
189	31	370	250	4.79	0	6	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
190	31	367	251	11.99	0	6	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
191	31	370	252	4.99	0	12	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
192	31	370	254	4.99	0	24	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
193	31	371	212	8.79	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
194	31	370	213	5.69	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
195	31	367	255	5.89	0	4	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
197	32	2	256	1.99	0	19	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
198	32	2	5	4.19	0	7	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
199	32	3	10	4.19	0	5	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
200	32	8	15	11.59	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
201	32	9	21	8.39	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
202	32	9	42	8.39	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
203	32	10	41	8.39	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
204	32	9	43	13.99	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
217	36	33	\N	30.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
223	37	312	260	37.99	0	10	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
218	36	45	\N	30.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
219	36	34	\N	30.99	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
210	34	311	153	24.49	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
211	35	309	146	24.9	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
212	35	311	257	26.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
220	36	47	240	27.99	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
213	35	311	258	26.9	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
215	35	309	151	20.9	0	3	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
216	35	311	259	17.38	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
221	36	47	61	37.64	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
222	36	47	63	37.64	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
247	44	308	\N	26.98	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
249	44	308	156	27.96	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
250	44	312	\N	39	0	2	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
251	44	312	260	39.99	0	8	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
252	44	309	\N	29.98	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
253	44	309	151	26.98	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
254	44	308	147	32.98	0	1	0	0	\N	\N	\N	\N	\N	\N	\N	\N	UN	\N	\N
\.


--
-- Data for Name: produto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.produto (produto_id, fornecedor_id, marca_id, categoria_id, linha_id, codigo_produto, descricao, descricao_curta, peso, peso_caixa, unidade_medida, unidades_caixa, caixas_pallet, ean, dun, ncm, cest, validade_dias, sub_categoria, grupo, observacao, ativo, shelf_life_resfriado, shelf_life_congelado) FROM stdin;
367	4	5	20	28	T2	Massa c/Ovos Caseira "DE", Talharim nº2 500g	Talharim Caseiro De n° 2 500g	500	0	g	20	\N	789.61938.0022-9	1.789.61938.0022-6	\N	\N	365	\N	\N	\N	1	\N	\N
368	4	5	20	28	T3	Massa c/Ovos Caseira "DE", Talharim nº3 500g	Talharim Caseiro De n° 3 500g	500	0	g	20	\N	789.61938.0033-5	1.789.61938.0033-2	\N	\N	365	\N	\N	\N	1	\N	\N
369	4	5	20	28	T4	Massa c/Ovos Caseira "DE", Talharim nº4 500g	Talharim Caseiro De n° 4 500g	500	0	g	20	\N	789.61938.0044-1	1.789.61938.0044-8	\N	\N	365	\N	\N	\N	1	\N	\N
371	4	5	22	28	GRAVA	Massa c/Ovos Caseira "DE", Gravata 500g	Gravata Caseira De 500g	500	\N	g	24	\N	789.61938.0003-8	1.789.61938.0003-5	\N	\N	365	\N	\N	\N	1	\N	\N
372	4	5	22	28	GRAVAT	Massa c/Ovos Caseira "DE", Gravatinha 500g	Gravatinha Caseira De 500g	500	\N	g	20	\N	789.61938.0005-2	1.789.61938.0005-9	\N	\N	365	\N	\N	\N	1	\N	\N
378	4	5	23	5	LASINST	Massa c/Ovos Caseira "DE", Lasanha Instantanea 200g	Lasanha Gourmet Caseira Instantânea De 200g	200	0	g	36	\N	789.61938.0010-6	1.789.61938.0010-3	\N	\N	365	\N	\N	\N	1	\N	\N
370	4	5	21	28	N2	Massa c/Ovos Caseira "DE", Ninho nº2 500g	Ninho Caseiro De n° 2 500g	500	0	g	24	\N	789.61938.0019-9	1.789.61938.0019-6	\N	\N	365	\N	\N	\N	1	\N	\N
373	4	5	23	28	LAS	Massa c/Ovos Caseira "DE", p/ Lasanha 500g	Lasanha Caseira De 500g	500	0	g	24	\N	789.61938.0002-1	1.789.61938.0002-8	\N	\N	365	\N	\N	\N	1	\N	\N
377	4	5	25	5	PAPPA	Massa c/Ovos Caseira "DE", Pappardelle 400g	Pappardelle De 400g	400	0	g	10	\N	789.61938.0042-7	1.789.61938.0042-4	\N	\N	365	\N	\N	\N	1	\N	\N
365	4	5	20	28	T0	Massa c/Ovos Caseira "DE", Talharim nº0 500g	Talharim Caseiro De n° 0 500g	500	0	g	20	\N	789.61938.0000-7	1.789.61938.0000-4	\N	\N	365	\N	\N	\N	1	\N	\N
366	4	5	20	28	T1	Massa c/Ovos Caseira "DE", Talharim nº1 500g	Talharim Caseiro De n° 1 500g	500	0	g	20	\N	789.61938.0011-3	1.789.61938.0011-0	\N	\N	365	\N	\N	\N	1	\N	\N
376	4	5	24	30	YAK200g	Massa c/Ovos Caseira "DE", Yakissoba 200g	Massa p/ Yakissoba De 200g	200	0	g	25	\N	789.61938.0028-1	1.789.61938.0028-8	\N	\N	365	\N	\N	\N	1	\N	\N
387	4	5	22	28	GRAVAT_B	Massa c/Ovos Caseira "DE",Gravata Borboleta 500g	Gravata Borboleta Caseira De 500g	500	\N	g	20	\N	\N	\N	\N	\N	365	\N	\N	\N	1	\N	\N
375	4	5	24	30	YAK1kg	Massa c/Ovos p/Yakissoba "DE"1kgTradicional (Trançada)	Massa p/ Yakissoba Matassado De 1Kg	1	0	Kg	10	\N	789.61938.0035-9	1.789.61938.0035-6	\N	\N	365	\N	\N	\N	1	\N	\N
374	4	5	20	29	INT2	Massa Integral Caseira"DE", Talharim nº2 500g	Macarrão com Trigo Integral De n° 2 500g	500	0	g	20	\N	789.61938.0038-0	1.789.61938.0038-7	\N	\N	365	\N	\N	\N	1	\N	\N
30	1	1	16	10	19.01.08.64	Molho De Alho 150ml	Molho De Alho 150ml	150	\N	ml	12	\N	\N	\N	\N	\N	180	\N	\N	\N	1	\N	\N
31	1	1	16	10	19.01.08.63	Molho De Pimenta 150ml	Molho De Pimenta 150ml	150	\N	ml	12	\N	789609050069-7	1789609050069-4	\N	\N	365	\N	\N	\N	1	\N	\N
382	1	2	2	1	10.02.03.01	Vinagre De Álcool Colorido Vinaro 750ml	Vinagre De Álcool Colorido Vinaro 750ml	750	\N	ml	12	\N	789609050097-0	2789609050097-4	\N	\N	1095	\N	\N	\N	1	\N	\N
383	1	2	2	1	10.02.03.02	Vinagre De Álcool Vinaro 750ml	Vinagre De Álcool Vinaro 750ml	750	\N	ml	12	\N	789609050096-3	2789609050096-7	\N	\N	1095	\N	\N	\N	1	\N	\N
385	2	3	7	11	48	Cocada Diet 250g	Cocada Diet 250g	250	\N	g	12	\N	7897953700971	\N	20079990	\N	365	KIT JUNINO	COCADA	\N	1	\N	\N
384	2	3	7	11	49	Camafeu Diet 250g	Camafeu Diet 250g	250	\N	g	12	\N	789795370065-0	\N	20079990	\N	365	KIT JUNINO	CAMAFEU	\N	1	\N	\N
386	2	3	7	11	50	Pé de Moça 250g	Pé de Moça 250g	250	\N	g	12	\N	789795370083-4	\N	20079990	\N	365	KIT JUNINO	PÉ DE MOÇA	\N	1	\N	\N
29	1	1	5	9	18.01.07.30	Puro Alho Sem Sal 200g	Puro Alho Sem Sal 200g	200	\N	g	12	\N	789609050117-5	2789609050117-9	\N	\N	180	\N	\N	\N	1	\N	\N
28	1	1	5	9	18.01.07.29	Tempero Completo Com Pimenta 200g	Tempero Completo Com Pimenta 200g	200	\N	g	12	\N	\N	\N	\N	\N	180	\N	\N	\N	1	\N	\N
27	1	1	5	9	18.01.07.28	Tempero Completo Cremoso 200g	Tempero Completo Cremoso 200g	200	\N	g	12	\N	789609050119-9	2789609050119-3	\N	\N	1095	\N	\N	\N	1	\N	\N
35	2	3	7	11	4	Doce de Abacaxi Cremoso Diet 250g	Doce de Abacaxi Cremoso Diet 250g	250	\N	g	12	\N	7897953700537	\N	20079990	\N	365	ABACAXÍ	CREMOSO	\N	1	\N	\N
1	1	1	1	1	10.01.03.60	Limpeza Vinagre Concent.5% 2lts	Limpeza Vinagre Concent.5% 2lts	2	\N	L	6	\N	789609050164-9	1789609050164-6	\N	\N	180	\N	\N	\N	1	\N	\N
16	1	1	3	5	12.01.09.65	Oleo Comp.de Soja E Azeite De Oliva 500ml	Oleo Comp.de Soja E Azeite De Oliva 500ml	500	\N	ml	12	\N	789609050187-8	\N	\N	\N	180	\N	\N	\N	1	\N	\N
24	1	1	4	8	17.01.06.25	Palmito Pupunha Inteiro 300g	Palmito Pupunha Inteiro 300g	300	\N	g	15	\N	\N	\N	\N	\N	180	\N	\N	\N	1	\N	\N
11	1	1	2	5	13.01.02.17	Vinagre Balsâmico 380ml	Vinagre Balsâmico 380ml	380	\N	ml	12	\N	789609050165-6	9789609050173-4	\N	\N	1095	\N	\N	\N	1	\N	\N
20	1	1	2	7	14.01.04.18	Vinagre Composto Branco 5 Lts	Vinagre Composto Branco 5 Lts	5	\N	L	1	\N	789609050025-3	\N	\N	\N	1095	\N	\N	\N	1	\N	\N
5	1	1	2	3	11.01.04.09	Vinagre Composto Branco 750ml	Vinagre Composto Branco 750ml	750	\N	ml	12	\N	789609050021-5	2789609050021-9	\N	\N	1095	\N	\N	\N	1	\N	\N
19	1	1	2	7	14.01.04.17	Vinagre Composto Tinto 5 Lts	Vinagre Composto Tinto 5 Lts	5	\N	L	1	\N	789609050024-6	\N	\N	\N	1095	\N	\N	\N	1	\N	\N
4	1	1	2	3	11.01.04.08	Vinagre Composto Tinto 750ml	Vinagre Composto Tinto 750ml	750	\N	ml	12	\N	789609050001-7	2789609050001-1	\N	\N	1095	\N	\N	\N	1	\N	\N
17	1	1	2	7	14.01.03.20	Vinagre De Álcool 5 Lts	Vinagre De Álcool 5 Lts	5	\N	L	1	\N	789609050011-6	\N	\N	\N	1095	\N	\N	\N	1	\N	\N
2	1	1	2	1	10.01.03.10	Vinagre De Álcool 750ml	Vinagre De Álcool 750ml	750	\N	ml	12	\N	789609050005-5	2789609050005-9	\N	\N	1095	\N	\N	\N	1	\N	\N
18	1	1	2	7	14.01.03.19	Vinagre De Álcool Colorido 5 Lts	Vinagre De Álcool Colorido 5 Lts	5	\N	L	1	\N	789609050093-2	\N	\N	\N	1095	\N	\N	\N	1	\N	\N
3	1	1	2	1	10.01.03.11	Vinagre De Álcool Colorido 750ml	Vinagre De Álcool Colorido 750ml	750	\N	ml	12	\N	789609050090-1	2789609050090-8	\N	\N	1095	\N	\N	\N	1	\N	\N
10	1	1	2	4	12.01.04.03	Vinagre De Alho 750ml	Vinagre De Alho 750ml	750	\N	ml	12	\N	789609050091-8	2789609050091-5	\N	\N	1095	\N	\N	\N	1	\N	\N
9	1	1	2	4	12.01.04.02	Vinagre De Limão 750ml	Vinagre De Limão 750ml	750	\N	ml	12	\N	789609050092-5	2789609050092-2	\N	\N	1095	\N	\N	\N	1	\N	\N
12	1	1	2	5	13.01.02.16	Vinagre De Maçã 380ml	Vinagre De Maçã 380ml	380	\N	ml	12	\N	789609050155-7	1789609050155-4	\N	\N	1095	\N	\N	\N	1	\N	\N
21	1	1	2	7	14.01.01.21	Vinagre De Maçã 5 Lts	Vinagre De Maçã 5 Lts	5	\N	L	1	\N	\N	\N	\N	\N	1095	\N	\N	\N	1	\N	\N
6	1	1	2	4	12.01.01.40	Vinagre De Maçã 750ml	Vinagre De Maçã 750ml	750	\N	ml	12	\N	789609050007-9	2789609050007-3	\N	\N	1095	\N	\N	\N	1	\N	\N
14	1	1	2	5	13.01.02.14	Vinagre De Vinho Branco 380ml	Vinagre De Vinho Branco 380ml	380	\N	ml	12	\N	789609050034-5	1789609050034-2	\N	\N	1095	\N	\N	\N	1	\N	\N
23	1	1	2	7	14.01.02.34	Vinagre De Vinho Branco 5 Lts	Vinagre De Vinho Branco 5 Lts	5	\N	L	1	\N	\N	\N	\N	\N	1095	\N	\N	\N	1	\N	\N
8	1	1	2	4	12.01.02.05	Vinagre De Vinho Branco 750ml	Vinagre De Vinho Branco 750ml	750	\N	ml	12	\N	789609050003-1	2789609050003-5	\N	\N	1095	\N	\N	\N	1	\N	\N
15	1	1	2	5	13.01.02.15	Vinagre De Vinho Branco Ervas 380ml	Vinagre De Vinho Branco Ervas 380ml	380	\N	ml	12	\N	789609050015-4	1789609050015-1	\N	\N	1095	\N	\N	\N	1	\N	\N
13	1	1	2	5	13.01.02.13	Vinagre De Vinho Tinto 380ml	Vinagre De Vinho Tinto 380ml	380	\N	ml	12	\N	789609050033-8	1789609050033-5	\N	\N	1095	\N	\N	\N	1	\N	\N
22	1	1	2	7	14.01.02.35	Vinagre De Vinho Tinto 5 Lts	Vinagre De Vinho Tinto 5 Lts	5	\N	L	1	\N	\N	\N	\N	\N	1095	\N	\N	\N	1	\N	\N
7	1	1	2	4	12.01.02.04	Vinagre De Vinho Tinto 750ml	Vinagre De Vinho Tinto 750ml	750	\N	ml	12	\N	789609050020-8	\N	\N	\N	\N	\N	\N	\N	1	\N	\N
36	2	3	7	11	5	Doce de Abacaxi com Morango Diet 250g	Doce de Abacaxi com Morango Diet 250g	250	\N	g	12	\N	7897953700339	\N	20079990	\N	365	ABACAXÍ	COM MORANGO	\N	1	\N	\N
37	2	3	7	11	6	Doce de Abacaxi com Coco Diet 250g	Doce de Abacaxi com Coco Diet 250g	250	\N	g	12	\N	7897953700223	\N	20079990	\N	365	ABACAXÍ	COM COCO	\N	1	\N	\N
38	2	3	7	11	7	Doce De Abacaxi com Pimenta Diet 250g	Doce De Abacaxi com Pimenta Diet 250g	250	\N	g	12	\N	7897953700315	\N	20079990	\N	365	ABACAXÍ	COM PIMENTA	\N	1	\N	\N
39	2	3	7	11	8	Doce de Bananada Diet 250g	Doce de Bananada Diet 250g	250	\N	g	12	\N	7897953700377	\N	20079990	\N	365	BANANA	CREMOSA	\N	1	\N	\N
40	2	3	7	11	9	Doce de Batata Doce com Abacaxi Diet 250g	Doce de Batata Doce com Abacaxi Diet 250	250	\N	g	12	\N	7897953700551	\N	20079990	\N	365	BATATA DOCE	COM ABACAXI	\N	1	\N	\N
41	2	3	7	11	10	Doce de Caju em Calda Diet 250g	Doce de Caju em Calda Diet 250g	250	\N	g	12	\N	7897953700520	\N	20079100	\N	365	CAJU	EM CALDA	\N	1	\N	\N
42	2	3	7	11	11	Doce de Carambola em Calda Diet 250g	Doce de Carambola em Calda Diet 250g	250	\N	g	12	\N	7897953700322	\N	20079100	\N	365	CARAMBOLA	EM CALDA	\N	1	\N	\N
43	2	3	7	11	12	Doce de Chocolate Cream Diet 250g	Doce de Chocolate Cream Diet 250g	250	\N	g	12	\N	7897953700599	\N	18063110	\N	365	CHOCOLATE	CHOCOCREAM	\N	1	\N	\N
44	2	3	7	11	13	Doce de Cidra Diet 250g	Doce de Cidra Diet 250g	250	\N	g	12	\N	7897953700476	\N	20079100	\N	365	CIDRA	CREMOSA	\N	1	\N	\N
45	2	3	7	11	14	Doce de Figo em Calda Diet 250g	Doce de Figo em Calda Diet 250g	250	\N	g	12	\N	7897953700445	\N	20079100	\N	365	FIGO	EM CALDA	\N	1	\N	\N
46	2	3	7	11	15	Doce de Figo Cremoso Diet 250g	Doce de Figo Cremoso Diet 250g	250	\N	g	12	\N	7897953700742	\N	20079100	\N	365	FIGO	CREMOSO	\N	1	\N	\N
47	2	3	8	11	16	Geleia de Frutas Vermelhas 250g	Geleia de Frutas Vermelhas 250g	250	\N	g	12	\N	7897953700704	\N	20079990	\N	365	GELÉIAS	CREMOSA	\N	1	\N	\N
48	2	3	9	11	17	Fondant de Leite Cremoso Diet 250g	Fondant de Leite Cremoso Diet 250g	250	\N	g	12	\N	7897953700414	\N	19019020	\N	365	FOUNDANT LEITE	CREMOSO	\N	1	\N	\N
49	2	3	9	11	18	Fondant de Leite com Amendoim Diet 250g	Fondant de Leite com Amendoim Diet 250g	250	\N	g	12	\N	7897953700797	\N	19019090	\N	365	FOUNDANT LEITE	COM AMENDOIM	\N	1	\N	\N
50	2	3	9	11	19	Fondant de Leite e Cacau Diet 250g	Fondant de Leite e Cacau Diet 250g	250	\N	g	12	\N	7897953700995	\N	19019090	\N	365	FOUNDANT LEITE	COM CACAU	\N	1	\N	\N
51	2	3	9	11	20	Fondant de Leite com Goiaba Diet 250g	Fondant de Leite com Goiaba Diet 250g	250	\N	g	12	\N	7897953700889	\N	19019090	\N	365	FOUNDANT LEITE	COM GOIABADA	\N	1	\N	\N
52	2	3	7	11	21	Doce de Goiabada Cremosa Diet 250g	Doce de Goiabada Cremosa Diet 250g	250	\N	g	12	\N	7897953700360	\N	20079990	\N	365	GOIABA	CREMOSA	\N	1	\N	\N
53	2	3	7	11	22	Doce de Goiabada Cascão Diet 250g	Doce de Goiabada Cascão Diet 250g	250	\N	g	12	\N	7897953700926	\N	20079990	\N	365	GOIABA	CASCÃO	\N	1	\N	\N
54	2	3	7	11	23	Doce de Goiaba em Calda Diet 250g	Doce de Goiaba em Calda Diet 250g	250	\N	g	12	\N	7897953700346	\N	20079990	\N	365	GOIABA	EM CALDA	\N	1	\N	\N
26	1	1	4	8	17.01.06.27	Palmito Pupunha Picado 300g	Palmito Pupunha Picado 300g	300	\N	g	15	\N	\N	\N	\N	\N	180	\N	\N	\N	1	\N	\N
25	1	1	4	8	17.01.06.26	Palmito Pupunha Rodelas 300g	Palmito Pupunha Rodelas 300g	300	\N	g	15	\N	\N	\N	\N	\N	180	\N	\N	\N	1	\N	\N
32	2	3	7	11	1	Doce de Abóbora em Calda Diet 250g	Doce de Abóbora em Calda Diet 250g	250	\N	g	12	\N	7897953700391	\N	20079990	\N	365	ABÓBORA	EM CALDA	\N	1	\N	\N
33	2	3	7	11	2	Doce de Abóbora com Coco Diet 250g	Doce de Abóbora com Coco Diet 250g	250	\N	g	12	\N	7897953700384	\N	20079990	\N	365	ABÓBORA	COM COCO	\N	1	\N	\N
34	2	3	7	11	3	Doce de Abacaxi em Calda Diet 250g	Doce de Abacaxi em Calda Diet 250g	250	\N	g	12	\N	7897953700421	\N	20079990	\N	365	ABACAXÍ	EM CALDA	\N	1	\N	\N
242	3	4	18	27	CX 3 Molhos	Caixa com Molhos (3 molhos)	Caixa com Molhos (3 molhos)	6	3	UNID	30	\N	—	—	—	—	330	Unidade	—	Kit composto pelos três molhos	1	\N	\N
243	3	4	18	27	CX 3 Fatiados	Caixa de Fatiados (Copa, Salame, Culatello) 100g	Caixa de Fatiados (Copa, Salame, Culatello) 100g	100	3	g	30	\N	—	—	—	—	90	Fatiado	Resfriado	—	1	\N	\N
244	3	4	18	27	CX Fat Especial	Caixa de Fatiados Especial (Mortadela, Copa, Salame, Culatello)	Caixa de Fatiados Especial (Mortadela, Copa, Salame, Culatello)	4	2	PCT	40	\N	—	—	—	—	90	Fatiado	Resfriado	—	1	\N	\N
245	3	4	18	27	CX Fat Premium	Caixa de Fatiados Premium (Mortadela, Copa, Salame, Culatello, Pastrami)	Caixa de Fatiados Premium (Mortadela, Copa, Salame, Culatello, Pastrami)	5	5	PCT	50	\N	—	—	—	—	90	Fatiado	Resfriado	—	1	\N	\N
246	3	4	15	14	37	Copa Curada e Defumada 100g	Copa Curada e Defumada 100g	100	3	g	30	\N	7898962782163	17898962782160	2101900	1708701	90	Fatiado	Resfriado	—	1	\N	\N
247	3	4	15	14	1567	Culatello 100g	Culatello 100g	100	3	g	30	\N	7898962782606	97898962782609	2101900	1708701	90	Fatiado	Resfriado	—	1	\N	\N
248	3	4	12	14	7	Linguiça Apimentada 300g - Resfriado	Linguiça Apimentada 300g - Resfriado	300	6	g	20	\N	7898994688167	17898994688164	16010000	1707700	50	Fina	Resfriado	—	1	\N	\N
249	3	4	10	14	11	Linguiça Calábria 400g - Resfriado	Linguiça Calábria 400g - Resfriado	400	6.4	g	16	\N	7898994688181	17898962782252	16010000	1707700	50	Grossa	Resfriado	—	1	\N	\N
250	3	4	12	15	4	Linguiça de Costela - Campeira 300g - Resfriado	Linguiça de Costela - Campeira 300g - Resfriado	300	6	g	20	\N	7898962782019	17898962782290	16010000	1707700	50	Fina	Resfriado	—	1	\N	\N
251	3	4	10	14	5	Linguiça Chimichurri 400g - Resfriado	Linguiça Chimichurri 400g - Resfriado	400	6.4	g	16	\N	7898994688136	17898962782757	16010000	1707700	50	Grossa	Resfriado	—	1	\N	\N
252	3	4	12	15	lingui_a_costela_c__pimenta_biquinho___r	Linguiça Costela c/ Pimenta Biquinho 300g - Resfriado	Linguiça Costela c/ Pimenta Biquinho 300g - Resfriado	300	6	g	20	\N	—	—	—	—	50	Fina	Resfriado	—	1	\N	\N
253	3	4	11	15	12	Linguiça Cuiabana 400g - Resfriado	Linguiça Cuiabana 400g - Resfriado	400	6.4	g	16	\N	7898962782040	17898962782054	16010000	1707700	50	Grossa	Resfriado	—	1	\N	\N
254	3	4	13	14	lingui_a_defumada_cebola_e_salsa___resfr	Linguiça Defumada Cebola e Salsa 420g - Resfriado	Linguiça Defumada Cebola e Salsa 420g - Resfriado	420	5.04	g	12	\N	7898962782583	17898962782580	16010000	1707700	60	Fina	Resfriado	Peso aprox. - valor por kg	1	\N	\N
255	3	4	13	14	41	Linguiça Defumada Provolone 420g - Resfriado	Linguiça Defumada Provolone 420g - Resfriado	420	5.04	g	12	\N	7898962782132	17898962782139	16010000	1707700	60	Fina	Resfriado	Peso aprox. - valor por kg	1	\N	\N
256	3	4	13	14	lingui_a_defumada_tex_mex___resfriado	Linguiça Defumada Tex Mex 420g - Resfriado	Linguiça Defumada Tex Mex 420g - Resfriado	420	5.04	g	12	\N	—	—	—	—	60	Fina	Resfriado	Peso aprox. - valor por kg	1	\N	\N
257	3	4	12	18	1504	Linguiça Frango Mineira 300g - Resfriado	Linguiça Frango Mineira 300g - Resfriado	300	6	g	20	\N	7898962782156	17898962782153	16010000	1707700	50	Fina	Resfriado	—	1	\N	\N
258	3	4	10	14	13	Linguiça Gorgonzola 400g - Resfriado	Linguiça Gorgonzola 400g - Resfriado	400	6.4	g	16	\N	7898962782033	17898962782276	16010000	1707700	50	Grossa	Resfriado	—	1	\N	\N
259	3	4	10	14	3	Linguiça Grelhada ao Alho 400g - Resfriado	Linguiça Grelhada ao Alho 400g - Resfriado	400	6.4	g	16	\N	7898994688150	17898994688157	16010000	1707700	50	Grossa	Resfriado	—	1	\N	\N
260	3	4	11	15	20	Linguiça Kibe 400g - Resfriado	Linguiça Kibe 400g - Resfriado	400	6.4	g	16	\N	7898962782125	17898962782122	16010000	1707700	50	Grossa	Resfriado	—	1	\N	\N
261	3	4	12	15	1565	Linguiça Libanesa 300g - Resfriado	Linguiça Libanesa 300g - Resfriado	300	6	g	20	\N	7898962782569	17898962782566	16010000	1707700	50	Fina	Resfriado	—	1	\N	\N
262	3	4	10	14	6	Linguiça Margherita 400g - Resfriado	Linguiça Margherita 400g - Resfriado	400	6.4	g	16	\N	7898994688143	17898962782214	16010000	1707700	50	Grossa	Resfriado	—	1	\N	\N
263	3	4	12	16	14	Linguiça de Cordeiro - Mediterrânea 300g - Resfriado	Linguiça de Cordeiro - Mediterrânea 300g - Resfriado	300	6	g	20	\N	7898994688174	17898994688171	16010000	1707700	50	Fina	Resfriado	—	1	\N	\N
264	3	4	12	14	9	Linguiça Pernil 300g - Resfriado	Linguiça Pernil 300g - Resfriado	300	6	g	20	\N	7898962782095	17898962782092	16010000	1707700	50	Fina	Resfriado	—	1	\N	\N
265	3	4	10	14	8	Linguiça Pimenta Biquinho 400g - Resfriado	Linguiça Pimenta Biquinho 400g - Resfriado	400	6.4	g	16	\N	7898994688129	17898994688126	16010000	1707700	50	Grossa	Resfriado	—	1	\N	\N
266	3	4	10	14	lingui_a_requeij_o__cerveja_e_bacon___re	Linguiça Requeijão, Cerveja e Bacon 400g - Resfriado	Linguiça Requeijão, Cerveja e Bacon 400g - Resfriado	400	6.4	g	16	\N	—	—	—	—	50	Grossa	Resfriado	—	1	\N	\N
267	3	4	10	14	1457	Linguiça Rúcula c/ Parmesão 400g - Resfriado	Linguiça Rúcula c/ Parmesão 400g - Resfriado	400	6.4	g	16	\N	7898962782347	17898962782344	16010000	1707700	50	Grossa	Resfriado	—	1	\N	\N
268	3	4	10	14	10	Linguiça Tex Mex 400g - Resfriado	Linguiça Tex Mex 400g - Resfriado	400	6.4	g	16	\N	7898962782026	17898962782023	16010000	1707700	50	Grossa	Resfriado	—	1	\N	\N
269	3	4	12	14	1580	Linguiça Toscana 400g - Resfriado	Linguiça Toscana 400g - Resfriado	400	6	g	16	\N	7898962782613	17898962782610	16010000	1707700	50	Fina	Resfriado	—	1	\N	\N
270	3	4	15	14	37 M	Copa Curada e Defumada 100g (Meia CX)	Copa Curada e Defumada 100g (Meia CX)	100	1.5	g	15	\N	7898962782163	—	—	—	90	Fatiado	Resfriado	—	1	\N	\N
271	3	4	15	14	1567 M	Culatello 100g (Meia CX)	Culatello 100g (Meia CX)	100	1.5	g	15	\N	7898962782606	—	—	—	90	Fatiado	Resfriado	—	1	\N	\N
272	3	4	12	14	7 M	Linguiça Apimentada 300g (Meia CX) - Resfriado	Linguiça Apimentada 300g (Meia CX) - Resfriado	300	3	g	10	\N	7898994688167	—	—	—	50	Fina	Resfriado	—	1	\N	\N
273	3	4	10	14	11 M	Linguiça Calábria 400g (Meia CX) - Resfriado	Linguiça Calábria 400g (Meia CX) - Resfriado	400	3.2	g	8	\N	7898994688181	—	—	—	50	Grossa	Resfriado	—	1	\N	\N
274	3	4	12	15	4 M	Linguiça Campeira 300g (Meia CX) - Resfriado	Linguiça Campeira 300g (Meia CX) - Resfriado	300	3	g	10	\N	7898962782019	—	—	—	50	Fina	Resfriado	—	1	\N	\N
275	3	4	10	14	5 M	Linguiça Chimichurri 400g (Meia CX) - Resfriado	Linguiça Chimichurri 400g (Meia CX) - Resfriado	400	3.2	g	8	\N	7898994688136	—	—	—	50	Grossa	Resfriado	—	1	\N	\N
276	3	4	12	15	lingui_a_costela_c__pimenta_biquinho__me	Linguiça Costela c/ Pimenta Biquinho 300g (Meia CX) - Congelado	Linguiça Costela c/ Pimenta Biquinho 300g (Meia CX) - Congelado	300	3	g	10	\N	—	—	—	—	120	Fina	Congelado	—	1	\N	\N
277	3	4	11	15	12 M	Linguiça Cuiabana 400g (Meia CX) - Resfriado	Linguiça Cuiabana 400g (Meia CX) - Resfriado	400	3.2	g	8	\N	7898962782040	—	—	—	50	Grossa	Resfriado	—	1	\N	\N
278	3	4	13	14	lingui_a_defumada_cebola_e_salsa__meia_c	Linguiça Defumada Cebola e Salsa 420g (Meia CX) - Resfriado	Linguiça Defumada Cebola e Salsa 420g (Meia CX) - Resfriado	420	2.52	g	6	\N	7898962782583	—	—	—	60	Fina	Resfriado	Peso aprox. - valor por kg	1	\N	\N
279	3	4	13	14	41 M	Linguiça Defumada Provolone 420g (Meia CX) - Resfriado	Linguiça Defumada Provolone 420g (Meia CX) - Resfriado	420	2.52	g	6	\N	7898962782132	—	—	—	60	Fina	Resfriado	Peso aprox. - valor por kg	1	\N	\N
280	3	4	13	14	lingui_a_defumada_tex_mex__meia_cx____re	Linguiça Defumada Tex Mex 420g (Meia CX) - Resfriado	Linguiça Defumada Tex Mex 420g (Meia CX) - Resfriado	420	2.52	g	6	\N	—	—	—	—	60	Fina	Resfriado	Peso aprox. - valor por kg	1	\N	\N
281	3	4	12	18	1504 M	Linguiça Frango Mineira 300g (Meia CX) - Resfriado	Linguiça Frango Mineira 300g (Meia CX) - Resfriado	300	3	g	10	\N	7898962782156	—	—	—	50	Fina	Resfriado	—	1	\N	\N
282	3	4	10	14	13 M	Linguiça Gorgonzola 400g (Meia CX) - Resfriado	Linguiça Gorgonzola 400g (Meia CX) - Resfriado	400	3.2	g	8	\N	7898962782033	—	—	—	50	Grossa	Resfriado	—	1	\N	\N
283	3	4	10	14	3 M	Linguiça Grelhada ao Alho 400g (Meia CX) - Resfriado	Linguiça Grelhada ao Alho 400g (Meia CX) - Resfriado	400	3.2	g	8	\N	7898994688150	—	—	—	50	Grossa	Resfriado	—	1	\N	\N
284	3	4	11	15	20 M	Linguiça Kibe 400g (Meia CX) - Resfriado	Linguiça Kibe 400g (Meia CX) - Resfriado	400	3.2	g	8	\N	7898962782125	—	—	—	50	Grossa	Resfriado	—	1	\N	\N
285	3	4	12	15	1565 M	Linguiça Libanesa 300g (Meia CX) - Resfriado	Linguiça Libanesa 300g (Meia CX) - Resfriado	300	3	g	10	\N	7898962782569	—	—	—	50	Fina	Resfriado	—	1	\N	\N
286	3	4	10	14	6 M	Linguiça Margherita 400g (Meia CX) - Resfriado	Linguiça Margherita 400g (Meia CX) - Resfriado	400	3.2	g	8	\N	7898994688143	—	—	—	50	Grossa	Resfriado	—	1	\N	\N
287	3	4	12	16	14 M	Linguiça Mediterrânea 300g (Meia CX) - Resfriado	Linguiça Mediterrânea 300g (Meia CX) - Resfriado	300	3	g	10	\N	7898994688174	—	—	—	50	Fina	Resfriado	—	1	\N	\N
288	3	4	12	14	9 M	Linguiça Pernil 300g (Meia CX) - Resfriado	Linguiça Pernil 300g (Meia CX) - Resfriado	300	3	g	10	\N	7898962782095	—	—	—	50	Fina	Resfriado	—	1	\N	\N
289	3	4	10	14	8 M	Linguiça Pimenta Biquinho 400g (Meia CX) - Resfriado	Linguiça Pimenta Biquinho 400g (Meia CX) - Resfriado	400	3.2	g	8	\N	7898994688129	—	—	—	50	Grossa	Resfriado	—	1	\N	\N
290	3	4	10	14	lingui_a_requeij_o__cerveja_e_bacon__mei	Linguiça Requeijão, Cerveja e Bacon 400g (Meia CX) - Resfriado	Linguiça Requeijão, Cerveja e Bacon 400g (Meia CX) - Resfriado	400	3.2	g	8	\N	—	—	—	—	50	Grossa	Resfriado	—	1	\N	\N
291	3	4	10	14	1457 M	Linguiça Rúcula c/ Parmesão 400g (Meia CX) - Resfriado	Linguiça Rúcula c/ Parmesão 400g (Meia CX) - Resfriado	400	3.2	g	8	\N	7898962782347	—	—	—	50	Grossa	Resfriado	—	1	\N	\N
292	3	4	10	14	10 M	Linguiça Tex Mex 400g (Meia CX) - Resfriado	Linguiça Tex Mex 400g (Meia CX) - Resfriado	400	3.2	g	8	\N	7898962782026	—	—	—	50	Grossa	Resfriado	—	1	\N	\N
293	3	4	12	14	1580 M	Linguiça Toscana 400g (Meia CX) - Resfriado	Linguiça Toscana 400g (Meia CX) - Resfriado	400	3	g	8	\N	7898962782613	—	—	—	50	Fina	Resfriado	—	1	\N	\N
294	3	4	16	27	1628	Molho American Burguer c/ Relish Pepino 200g	Molho American Burguer c/ Relish Pepino 200g	200	6	g	10	\N	7898962782675	17898962782672	21039011	1703500	330	Unidade	—	—	1	\N	\N
295	3	4	16	27	1628 M	Molho American Burguer c/ Relish Pepino 200g (Meia CX)	Molho American Burguer c/ Relish Pepino 200g (Meia CX)	200	0	g	10	\N	7898962782675	—	—	—	330	Unidade	—	—	1	\N	\N
296	3	4	16	27	1629	Molho Ketchup c/ Curry 200g	Molho Ketchup c/ Curry 200g	200	6	g	30	\N	7898962782682	17898962782689	21032010	1703400	330	Unidade	—	—	1	\N	\N
297	3	4	16	27	1629 M	Molho Ketchup c/ Curry 200g (Meia CX)	Molho Ketchup c/ Curry 200g (Meia CX)	200	2	g	10	\N	7898962782682	—	—	—	330	Unidade	—	—	1	\N	\N
298	3	4	16	27	1627	Molho Mostarda c/ Aipo 200g	Molho Mostarda c/ Aipo 200g	200	6	g	30	\N	7898962782668	17898962782665	21033021	1703800	330	Unidade	—	—	1	\N	\N
299	3	4	16	27	1627 M	Molho Mostarda c/ Aipo 200g (Meia CX)	Molho Mostarda c/ Aipo 200g (Meia CX)	200	2	g	10	\N	7898962782668	—	—	—	330	Unidade	—	—	1	\N	\N
300	3	4	17	14	mortadela__fatiada_	Mortadela (fatiada) 100g	Mortadela (fatiada) 100g	100	2	g	30	\N	—	—	—	—	90	Fatiado	Resfriado	—	1	\N	\N
301	3	4	17	14	mortadela__fatiada___meia_cx_	Mortadela (fatiada) 100g (Meia CX)	Mortadela (fatiada) 100g (Meia CX)	100	0.6666667	g	10	\N	—	—	—	—	90	Fatiado	Resfriado	—	1	\N	\N
302	3	4	17	14	38	Mortadela 3,1kg (peça)	Mortadela 3,1kg (peça)	3.1	9.3	Kg	3	\N	7898962782170	17898962782177	2013000	1707700	90	Peça	Resfriado	Peso aprox. da peça em kg	1	\N	\N
303	3	4	17	15	pastrami__fatiado_	Pastrami 100g (fatiado)	Pastrami 100g (fatiado)	100	2	g	30	\N	—	—	—	—	90	Fatiado	Resfriado	—	1	\N	\N
304	3	4	17	15	pastrami__fatiado___meia_cx_	Pastrami 100g (fatiado) (Meia CX)	Pastrami 100g (fatiado) (Meia CX)	100	0.6666667	g	10	\N	—	—	—	—	90	Fatiado	Resfriado	—	1	\N	\N
305	3	4	17	15	1651	Pastrami 1,1kg (peça)	Pastrami 1,1kg (peça)	1.1	4	Kg	4	\N	7898962782767	17898962782764	2102000	—	90	Peça	Resfriado	Peso aprox. da peça em kg	1	\N	\N
306	3	4	17	15	1651 M	Pastrami 1,1kg (peça) (CX c/10)	Pastrami 1,1kg (peça) (CX c/10)	1.1	10	Kg	10	\N	—	—	—	—	90	Peça	Resfriado	Peso aprox. da peça em kg	1	\N	\N
307	3	4	15	14	36	Salame Colonial 100g	Salame Colonial 100g	100	3	g	30	\N	7898994688198	27898994688192	16010000	1707600	90	Fatiado	Resfriado	—	1	\N	\N
308	3	4	14	15	43	Salsicha All Beef 290g	Salsicha All Beef 290g	290	5.22	g	18	\N	7898962782194	97898962782197	16010000	1707700	90	Fina	Resfriado	Peso aprox. - valor por kg	1	\N	\N
309	3	4	14	14	17	Salsicha Frankfurter 290g	Salsicha Frankfurter 290g	290	5.22	g	18	\N	7898962782088	17898962782085	16010000	1707700	90	Fina	Resfriado	Peso aprox. - valor por kg	1	\N	\N
310	3	4	14	14	19	Salsicha Kasewurst 320g	Salsicha Kasewurst 320g	320	3.2	g	10	\N	7898962782118	17898962782115	16010000	1707700	90	Grossa	Resfriado	Peso aprox. - valor por kg	1	\N	\N
311	3	4	14	22	16	Salsicha Viena 250g	Salsicha Viena 250g	250	4.5	g	18	\N	7898994688105	17898994688102	16010000	1707700	90	Fina	Resfriado	Peso aprox. - valor por kg	1	\N	\N
312	3	4	14	14	18	Salsicha c/ Alho 220g	Salsicha c/ Alho 220g	220	3.96	g	18	\N	7898962782101	17898962782108	16010000	1707700	90	Grossa	Resfriado	Peso aprox. - valor por kg	1	\N	\N
313	3	4	14	14	15	Salsicha c/ Bacon 320g	Salsicha c/ Bacon 320g	320	5.76	g	18	\N	7898962782002	17898962782009	16010000	1707700	90	Fina	Resfriado	Peso aprox. - valor por kg	1	\N	\N
314	3	4	15	14	36 M	Salame Colonial 100g (Meia CX)	Salame Colonial 100g (Meia CX)	100	1.5	g	15	\N	7898994688198	—	—	—	90	Fatiado	Resfriado	—	1	\N	\N
315	3	4	14	15	43 M	Salsicha All Beef 290g (Meia CX)	Salsicha All Beef 290g (Meia CX)	290	2.61	g	9	\N	7898962782194	—	—	—	90	Fina	Resfriado	Peso aprox. - valor por kg	1	\N	\N
316	3	4	14	14	17 M	Salsicha Frankfurter 290g (Meia CX)	Salsicha Frankfurter 290g (Meia CX)	290	2.61	g	9	\N	7898962782088	—	—	—	90	Fina	Resfriado	Peso aprox. - valor por kg	1	\N	\N
317	3	4	14	14	19 M	Salsicha Kasewurst 320g (Meia CX)	Salsicha Kasewurst 320g (Meia CX)	320	1.92	g	6	\N	7898962782118	—	—	—	90	Grossa	Resfriado	Peso aprox. - valor por kg	1	\N	\N
318	3	4	14	22	16 M	Salsicha Viena 250g (Meia CX)	Salsicha Viena 250g (Meia CX)	250	2.25	g	9	\N	7898994688105	—	—	—	90	Fina	Resfriado	Peso aprox. - valor por kg	1	\N	\N
319	3	4	14	14	18 M	Salsicha c/ Alho 220g (Meia CX)	Salsicha c/ Alho 220g (Meia CX)	220	1.98	g	9	\N	7898962782101	—	—	—	90	Grossa	Resfriado	Peso aprox. - valor por kg	1	\N	\N
320	3	4	14	14	15 M	Salsicha c/ Bacon 320g (Meia CX)	Salsicha c/ Bacon 320g (Meia CX)	320	2.88	g	9	\N	7898962782002	—	—	—	90	Fina	Resfriado	Peso aprox. - valor por kg	1	\N	\N
321	3	4	12	14	26	Linguiça Apimentada 300g - Congelado	Linguiça Apimentada 300g - Congelado	300	6	g	20	\N	7898962782309	17898962782306	16010000	1707700	120	Fina	Congelado	—	1	\N	\N
322	3	4	10	14	30	Linguiça Calábria 400g - Congelado	Linguiça Calábria 400g - Congelado	400	6.4	g	16	\N	7898962782255	27898962782259	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
323	3	4	12	15	23	Linguiça de Costela - Campeira 300g - Congelado	Linguiça de Costela - Campeira 300g - Congelado	300	6	g	20	\N	7898962782293	27898962782297	16010000	1707700	120	Fina	Congelado	—	1	\N	\N
324	3	4	10	14	24	Linguiça Chimichurri 400g - Congelado	Linguiça Chimichurri 400g - Congelado	400	6.4	g	16	\N	7898962782231	27898962782235	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
325	3	4	12	15	lingui_a_costela_c__pimenta_biquinho___c	Linguiça Costela c/ Pimenta Biquinho 300g - Congelado	Linguiça Costela c/ Pimenta Biquinho 300g - Congelado	300	6	g	20	\N	—	—	—	—	120	Fina	Congelado	—	1	\N	\N
326	3	4	11	15	31	Linguiça Cuiabana 400g - Congelado	Linguiça Cuiabana 400g - Congelado	400	6.4	g	16	\N	7898962782262	17898962782269	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
327	3	4	12	18	1503	Linguiça Frango Mineira 300g - Congelado	Linguiça Frango Mineira 300g - Congelado	300	6	g	20	\N	7898962782354	17898962782351	16010000	1707700	120	Fina	Congelado	—	1	\N	\N
328	3	4	10	14	32	Linguiça Gorgonzola 400g - Congelado	Linguiça Gorgonzola 400g - Congelado	400	6.4	g	16	\N	7898962782279	27898962782273	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
329	3	4	10	14	22	Linguiça Grelhada ao Alho 400g - Congelado	Linguiça Grelhada ao Alho 400g - Congelado	400	6.4	g	16	\N	7898962782200	27898962782204	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
330	3	4	11	15	34	Linguiça Kibe 400g - Congelado	Linguiça Kibe 400g - Congelado	400	6.4	g	16	\N	7898962782286	17898962782283	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
331	3	4	12	15	1566	Linguiça Libanesa 300g - Congelado	Linguiça Libanesa 300g - Congelado	300	6	g	20	\N	7898962782576	17898962782573	16010000	1707700	120	Fina	Congelado	—	1	\N	\N
332	3	4	10	14	25	Linguiça Margherita 400g - Congelado	Linguiça Margherita 400g - Congelado	400	6.4	g	16	\N	7898962782217	17898994688140	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
333	3	4	12	16	33	Linguiça de Cordeiro - Mediterrânea 300g - Congelado	Linguiça de Cordeiro - Mediterrânea 300g - Congelado	300	6	g	20	\N	7898962782323	17898962782320	16010000	1707700	120	Fina	Congelado	—	1	\N	\N
334	3	4	12	14	28	Linguiça Pernil 300g - Congelado	Linguiça Pernil 300g - Congelado	300	6	g	20	\N	7898962782316	17898962782313	16010000	1707700	120	Fina	Congelado	—	1	\N	\N
335	3	4	10	14	27	Linguiça Pimenta Biquinho 400g - Congelado	Linguiça Pimenta Biquinho 400g - Congelado	400	6.4	g	16	\N	7898962782224	17898962782221	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
336	3	4	10	14	1177	Linguiça Requeijão, Cerveja e Bacon 400g - Congelado	Linguiça Requeijão, Cerveja e Bacon 400g - Congelado	400	6.4	g	16	\N	7898962782071	27898962782075	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
337	3	4	10	14	1458	Linguiça Rúcula c/ Parmesão 400g - Congelado	Linguiça Rúcula c/ Parmesão 400g - Congelado	400	6.4	g	16	\N	7898962782361	17898962782368	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
338	3	4	10	14	29	Linguiça Tex Mex 400g - Congelado	Linguiça Tex Mex 400g - Congelado	400	6.4	g	16	\N	7898962782248	17898962782245	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
339	3	4	12	14	1579	Linguiça Toscana 400g - Congelado	Linguiça Toscana 400g - Congelado	400	6	g	16	\N	7898962782620	17898962782627	16010000	1707700	120	Fina	Congelado	—	1	\N	\N
340	3	4	12	14	26 M	Linguiça Apimentada 300g (Meia CX) - Congelado	Linguiça Apimentada 300g (Meia CX) - Congelado	300	3	g	10	\N	7898962782309	—	16010000	1707700	120	Fina	Congelado	—	1	\N	\N
341	3	4	10	14	30 M	Linguiça Calábria 400 g (Meia CX) - Congelado	Linguiça Calábria 400 g (Meia CX) - Congelado	400	3.2	g	8	\N	7898962782255	—	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
342	3	4	12	15	23 M	Linguiça Campeira 300g (Meia CX) - Congelado	Linguiça Campeira 300g (Meia CX) - Congelado	300	3	g	10	\N	7898962782293	—	16010000	1707700	120	Fina	Congelado	—	1	\N	\N
343	3	4	10	14	24 M	Linguiça Chimichurri 400g (Meia CX) - Congelado	Linguiça Chimichurri 400g (Meia CX) - Congelado	400	3.2	g	8	\N	7898962782231	—	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
344	3	4	11	15	31 M	Linguiça Cuiabana 400g (Meia CX) - Congelado	Linguiça Cuiabana 400g (Meia CX) - Congelado	400	3.2	g	8	\N	7898962782262	—	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
345	3	4	12	18	1503 M	Linguiça Frango Mineira 300g (Meia CX) - Congelado	Linguiça Frango Mineira 300g (Meia CX) - Congelado	300	3	g	10	\N	7898962782354	—	16010000	1707700	120	Fina	Congelado	—	1	\N	\N
346	3	4	10	14	32 M	Linguiça Gorgonzola 400g (Meia CX) - Congelado	Linguiça Gorgonzola 400g (Meia CX) - Congelado	400	3.2	g	8	\N	7898962782279	—	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
347	3	4	10	14	22 M	Linguiça Grelhada ao Alho 400g (Meia CX) - Congelado	Linguiça Grelhada ao Alho 400g (Meia CX) - Congelado	400	3.2	g	8	\N	7898962782200	—	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
348	3	4	11	15	34 M	Linguiça Kibe 400g (Meia CX) - Congelado	Linguiça Kibe 400g (Meia CX) - Congelado	400	3.2	g	8	\N	7898962782286	—	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
349	3	4	12	15	1566 M	Linguiça Libanesa 300g (Meia CX) - Congelado	Linguiça Libanesa 300g (Meia CX) - Congelado	300	3	g	10	\N	7898962782576	—	16010000	1707700	120	Fina	Congelado	—	1	\N	\N
350	3	4	10	14	25 M	Linguiça Margherita 400g (Meia CX) - Congelado	Linguiça Margherita 400g (Meia CX) - Congelado	400	3.2	g	8	\N	7898962782217	—	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
351	3	4	12	16	33 M	Linguiça Mediterrânea 300g (Meia CX) - Congelado	Linguiça Mediterrânea 300g (Meia CX) - Congelado	300	3	g	10	\N	7898962782323	—	16010000	1707700	120	Fina	Congelado	—	1	\N	\N
352	3	4	12	14	28 M	Linguiça Pernil 300g (Meia CX) - Congelado	Linguiça Pernil 300g (Meia CX) - Congelado	300	3	g	10	\N	7898962782316	—	16010000	1707700	120	Fina	Congelado	—	1	\N	\N
353	3	4	10	14	27 M	Linguiça Pimenta Biquinho 400g (Meia CX) - Congelado	Linguiça Pimenta Biquinho 400g (Meia CX) - Congelado	400	3.2	g	8	\N	7898962782224	—	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
354	3	4	10	14	1177 M	Linguiça Requeijão, Cerveja e Bacon 400g (Meia CX) - Congelado	Linguiça Requeijão, Cerveja e Bacon 400g (Meia CX) - Congelado	400	3.2	g	8	\N	7898962782071	—	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
355	3	4	10	14	1458 M	Linguiça Rúcula c/ Parmesão 400g (Meia CX) - Congelado	Linguiça Rúcula c/ Parmesão 400g (Meia CX) - Congelado	400	3.2	g	8	\N	7898962782361	—	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
356	3	4	10	14	29 M	Linguiça Tex Mex 400g (Meia CX) - Congelado	Linguiça Tex Mex 400g (Meia CX) - Congelado	400	3.2	g	8	\N	7898962782248	—	16010000	1707700	120	Grossa	Congelado	—	1	\N	\N
357	3	4	12	14	1579 M	Linguiça 400g (Meia CX) - Congelado	Linguiça 400g (Meia CX) - Congelado	400	3	g	8	\N	7898962782620	—	16010000	1707700	120	Fina	Congelado	—	1	\N	\N
358	3	4	19	14	massa_lingui_a_cal_bria_500g___resfriado	Massa Linguiça Calábria 500g - Resfriado	Massa Linguiça Calábria 500g - Resfriado	500	0	g	1	\N	—	—	—	—	50	Massa	Resfriado	—	1	\N	\N
359	3	4	19	14	massa_lingui_a_toscana_500g___resfriado	Massa Linguiça Toscana 500g - Resfriado	Massa Linguiça Toscana 500g - Resfriado	500	0	g	1	\N	—	—	—	—	50	Massa	Resfriado	—	1	\N	\N
360	3	4	19	14	massa_lingui_a_toscana_5kg___resfriado	Massa Linguiça Toscana 5Kg - Resfriado	Massa Linguiça Toscana 5Kg - Resfriado	5	5	Kg	1	\N	—	—	—	—	50	Massa	Resfriado	—	1	\N	\N
361	3	4	12	14	1634	Linguiça Toscana 3,200kg Food - Resfriado	Linguiça Toscana 3,200kg Food - Resfriado	3.2	6.4	Kg	2	\N	7898962782637	17898962782634	16010000	1707700	0	Fina	Resfriado	—	1	\N	\N
362	3	4	12	14	1606	Linguiça Toscana 3,200kg Food - Congelado	Linguiça Toscana 3,200kg Food - Congelado	3.2	6.4	Kg	2	\N	7898962782644	17898962782641	16010000	1707700	0	Fina	Congelado	—	1	\N	\N
363	3	4	12	15	ling_costela_pimenta_biquinho_M_CONG	Linguiça Costela c/ Pimenta Biquinho 300g (Meia CX) - Resfriado	Linguiça Costela c/ Pimenta Biquinho 300g (Meia CX) - Resfriado	300	3	g	10	\N	—	—	—	—	50	Fina	Resfriado	—	1	\N	\N
55	2	3	7	11	24	Doce de Jaca em Calda Diet 250g	Doce de Jaca em Calda Diet 250g	250	\N	g	12	\N	7897953700452	\N	20079100	\N	365	JACA	EM CALDA	\N	1	\N	\N
56	2	3	7	11	25	Doce de Laranja com Pimenta Diet 250g	Doce de Laranja com Pimenta Diet 250g	250	\N	g	12	\N	7897953700117	\N	20079100	\N	365	LARANJA	COM PIMENTA	\N	1	\N	\N
57	2	3	7	11	26	Doce de Laranja em Calda Diet 250g	Doce de Laranja em Calda Diet 250g	250	\N	g	12	\N	7897953700407	\N	20079100	\N	365	LARANJA	EM CALDA	\N	1	\N	\N
58	2	3	7	11	27	Doce de Laranja Cremosa Diet 250g	Doce de Laranja Cremosa Diet 250g	250	\N	g	12	\N	7897953700780	\N	20079100	\N	365	LARANJA	CREMOSA	\N	1	\N	\N
59	2	3	7	11	28	Doce de Laranja com Morango Diet 250g	Doce de Laranja com Morango Diet 250g	250	\N	g	12	\N	7897953700773	\N	20079100	\N	365	LARANJA	COM MORANGO	\N	1	\N	\N
60	2	3	7	11	29	Doce de Laranja Kinkan Cremosa Diet 250g	Doce de Laranja Kinkan Cremosa Diet 250g	250	\N	g	12	\N	7897953700667	\N	20079100	\N	365	LARANJA	KINKAN CREMOSA	\N	1	\N	\N
61	2	3	7	11	30	Doce de Laranja Kinkan em Calda Diet 250g	Doce de Laranja Kinkan em Calda Diet 250	250	\N	g	12	\N	7897953700438	\N	20079100	\N	365	LARANJA	KINKAN EM CALDA	\N	1	\N	\N
62	2	3	7	11	31	Doce de Laranja Kinkan com Pimenta Diet 250g	Doce de Laranja Kinkan com Pimenta Diet	250	\N	g	12	\N	7897953700988	\N	20079100	\N	365	LARANJA	KINKAN COM PIMENTA	\N	1	\N	\N
63	2	3	7	11	32	Doce de Manga em Calda Diet 250g	Doce de Manga em Calda Diet 250g	250	\N	g	12	\N	7897953700513	\N	20079990	\N	365	MANGA	EM CALDA	\N	1	\N	\N
64	2	3	7	11	33	Doce de Manga com Abacaxi Diet 250g	Doce de Manga com Abacaxi Diet 250g	250	\N	g	12	\N	7897953700490	\N	20079990	\N	365	MANGA	COM ABACAXI	\N	1	\N	\N
65	2	3	7	11	34	Doce de Mamão Enrolado Diet 250g	Doce de Mamão Enrolado Diet 250g	250	\N	g	12	\N	7897953700483	\N	20079990	\N	365	MAMÃO	ENROLADO	\N	1	\N	\N
66	2	3	7	11	35	Doce de Mamão Ralado Diet 250g	Doce de Mamão Ralado Diet 250g	365	\N	g	12	\N	7897953700353	\N	20079990	\N	365	MAMÃO	RALADO	\N	1	\N	\N
67	2	3	7	11	36	Doce de Mamão com Coco Diet 250g	Doce de Mamão com Coco Diet 250g	250	\N	g	12	\N	7897953700940	\N	20079990	\N	365	MAMÃO	RALADO COM COCO	\N	1	\N	\N
68	2	3	7	11	37	Doce de Morango Cremoso Diet 250g	Doce de Morango Cremoso Diet 250g	250	\N	g	12	\N	7897953700803	\N	20079910	\N	365	MORANGO	CREMOSO	\N	1	\N	\N
69	2	3	7	11	38	Doce de Pêra em Calda Diet 250g	Doce de Pêra em Calda Diet 250g	250	\N	g	12	\N	7897953700469	\N	20079990	\N	365	PERA	EM CALDA	\N	1	\N	\N
70	2	3	7	11	39	Doce de Pêssego Cremoso Diet 250g	Doce de Pêssego Cremoso Diet 250g	365	\N	g	12	\N	7897953700810	\N	20079990	\N	365	PÊSSEGO	CREMOSO	\N	1	\N	\N
71	2	3	7	11	40	Doce de Pêssego em Calda Diet 250g	Doce de Pêssego em Calda Diet 250g	365	\N	g	12	\N	7897953700506	\N	20079990	\N	365	PÊSSEGO	EM CALDA	\N	1	\N	\N
72	2	3	7	11	41	Doce de Pêssego com Morango Diet 250g	Doce de Pêssego com Morango Diet 250g	250	\N	g	12	\N	7897953700759	\N	20079990	\N	365	PÊSSEGO	COM MORANGO	\N	1	\N	\N
73	2	3	7	11	42	Doce de Pêssego com Pimenta Diet 250g	Doce de Pêssego com Pimenta Diet 250g	250	\N	g	12	\N	7897953700919	\N	20079990	\N	365	PÊSSEGO	COM PIMENTA	\N	1	\N	\N
74	2	3	7	11	43	Doce de Tangerina Cremosa Diet 250g	Doce de Tangerina Cremosa Diet 250g	250	\N	g	12	\N	7897953700933	\N	20079100	\N	365	TANGERINA	CREMOSA	\N	1	\N	\N
75	2	3	8	11	44	Geleia de Pimenta Diet 250g	Geleia de Pimenta Diet 250g	365	\N	g	12	\N	7897953700308	\N	20079990	\N	365	GELÉIAS	PIMENTA	\N	1	\N	\N
76	2	3	8	11	45	Geleia de Pimenta em Pedaços Diet 250g	Geleia de Pimenta em Pedaços Diet 250g	250	\N	g	12	\N	7897953700858	\N	20079990	\N	365	GELÉIAS	PIMENTA PEDAÇOS	\N	1	\N	\N
77	2	3	8	11	46	Geleia de Pimenta com Abacaxi Diet 250g	Geleia de Pimenta com Abacaxi Diet 250g	250	\N	g	12	\N	7897953700902	\N	20079990	\N	365	GELÉIAS	PIMENTA COM ABACAXI	\N	1	\N	\N
78	2	3	8	11	47	Geleia de Manga com Maracujá e Pimenta Rosa Diet 250g	Geleia de Manga com Maracujá e Pimenta R	250	\N	g	12	\N	7897953700735	\N	20079990	\N	365	GELÉIAS	MANGA COM MARACUJÁ	\N	1	\N	\N
380	4	5	27	31	PASTAFIT	Fast Past Fitness Integral "DE" 400g	Macarrão Fast Pasta Fitness De 400g	400	\N	g	20	\N	789.61938.0050-2	1.789.61938.0050-9	\N	\N	365	\N	\N	\N	1	\N	\N
379	4	5	27	31	PASTA	Massa Fast Past "DE" 200g	Macarrão Fast Pasta De 200g	200	0	g	20	\N	789.61938.0032-8	1.789.61938.0032-5	\N	\N	365	\N	\N	\N	1	\N	\N
381	4	5	28	32	TRICO	Massa Tricolori Gravata Salada "DE" 200g	Tricolori Salada De 200g	200	0	g	20	\N	789.61938.0053-3	1.789.61938.0053-0	\N	\N	365	\N	\N	\N	1	\N	\N
\.


--
-- Data for Name: produto_codigo_cliente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.produto_codigo_cliente (produto_codigo_id, cliente_id, produto_id, codigo_cliente) FROM stdin;
\.


--
-- Data for Name: produto_concorrente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.produto_concorrente (produto_concorrente_id, concorrente_id, categoria_id, linha_id, descricao, descricao_curta, peso, unidade_medida, ean_concorrente, auditavel, validade_dias, observacao, ativo, unidades_caixa, ean, preco_referencia) FROM stdin;
1	1	2	\N	Vinagre de Maçã Castelo 750ml	Vinagre de Maçã Castelo 750ml	750	ml	\N	1	\N	\N	1	\N	7896048200105	14.99
2	2	2	\N	Vinagre de Álcool Vitalia 750ml	Vinagre de Álcool Vitalia 750ml	0.75	UN	\N	1	\N	\N	1	\N	\N	\N
4	5	2	\N	Vinagre de Álcool Colorido Palladio 750ml	Vinagre de Álcool Colorido Palladio 750m	750	ml	\N	1	\N	\N	1	\N	\N	\N
5	1	2	\N	Vinagre de Álcool Castelo 750ml	Vinagre de Álcool Castelo 750ml	750	ml	\N	1	\N	\N	1	\N	7896048200051	\N
6	7	2	\N	Vinagre de Álcool Fortaleza 750ml	Vinagre de Álcool Fortaleza 750ml	750	ml	\N	1	\N	\N	1	\N	\N	\N
7	5	2	\N	Vinagre de Álcool Palladio 750ml	Vinagre de Álcool Palladio 750ml	750	ml	\N	1	\N	\N	1	\N	\N	\N
8	15	2	\N	Vinagre de Álcool Toscano 750ml	Vinagre de Álcool Toscano 750ml	750	ml	\N	1	\N	\N	1	\N	\N	\N
10	1	2	\N	Vinagre de Álcool Colorido Castelo 750ml	Vinagre de Álcool Colorido Castelo 750ml	750	ml	\N	1	\N	\N	1	\N	7896048284778	\N
11	7	2	\N	Vinagre de Álcool Colorido Fortaleza 750ml	Vinagre de Álcool Colorido Fortaleza 750	750	ml	\N	1	\N	\N	1	\N	7896048284785	\N
12	9	2	\N	Vinagre de Álcool Colorido Palhinha 750ml	Vinagre de Álcool Colorido Palhinha 750	750	ml	\N	1	\N	\N	1	\N	\N	\N
13	3	2	\N	Vinagre de Álcool Colorido Vitalia 750ml	Vinagre de Álcool Colorido Vitalia 750ml	750	ml	\N	1	\N	\N	1	\N	7896048284792	\N
153	42	14	\N	Salsicha Hans Viena 200g	Salsicha Viena Hans 200g	200	g	7894904285921	1	\N	Artesanal, Viena	1	\N	\N	\N
15	1	2	\N	Vinagre de Vinho Branco Castelo 750ml	Vinagre de Vinho Branco Castelo 750ml	750	ml	\N	1	\N	\N	1	\N	\N	\N
16	15	2	\N	Vinagre de Vinho Branco Toscano 750ml	Vinagre de Vinho Branco Toscano 750ml	750	ml	\N	1	\N	\N	1	\N	\N	\N
17	1	2	\N	Vinagre de Vinho Tinto Castelo 750ml	Vinagre de Vinho Tinto Castelo 750ml	750	ml	\N	1	\N	\N	1	\N	7896048256010	\N
18	1	2	\N	Vinagre de Álcool c/Alho Castelo 750ml	Vinagre de Álcool c/Alho Castelo 750ml	750	ml	\N	1	\N	\N	1	\N	\N	\N
19	9	2	\N	Vinagre de Álcool c/Alho Palhinha 750ml	Vinagre de Álcool c/Alho Palhinha 750ml	750	ml	\N	1	\N	\N	1	\N	\N	\N
20	15	2	\N	Vinagre de Álcool c/Alho Toscano 750ml	Vinagre de Álcool c/Alho Toscano 750ml	750	ml	\N	1	\N	\N	1	\N	\N	\N
21	1	2	\N	Vinagre de Álcool c/Limão 750ml	Vinagre de Álcool c/Limão 750ml	750	ml	\N	1	\N	\N	1	\N	7896048255013	\N
22	9	2	\N	Vinagre de Álcool c/Limão 750ml	Vinagre de Álcool c/Limão 750ml	750	ml	\N	1	\N	\N	1	\N	\N	\N
23	15	2	\N	Vinagre de Álcool c/Limão 750ml	Vinagre de Álcool c/Limão 750ml	750	ml	\N	1	\N	\N	1	\N	7891144000604	\N
24	6	2	\N	Vinagre de Maçã c/Ervas Finas Almaromi 400ml	Vinagre de Maçã c/Ervas Finas 400ml	400	ml	\N	1	\N	\N	1	\N	7898908593716	\N
25	6	2	\N	Vinagre de Maçã Almaromi 400ml	Vinagre de Maçã Almaromi 400ml	400	ml	\N	1	\N	\N	1	\N	7898908593310	\N
26	6	2	\N	Vinagre de Vinho Tinto Almaromi 400ml	Vinagre de Vinho Tinto Almaromi 400ml	400	ml	\N	1	\N	\N	1	\N	7898908593631	\N
29	18	5	\N	Alho Triturado Dai 200g	Alho Triturado Dai 200g	200	g	\N	1	\N	\N	1	\N	\N	\N
30	18	5	\N	Alho Refoga Dai 200g	Alho Refoga Dai 200g	200	g	\N	1	\N	\N	1	\N	\N	\N
31	18	5	\N	Alho e Cebola Triturada Dai 200g	Alho e Cebola Triturada Dai 200g	200	g	\N	1	\N	\N	1	\N	\N	\N
32	10	2	\N	Vinagre de Maçã Puro Pomar 250ml	Vinagre de Maçã Puro Pomar 250ml	250	ml	\N	1	\N	\N	1	\N	\N	\N
33	13	2	\N	Vinagre de Maçã São Francisco 250ml Vidro	Vinagre de Maçã 250ml Vidro	250	ml	\N	1	\N	\N	1	\N	\N	\N
34	14	2	\N	Vinagre de Maçã Orgânico São Roque 250ml Vidro	Vinagre de Maçã Orgânico 250ml Vidro	250	ml	\N	1	\N	\N	1	\N	\N	\N
35	8	2	\N	Vinagre de Maçã Kodilar 500ml	Vinagre de Maçã Kodilar 500ml	500	ml	\N	1	\N	\N	1	\N	\N	\N
36	19	2	\N	Vinagre de Maçã 750ml (MP)	Vinagre de Maçã 750ml (MP)	750	ml	\N	1	\N	produzido por Toscano (Antônio Borin)	1	\N	\N	\N
37	11	2	\N	Vinagre de Maçã Rosani 500ml	Vinagre de Maçã Rosani 500ml	500	ml	\N	1	\N	\N	1	\N	\N	\N
38	11	2	\N	Vinagre de Álcool Rosani 500ml	Vinagre de Álcool Rosani 500ml	500	ml	\N	1	\N	\N	1	\N	\N	\N
39	1	2	\N	Vinagre de Maçã Castelo 500ml	Vinagre de Maçã Castelo 500ml	500	ml	\N	1	\N	\N	1	\N	7896048284563	\N
40	1	2	\N	Vinagre Álcool Castelo 2Lt	Vinagre Álcool Castelo 2Lt	2	L	\N	1	\N	\N	1	\N	\N	\N
41	1	2	\N	Vinagre Álcool Ervas Finas Castelo 750ml	Vinagre Álcool Ervas Finas Castelo 750ml	750	ml	\N	1	\N	\N	1	\N	\N	\N
42	1	2	\N	Vinagre de Álcool Hortelã Castelo 750ml	Vinagre de Álcool Hortelã Castelo 750ml	750	ml	\N	1	\N	\N	1	\N	7896048282484	\N
43	1	2	\N	Sumo de Limão Castelo 500ml	Sumo de Limão Castelo 500ml	500	ml	\N	1	\N	\N	1	\N	\N	\N
44	6	2	\N	Vinagre de Álcool Limão Almaroni 400ml	Vinagre de Álcool Limão Almaroni 400ml	400	ml	\N	1	\N	\N	1	\N	7898908593976	\N
45	6	2	\N	Vinagre de Álcool Limão Siciliano 400ml	Vinagre de Álcool Limão Siciliano 400ml	400	ml	\N	1	\N	\N	1	\N	7898908593983	\N
46	1	2	\N	Vinagre de Maçã 500ml 100% Natural 500ml Vidro	Vinagre de Maçã 500ml 100% Nat 500ml VD	500	ml	\N	1	\N	\N	1	\N	\N	\N
47	1	2	\N	Vinagre de Maçã Castelo 500ml Vidro	Vinagre de Maçã Castelo 500ml Vidro	500	ml	\N	1	\N	\N	1	\N	\N	\N
48	1	2	\N	Vinagre de Maçã Orgânico Castelo 250ml Vidro	Vinagre de Maçã Orgânico 250ml Vidro	250	ml	\N	1	\N	\N	1	\N	\N	\N
49	6	2	\N	Vinagre de Maçã Orgânico Almaromi 400ml	Vinagre de Maçã Orgânico 400ml	400	ml	\N	1	\N	\N	1	\N	7898908593617	\N
50	6	2	\N	Vinagre de Maçã Orgânico Almaromi 500ml Vidro	Vinagre de Maçã Orgânico 500ml Vidro	500	ml	\N	1	\N	\N	1	\N	7898908593624	\N
51	13	2	\N	Vinagre de Maçã Orgânico 500ml São Francisco Vidro	Vinagre de Maçã Orgânico 500ml Vidro	500	ml	\N	1	\N	\N	1	\N	7898912678072	\N
52	20	2	\N	Vinagre de Maçã Orgânico Viccino 250ml	Vinagre de Maçã Orgânico Viccino 250ml	250	ml	\N	1	\N	\N	1	\N	\N	\N
53	20	2	\N	Vinagre de Maçã Orgânico Viccino 500ml	Vinagre de Maçã Orgânico Viccino 500ml	500	ml	\N	1	\N	\N	1	\N	\N	\N
54	15	2	\N	Vinagre de Álcool Colorido Toscano 750ml	Vinagre de Álcool Colorido 750ml	750	ml	\N	1	\N	\N	1	\N	\N	\N
55	20	2	\N	Vinagre de Maçã Orgânico Viccino 500ml Vidro	Vinagre de Maçã Orgânico 500ml Vidro	500	ml	\N	1	\N	\N	1	\N	\N	\N
9	3	2	\N	Vinagre de Álcool Vitalia 750ml	Vinagre de Álcool Vitalia 750ml	750	ml	7896048284631	1	\N	\N	1	\N	\N	\N
27	17	16	\N	Molho de Alho Maratá 150ml	Molho de Alho Maratá 150ml	150	ml	\N	1	\N	\N	1	\N	\N	\N
56	11	2	\N	Vinagre de Álcool Limão Rosani 500ml	Vinagre de Álcool Limão Rosani 500ml	500	ml	\N	1	\N	\N	1	\N	\N	\N
58	22	8	\N	Geleia de Frutas Vermelhas Diet Bom Princípio 230g	Geleia de Frutas Vermelhas Diet 230g	230	g	\N	1	\N	\N	1	\N	\N	\N
59	23	8	\N	Geleia de Morango Zero Reserva de Minas 200g	Geleia de Morango Zero 200g	200	g	\N	1	\N	\N	1	\N	\N	\N
60	23	8	\N	Gelia de Amora Zero Reserva de Minas 200g	Gelia de Amora Zero 200g	200	g	\N	1	\N	\N	1	\N	\N	\N
61	24	8	\N	Geleia de Frutas Vermelhas Queensberry Diet 280g	Geleia de Frutas Vermelhas Diet 280g	280	g	\N	1	\N	\N	1	\N	\N	\N
62	24	8	\N	Geleia de Framboesa Queensberry Diet 280g	Geleia de Framboesa Diet 280g	280	g	\N	1	\N	\N	1	\N	\N	\N
63	24	8	\N	Geleia de Amora Queensberry Diet 280g	Geleia de Amora Diet 280g	280	g	\N	1	\N	\N	1	\N	\N	\N
64	24	8	\N	Geleia de Pimenta Verde Queensberry 320g	Geleia de Pimenta Verde 320g	320	g	\N	1	\N	\N	1	\N	\N	\N
65	25	8	\N	Geleia de Morango Zero Vitao 200g	Geleia de Morango Zero 200g	200	g	\N	1	\N	\N	1	\N	\N	\N
66	26	8	\N	Geleia de Pimenta Premium Amore 220g	Geleia de Pimenta Premium 220g	220	g	\N	1	\N	\N	1	\N	\N	\N
67	6	2	\N	Vinagre Balsâmico Almaromi 280ml	Vinagre Balsâmico Almaromi 280ml	280	ml	\N	1	\N	\N	1	\N	\N	\N
68	8	2	\N	Vinagre Balsâmico Kodilar 250ml	Vinagre Balsâmico Kodilar 250ml	250	ml	\N	1	\N	\N	1	\N	\N	\N
69	15	2	\N	Vinagre de Vinho Tinto Toscano 750ml	Vinagre de Vinho Tinto Toscano 750ml	750	ml	\N	1	\N	\N	1	\N	\N	\N
70	1	2	\N	Vinagre Álcool Citrus Castelo 2Lt	Vinagre Álcool Citrus Castelo 2Lt	2	L	\N	1	\N	\N	1	\N	\N	\N
71	1	2	\N	Vinagre Álcool Maçã Verde Castelo 2Lt	Vinagre Álcool Maçã Verde Castelo 2Lt	2	L	\N	1	\N	\N	1	\N	\N	\N
72	28	2	\N	Vinagre Balsâmico La Pastina 500ml Vidro	Vinagre Balsâmico La Pastina 500ml Vidro	500	ml	\N	1	\N	\N	1	\N	\N	\N
73	28	2	\N	Vinagre de Vinho Branco La Pastina 500ml Vidro	Vinagre de Vinho Branco La Pastina 500ml	500	ml	\N	1	\N	\N	1	\N	\N	\N
75	30	2	\N	Vinagre Balsâmico Ponti 250ml Vidro	Vinagre Balsâmico Ponti 250ml Vidro	250	ml	\N	1	\N	\N	1	\N	\N	\N
77	30	2	\N	Vinagre Balsâmico Ponti 500ml Vidro	Vinagre Balsâmico Ponti 500ml Vidro	500	ml	\N	1	\N	\N	1	\N	\N	\N
78	1	2	\N	Vinagre Balsâmico Tradizionale Castelo 500ml Vidro	Vinagre Balsâmico Castelo 500ml Vidro	500	ml	\N	1	\N	\N	1	\N	\N	\N
79	32	2	\N	Vinagre Balsâmico Glazé Colavita 250ml Vidro	Vinagre Balsâmico Glazé Colavita 250ml	250	ml	\N	1	\N	\N	1	\N	\N	\N
80	33	2	\N	Vinagre de Vinho Branco Beaufor 250ml Vidro	Vinagre de Vinho Branco Beaufor 250ml	250	ml	\N	1	\N	\N	1	\N	\N	\N
81	34	2	\N	Aceto Balsâmico Mastroiani 250ml Vidro	Aceto Balsâmico Mastroiani 250ml Vidro	250	ml	\N	1	\N	\N	1	\N	\N	\N
82	28	2	\N	Crema Balsâmico de Morango La Pastina 150ml	Crema Balsâmico Morango La Pastina 150ml	150	ml	\N	0	\N	\N	1	\N	\N	\N
257	39	14	\N	Salsicha Viena Com Corante Ceratti 200g	Salsicha Viena Com Corante Ceratti 200g	200	g	\N	1	\N	\N	1	\N	\N	\N
258	39	14	\N	Salsicha Viena Sem Corante Ceratti 200g	Salsicha Viena Sem Corante Ceratti 200g	200	g	\N	1	\N	\N	1	\N	\N	\N
259	80	14	\N	Salsicha Viena Prieto 200g	Salsicha Viena Prieto 200g	200	UN	\N	1	\N	\N	1	\N	\N	\N
57	21	16	\N	Molho de Pimenta Vermelha Cepêra 150ml	Molho de Pimenta Vermelha Cepêra 150ml	150	ml	\N	1	\N	\N	1	\N	\N	\N
83	35	10	\N	Linguiça Calabresa Swift 500g	Ling. Calabresa Swift 500g	500	g	\N	1	\N	Industrial	1	\N	\N	\N
3	4	2	\N	Vinagre de Maçã Neval 750ml	Vinagre de Maçã Neval 750ml	750	ml	\N	1	\N	\N	1	\N	\N	\N
143	40	17	\N	Mortadela defumada fatiada Sadia 180g	Mortadela Def. Sadia 180g	180	g	7891515598259	0	\N	Industrial de massa, não auditável	1	\N	\N	\N
144	40	17	\N	Mortadela defumada Soltíssimo Sadia 200g	Mortadela Soltíssimo Sadia 200g	200	g	7891515431587	0	\N	Industrial, não auditável	1	\N	\N	\N
145	40	15	\N	Copa Fatiada Specialle Sadia 100g	Copa Fatiada Sadia 100g	100	g	7893000290174	1	\N	Industrial, mesmo peso	1	\N	\N	\N
112	36	12	\N	Linguiça Toscana Seara 5kg	Ling. Toscana Seara 5kg	5000	g	\N	0	\N	Food service exclusivo	1	\N	\N	\N
28	17	16	\N	Molho de Pimenta Gota 150ml	Molho de Pimenta Gota 150ml	150	ml	\N	1	\N	\N	1	\N	\N	\N
244	74	16	\N	Molho de Pimenta Kenko 150ml	Molho de Pimenta Kenko 150ml	150	ml	\N	1	\N	\N	1	\N	\N	\N
245	19	16	\N	Molho de Pimenta Marca Própria 150ml	Molho de Pimenta Marca Própria 150ml	150	ml	\N	1	\N	\N	1	\N	\N	\N
214	59	23	\N	Lasanha com Ovos Dona Benta 500g	Lasanha Dona Benta Ovos 500g	500	g	7896005281673	1	\N	EAN disponível — lasanha caseira com ovos	1	\N	\N	\N
238	35	12	\N	Linguiça Fina Tipo Toscana Swift 500g	Linguiça Fina Tipo Toscana Swift 500g	500	g	\N	1	\N	\N	1	\N	\N	\N
239	35	12	\N	Linguiça Fina de Pernil Apimentada Swift 500g	Ling. Fina Pernil Apimentada Swift 500g	500	g	\N	1	\N	\N	1	\N	\N	\N
240	70	8	\N	Geleia De Frutas Vermelhas Sem Açúcar Linea 230g	Geleia De Frutas Vermelhas S/ Açúcar Linea 230g	230	g	\N	1	\N	\N	1	\N	\N	\N
241	71	7	\N	Goiabada Cremosa Zero Flormel 210g	Goiabada Cremosa Zero Flormel 210g	210	g	\N	1	\N	\N	1	\N	\N	\N
246	58	23	\N	Lasanha Direto Ao Forno Petybon 500g	Lasanha Direto Ao Forno Petybon 500g	500	g	\N	1	\N	\N	1	\N	\N	\N
247	58	23	\N	Lasanha Direto Ao Forno Petybon 500g	Lasanha Direto Ao Forno Petybon 500g	500	g	\N	1	\N	\N	1	\N	\N	\N
248	58	23	\N	Lasanha Direto Ao Forno Petybon 500g	Lasanha Direto Ao Forno Petybon 500g	500	g	\N	1	\N	\N	1	\N	\N	\N
249	64	23	\N	Lasanha Direto Ao Forno Adria 500g	Lasanha Direto Ao Forno Adria 500g	500	g	\N	1	\N	\N	1	\N	\N	\N
250	64	21	\N	Ninho Adria 500g	Ninho Adria 500g	500	g	\N	1	\N	\N	1	\N	\N	\N
251	57	20	\N	Macarrão Tagliarini Superiore Renata 500g	Macarrão Tagliarini Superiore Renata 500g	500	g	\N	1	\N	\N	1	\N	\N	\N
252	\N	21	\N	Ninho Galla n°2 500g	Ninho Galla n°2 500g	500	g	\N	1	\N	\N	1	\N	\N	\N
254	77	21	\N	Ninho Galla n°2 500g	Ninho Galla n°2 500g	500	g	\N	1	\N	\N	1	\N	\N	\N
255	78	20	\N	Talharim com ovos Orquídea 500g	Talharim com ovos Orquídea 500g	500	g	\N	1	\N	\N	1	\N	\N	\N
260	81	14	\N	Salsicha com Alho Kassel Kg	Salsicha com Alho Kassel Kg	1	kg	\N	1	\N	\N	1	\N	\N	\N
256	19	2	\N	Vinagre de Álcool MP 750ml	Vinagre de Álcool MP 750ml	750	ml	\N	1	\N	\N	1	\N	\N	\N
14	15	2	\N	Vinagre de Maçã Toscano 750ml	Vinagre de Maçã Toscano 750ml	750	ml	7891144000147	1	\N	\N	1	\N	7891144000147	\N
84	35	10	\N	Linguiça tipo Calabresa Defumada Swift 400g	Ling. Calabresa Def. Swift 400g	400	g	\N	1	\N	Industrial, mesmo peso	1	\N	\N	\N
85	35	10	\N	Linguiça tipo Calabresa Fina Swift 500g	Ling. Calabresa Fina Swift 500g	500	g	\N	1	\N	Industrial	1	\N	\N	\N
86	35	12	\N	Linguiça de Pernil Swift 700g	Ling. Pernil Swift 700g	700	g	\N	1	\N	Industrial, peso diferente	1	\N	\N	\N
87	35	12	\N	Linguiça de Pernil com Alho Swift 500g	Ling. Pernil Alho Swift 500g	500	g	\N	1	\N	Industrial	1	\N	\N	\N
88	35	10	\N	Linguiça de Pernil com Pimenta Biquinho Swift 500g	Ling. Pernil Pim. Biquinho Swift	500	g	\N	1	\N	Industrial	1	\N	\N	\N
89	35	13	\N	Linguiça de Pernil com Provolone Swift 500g	Ling. Pernil Provolone Swift 500g	500	g	\N	1	\N	Industrial	1	\N	\N	\N
90	35	10	\N	Linguiça de Pernil com Queijo Coalho Tomate Seco e Manjericão Swift 500g	Ling. Queijo Coalho Swift 500g	500	g	\N	1	\N	Industrial	1	\N	\N	\N
91	35	12	\N	Linguiça Toscana Swift 700g	Ling. Toscana Swift 700g	700	g	\N	1	\N	Industrial, peso diferente	1	\N	\N	\N
92	35	12	\N	Linguiça de Frango Fina Swift 400g	Ling. Frango Fina Swift 400g	400	g	\N	1	\N	Industrial	1	\N	\N	\N
93	35	12	\N	Linguiça de Frango Swift 700g	Ling. Frango Swift 700g	700	g	\N	1	\N	Industrial, peso diferente	1	\N	\N	\N
94	35	11	\N	Linguiça de Carne Bovina tipo Cuiabana Swift 900g	Ling. Cuiabana Bovina Swift 900g	900	g	\N	1	\N	Industrial, peso muito diferente	1	\N	\N	\N
95	35	11	\N	Linguiça de Carne Suína tipo Cuiabana Swift 900g	Ling. Cuiabana Suína Swift 900g	900	g	\N	1	\N	Industrial	1	\N	\N	\N
96	35	11	\N	Linguiça de Carne de Frango tipo Cuiabana Swift 900g	Ling. Cuiabana Frango Swift 900g	900	g	\N	1	\N	Industrial, frango vs bovina	1	\N	\N	\N
97	35	13	\N	Linguiça Defumada Fininha Swift 215g	Ling. Defumada Fininha Swift 215g	215	g	\N	1	\N	Industrial, peso muito diferente	1	\N	\N	\N
98	35	12	\N	Linguiça Fina de Pernil Apimentada Swift 500g	Ling. Pernil Apim. Swift 500g	500	g	\N	1	\N	Industrial	1	\N	\N	\N
99	35	12	\N	Linguiça de Lombo Fina Swift 500g	Ling. Lombo Fina Swift 500g	500	g	\N	1	\N	Industrial, corte diferente	1	\N	\N	\N
100	35	12	\N	Linguiça de Frango Seara 600g	Ling. Frango Seara 600g	600	g	\N	1	\N	Atenção: listada como Swift mas parece Seara	1	\N	\N	\N
101	36	12	\N	Linguiça de Pernil Seara 600g	Ling. Pernil Seara 600g	600	g	\N	1	\N	Industrial	1	\N	\N	\N
102	36	10	\N	Linguiça Suína Seara 600g	Ling. Suína Seara 600g	600	g	\N	1	\N	Industrial	1	\N	\N	\N
103	36	10	\N	Linguiça chimichurri Seara 600g	Ling. Chimichurri Seara 600g	600	g	\N	1	\N	Industrial	1	\N	\N	\N
104	36	12	\N	Linguiça Toscana Seara 600g	Ling. Toscana Seara 600g	600	g	\N	1	\N	Industrial	1	\N	\N	\N
105	36	12	\N	Linguiça Toscana Seara 700g	Ling. Toscana Seara 700g	700	g	\N	1	\N	Industrial	1	\N	\N	\N
106	36	10	\N	Linguiça com Bacon 600g Seara	Ling. com Bacon Seara 600g	600	g	\N	1	\N	Industrial	1	\N	\N	\N
107	36	12	\N	Linguiça Apimentada Seara 600g	Ling. Apimentada Seara 600g	600	g	\N	1	\N	Industrial	1	\N	\N	\N
108	36	12	\N	Linguiça de Frango Seara 700g	Ling. Frango Seara 700g	700	g	\N	1	\N	Industrial	1	\N	\N	\N
109	36	10	\N	Linguiça fina Tipo Calabresa Seara 400g	Ling. Calabresa Fina Seara 400g	400	g	\N	1	\N	Industrial, mesmo peso	1	\N	\N	\N
110	36	13	\N	Linguiça Fininha Defumada Seara 215g	Ling. Fininha Def. Seara 215g	215	g	\N	1	\N	Industrial	1	\N	\N	\N
111	36	10	\N	Linguiça Tipo Calabresa Seara 2,5Kg	Ling. Calabresa Seara 2,5Kg	2500	g	\N	1	\N	Food service, peso incomparável	1	\N	\N	\N
113	36	10	\N	Linguiça Suína Seara 5kg	Ling. Suína Seara 5kg	5000	g	\N	0	\N	Food service exclusivo	1	\N	\N	\N
114	36	12	\N	Linguiça de Pernil Seara 5kg	Ling. Pernil Seara 5kg	5000	g	\N	0	\N	Food service exclusivo	1	\N	\N	\N
115	36	12	\N	Linguiça de Frango Seara 5kg	Ling. Frango Seara 5kg	5000	g	\N	0	\N	Food service exclusivo	1	\N	\N	\N
116	36	13	\N	Linguiça Defumada Reta Seara 2,5Kg	Ling. Def. Reta Seara 2,5Kg	2500	g	\N	0	\N	Food service	1	\N	\N	\N
117	36	13	\N	Linguiça Fininha Defumada Seara 2,5Kg	Ling. Fininha Def. Seara 2,5Kg	2500	g	\N	0	\N	Food service	1	\N	\N	\N
118	37	10	\N	Linguiça Suína Rezende 700g	Ling. Suína Rezende 700g	700	g	\N	1	\N	Industrial	1	\N	\N	\N
119	37	10	\N	Linguiça Palitus Rezende 2,5Kg	Ling. Palitus Rezende 2,5Kg	2500	g	\N	0	\N	Food service	1	\N	\N	\N
242	72	16	\N	Molho de Pimenta KiSabor 150ml	Molho de Pimenta KiSabor 150ml	150	ml	\N	1	\N	\N	1	\N	\N	\N
243	73	16	\N	Molho de Pimenta Knorr 150ml	Molho de Pimenta Knorr 150ml	150	ml	\N	1	\N	\N	1	\N	\N	\N
120	37	13	\N	Linguiça Defumada Rezende 2,5Kg	Ling. Defumada Rezende 2,5Kg	2500	g	\N	0	\N	Food service	1	\N	\N	\N
121	37	10	\N	Linguiça Churrasco Rezende 5Kg	Ling. Churrasco Rezende 5Kg	5000	g	\N	0	\N	Food service	1	\N	\N	\N
122	37	13	\N	Linguiça Defumada Reta Rezende 2,5Kg	Ling. Def. Reta Rezende 2,5Kg	2500	g	\N	0	\N	Food service	1	\N	\N	\N
123	38	13	\N	Linguiça de Pernil com Queijo Coalho Seara Gourmet 500g	Ling. Queijo Coalho SG 500g	500	g	\N	1	\N	Gourmet industrial, sabor premium	1	\N	\N	\N
124	38	10	\N	Linguiça com Alho Poró Seara Gourmet 500g	Ling. Alho Poró SG 500g	500	g	\N	1	\N	Gourmet, sabor similar	1	\N	\N	\N
125	38	12	\N	Linguiça de Frango com Bacon Seara Gourmet 500g	Ling. Frango Bacon SG 500g	500	g	\N	1	\N	Gourmet, frango	1	\N	\N	\N
126	38	10	\N	Linguiça com Pimenta Biquinho Seara Gourmet 500g	Ling. Pim. Biquinho SG 500g	500	g	\N	1	\N	Gourmet, mesmo sabor	1	\N	\N	\N
127	38	12	\N	Linguiça Apimentada Seara Gourmet 450g	Ling. Apimentada SG 450g	450	g	\N	1	\N	Gourmet, peso próximo	1	\N	\N	\N
128	38	11	\N	Linguiça Tipo Cuiabana Seara Gourmet 500g	Ling. Cuiabana SG 500g	500	g	\N	1	\N	Gourmet, mesmo tipo	1	\N	\N	\N
129	38	17	\N	Mortadela Defumada Fatiada Seara Gourmet 180g	Mortadela Def. SG 180g	180	g	\N	0	\N	Industrial vs artesanal, não auditável	1	\N	\N	\N
130	39	10	\N	Linguiça Tipo Calabresa Ceratti 370g	Ling. Calabresa Ceratti 370g	370	g	\N	1	\N	Premium, peso próximo	1	\N	\N	\N
131	39	10	\N	Linguiça Toscana sabor Pimenta Jalapeño Ceratti 400g	Ling. Toscana Jalapeño Ceratti 400g	400	g	\N	1	\N	Premium, mesmo peso	1	\N	\N	\N
132	39	10	\N	Linguiça Toscana Sabor Limão Siciliano Ceratti 400g	Ling. Limão Siciliano Ceratti 400g	400	g	\N	1	\N	Premium, perfil italiano	1	\N	\N	\N
133	39	10	\N	Linguiça Toscana com Cachaça e Mel Ceratti 400g	Ling. Cachaça e Mel Ceratti 400g	400	g	\N	1	\N	Premium, mesmo peso	1	\N	\N	\N
134	39	12	\N	Linguiça com Costela Suína Ceratti 400g	Ling. Costela Suína Ceratti 400g	400	g	\N	1	\N	Premium	1	\N	\N	\N
135	39	10	\N	Linguiça com Pimenta Biquinho Ceratti 400g	Ling. Pim. Biquinho Ceratti 400g	400	g	\N	1	\N	Premium, mesmo peso e sabor	1	\N	\N	\N
136	39	10	\N	Linguiça com Limão Siciliano Ceratti 400g	Ling. Limão Siciliano Ceratti 400g	400	g	\N	1	\N	Premium, mesmo peso	1	\N	\N	\N
137	39	10	\N	Linguiça com Chimichurri Ceratti 400g	Ling. Chimichurri Ceratti 400g	400	g	\N	1	\N	Premium, mesmo peso e sabor	1	\N	\N	\N
138	39	10	\N	Linguiça com Alho Poró e Bacon Ceratti 400g	Ling. Alho Poró Bacon Ceratti 400g	400	g	\N	1	\N	Premium, sabor similar	1	\N	\N	\N
139	39	10	\N	Linguiça Calabresa Fresca Fininha Ceratti 400g	Ling. Calabresa Fina Ceratti 400g	400	g	\N	1	\N	Premium, mesmo peso	1	\N	\N	\N
140	39	10	\N	Linguiça Suína para Churrasco Ceratti 5Kg	Ling. Suína Churrasco Ceratti 5Kg	5000	g	\N	0	\N	Food service	1	\N	\N	\N
141	39	10	\N	Linguiça Tipo Calabresa Ceratti 2,5Kg	Ling. Calabresa Ceratti 2,5Kg	2500	g	\N	0	\N	Food service	1	\N	\N	\N
142	39	15	\N	Copa Fatiada Ceratti 100g	Copa Fatiada Ceratti 100g	100	g	\N	1	\N	Premium, mesmo peso, mesmo produto	1	\N	\N	\N
146	41	14	\N	Salsicha Frankfurter Berna 300g	Salsicha Frankfurter Berna 300g	300	g	\N	1	\N	Artesanal, peso praticamente igual	1	\N	\N	\N
147	41	14	\N	Salsicha All Beef Berna 360g	Salsicha All Beef Berna 360g	360	g	\N	1	\N	Artesanal, All Beef, peso próximo	1	\N	\N	\N
148	41	14	\N	Salsicha Viena Aperitivo Berna 300g	Salsicha Viena Aperitivo Berna	300	g	\N	1	\N	Artesanal, Viena	1	\N	\N	\N
149	41	10	\N	Linguiça Calabresa Berna 345g	Ling. Calabresa Berna 345g	345	g	\N	1	\N	Artesanal, peso próximo	1	\N	\N	\N
150	41	12	\N	Linguiça Cordeiro Berna 310g	Ling. Cordeiro Berna 310g	310	g	\N	1	\N	Artesanal, cordeiro, peso igual	1	\N	\N	\N
151	42	14	\N	Salsicha Frankfurt Hans 200g	Salsicha Frankfurt Hans 200g	200	g	\N	1	\N	Artesanal premium, peso diferente	1	\N	\N	\N
152	42	14	\N	Salsicha com Alho Hans 240g	Salsicha c/ Alho Hans 240g	240	g	\N	1	\N	Artesanal, peso praticamente igual	1	\N	\N	\N
154	43	14	\N	Salsicha Viena 100% suína F.A. 290g	Salsicha Viena F.A. 290g	290	g	\N	1	\N	Artesanal, peso próximo	1	\N	\N	\N
155	43	14	\N	Salsicha Frankfurter Estilo Alemã 100% Suína F.A. 290g	Salsicha Frankfurter F.A. 290g	290	g	\N	1	\N	Artesanal, peso igual	1	\N	\N	\N
156	43	14	\N	Salsicha AllBeef Defumada Estilo Americana 100% Bovina F.A. 310g	Salsicha AllBeef F.A. 310g	310	g	\N	1	\N	Artesanal, All Beef, peso igual	1	\N	\N	\N
157	43	10	\N	Linguiça Calabresa 100% Suína F.A. 290g	Ling. Calabresa F.A. 290g	290	g	\N	1	\N	Artesanal	1	\N	\N	\N
158	43	12	\N	Linguiça Toscana Tradicional 100% Suína F.A. 290g	Ling. Toscana F.A. 290g	290	g	\N	1	\N	Artesanal	1	\N	\N	\N
159	43	10	\N	Linguiça Calabresa Defumada 100% Suína F.A. 290g	Ling. Calabresa Def. F.A. 290g	290	g	\N	1	\N	Artesanal	1	\N	\N	\N
199	57	20	\N	Macarrão Renata Ovos Talharim 1 Massa Tipo Caseira 500g	Talharim Caseiro Renata n°1 500g	500	g	\N	1	\N	Principal concorrente direto. Mesmo corte e peso, presença ampla em SP e BS	1	\N	\N	\N
200	57	20	\N	Macarrão Renata Ovos Talharim 2 Massa Tipo Caseira 500g	Talharim Caseiro Renata n°2 500g	500	g	\N	1	\N	Concorrente direto — talharim n°2 é o corte mais vendido na categoria	1	\N	\N	\N
201	57	20	\N	Macarrão Renata Ovos Talharim 3 Massa Tipo Caseira 500g	Talharim Caseiro Renata n°3 500g	500	g	\N	1	\N	Concorrente direto	1	\N	\N	\N
202	57	21	\N	Macarrão Renata Ovos Ninho 2 500g	Ninho Caseiro Renata n°2 500g	500	g	\N	1	\N	Ninho caseiro, mesmo peso — concorrência direta	1	\N	\N	\N
203	57	22	\N	Macarrão Renata Ovos Gravata Massa Tipo Caseira 500g	Gravata Caseira Renata 500g	500	g	\N	1	\N	Gravata caseira, mesmo peso — concorrência direta	1	\N	\N	\N
204	57	23	\N	Macarrão Renata Ovos Lasanha 500g	Lasanha Renata Ovos 500g	500	g	\N	1	\N	Lasanha caseira com ovos, mesmo peso — concorrência direta	1	\N	\N	\N
205	57	23	\N	Lasanha Pré-cozida Renata Ovos 200g	Lasanha Pré-cozida Renata 200g	200	g	\N	1	\N	Indireto: pré-cozida industrial vs gourmet instantânea artesanal De	1	\N	\N	\N
206	58	20	\N	Macarrão Talharim Caseiro Petybon com Ovos n°2 500g	Talharim Caseiro Petybon n°2 500g	500	g	\N	1	\N	Industrial com posicionamento caseiro — concorrência direta em preço e gôndola	1	\N	\N	\N
207	58	22	\N	Macarrão Gravata Caseiro Petybon com Ovos 500g	Gravata Caseira Petybon 500g	500	g	\N	1	\N	Concorrência direta, mesmo peso	1	\N	\N	\N
208	58	23	\N	Massa para Lasanha Petybon com Ovos 500g	Lasanha Petybon Ovos 500g	500	g	\N	1	\N	Lasanha industrial, mesmo peso — concorrência direta	1	\N	\N	\N
209	58	23	\N	Massa para Lasanha Tradicional Petybon 200g	Lasanha Petybon Tradicional 200g	200	g	\N	1	\N	Indireto: direto ao forno 200g vs gourmet instantânea De 200g	1	\N	\N	\N
210	58	23	\N	Massa para Lasanha Petybon Grano Duro 260g	Lasanha Grano Duro Petybon 260g	260	g	\N	1	\N	Indireto: grano duro vs caseira com ovos — posicionamento e preço diferentes	1	\N	\N	\N
211	59	20	\N	Massa Talharim com Ovos Dona Benta Caseira 500g	Talharim Caseiro Dona Benta 500g	500	g	\N	1	\N	Linha Caseira lançada recentemente — mesmo posicionamento, mesmo peso	1	\N	\N	\N
212	59	22	\N	Massa Gravata com Ovos Dona Benta Caseira 500g	Gravata Caseira Dona Benta 500g	500	g	\N	1	\N	Linha Caseira, concorrência direta	1	\N	\N	\N
213	59	21	\N	Massa Ninho com Ovos Dona Benta 500g	Ninho Dona Benta Ovos 500g	500	g	\N	1	\N	Concorrência direta, mesmo peso	1	\N	\N	\N
215	59	23	\N	Lasanha com Ovos Direto ao Forno Dona Benta 200g	Lasanha DAF Dona Benta 200g	200	g	\N	1	\N	Indireto: direto ao forno 200g vs gourmet instantânea De 200g	1	\N	\N	\N
216	60	20	\N	Macarrão Talharim Caseiro Romanha 500g	Talharim Caseiro Romanha 500g	500	g	\N	1	\N	Artesanal sulista, mesmo posicionamento e peso — concorrência direta	1	\N	\N	\N
217	60	20	\N	Macarrão Talharim Fresco Romanha 500g	Talharim Fresco Romanha 500g	500	g	\N	1	\N	Massa fresca refrigerada — concorrência direta premium	1	\N	\N	\N
218	60	23	\N	Lasanha Caseira Romanha 500g	Lasanha Caseira Romanha 500g	500	g	\N	1	\N	Artesanal, mesmo peso — concorrência direta	1	\N	\N	\N
219	60	24	\N	Macarrão para Yakissoba Caseiro Romanha 500g	Yakissoba Caseiro Romanha 500g	500	g	\N	1	\N	Artesanal, concorrência direta	1	\N	\N	\N
220	60	20	\N	Macarrão Integral Romanha 500g	Macarrão Integral Romanha 500g	500	g	\N	1	\N	Integral artesanal, mesmo peso	1	\N	\N	\N
221	60	21	\N	Talharim Caseiro Ninho Romanha 1kg	Talharim Ninho Romanha 1kg	1000	g	\N	1	\N	Indireto: peso dobro (1kg vs 500g De)	1	\N	\N	\N
222	61	24	\N	Macarrão para Yakissoba Nissin 500g	Yakissoba Nissin 500g	500	g	\N	1	\N	Industrial semi-instantâneo vs artesanal De — indireto por processo	1	\N	\N	\N
223	61	24	\N	Macarrão para Yakissoba Nissin 1000g	Yakissoba Nissin 1000g	1000	g	\N	1	\N	Industrial, mesmo peso que o Matassado De — indireto por processo	1	\N	\N	\N
224	61	24	\N	Macarrão Instantâneo Yakissoba Nissin 87g	Yakissoba Instantâneo Nissin 87g	87	g	\N	0	\N	NÃO AUDITÁVEL: instantâneo snack — categoria completamente diferente	1	\N	\N	\N
225	62	24	\N	Macarrão para Yakissoba Tipo Caseiro Kirin 500g	Yakissoba Caseiro Kirin 500g	500	g	\N	1	\N	Artesanal tipo caseiro, mesmo peso — concorrência direta	1	\N	\N	\N
226	63	25	\N	Macarrão Pappardelle Barilla 500g	Pappardelle Barilla 500g	500	g	\N	1	\N	Importada, peso diferente (500g vs 400g De) — indireto	1	\N	\N	\N
227	63	23	\N	Macarrão Lasagna Barilla 500g	Lasagna Barilla 500g	500	g	\N	1	\N	Importada sêmola sem ovos vs caseira com ovos — indireto	1	\N	\N	\N
228	63	28	\N	Macarrão Farfalle Tricolor Barilla 500g	Farfalle Tricolor Barilla 500g	500	g	\N	1	\N	Importada, peso diferente vs Tricolori De 200g — indireto	1	\N	\N	\N
229	64	20	\N	Macarrão com Ovos Talharim 2 Adria 500g	Talharim Adria n°2 500g	500	g	\N	1	\N	Industrial líder nacional — define o preço teto que o consumidor aceita	1	\N	\N	\N
230	64	23	\N	Lasanha com Ovos Adria 500g	Lasanha Adria Ovos 500g	500	g	\N	1	\N	Industrial, mesmo peso — indireto por posicionamento	1	\N	\N	\N
231	65	20	\N	Macarrão Talharim Caseiro San Vito Speciale 500g	Talharim Caseiro San Vito 500g	500	g	\N	1	\N	Artesanal caseiro, mesmo peso — concorrência direta nas gôndolas SP/BS	1	\N	\N	\N
232	66	25	\N	Macarrão com Ovos Caseiro Pappardelle Sacciali 400g	Pappardelle Caseiro Sacciali 400g	400	g	\N	1	\N	Gourmet artesanal, mesmo peso 400g — concorrência direta	1	\N	\N	\N
233	67	20	\N	Macarrão Caseiro Talharim 2 Qualitá 500g	Talharim Caseiro Qualitá 500g	500	g	\N	1	\N	ATENÇÃO: fabricada pela própria Massas De para o GPA — risco de canibalização	1	\N	\N	\N
234	67	22	\N	Macarrão Caseiro Gravata Qualitá 500g	Gravata Caseira Qualitá 500g	500	g	\N	1	\N	Fabricada pela De para GPA — concorrência direta em preço	1	\N	\N	\N
235	68	20	\N	Macarrão Talharim Caseiro com Ovos Floriani 500g	Talharim Caseiro Floriani 500g	500	g	\N	1	\N	Artesanal caseiro com ovos, mesmo peso — concorrência direta	1	\N	\N	\N
236	69	20	\N	Macarrão Orgânico Talharim Native 500g	Talharim Orgânico Native 500g	500	g	\N	1	\N	Orgânico premium — indireto por posicionamento e público	1	\N	\N	\N
237	69	20	\N	Macarrão Integral Orgânico Native 500g	Integral Orgânico Native 500g	500	g	\N	1	\N	Orgânico premium — indireto por posicionamento	1	\N	\N	\N
\.


--
-- Data for Name: produto_concorrente_relacao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.produto_concorrente_relacao (relacao_id, produto_id, produto_concorrente_id, tipo_relacao, observacao) FROM stdin;
198	373	\N	direto	\N
201	370	250	direto	\N
204	370	254	direto	\N
207	311	257	indireto	\N
208	311	258	indireto	\N
209	311	259	indireto	\N
199	373	248	direto	\N
202	367	251	direto	\N
205	367	255	direto	\N
210	312	260	direto	\N
1	6	1	direto	\N
4	6	3	direto	\N
5	3	4	direto	\N
6	2	5	direto	\N
7	2	6	direto	\N
8	2	7	direto	\N
9	2	8	direto	\N
10	2	9	direto	\N
11	3	10	direto	\N
12	3	11	direto	\N
13	3	12	direto	\N
14	3	13	direto	\N
15	6	14	direto	\N
16	8	15	direto	\N
17	8	16	direto	\N
18	7	17	direto	\N
19	10	18	direto	\N
20	10	20	direto	\N
21	10	19	direto	\N
22	9	21	direto	\N
23	9	22	direto	\N
24	9	23	direto	\N
25	15	24	direto	\N
26	12	25	direto	\N
27	13	26	direto	\N
28	30	27	direto	\N
29	31	28	direto	\N
30	29	29	direto	\N
31	27	30	direto	\N
32	27	31	direto	\N
33	12	24	direto	\N
34	12	32	indireto	\N
35	12	33	indireto	\N
36	12	34	indireto	\N
37	12	35	indireto	\N
38	6	36	direto	\N
39	12	37	indireto	\N
40	2	38	indireto	\N
41	12	39	indireto	\N
42	2	40	indireto	\N
43	10	41	indireto	\N
44	9	42	indireto	\N
45	9	43	indireto	\N
46	9	44	indireto	\N
47	9	45	indireto	\N
48	12	46	indireto	\N
49	12	47	indireto	\N
50	12	48	indireto	\N
51	12	49	indireto	\N
52	12	50	indireto	\N
53	12	51	indireto	\N
54	12	52	indireto	\N
55	12	53	indireto	\N
56	3	54	direto	\N
57	12	55	indireto	\N
58	9	56	indireto	\N
59	31	57	direto	\N
60	47	58	direto	\N
61	47	59	indireto	\N
62	47	60	indireto	\N
63	47	61	direto	\N
64	47	62	direto	\N
65	47	63	direto	\N
66	75	64	indireto	\N
67	47	65	indireto	\N
68	75	66	indireto	\N
69	11	67	indireto	\N
70	11	68	indireto	\N
71	7	69	direto	\N
72	2	70	indireto	\N
73	2	71	indireto	\N
74	11	72	indireto	\N
75	14	73	indireto	\N
77	11	75	indireto	\N
79	11	77	indireto	\N
80	11	78	indireto	\N
81	11	79	indireto	\N
82	14	80	indireto	\N
83	11	81	indireto	\N
84	249	83	indireto	\N
85	249	84	indireto	\N
87	264	86	indireto	\N
88	264	87	indireto	\N
89	265	88	indireto	\N
90	255	89	indireto	\N
91	332	90	indireto	\N
92	269	91	indireto	\N
93	257	92	indireto	\N
94	257	93	indireto	\N
95	253	94	indireto	\N
96	253	95	indireto	\N
97	253	96	indireto	\N
98	254	97	indireto	\N
99	248	98	indireto	\N
100	264	99	indireto	\N
101	257	100	indireto	\N
102	264	101	indireto	\N
103	249	102	indireto	\N
104	251	103	indireto	\N
105	269	104	indireto	\N
106	269	105	indireto	\N
107	266	106	indireto	\N
108	248	107	indireto	\N
109	257	108	indireto	\N
110	249	109	indireto	\N
111	254	110	indireto	\N
112	249	111	indireto	\N
113	249	118	indireto	\N
114	255	123	direto	\N
115	329	124	direto	\N
116	257	125	indireto	\N
117	265	126	direto	\N
118	248	127	direto	\N
119	253	128	direto	\N
120	249	130	direto	\N
121	265	131	direto	\N
122	332	132	direto	\N
123	251	133	direto	\N
124	252	134	direto	\N
125	265	135	direto	\N
126	332	136	direto	\N
127	251	137	direto	\N
128	329	138	direto	\N
129	249	139	indireto	\N
130	246	142	direto	\N
131	246	145	indireto	\N
132	309	146	direto	\N
133	308	147	direto	\N
135	249	149	direto	\N
136	263	150	direto	\N
137	309	151	direto	\N
138	312	152	direto	\N
139	311	153	direto	\N
140	311	154	direto	\N
141	309	155	direto	\N
142	308	156	direto	\N
143	249	157	direto	\N
144	269	158	direto	\N
145	249	159	direto	\N
146	366	199	direto	\N
147	367	200	direto	\N
148	368	201	direto	\N
149	370	202	direto	\N
150	371	203	direto	\N
151	373	204	direto	\N
152	378	205	indireto	\N
153	367	206	direto	\N
154	371	207	direto	\N
155	373	208	direto	\N
156	378	209	indireto	\N
157	373	210	indireto	\N
158	367	211	direto	\N
159	371	212	direto	\N
160	370	213	direto	\N
161	373	214	direto	\N
162	378	215	indireto	\N
163	367	216	direto	\N
164	367	217	indireto	\N
165	373	218	direto	\N
166	376	219	indireto	\N
167	374	220	direto	\N
168	370	221	indireto	\N
169	376	222	indireto	\N
170	375	223	indireto	\N
171	376	225	indireto	\N
172	377	226	indireto	\N
173	373	227	indireto	\N
174	381	228	indireto	\N
175	367	229	indireto	\N
176	373	230	indireto	\N
177	367	231	direto	\N
178	377	232	direto	\N
179	367	233	direto	\N
180	371	234	direto	\N
181	366	235	direto	\N
182	367	236	indireto	\N
183	374	237	indireto	\N
184	248	85	indireto	\N
185	248	139	indireto	\N
186	249	85	indireto	\N
187	248	109	indireto	\N
188	269	238	indireto	\N
189	264	239	indireto	\N
190	47	240	indireto	\N
191	52	241	indireto	\N
192	31	242	direto	\N
193	31	243	direto	\N
194	31	244	direto	\N
195	31	245	direto	\N
196	375	225	indireto	\N
197	375	219	indireto	\N
200	373	249	direto	\N
203	370	252	direto	\N
206	2	256	direto	\N
134	311	148	indireto	\N
\.


--
-- Data for Name: promotor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.promotor (promotor_id, nome, fone, email, cpf, cnh, veiculo, cidade, estado, bairro, endereco, observacao, ativo) FROM stdin;
\.


--
-- Data for Name: representante; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.representante (representante_id, razao_social, nome_fantasia, cnpj, endereco, bairro, cidade, estado, fone, whatsapp, email, site, observacao, ativo) FROM stdin;
1	Azevedo & Filhos Representação Comercial	Azevedo e Filhos	20.086.123/0001-02	R. Jaú, 855 - sala 141 D	Boqueirão	Praia Grande	SP	11988334747	\N	fernandojr@azevedoefilhos.com.br	www.azevedoefilhos.com.br		1
\.


--
-- Data for Name: tabela_preco; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tabela_preco (tabela_preco_id, fornecedor_id, nome_tabela, tipo_tabela, prazo_pagamento, frete, data_inicio, data_fim, ativo) FROM stdin;
2	1	Rede 28d (2025)	rede	28 dias	CIF	2025-02-01	2026-03-31	0
3	1	Rede 42d (2025)	rede	42 dias	CIF	2025-02-01	2026-03-31	0
4	1	Atacado à vista (2025)	atacado	á vista	CIF	2025-02-01	2026-03-31	0
5	1	Atacado 28d (2025)	atacado	28 dias	CIF	2025-02-01	2026-03-31	0
1	1	Varejo 28d (2025)	varejo	28 dias	CIF	2025-02-01	2026-03-31	0
10	1	Atacado 7D (2026 Sem 1)	atacado	7 dias	CIF	2026-04-01	2026-04-30	0
8	1	Rede 28d (2026 Sem 1)	rede	28 dias	CIF	2026-04-01	2026-04-30	0
7	1	Varejo 28d (2026 Sem 1)	varejo	28 dias	CIF	2026-04-01	2026-04-30	0
11	1	Atacado 28D (2026 Sem 1)	atacado	28 dias	CIF	2026-04-01	2026-04-30	0
9	1	Rede 42d (2026 Sem 1)	rede	42 dias	CIF	2026-04-01	2026-04-30	0
19	4	Tabela 28d (2026)	Varejo	28	CIF	2026-01-01	\N	1
20	1	Varejo 28D (2026)	Varejo	28	CIF	2026-05-01	\N	1
21	1	Rede 28D (2026)	Rede	28	CIF	2026-05-01	\N	1
22	1	Rede 42D (2026)	Rede	42	CIF	2026-05-01	\N	1
23	1	Atacado 7D (2026)	Atacado	7	CIF	2026-05-01	\N	1
24	1	Atacado 28D (2026)	Atacado	28	CIF	2026-05-01	\N	1
12	3	Varejo 12d (2026)	varejo	12	FOB	2025-12-01	\N	1
6	2	Varejo 30d	varejo	30	CIF	2026-02-01	\N	1
\.


--
-- Data for Name: tabela_preco_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tabela_preco_item (tabela_preco_item_id, tabela_preco_id, produto_id, preco_caixa, desconto_maximo, preco_kg, observacao, peso_unidade) FROM stdin;
808	6	384	223.2	20	\N	\N	\N
809	6	385	223.2	20	\N	\N	\N
810	6	386	223.2	20	\N	\N	\N
876	21	27	42.33	10	\N	nan	\N
877	21	29	44.06	10	\N	nan	\N
878	21	31	41.31	10	\N	nan	\N
879	22	2	23.9	10	\N	nan	\N
880	22	3	23.9	10	\N	nan	\N
881	22	1	43.13	10	\N	nan	\N
882	22	382	18.98	10	\N	nan	\N
883	22	383	18.98	10	\N	nan	\N
884	22	4	28.95	10	\N	nan	\N
885	22	5	28.95	10	\N	nan	\N
886	22	6	71.59	10	\N	nan	\N
887	22	7	66.69	10	\N	nan	\N
888	22	8	66.69	10	\N	nan	\N
889	22	9	45.08	10	\N	nan	\N
890	22	10	45.08	10	\N	nan	\N
891	22	16	118.94	10	\N	nan	\N
892	22	13	31.12	10	\N	nan	\N
893	22	14	31.12	10	\N	nan	\N
894	22	15	34.22	10	\N	nan	\N
895	22	12	36.62	10	\N	nan	\N
896	22	11	37.23	10	\N	nan	\N
897	22	18	10.39	10	\N	nan	\N
898	22	17	10.39	10	\N	nan	\N
899	22	19	12.69	10	\N	nan	\N
900	22	20	12.69	10	\N	nan	\N
901	22	27	42.92	10	\N	nan	\N
902	22	29	44.68	10	\N	nan	\N
903	22	31	41.89	10	\N	nan	\N
904	23	2	20.96	10	\N	nan	\N
905	23	3	20.96	10	\N	nan	\N
906	23	1	36.05	10	\N	nan	\N
907	23	382	16.56	10	\N	nan	\N
908	23	383	16.56	10	\N	nan	\N
909	23	4	25.04	10	\N	nan	\N
910	23	5	25.04	10	\N	nan	\N
911	23	6	62.17	10	\N	nan	\N
912	23	7	57.92	10	\N	nan	\N
913	23	8	57.92	10	\N	nan	\N
914	23	9	39.15	10	\N	nan	\N
915	23	10	39.15	10	\N	nan	\N
916	23	16	108.61	10	\N	nan	\N
917	23	13	26.8	10	\N	nan	\N
918	23	14	26.8	10	\N	nan	\N
919	23	15	29.35	10	\N	nan	\N
920	23	12	31.53	10	\N	nan	\N
921	23	11	32.06	10	\N	nan	\N
922	23	18	9.49	10	\N	nan	\N
923	23	17	9.49	10	\N	nan	\N
924	23	19	11.59	10	\N	nan	\N
925	23	20	11.59	10	\N	nan	\N
926	23	27	39.19	10	\N	nan	\N
927	23	29	40.8	10	\N	nan	\N
928	23	31	38.25	10	\N	nan	\N
929	24	2	18.63	10	\N	nan	\N
930	24	3	18.63	10	\N	nan	\N
931	24	1	32.04	10	\N	nan	\N
932	24	382	14.72	10	\N	nan	\N
933	24	383	14.72	10	\N	nan	\N
934	24	4	22.26	10	\N	nan	\N
935	24	5	22.26	10	\N	nan	\N
936	24	6	55.26	10	\N	nan	\N
937	24	7	51.48	10	\N	nan	\N
938	24	8	51.48	10	\N	nan	\N
939	24	9	34.8	10	\N	nan	\N
940	24	10	34.8	10	\N	nan	\N
941	24	16	100.57	10	\N	nan	\N
942	24	13	23.82	10	\N	nan	\N
943	24	14	23.82	10	\N	nan	\N
944	24	15	26.09	10	\N	nan	\N
945	24	12	28.03	10	\N	nan	\N
946	24	11	28.49	10	\N	nan	\N
947	24	18	8.43	10	\N	nan	\N
948	24	17	8.43	10	\N	nan	\N
949	24	19	10.3	10	\N	nan	\N
950	24	20	10.3	10	\N	nan	\N
951	24	27	34.84	10	\N	nan	\N
952	24	29	36.27	10	\N	nan	\N
953	24	31	34	10	\N	nan	\N
811	19	380	232.8	5	\N	nan	\N
812	19	371	220.8	5	\N	nan	\N
813	19	372	164.6	5	\N	nan	\N
814	19	378	155.88	5	\N	nan	\N
815	19	370	206.88	5	\N	nan	\N
816	19	373	245.28	5	\N	nan	\N
817	19	377	82.3	5	\N	nan	\N
818	19	365	164.6	5	\N	nan	\N
819	19	366	164.6	5	\N	nan	\N
820	19	367	164.6	5	\N	nan	\N
821	19	368	164.6	5	\N	nan	\N
822	19	369	164.6	5	\N	nan	\N
823	19	376	108.25	5	\N	nan	\N
824	19	387	184	5	\N	nan	\N
825	19	375	179.8	5	\N	nan	\N
826	19	379	87.8	5	\N	nan	\N
827	19	374	204.4	5	\N	nan	\N
828	19	381	125.6	5	\N	nan	\N
1	1	1	41.2	20	\N	\N	\N
2	1	2	24.35	20	\N	\N	\N
3	1	3	24.35	20	\N	\N	\N
6	1	4	28.13	20	\N	\N	\N
7	1	5	27.59	20	\N	\N	\N
8	1	6	74.91	20	\N	\N	\N
9	1	7	69.07	20	\N	\N	\N
10	1	8	69.07	20	\N	\N	\N
11	1	9	46.35	20	\N	\N	\N
12	1	10	46.35	20	\N	\N	\N
13	1	11	30.39	20	\N	\N	\N
14	1	12	20.87	20	\N	\N	\N
15	1	13	19.6	20	\N	\N	\N
16	1	14	19.6	20	\N	\N	\N
17	1	15	22.76	20	\N	\N	\N
18	1	16	108.15	20	\N	\N	\N
829	20	2	23.22	10	\N	nan	\N
830	20	3	23.22	10	\N	nan	\N
831	20	1	41.5	10	\N	nan	\N
832	20	382	18.44	10	\N	nan	\N
833	20	383	18.44	10	\N	nan	\N
834	20	4	28.13	10	\N	nan	\N
835	20	5	28.13	10	\N	nan	\N
836	20	6	70.18	10	\N	nan	\N
837	20	7	65.37	10	\N	nan	\N
838	20	8	65.37	10	\N	nan	\N
839	20	9	44.19	10	\N	nan	\N
840	20	10	44.19	10	\N	nan	\N
841	20	16	115	10	\N	nan	\N
842	20	13	30.51	10	\N	nan	\N
843	20	14	30.51	10	\N	nan	\N
844	20	15	33.09	10	\N	nan	\N
19	1	17	10.2	20	\N	\N	\N
20	1	18	10.2	20	\N	\N	\N
21	1	19	12.83	20	\N	\N	\N
22	1	20	12.83	20	\N	\N	\N
23	1	21	29.15	20	\N	\N	\N
24	1	22	27.21	20	\N	\N	\N
25	1	23	27.21	20	\N	\N	\N
26	1	24	272.54	20	\N	\N	\N
27	1	25	229.28	20	\N	\N	\N
28	1	26	172.61	20	\N	\N	\N
29	1	27	42.64	20	\N	\N	\N
30	1	28	50.06	20	\N	\N	\N
31	1	29	46.35	20	\N	\N	\N
32	1	30	39.55	20	\N	\N	\N
33	1	31	41.15	20	\N	\N	\N
34	2	1	40	20	\N	\N	\N
35	2	2	23.64	20	\N	\N	\N
36	2	3	23.64	20	\N	\N	\N
39	2	4	26.79	20	\N	\N	\N
40	2	5	26.79	20	\N	\N	\N
41	2	6	72.73	20	\N	\N	\N
42	2	7	67.05	20	\N	\N	\N
43	2	8	67.05	20	\N	\N	\N
44	2	9	45	20	\N	\N	\N
45	2	10	45	20	\N	\N	\N
46	2	11	29.5	20	\N	\N	\N
47	2	12	20.27	20	\N	\N	\N
48	2	13	19.03	20	\N	\N	\N
49	2	14	19.03	20	\N	\N	\N
50	2	15	22.1	20	\N	\N	\N
51	2	16	105	20	\N	\N	\N
52	2	17	9.91	20	\N	\N	\N
53	2	18	9.91	20	\N	\N	\N
54	2	19	12.45	20	\N	\N	\N
55	2	20	12.45	20	\N	\N	\N
56	2	21	28.3	20	\N	\N	\N
57	2	22	26.42	20	\N	\N	\N
58	2	23	26.42	20	\N	\N	\N
59	2	24	264.6	20	\N	\N	\N
60	2	25	222.6	20	\N	\N	\N
61	2	26	167.58	20	\N	\N	\N
62	2	27	41.4	20	\N	\N	\N
63	2	28	48.6	20	\N	\N	\N
64	2	29	45	20	\N	\N	\N
65	2	30	38.4	20	\N	\N	\N
66	2	31	39.95	20	\N	\N	\N
67	3	1	42.06	20	\N	\N	\N
68	3	2	24.85	20	\N	\N	\N
69	3	3	24.85	20	\N	\N	\N
72	3	4	28.17	20	\N	\N	\N
73	3	5	28.17	20	\N	\N	\N
74	3	6	76.47	20	\N	\N	\N
75	3	7	70.51	20	\N	\N	\N
76	3	8	70.51	20	\N	\N	\N
77	3	9	47.32	20	\N	\N	\N
78	3	10	47.32	20	\N	\N	\N
79	3	11	31.02	20	\N	\N	\N
80	3	12	21.31	20	\N	\N	\N
81	3	13	20.01	20	\N	\N	\N
82	3	14	20.01	20	\N	\N	\N
83	3	15	23.24	20	\N	\N	\N
84	3	16	110.82	20	\N	\N	\N
85	3	17	10.42	20	\N	\N	\N
86	3	18	10.42	20	\N	\N	\N
87	3	19	13.09	20	\N	\N	\N
88	3	20	13.09	20	\N	\N	\N
89	3	21	29.76	20	\N	\N	\N
90	3	22	27.78	20	\N	\N	\N
91	3	23	27.78	20	\N	\N	\N
92	3	24	278.23	20	\N	\N	\N
93	3	25	234.07	20	\N	\N	\N
94	3	26	176.21	20	\N	\N	\N
95	3	27	43.53	20	\N	\N	\N
96	3	28	51.1	20	\N	\N	\N
97	3	29	47.32	20	\N	\N	\N
98	3	30	40.38	20	\N	\N	\N
99	3	31	42.01	20	\N	\N	\N
100	4	1	32	20	\N	\N	\N
101	4	2	18.91	20	\N	\N	\N
102	4	3	18.91	20	\N	\N	\N
105	4	4	21.43	20	\N	\N	\N
106	4	5	21.43	20	\N	\N	\N
107	4	6	66.12	20	\N	\N	\N
108	4	7	60.96	20	\N	\N	\N
109	4	8	60.96	20	\N	\N	\N
110	4	9	45	20	\N	\N	\N
111	4	10	45	20	\N	\N	\N
112	4	11	28.1	20	\N	\N	\N
113	4	12	19.3	20	\N	\N	\N
114	4	13	18.12	20	\N	\N	\N
115	4	14	18.12	20	\N	\N	\N
116	4	15	21.05	20	\N	\N	\N
117	4	16	105	20	\N	\N	\N
118	4	17	8.25	20	\N	\N	\N
119	4	18	8.25	20	\N	\N	\N
120	4	19	10.38	20	\N	\N	\N
121	4	20	10.38	20	\N	\N	\N
122	4	21	23.58	20	\N	\N	\N
123	4	22	22.01	20	\N	\N	\N
124	4	23	22.01	20	\N	\N	\N
125	4	24	264.6	20	\N	\N	\N
126	4	25	222.6	20	\N	\N	\N
127	4	26	167.58	20	\N	\N	\N
128	4	27	37.64	20	\N	\N	\N
129	4	28	44.18	20	\N	\N	\N
130	4	29	40.91	20	\N	\N	\N
131	4	30	34.91	20	\N	\N	\N
132	4	31	36.32	20	\N	\N	\N
133	5	1	33.08	20	\N	\N	\N
134	5	2	19.55	20	\N	\N	\N
135	5	3	19.55	20	\N	\N	\N
138	5	4	22.15	20	\N	\N	\N
139	5	5	22.15	20	\N	\N	\N
140	5	6	68.35	20	\N	\N	\N
141	5	7	63.02	20	\N	\N	\N
142	5	8	63.02	20	\N	\N	\N
143	5	9	46.52	20	\N	\N	\N
144	5	10	46.52	20	\N	\N	\N
145	5	11	29.05	20	\N	\N	\N
146	5	12	19.95	20	\N	\N	\N
147	5	13	18.73	20	\N	\N	\N
148	5	14	18.73	20	\N	\N	\N
149	5	15	21.76	20	\N	\N	\N
150	5	16	105	20	\N	\N	\N
151	5	17	8.53	20	\N	\N	\N
152	5	18	8.53	20	\N	\N	\N
153	5	19	10.73	20	\N	\N	\N
154	5	20	10.73	20	\N	\N	\N
155	5	21	24.38	20	\N	\N	\N
156	5	22	22.76	20	\N	\N	\N
157	5	23	22.76	20	\N	\N	\N
158	5	24	273.54	20	\N	\N	\N
159	5	25	230.13	20	\N	\N	\N
160	5	26	173.25	20	\N	\N	\N
161	5	27	38.91	20	\N	\N	\N
162	5	28	45.68	20	\N	\N	\N
163	5	29	42.29	20	\N	\N	\N
164	5	30	36.09	20	\N	\N	\N
165	5	31	37.55	20	\N	\N	\N
166	6	32	195.6	20	\N	\N	\N
333	6	33	195.6	20	\N	\N	\N
334	6	34	195.6	20	\N	\N	\N
335	6	35	195.6	20	\N	\N	\N
336	6	36	195.6	20	\N	\N	\N
337	6	37	195.6	20	\N	\N	\N
338	6	38	195.6	20	\N	\N	\N
339	6	39	195.6	20	\N	\N	\N
340	6	40	195.6	20	\N	\N	\N
341	6	41	195.6	20	\N	\N	\N
342	6	42	195.6	20	\N	\N	\N
343	6	43	248.4	20	\N	\N	\N
344	6	44	195.6	20	\N	\N	\N
345	6	45	195.6	20	\N	\N	\N
346	6	46	195.6	20	\N	\N	\N
347	6	47	223.2	20	\N	\N	\N
348	6	48	208.8	20	\N	\N	\N
349	6	49	208.8	20	\N	\N	\N
350	6	50	208.8	20	\N	\N	\N
351	6	51	208.8	20	\N	\N	\N
352	6	52	195.6	20	\N	\N	\N
353	6	53	195.6	20	\N	\N	\N
354	6	54	195.6	20	\N	\N	\N
355	6	55	195.6	20	\N	\N	\N
356	6	56	195.6	20	\N	\N	\N
357	6	57	195.6	20	\N	\N	\N
358	6	58	195.6	20	\N	\N	\N
359	6	59	195.6	20	\N	\N	\N
360	6	60	195.6	20	\N	\N	\N
361	6	61	195.6	20	\N	\N	\N
362	6	62	195.6	20	\N	\N	\N
363	6	63	195.6	20	\N	\N	\N
364	6	64	195.6	20	\N	\N	\N
365	6	65	195.6	20	\N	\N	\N
366	6	66	195.6	20	\N	\N	\N
367	6	67	195.6	20	\N	\N	\N
368	6	68	208.8	20	\N	\N	\N
369	6	69	195.6	20	\N	\N	\N
370	6	70	195.6	20	\N	\N	\N
371	6	71	195.6	20	\N	\N	\N
372	6	72	195.6	20	\N	\N	\N
373	6	73	195.6	20	\N	\N	\N
374	6	74	208.8	20	\N	\N	\N
375	6	75	208.8	20	\N	\N	\N
376	6	76	208.8	20	\N	\N	\N
377	6	77	208.8	20	\N	\N	\N
378	6	78	208.8	20	\N	\N	\N
379	7	1	39.95	20	\N	\N	\N
380	7	2	21.1	20	\N	\N	\N
381	7	3	21.1	20	\N	\N	\N
382	7	4	24.2	20	\N	\N	\N
383	7	5	24.2	20	\N	\N	\N
384	7	6	64	20	\N	\N	\N
385	7	7	59.8	20	\N	\N	\N
386	7	8	59.8	20	\N	\N	\N
387	7	9	38	20	\N	\N	\N
388	7	10	38	20	\N	\N	\N
389	7	11	23.181818	20	\N	\N	\N
390	7	12	19.772728	20	\N	\N	\N
391	7	13	19.5	20	\N	\N	\N
392	7	14	19.5	20	\N	\N	\N
393	7	15	19.77	20	\N	\N	\N
394	7	16	105	20	\N	\N	\N
395	7	17	9.1	20	\N	\N	\N
396	7	18	9.1	20	\N	\N	\N
397	7	19	10.05	20	\N	\N	\N
398	7	20	10.05	20	\N	\N	\N
399	7	27	34.2	20	\N	\N	\N
400	7	29	35.7	20	\N	\N	\N
401	7	31	33.5	20	\N	\N	\N
402	8	1	40.94875	20	\N	\N	\N
403	8	2	21.4165	20	\N	\N	\N
404	8	3	21.4165	20	\N	\N	\N
405	8	4	24.563	20	\N	\N	\N
406	8	5	24.563	20	\N	\N	\N
407	8	6	64.96	20	\N	\N	\N
408	8	7	60.697	20	\N	\N	\N
409	8	8	60.697	20	\N	\N	\N
410	8	9	38.57	20	\N	\N	\N
411	8	10	38.57	20	\N	\N	\N
412	8	11	23.645454	20	\N	\N	\N
413	8	12	20.168182	20	\N	\N	\N
414	8	13	19.89	20	\N	\N	\N
415	8	14	19.89	20	\N	\N	\N
416	8	15	20.1654	20	\N	\N	\N
417	8	16	107.1	20	\N	\N	\N
418	8	17	9.282	20	\N	\N	\N
419	8	18	9.282	20	\N	\N	\N
420	8	19	10.251	20	\N	\N	\N
421	8	20	10.251	20	\N	\N	\N
422	8	27	34.884	20	\N	\N	\N
423	8	29	36.414	20	\N	\N	\N
424	8	31	34.17	20	\N	\N	\N
425	9	1	41.96275	20	\N	\N	\N
426	9	2	22.4305	20	\N	\N	\N
427	9	3	22.4305	20	\N	\N	\N
428	9	4	25.577	20	\N	\N	\N
429	9	5	25.577	20	\N	\N	\N
430	9	6	65.974	20	\N	\N	\N
431	9	7	61.711	20	\N	\N	\N
432	9	8	61.711	20	\N	\N	\N
433	9	9	39.584	20	\N	\N	\N
434	9	10	39.584	20	\N	\N	\N
435	9	11	24.659454	20	\N	\N	\N
436	9	12	21.182182	20	\N	\N	\N
437	9	13	20.904	20	\N	\N	\N
438	9	14	20.904	20	\N	\N	\N
439	9	15	21.1794	20	\N	\N	\N
440	9	16	108.114	20	\N	\N	\N
441	9	17	10.296	20	\N	\N	\N
442	9	18	10.296	20	\N	\N	\N
443	9	19	11.265	20	\N	\N	\N
444	9	20	11.265	20	\N	\N	\N
445	9	27	35.898	20	\N	\N	\N
446	9	29	37.428	20	\N	\N	\N
447	9	31	35.184	20	\N	\N	\N
448	10	1	34.70233	20	\N	\N	\N
449	10	2	18.149576	20	\N	\N	\N
450	10	3	18.149576	20	\N	\N	\N
451	10	4	20.816101	20	\N	\N	\N
452	10	5	20.816101	20	\N	\N	\N
453	10	6	55.050846	20	\N	\N	\N
454	10	7	51.438137	20	\N	\N	\N
455	10	8	51.438137	20	\N	\N	\N
456	10	9	32.68644	20	\N	\N	\N
457	10	10	32.68644	20	\N	\N	\N
458	10	11	21.495869	20	\N	\N	\N
459	10	12	18.334711	20	\N	\N	\N
460	10	13	18.081818	20	\N	\N	\N
461	10	14	18.081818	20	\N	\N	\N
462	10	15	18.332182	20	\N	\N	\N
463	10	16	97.36364	20	\N	\N	\N
464	10	17	8.438182	20	\N	\N	\N
465	10	18	8.438182	20	\N	\N	\N
466	10	19	9.319091	20	\N	\N	\N
467	10	20	9.319091	20	\N	\N	\N
468	10	27	31.712727	20	\N	\N	\N
469	10	29	33.103638	20	\N	\N	\N
470	10	31	31.063637	20	\N	\N	\N
471	11	1	35.43108	20	\N	\N	\N
472	11	2	18.530718	20	\N	\N	\N
473	11	3	18.530718	20	\N	\N	\N
474	11	4	21.25324	20	\N	\N	\N
475	11	5	21.25324	20	\N	\N	\N
476	11	6	56.206917	20	\N	\N	\N
477	11	7	52.518337	20	\N	\N	\N
478	11	8	52.518337	20	\N	\N	\N
479	11	9	33.372856	20	\N	\N	\N
480	11	10	33.372856	20	\N	\N	\N
481	11	11	21.94728	20	\N	\N	\N
482	11	12	18.71974	20	\N	\N	\N
483	11	13	18.461536	20	\N	\N	\N
484	11	14	18.461536	20	\N	\N	\N
485	11	15	18.717157	20	\N	\N	\N
486	11	16	99.40827	20	\N	\N	\N
487	11	17	8.615384	20	\N	\N	\N
488	11	18	8.615384	20	\N	\N	\N
489	11	19	9.5147915	20	\N	\N	\N
490	11	20	9.5147915	20	\N	\N	\N
491	11	27	32.378696	20	\N	\N	\N
492	11	29	33.798813	20	\N	\N	\N
493	11	31	31.715973	20	\N	\N	\N
688	12	242	404.1	20	13.47	nan	\N
689	12	243	459	20	\N	nan	\N
690	12	244	522.5	20	\N	nan	\N
691	12	245	684	20	\N	nan	\N
692	12	246	479.7	20	15.99	nan	\N
693	12	247	569.7	20	18.99	nan	\N
694	12	248	439.79	20	21.99	nan	\N
695	12	249	383.84	20	23.99	nan	\N
696	12	250	579.8	20	28.99	nan	\N
697	12	251	367.84	20	22.99	nan	\N
698	12	252	550	20	27.5	nan	\N
699	12	253	512	20	32	nan	\N
700	12	254	337.68	20	67	nan	\N
701	12	255	352.75	20	69.99	nan	\N
702	12	256	322.51	20	63.99	nan	\N
703	12	257	410	20	20.5	nan	\N
704	12	258	415.84	20	25.99	nan	\N
705	12	259	376	20	23.5	nan	\N
706	12	260	504	20	31.5	nan	\N
707	12	261	519.8	20	25.99	nan	\N
708	12	262	383.84	20	23.99	nan	\N
709	12	263	670	20	33.5	nan	\N
710	12	264	439.79	20	21.99	nan	\N
711	12	265	384	20	24	nan	\N
712	12	266	424	20	26.5	nan	\N
713	12	267	431.84	20	26.99	nan	\N
714	12	268	424	20	26.5	nan	\N
715	12	269	255.84	20	15.99	nan	\N
716	12	270	239.85	20	15.99	nan	\N
717	12	271	284.85	20	18.99	nan	\N
718	12	272	219.9	20	21.99	nan	\N
719	12	273	191.92	20	23.99	nan	\N
720	12	274	289.9	20	28.99	nan	\N
721	12	275	183.92	20	22.99	nan	\N
722	12	363	275	20	27.5	nan	\N
723	12	277	256	20	32	nan	\N
724	12	278	402	20	67	nan	\N
725	12	279	419.94	20	69.99	nan	\N
726	12	280	383.94	20	63.99	nan	\N
727	12	281	205	20	20.5	nan	\N
728	12	282	207.92	20	25.99	nan	\N
729	12	283	188	20	23.5	nan	\N
730	12	284	252	20	31.5	nan	\N
731	12	285	259.9	20	25.99	nan	\N
732	12	286	191.92	20	23.99	nan	\N
733	12	287	335	20	33.5	nan	\N
734	12	288	219.9	20	21.99	nan	\N
735	12	289	192	20	24	nan	\N
736	12	290	212	20	26.5	nan	\N
737	12	291	215.92	20	26.99	nan	\N
738	12	292	212	20	26.5	nan	\N
739	12	293	127.92	20	15.99	nan	\N
740	12	294	449.7	20	14.99	nan	\N
741	12	295	149.9	20	14.99	nan	\N
742	12	296	449.7	20	14.99	nan	\N
743	12	297	149.9	20	14.99	nan	\N
744	12	298	449.7	20	14.99	nan	\N
745	12	299	149.9	20	14.99	nan	\N
746	12	300	209.7	20	6.99	nan	\N
747	12	301	69.9	20	6.99	nan	\N
748	12	302	185.97	20	61.99	nan	\N
749	12	303	600	20	20	nan	\N
750	12	304	200	20	20	nan	\N
751	12	305	799.96	20	199.99	nan	\N
752	12	306	1999.9	20	199.99	nan	\N
753	12	307	419.7	20	13.99	nan	\N
754	12	308	423	20	23.5	nan	\N
755	12	309	341.82	20	18.99	nan	\N
756	12	310	225	20	22.5	nan	\N
757	12	311	306	20	17	nan	\N
758	12	312	279	20	15.5	nan	\N
759	12	313	378	20	21	nan	\N
760	12	314	209.85	20	13.99	nan	\N
761	12	315	211.5	20	23.5	nan	\N
762	12	316	170.91	20	18.99	nan	\N
763	12	317	135	20	22.5	nan	\N
764	12	318	153	20	17	nan	\N
765	12	319	139.5	20	15.5	nan	\N
766	12	320	189	20	21	nan	\N
767	12	321	439.79	20	21.99	nan	\N
768	12	322	383.84	20	23.99	nan	\N
769	12	323	579.8	20	28.99	nan	\N
770	12	324	367.84	20	22.99	nan	\N
771	12	325	550	20	27.5	nan	\N
772	12	326	512	20	32	nan	\N
773	12	327	410	20	20.5	nan	\N
774	12	328	415.84	20	25.99	nan	\N
775	12	329	376	20	23.5	nan	\N
776	12	330	504	20	31.5	nan	\N
777	12	331	519.8	20	25.99	nan	\N
778	12	332	383.84	20	23.99	nan	\N
779	12	333	670	20	33.5	nan	\N
780	12	334	439.79	20	21.99	nan	\N
781	12	335	384	20	24	nan	\N
782	12	336	424	20	26.5	nan	\N
783	12	337	431.84	20	26.99	nan	\N
784	12	338	424	20	26.5	nan	\N
785	12	339	255.84	20	15.99	nan	\N
786	12	340	219.9	20	21.99	nan	\N
787	12	341	191.92	20	23.99	nan	\N
788	12	342	289.9	20	28.99	nan	\N
789	12	343	183.92	20	22.99	nan	\N
790	12	276	275	20	27.5	nan	\N
791	12	344	256	20	32	nan	\N
792	12	345	205	20	20.5	nan	\N
793	12	346	207.92	20	25.99	nan	\N
794	12	347	188	20	23.5	nan	\N
795	12	348	252	20	31.5	nan	\N
796	12	349	259.9	20	25.99	nan	\N
797	12	350	191.92	20	23.99	nan	\N
798	12	351	335	20	33.5	nan	\N
799	12	352	219.9	20	21.99	nan	\N
800	12	353	192	20	24	nan	\N
801	12	354	212	20	26.5	nan	\N
802	12	355	215.92	20	26.99	nan	\N
803	12	356	212	20	26.5	nan	\N
804	12	357	127.92	20	15.99	nan	\N
805	12	358	23.6	20	\N	nan	\N
806	12	359	17.99	20	\N	nan	\N
807	12	360	166.5	20	\N	nan	\N
845	20	12	35.9	10	\N	nan	\N
846	20	11	36.5	10	\N	nan	\N
847	20	18	10.05	10	\N	nan	\N
848	20	17	10.05	10	\N	nan	\N
849	20	19	12.27	10	\N	nan	\N
850	20	20	12.27	10	\N	nan	\N
851	20	27	41.5	10	\N	nan	\N
852	20	29	43.2	10	\N	nan	\N
853	20	31	40.5	10	\N	nan	\N
854	21	2	23.57	10	\N	nan	\N
855	21	3	23.57	10	\N	nan	\N
856	21	1	42.54	10	\N	nan	\N
857	21	382	18.71	10	\N	nan	\N
858	21	383	18.71	10	\N	nan	\N
859	21	4	28.55	10	\N	nan	\N
860	21	5	28.55	10	\N	nan	\N
861	21	6	70.88	10	\N	nan	\N
862	21	7	66.03	10	\N	nan	\N
863	21	8	66.03	10	\N	nan	\N
864	21	9	44.63	10	\N	nan	\N
865	21	10	44.63	10	\N	nan	\N
866	21	16	117.3	10	\N	nan	\N
867	21	13	30.82	10	\N	nan	\N
868	21	14	30.82	10	\N	nan	\N
869	21	15	33.75	10	\N	nan	\N
870	21	12	36.26	10	\N	nan	\N
871	21	11	36.87	10	\N	nan	\N
872	21	18	10.25	10	\N	nan	\N
873	21	17	10.25	10	\N	nan	\N
874	21	19	12.52	10	\N	nan	\N
875	21	20	12.52	10	\N	nan	\N
\.


--
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario (usuario_id, nome, email, senha_hash, tipo, vendedor_id, ativo) FROM stdin;
\.


--
-- Data for Name: vendedor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vendedor (vendedor_id, representante_id, nome, fone, whatsapp, email, cpf, chave_pix, data_aniversario, observacao, ativo) FROM stdin;
1	1	Fernando Azevedo Jr	11988334747	\N	fernandojr@azevedoefilhos.com.br	10538292806	11988334747	18/10	\N	1
\.


--
-- Data for Name: visita_cliente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.visita_cliente (visita_id, cliente_id, pdv_id, local, data_visita, contato, resumo, produtos_tratados, pedido_id, proxima_acao, data_followup, observacao, pesquisa_preco_id, latitude, longitude, endereco_gps, duracao_minutos) FROM stdin;
1	3	2	PDV	2026-03-31	Carlos (Compras)	Emitido o primeiro pedido e encaminhado os dados cadastrais do cliente para a Belmont.	\N	\N	Acompanhar pedido e entrega	\N	\N	\N	\N	\N	\N	\N
2	58	114	Prospeccao	2026-05-13	Ed Carlo	Tratamos Introdução DIET HOUSE e solicitou amostras SPECIALLI.	\N	\N	\N	2026-05-20	\N	\N	\N	\N	\N	30
\.


--
-- Data for Name: schema_migrations; Type: TABLE DATA; Schema: realtime; Owner: supabase_admin
--

COPY realtime.schema_migrations (version, inserted_at) FROM stdin;
20211116024918	2026-04-26 16:03:53
20211116045059	2026-04-26 16:03:54
20211116050929	2026-04-26 16:03:56
20211116051442	2026-04-26 16:03:57
20211116212300	2026-04-26 16:03:58
20211116213355	2026-04-26 16:03:59
20211116213934	2026-04-26 16:04:00
20211116214523	2026-04-26 16:04:02
20211122062447	2026-04-26 16:04:03
20211124070109	2026-04-26 16:04:04
20211202204204	2026-04-26 16:04:05
20211202204605	2026-04-26 16:04:06
20211210212804	2026-04-26 16:04:10
20211228014915	2026-04-26 16:04:11
20220107221237	2026-04-26 16:04:12
20220228202821	2026-04-26 16:04:14
20220312004840	2026-04-26 16:04:15
20220603231003	2026-04-26 16:04:17
20220603232444	2026-04-26 16:04:18
20220615214548	2026-04-26 16:04:19
20220712093339	2026-04-26 16:04:20
20220908172859	2026-04-26 16:04:21
20220916233421	2026-04-26 16:04:22
20230119133233	2026-04-26 16:04:24
20230128025114	2026-04-26 16:04:25
20230128025212	2026-04-26 16:04:26
20230227211149	2026-04-26 16:04:27
20230228184745	2026-04-26 16:04:28
20230308225145	2026-04-26 16:04:30
20230328144023	2026-04-26 16:04:31
20231018144023	2026-04-26 16:04:32
20231204144023	2026-04-26 16:04:34
20231204144024	2026-04-26 16:04:35
20231204144025	2026-04-26 16:04:36
20240108234812	2026-04-26 16:04:37
20240109165339	2026-04-26 16:04:38
20240227174441	2026-04-26 16:04:40
20240311171622	2026-04-26 16:04:42
20240321100241	2026-04-26 16:04:44
20240401105812	2026-04-26 16:04:48
20240418121054	2026-04-26 16:04:49
20240523004032	2026-04-26 16:04:53
20240618124746	2026-04-26 16:04:54
20240801235015	2026-04-26 16:04:56
20240805133720	2026-04-26 16:04:57
20240827160934	2026-04-26 16:04:58
20240919163303	2026-04-26 16:04:59
20240919163305	2026-04-26 16:05:01
20241019105805	2026-04-26 16:05:02
20241030150047	2026-04-26 16:05:06
20241108114728	2026-04-26 16:05:08
20241121104152	2026-04-26 16:05:09
20241130184212	2026-04-26 16:05:10
20241220035512	2026-04-26 16:05:11
20241220123912	2026-04-26 16:05:12
20241224161212	2026-04-26 16:05:13
20250107150512	2026-04-26 16:05:15
20250110162412	2026-04-26 16:05:16
20250123174212	2026-04-26 16:05:17
20250128220012	2026-04-26 16:05:18
20250506224012	2026-04-26 16:05:19
20250523164012	2026-04-26 16:05:20
20250714121412	2026-04-26 16:05:21
20250905041441	2026-04-26 16:05:22
20251103001201	2026-04-26 16:05:23
20251120212548	2026-04-26 16:05:25
20251120215549	2026-04-26 16:05:26
20260218120000	2026-04-26 16:05:27
20260326120000	2026-04-26 16:05:28
\.


--
-- Data for Name: subscription; Type: TABLE DATA; Schema: realtime; Owner: supabase_admin
--

COPY realtime.subscription (id, subscription_id, entity, filters, claims, created_at, action_filter) FROM stdin;
\.


--
-- Data for Name: buckets; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.buckets (id, name, owner, created_at, updated_at, public, avif_autodetection, file_size_limit, allowed_mime_types, owner_id, type) FROM stdin;
\.


--
-- Data for Name: buckets_analytics; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.buckets_analytics (name, type, format, created_at, updated_at, id, deleted_at) FROM stdin;
\.


--
-- Data for Name: buckets_vectors; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.buckets_vectors (id, type, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: migrations; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.migrations (id, name, hash, executed_at) FROM stdin;
0	create-migrations-table	e18db593bcde2aca2a408c4d1100f6abba2195df	2026-04-26 01:57:35.8712
1	initialmigration	6ab16121fbaa08bbd11b712d05f358f9b555d777	2026-04-26 01:57:35.901195
2	storage-schema	f6a1fa2c93cbcd16d4e487b362e45fca157a8dbd	2026-04-26 01:57:35.902703
3	pathtoken-column	2cb1b0004b817b29d5b0a971af16bafeede4b70d	2026-04-26 01:57:35.924219
4	add-migrations-rls	427c5b63fe1c5937495d9c635c263ee7a5905058	2026-04-26 01:57:35.93266
5	add-size-functions	79e081a1455b63666c1294a440f8ad4b1e6a7f84	2026-04-26 01:57:35.93456
6	change-column-name-in-get-size	ded78e2f1b5d7e616117897e6443a925965b30d2	2026-04-26 01:57:35.939162
7	add-rls-to-buckets	e7e7f86adbc51049f341dfe8d30256c1abca17aa	2026-04-26 01:57:35.94264
8	add-public-to-buckets	fd670db39ed65f9d08b01db09d6202503ca2bab3	2026-04-26 01:57:35.944793
9	fix-search-function	af597a1b590c70519b464a4ab3be54490712796b	2026-04-26 01:57:35.948423
10	search-files-search-function	b595f05e92f7e91211af1bbfe9c6a13bb3391e16	2026-04-26 01:57:35.950824
11	add-trigger-to-auto-update-updated_at-column	7425bdb14366d1739fa8a18c83100636d74dcaa2	2026-04-26 01:57:35.953189
12	add-automatic-avif-detection-flag	8e92e1266eb29518b6a4c5313ab8f29dd0d08df9	2026-04-26 01:57:35.95582
13	add-bucket-custom-limits	cce962054138135cd9a8c4bcd531598684b25e7d	2026-04-26 01:57:35.958039
14	use-bytes-for-max-size	941c41b346f9802b411f06f30e972ad4744dad27	2026-04-26 01:57:35.960271
15	add-can-insert-object-function	934146bc38ead475f4ef4b555c524ee5d66799e5	2026-04-26 01:57:35.980728
16	add-version	76debf38d3fd07dcfc747ca49096457d95b1221b	2026-04-26 01:57:35.98294
17	drop-owner-foreign-key	f1cbb288f1b7a4c1eb8c38504b80ae2a0153d101	2026-04-26 01:57:35.984958
18	add_owner_id_column_deprecate_owner	e7a511b379110b08e2f214be852c35414749fe66	2026-04-26 01:57:35.986957
19	alter-default-value-objects-id	02e5e22a78626187e00d173dc45f58fa66a4f043	2026-04-26 01:57:35.990558
20	list-objects-with-delimiter	cd694ae708e51ba82bf012bba00caf4f3b6393b7	2026-04-26 01:57:35.993528
21	s3-multipart-uploads	8c804d4a566c40cd1e4cc5b3725a664a9303657f	2026-04-26 01:57:35.997793
22	s3-multipart-uploads-big-ints	9737dc258d2397953c9953d9b86920b8be0cdb73	2026-04-26 01:57:36.010658
23	optimize-search-function	9d7e604cddc4b56a5422dc68c9313f4a1b6f132c	2026-04-26 01:57:36.017887
24	operation-function	8312e37c2bf9e76bbe841aa5fda889206d2bf8aa	2026-04-26 01:57:36.020238
25	custom-metadata	d974c6057c3db1c1f847afa0e291e6165693b990	2026-04-26 01:57:36.022436
26	objects-prefixes	215cabcb7f78121892a5a2037a09fedf9a1ae322	2026-04-26 01:57:36.024829
27	search-v2	859ba38092ac96eb3964d83bf53ccc0b141663a6	2026-04-26 01:57:36.026586
28	object-bucket-name-sorting	c73a2b5b5d4041e39705814fd3a1b95502d38ce4	2026-04-26 01:57:36.028241
29	create-prefixes	ad2c1207f76703d11a9f9007f821620017a66c21	2026-04-26 01:57:36.029991
30	update-object-levels	2be814ff05c8252fdfdc7cfb4b7f5c7e17f0bed6	2026-04-26 01:57:36.031618
31	objects-level-index	b40367c14c3440ec75f19bbce2d71e914ddd3da0	2026-04-26 01:57:36.033404
32	backward-compatible-index-on-objects	e0c37182b0f7aee3efd823298fb3c76f1042c0f7	2026-04-26 01:57:36.035095
33	backward-compatible-index-on-prefixes	b480e99ed951e0900f033ec4eb34b5bdcb4e3d49	2026-04-26 01:57:36.036757
34	optimize-search-function-v1	ca80a3dc7bfef894df17108785ce29a7fc8ee456	2026-04-26 01:57:36.038414
35	add-insert-trigger-prefixes	458fe0ffd07ec53f5e3ce9df51bfdf4861929ccc	2026-04-26 01:57:36.040041
36	optimise-existing-functions	6ae5fca6af5c55abe95369cd4f93985d1814ca8f	2026-04-26 01:57:36.041774
37	add-bucket-name-length-trigger	3944135b4e3e8b22d6d4cbb568fe3b0b51df15c1	2026-04-26 01:57:36.043324
38	iceberg-catalog-flag-on-buckets	02716b81ceec9705aed84aa1501657095b32e5c5	2026-04-26 01:57:36.04586
39	add-search-v2-sort-support	6706c5f2928846abee18461279799ad12b279b78	2026-04-26 01:57:36.052405
40	fix-prefix-race-conditions-optimized	7ad69982ae2d372b21f48fc4829ae9752c518f6b	2026-04-26 01:57:36.054123
41	add-object-level-update-trigger	07fcf1a22165849b7a029deed059ffcde08d1ae0	2026-04-26 01:57:36.05615
42	rollback-prefix-triggers	771479077764adc09e2ea2043eb627503c034cd4	2026-04-26 01:57:36.05786
43	fix-object-level	84b35d6caca9d937478ad8a797491f38b8c2979f	2026-04-26 01:57:36.059631
44	vector-bucket-type	99c20c0ffd52bb1ff1f32fb992f3b351e3ef8fb3	2026-04-26 01:57:36.061408
45	vector-buckets	049e27196d77a7cb76497a85afae669d8b230953	2026-04-26 01:57:36.063877
46	buckets-objects-grants	fedeb96d60fefd8e02ab3ded9fbde05632f84aed	2026-04-26 01:57:36.071071
47	iceberg-table-metadata	649df56855c24d8b36dd4cc1aeb8251aa9ad42c2	2026-04-26 01:57:36.073802
48	iceberg-catalog-ids	e0e8b460c609b9999ccd0df9ad14294613eed939	2026-04-26 01:57:36.07573
49	buckets-objects-grants-postgres	072b1195d0d5a2f888af6b2302a1938dd94b8b3d	2026-04-26 01:57:36.088385
50	search-v2-optimised	6323ac4f850aa14e7387eb32102869578b5bd478	2026-04-26 01:57:36.091161
51	index-backward-compatible-search	2ee395d433f76e38bcd3856debaf6e0e5b674011	2026-04-26 01:57:36.349646
52	drop-not-used-indexes-and-functions	5cc44c8696749ac11dd0dc37f2a3802075f3a171	2026-04-26 01:57:36.352073
53	drop-index-lower-name	d0cb18777d9e2a98ebe0bc5cc7a42e57ebe41854	2026-04-26 01:57:36.363116
54	drop-index-object-level	6289e048b1472da17c31a7eba1ded625a6457e67	2026-04-26 01:57:36.364767
55	prevent-direct-deletes	262a4798d5e0f2e7c8970232e03ce8be695d5819	2026-04-26 01:57:36.366087
57	s3-multipart-uploads-metadata	f127886e00d1b374fadbc7c6b31e09336aad5287	2026-04-26 01:57:36.372621
58	operation-ergonomics	00ca5d483b3fe0d522133d9002ccc5df98365120	2026-04-26 01:57:36.37477
56	fix-optimized-search-function	b823ed1e418101032fa01374edc9a436e54e3ed4	2026-04-26 01:57:36.369238
59	drop-unused-functions	38456f13e39691c2bbb4b5151d0d1cdbabd4a8c4	2026-05-07 13:57:39.803975
60	optimize-existing-functions-again	db35e1c91a9201e59f4fef8d972c2f277d68b157	2026-05-07 13:57:39.80905
\.


--
-- Data for Name: objects; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.objects (id, bucket_id, name, owner, created_at, updated_at, last_accessed_at, metadata, version, owner_id, user_metadata) FROM stdin;
\.


--
-- Data for Name: s3_multipart_uploads; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.s3_multipart_uploads (id, in_progress_size, upload_signature, bucket_id, key, version, owner_id, created_at, user_metadata, metadata) FROM stdin;
\.


--
-- Data for Name: s3_multipart_uploads_parts; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.s3_multipart_uploads_parts (id, upload_id, size, part_number, bucket_id, key, etag, owner_id, version, created_at) FROM stdin;
\.


--
-- Data for Name: vector_indexes; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.vector_indexes (id, name, bucket_id, data_type, dimension, distance_metric, metadata_configuration, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: secrets; Type: TABLE DATA; Schema: vault; Owner: supabase_admin
--

COPY vault.secrets (id, name, description, secret, key_id, nonce, created_at, updated_at) FROM stdin;
\.


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: auth; Owner: supabase_auth_admin
--

SELECT pg_catalog.setval('auth.refresh_tokens_id_seq', 1, false);


--
-- Name: associacao_associacao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.associacao_associacao_id_seq', 1, true);


--
-- Name: att_promotor_att_promotor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.att_promotor_att_promotor_id_seq', 1, true);


--
-- Name: att_vendedor_att_vendedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.att_vendedor_att_vendedor_id_seq', 1, true);


--
-- Name: categoria_categoria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categoria_categoria_id_seq', 28, true);


--
-- Name: central_compras_central_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.central_compras_central_id_seq', 1, true);


--
-- Name: cliente_cliente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cliente_cliente_id_seq', 119, true);


--
-- Name: cliente_fornecedor_cliente_fornecedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cliente_fornecedor_cliente_fornecedor_id_seq', 3, true);


--
-- Name: comissao_comissao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.comissao_comissao_id_seq', 4, true);


--
-- Name: comissao_pagamento_pagamento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.comissao_pagamento_pagamento_id_seq', 1, true);


--
-- Name: concorrente_concorrente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.concorrente_concorrente_id_seq', 81, true);


--
-- Name: configuracao_config_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.configuracao_config_id_seq', 1, true);


--
-- Name: contato_cliente_contato_cliente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contato_cliente_contato_cliente_id_seq', 20, true);


--
-- Name: contato_fornecedor_contato_fornecedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contato_fornecedor_contato_fornecedor_id_seq', 1, false);


--
-- Name: contato_fornecedor_topico_cft_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contato_fornecedor_topico_cft_id_seq', 1, false);


--
-- Name: contato_interacao_interacao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contato_interacao_interacao_id_seq', 72, true);


--
-- Name: contato_registro_contato_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contato_registro_contato_id_seq', 32, true);


--
-- Name: contato_x_fornecedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contato_x_fornecedor_id_seq', 53, true);


--
-- Name: fornecedor_fornecedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fornecedor_fornecedor_id_seq', 4, true);


--
-- Name: historico_preco_hist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.historico_preco_hist_id_seq', 705, true);


--
-- Name: interacao_interacao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.interacao_interacao_id_seq', 1, false);


--
-- Name: linha_linha_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.linha_linha_id_seq', 32, true);


--
-- Name: marca_marca_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marca_marca_id_seq', 1, true);


--
-- Name: mensagem_modelo_mensagem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mensagem_modelo_mensagem_id_seq', 3, true);


--
-- Name: meta_fornecedor_meta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.meta_fornecedor_meta_id_seq', 1, true);


--
-- Name: meta_mix_meta_mix_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.meta_mix_meta_mix_id_seq', 2, true);


--
-- Name: mix_cliente_mix_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mix_cliente_mix_id_seq', 39, true);


--
-- Name: negociacao_negociacao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.negociacao_negociacao_id_seq', 1, false);


--
-- Name: pdv_pdv_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pdv_pdv_id_seq', 191, true);


--
-- Name: pedido_historico_historico_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pedido_historico_historico_id_seq', 3, true);


--
-- Name: pedido_item_pedido_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pedido_item_pedido_item_id_seq', 22, true);


--
-- Name: pedido_pedido_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pedido_pedido_id_seq', 4, true);


--
-- Name: pesquisa_foto_foto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pesquisa_foto_foto_id_seq', 16, true);


--
-- Name: pesquisa_preco_item_pesquisa_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pesquisa_preco_item_pesquisa_item_id_seq', 254, true);


--
-- Name: pesquisa_preco_pesquisa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pesquisa_preco_pesquisa_id_seq', 44, true);


--
-- Name: produto_codigo_cliente_produto_codigo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.produto_codigo_cliente_produto_codigo_id_seq', 1, true);


--
-- Name: produto_concorrente_produto_concorrente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.produto_concorrente_produto_concorrente_id_seq', 260, true);


--
-- Name: produto_concorrente_relacao_relacao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.produto_concorrente_relacao_relacao_id_seq', 210, true);


--
-- Name: produto_produto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.produto_produto_id_seq', 387, true);


--
-- Name: promotor_promotor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.promotor_promotor_id_seq', 1, true);


--
-- Name: representante_representante_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.representante_representante_id_seq', 1, true);


--
-- Name: tabela_preco_item_tabela_preco_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tabela_preco_item_tabela_preco_item_id_seq', 953, true);


--
-- Name: tabela_preco_tabela_preco_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tabela_preco_tabela_preco_id_seq', 24, true);


--
-- Name: usuario_usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_usuario_id_seq', 1, true);


--
-- Name: vendedor_vendedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.vendedor_vendedor_id_seq', 1, true);


--
-- Name: visita_cliente_visita_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.visita_cliente_visita_id_seq', 2, true);


--
-- Name: subscription_id_seq; Type: SEQUENCE SET; Schema: realtime; Owner: supabase_admin
--

SELECT pg_catalog.setval('realtime.subscription_id_seq', 1, false);


--
-- Name: mfa_amr_claims amr_id_pk; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_amr_claims
    ADD CONSTRAINT amr_id_pk PRIMARY KEY (id);


--
-- Name: audit_log_entries audit_log_entries_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.audit_log_entries
    ADD CONSTRAINT audit_log_entries_pkey PRIMARY KEY (id);


--
-- Name: custom_oauth_providers custom_oauth_providers_identifier_key; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.custom_oauth_providers
    ADD CONSTRAINT custom_oauth_providers_identifier_key UNIQUE (identifier);


--
-- Name: custom_oauth_providers custom_oauth_providers_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.custom_oauth_providers
    ADD CONSTRAINT custom_oauth_providers_pkey PRIMARY KEY (id);


--
-- Name: flow_state flow_state_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.flow_state
    ADD CONSTRAINT flow_state_pkey PRIMARY KEY (id);


--
-- Name: identities identities_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.identities
    ADD CONSTRAINT identities_pkey PRIMARY KEY (id);


--
-- Name: identities identities_provider_id_provider_unique; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.identities
    ADD CONSTRAINT identities_provider_id_provider_unique UNIQUE (provider_id, provider);


--
-- Name: instances instances_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.instances
    ADD CONSTRAINT instances_pkey PRIMARY KEY (id);


--
-- Name: mfa_amr_claims mfa_amr_claims_session_id_authentication_method_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_amr_claims
    ADD CONSTRAINT mfa_amr_claims_session_id_authentication_method_pkey UNIQUE (session_id, authentication_method);


--
-- Name: mfa_challenges mfa_challenges_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_challenges
    ADD CONSTRAINT mfa_challenges_pkey PRIMARY KEY (id);


--
-- Name: mfa_factors mfa_factors_last_challenged_at_key; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_factors
    ADD CONSTRAINT mfa_factors_last_challenged_at_key UNIQUE (last_challenged_at);


--
-- Name: mfa_factors mfa_factors_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_factors
    ADD CONSTRAINT mfa_factors_pkey PRIMARY KEY (id);


--
-- Name: oauth_authorizations oauth_authorizations_authorization_code_key; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_authorizations
    ADD CONSTRAINT oauth_authorizations_authorization_code_key UNIQUE (authorization_code);


--
-- Name: oauth_authorizations oauth_authorizations_authorization_id_key; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_authorizations
    ADD CONSTRAINT oauth_authorizations_authorization_id_key UNIQUE (authorization_id);


--
-- Name: oauth_authorizations oauth_authorizations_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_authorizations
    ADD CONSTRAINT oauth_authorizations_pkey PRIMARY KEY (id);


--
-- Name: oauth_client_states oauth_client_states_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_client_states
    ADD CONSTRAINT oauth_client_states_pkey PRIMARY KEY (id);


--
-- Name: oauth_clients oauth_clients_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_clients
    ADD CONSTRAINT oauth_clients_pkey PRIMARY KEY (id);


--
-- Name: oauth_consents oauth_consents_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_consents
    ADD CONSTRAINT oauth_consents_pkey PRIMARY KEY (id);


--
-- Name: oauth_consents oauth_consents_user_client_unique; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_consents
    ADD CONSTRAINT oauth_consents_user_client_unique UNIQUE (user_id, client_id);


--
-- Name: one_time_tokens one_time_tokens_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.one_time_tokens
    ADD CONSTRAINT one_time_tokens_pkey PRIMARY KEY (id);


--
-- Name: refresh_tokens refresh_tokens_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.refresh_tokens
    ADD CONSTRAINT refresh_tokens_pkey PRIMARY KEY (id);


--
-- Name: refresh_tokens refresh_tokens_token_unique; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.refresh_tokens
    ADD CONSTRAINT refresh_tokens_token_unique UNIQUE (token);


--
-- Name: saml_providers saml_providers_entity_id_key; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.saml_providers
    ADD CONSTRAINT saml_providers_entity_id_key UNIQUE (entity_id);


--
-- Name: saml_providers saml_providers_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.saml_providers
    ADD CONSTRAINT saml_providers_pkey PRIMARY KEY (id);


--
-- Name: saml_relay_states saml_relay_states_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.saml_relay_states
    ADD CONSTRAINT saml_relay_states_pkey PRIMARY KEY (id);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: sso_domains sso_domains_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.sso_domains
    ADD CONSTRAINT sso_domains_pkey PRIMARY KEY (id);


--
-- Name: sso_providers sso_providers_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.sso_providers
    ADD CONSTRAINT sso_providers_pkey PRIMARY KEY (id);


--
-- Name: users users_phone_key; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.users
    ADD CONSTRAINT users_phone_key UNIQUE (phone);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: webauthn_challenges webauthn_challenges_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.webauthn_challenges
    ADD CONSTRAINT webauthn_challenges_pkey PRIMARY KEY (id);


--
-- Name: webauthn_credentials webauthn_credentials_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.webauthn_credentials
    ADD CONSTRAINT webauthn_credentials_pkey PRIMARY KEY (id);


--
-- Name: associacao associacao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.associacao
    ADD CONSTRAINT associacao_pkey PRIMARY KEY (associacao_id);


--
-- Name: att_promotor att_promotor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.att_promotor
    ADD CONSTRAINT att_promotor_pkey PRIMARY KEY (att_promotor_id);


--
-- Name: att_vendedor att_vendedor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.att_vendedor
    ADD CONSTRAINT att_vendedor_pkey PRIMARY KEY (att_vendedor_id);


--
-- Name: categoria categoria_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categoria
    ADD CONSTRAINT categoria_pkey PRIMARY KEY (categoria_id);


--
-- Name: central_compras central_compras_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.central_compras
    ADD CONSTRAINT central_compras_pkey PRIMARY KEY (central_id);


--
-- Name: cliente_fornecedor cliente_fornecedor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente_fornecedor
    ADD CONSTRAINT cliente_fornecedor_pkey PRIMARY KEY (cliente_fornecedor_id);


--
-- Name: cliente_fornecedor cliente_fornecedor_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente_fornecedor
    ADD CONSTRAINT cliente_fornecedor_unique UNIQUE (cliente_id, fornecedor_id);


--
-- Name: cliente cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (cliente_id);


--
-- Name: comissao comissao_fornecedor_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comissao
    ADD CONSTRAINT comissao_fornecedor_id_key UNIQUE (fornecedor_id);


--
-- Name: comissao_pagamento comissao_pagamento_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comissao_pagamento
    ADD CONSTRAINT comissao_pagamento_pkey PRIMARY KEY (pagamento_id);


--
-- Name: comissao comissao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comissao
    ADD CONSTRAINT comissao_pkey PRIMARY KEY (comissao_id);


--
-- Name: concorrente concorrente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.concorrente
    ADD CONSTRAINT concorrente_pkey PRIMARY KEY (concorrente_id);


--
-- Name: configuracao configuracao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.configuracao
    ADD CONSTRAINT configuracao_pkey PRIMARY KEY (config_id);


--
-- Name: contato_cliente contato_cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contato_cliente
    ADD CONSTRAINT contato_cliente_pkey PRIMARY KEY (contato_cliente_id);


--
-- Name: contato_fornecedor contato_fornecedor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contato_fornecedor
    ADD CONSTRAINT contato_fornecedor_pkey PRIMARY KEY (contato_fornecedor_id);


--
-- Name: contato_fornecedor_topico contato_fornecedor_topico_contato_id_fornecedor_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contato_fornecedor_topico
    ADD CONSTRAINT contato_fornecedor_topico_contato_id_fornecedor_id_key UNIQUE (contato_id, fornecedor_id);


--
-- Name: contato_fornecedor_topico contato_fornecedor_topico_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contato_fornecedor_topico
    ADD CONSTRAINT contato_fornecedor_topico_pkey PRIMARY KEY (cft_id);


--
-- Name: contato_interacao contato_interacao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contato_interacao
    ADD CONSTRAINT contato_interacao_pkey PRIMARY KEY (interacao_id);


--
-- Name: contato_registro contato_registro_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contato_registro
    ADD CONSTRAINT contato_registro_pkey PRIMARY KEY (contato_id);


--
-- Name: contato_x_fornecedor contato_x_forn_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contato_x_fornecedor
    ADD CONSTRAINT contato_x_forn_unique UNIQUE (contato_id, fornecedor_id);


--
-- Name: contato_x_fornecedor contato_x_fornecedor_contato_id_fornecedor_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contato_x_fornecedor
    ADD CONSTRAINT contato_x_fornecedor_contato_id_fornecedor_id_key UNIQUE (contato_id, fornecedor_id);


--
-- Name: contato_x_fornecedor contato_x_fornecedor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contato_x_fornecedor
    ADD CONSTRAINT contato_x_fornecedor_pkey PRIMARY KEY (id);


--
-- Name: fornecedor fornecedor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fornecedor
    ADD CONSTRAINT fornecedor_pkey PRIMARY KEY (fornecedor_id);


--
-- Name: historico_preco historico_preco_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.historico_preco
    ADD CONSTRAINT historico_preco_pkey PRIMARY KEY (hist_id);


--
-- Name: interacao interacao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.interacao
    ADD CONSTRAINT interacao_pkey PRIMARY KEY (interacao_id);


--
-- Name: linha linha_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.linha
    ADD CONSTRAINT linha_pkey PRIMARY KEY (linha_id);


--
-- Name: marca marca_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marca
    ADD CONSTRAINT marca_pkey PRIMARY KEY (marca_id);


--
-- Name: mensagem_modelo mensagem_modelo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mensagem_modelo
    ADD CONSTRAINT mensagem_modelo_pkey PRIMARY KEY (mensagem_id);


--
-- Name: meta_fornecedor meta_fornecedor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meta_fornecedor
    ADD CONSTRAINT meta_fornecedor_pkey PRIMARY KEY (meta_id);


--
-- Name: meta_mix meta_mix_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meta_mix
    ADD CONSTRAINT meta_mix_pkey PRIMARY KEY (meta_mix_id);


--
-- Name: mix_cliente mix_cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mix_cliente
    ADD CONSTRAINT mix_cliente_pkey PRIMARY KEY (mix_id);


--
-- Name: mix_cliente mix_cliente_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mix_cliente
    ADD CONSTRAINT mix_cliente_unique UNIQUE (cliente_id, produto_id, fornecedor_id);


--
-- Name: negociacao negociacao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.negociacao
    ADD CONSTRAINT negociacao_pkey PRIMARY KEY (negociacao_id);


--
-- Name: pdv pdv_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pdv
    ADD CONSTRAINT pdv_pkey PRIMARY KEY (pdv_id);


--
-- Name: pedido_historico pedido_historico_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedido_historico
    ADD CONSTRAINT pedido_historico_pkey PRIMARY KEY (historico_id);


--
-- Name: pedido_item pedido_item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedido_item
    ADD CONSTRAINT pedido_item_pkey PRIMARY KEY (pedido_item_id);


--
-- Name: pedido pedido_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedido
    ADD CONSTRAINT pedido_pkey PRIMARY KEY (pedido_id);


--
-- Name: pesquisa_foto pesquisa_foto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pesquisa_foto
    ADD CONSTRAINT pesquisa_foto_pkey PRIMARY KEY (foto_id);


--
-- Name: pesquisa_preco_item pesquisa_preco_item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pesquisa_preco_item
    ADD CONSTRAINT pesquisa_preco_item_pkey PRIMARY KEY (pesquisa_item_id);


--
-- Name: pesquisa_preco pesquisa_preco_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pesquisa_preco
    ADD CONSTRAINT pesquisa_preco_pkey PRIMARY KEY (pesquisa_id);


--
-- Name: produto_concorrente_relacao prod_conc_rel_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produto_concorrente_relacao
    ADD CONSTRAINT prod_conc_rel_unique UNIQUE (produto_id, produto_concorrente_id);


--
-- Name: produto_codigo_cliente produto_codigo_cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produto_codigo_cliente
    ADD CONSTRAINT produto_codigo_cliente_pkey PRIMARY KEY (produto_codigo_id);


--
-- Name: produto_concorrente produto_concorrente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produto_concorrente
    ADD CONSTRAINT produto_concorrente_pkey PRIMARY KEY (produto_concorrente_id);


--
-- Name: produto_concorrente_relacao produto_concorrente_relacao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produto_concorrente_relacao
    ADD CONSTRAINT produto_concorrente_relacao_pkey PRIMARY KEY (relacao_id);


--
-- Name: produto produto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produto
    ADD CONSTRAINT produto_pkey PRIMARY KEY (produto_id);


--
-- Name: promotor promotor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.promotor
    ADD CONSTRAINT promotor_pkey PRIMARY KEY (promotor_id);


--
-- Name: representante representante_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.representante
    ADD CONSTRAINT representante_pkey PRIMARY KEY (representante_id);


--
-- Name: tabela_preco_item tabela_preco_item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tabela_preco_item
    ADD CONSTRAINT tabela_preco_item_pkey PRIMARY KEY (tabela_preco_item_id);


--
-- Name: tabela_preco tabela_preco_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tabela_preco
    ADD CONSTRAINT tabela_preco_pkey PRIMARY KEY (tabela_preco_id);


--
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (usuario_id);


--
-- Name: vendedor vendedor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vendedor
    ADD CONSTRAINT vendedor_pkey PRIMARY KEY (vendedor_id);


--
-- Name: visita_cliente visita_cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visita_cliente
    ADD CONSTRAINT visita_cliente_pkey PRIMARY KEY (visita_id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: realtime; Owner: supabase_realtime_admin
--

ALTER TABLE ONLY realtime.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id, inserted_at);


--
-- Name: subscription pk_subscription; Type: CONSTRAINT; Schema: realtime; Owner: supabase_admin
--

ALTER TABLE ONLY realtime.subscription
    ADD CONSTRAINT pk_subscription PRIMARY KEY (id);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: realtime; Owner: supabase_admin
--

ALTER TABLE ONLY realtime.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: buckets_analytics buckets_analytics_pkey; Type: CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.buckets_analytics
    ADD CONSTRAINT buckets_analytics_pkey PRIMARY KEY (id);


--
-- Name: buckets buckets_pkey; Type: CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.buckets
    ADD CONSTRAINT buckets_pkey PRIMARY KEY (id);


--
-- Name: buckets_vectors buckets_vectors_pkey; Type: CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.buckets_vectors
    ADD CONSTRAINT buckets_vectors_pkey PRIMARY KEY (id);


--
-- Name: migrations migrations_name_key; Type: CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.migrations
    ADD CONSTRAINT migrations_name_key UNIQUE (name);


--
-- Name: migrations migrations_pkey; Type: CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.migrations
    ADD CONSTRAINT migrations_pkey PRIMARY KEY (id);


--
-- Name: objects objects_pkey; Type: CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.objects
    ADD CONSTRAINT objects_pkey PRIMARY KEY (id);


--
-- Name: s3_multipart_uploads_parts s3_multipart_uploads_parts_pkey; Type: CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.s3_multipart_uploads_parts
    ADD CONSTRAINT s3_multipart_uploads_parts_pkey PRIMARY KEY (id);


--
-- Name: s3_multipart_uploads s3_multipart_uploads_pkey; Type: CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.s3_multipart_uploads
    ADD CONSTRAINT s3_multipart_uploads_pkey PRIMARY KEY (id);


--
-- Name: vector_indexes vector_indexes_pkey; Type: CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.vector_indexes
    ADD CONSTRAINT vector_indexes_pkey PRIMARY KEY (id);


--
-- Name: audit_logs_instance_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX audit_logs_instance_id_idx ON auth.audit_log_entries USING btree (instance_id);


--
-- Name: confirmation_token_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX confirmation_token_idx ON auth.users USING btree (confirmation_token) WHERE ((confirmation_token)::text !~ '^[0-9 ]*$'::text);


--
-- Name: custom_oauth_providers_created_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX custom_oauth_providers_created_at_idx ON auth.custom_oauth_providers USING btree (created_at);


--
-- Name: custom_oauth_providers_enabled_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX custom_oauth_providers_enabled_idx ON auth.custom_oauth_providers USING btree (enabled);


--
-- Name: custom_oauth_providers_identifier_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX custom_oauth_providers_identifier_idx ON auth.custom_oauth_providers USING btree (identifier);


--
-- Name: custom_oauth_providers_provider_type_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX custom_oauth_providers_provider_type_idx ON auth.custom_oauth_providers USING btree (provider_type);


--
-- Name: email_change_token_current_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX email_change_token_current_idx ON auth.users USING btree (email_change_token_current) WHERE ((email_change_token_current)::text !~ '^[0-9 ]*$'::text);


--
-- Name: email_change_token_new_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX email_change_token_new_idx ON auth.users USING btree (email_change_token_new) WHERE ((email_change_token_new)::text !~ '^[0-9 ]*$'::text);


--
-- Name: factor_id_created_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX factor_id_created_at_idx ON auth.mfa_factors USING btree (user_id, created_at);


--
-- Name: flow_state_created_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX flow_state_created_at_idx ON auth.flow_state USING btree (created_at DESC);


--
-- Name: identities_email_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX identities_email_idx ON auth.identities USING btree (email text_pattern_ops);


--
-- Name: INDEX identities_email_idx; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON INDEX auth.identities_email_idx IS 'Auth: Ensures indexed queries on the email column';


--
-- Name: identities_user_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX identities_user_id_idx ON auth.identities USING btree (user_id);


--
-- Name: idx_auth_code; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX idx_auth_code ON auth.flow_state USING btree (auth_code);


--
-- Name: idx_oauth_client_states_created_at; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX idx_oauth_client_states_created_at ON auth.oauth_client_states USING btree (created_at);


--
-- Name: idx_user_id_auth_method; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX idx_user_id_auth_method ON auth.flow_state USING btree (user_id, authentication_method);


--
-- Name: idx_users_created_at_desc; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX idx_users_created_at_desc ON auth.users USING btree (created_at DESC);


--
-- Name: idx_users_email; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX idx_users_email ON auth.users USING btree (email);


--
-- Name: idx_users_last_sign_in_at_desc; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX idx_users_last_sign_in_at_desc ON auth.users USING btree (last_sign_in_at DESC);


--
-- Name: idx_users_name; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX idx_users_name ON auth.users USING btree (((raw_user_meta_data ->> 'name'::text))) WHERE ((raw_user_meta_data ->> 'name'::text) IS NOT NULL);


--
-- Name: mfa_challenge_created_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX mfa_challenge_created_at_idx ON auth.mfa_challenges USING btree (created_at DESC);


--
-- Name: mfa_factors_user_friendly_name_unique; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX mfa_factors_user_friendly_name_unique ON auth.mfa_factors USING btree (friendly_name, user_id) WHERE (TRIM(BOTH FROM friendly_name) <> ''::text);


--
-- Name: mfa_factors_user_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX mfa_factors_user_id_idx ON auth.mfa_factors USING btree (user_id);


--
-- Name: oauth_auth_pending_exp_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX oauth_auth_pending_exp_idx ON auth.oauth_authorizations USING btree (expires_at) WHERE (status = 'pending'::auth.oauth_authorization_status);


--
-- Name: oauth_clients_deleted_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX oauth_clients_deleted_at_idx ON auth.oauth_clients USING btree (deleted_at);


--
-- Name: oauth_consents_active_client_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX oauth_consents_active_client_idx ON auth.oauth_consents USING btree (client_id) WHERE (revoked_at IS NULL);


--
-- Name: oauth_consents_active_user_client_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX oauth_consents_active_user_client_idx ON auth.oauth_consents USING btree (user_id, client_id) WHERE (revoked_at IS NULL);


--
-- Name: oauth_consents_user_order_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX oauth_consents_user_order_idx ON auth.oauth_consents USING btree (user_id, granted_at DESC);


--
-- Name: one_time_tokens_relates_to_hash_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX one_time_tokens_relates_to_hash_idx ON auth.one_time_tokens USING hash (relates_to);


--
-- Name: one_time_tokens_token_hash_hash_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX one_time_tokens_token_hash_hash_idx ON auth.one_time_tokens USING hash (token_hash);


--
-- Name: one_time_tokens_user_id_token_type_key; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX one_time_tokens_user_id_token_type_key ON auth.one_time_tokens USING btree (user_id, token_type);


--
-- Name: reauthentication_token_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX reauthentication_token_idx ON auth.users USING btree (reauthentication_token) WHERE ((reauthentication_token)::text !~ '^[0-9 ]*$'::text);


--
-- Name: recovery_token_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX recovery_token_idx ON auth.users USING btree (recovery_token) WHERE ((recovery_token)::text !~ '^[0-9 ]*$'::text);


--
-- Name: refresh_tokens_instance_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX refresh_tokens_instance_id_idx ON auth.refresh_tokens USING btree (instance_id);


--
-- Name: refresh_tokens_instance_id_user_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX refresh_tokens_instance_id_user_id_idx ON auth.refresh_tokens USING btree (instance_id, user_id);


--
-- Name: refresh_tokens_parent_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX refresh_tokens_parent_idx ON auth.refresh_tokens USING btree (parent);


--
-- Name: refresh_tokens_session_id_revoked_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX refresh_tokens_session_id_revoked_idx ON auth.refresh_tokens USING btree (session_id, revoked);


--
-- Name: refresh_tokens_updated_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX refresh_tokens_updated_at_idx ON auth.refresh_tokens USING btree (updated_at DESC);


--
-- Name: saml_providers_sso_provider_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX saml_providers_sso_provider_id_idx ON auth.saml_providers USING btree (sso_provider_id);


--
-- Name: saml_relay_states_created_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX saml_relay_states_created_at_idx ON auth.saml_relay_states USING btree (created_at DESC);


--
-- Name: saml_relay_states_for_email_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX saml_relay_states_for_email_idx ON auth.saml_relay_states USING btree (for_email);


--
-- Name: saml_relay_states_sso_provider_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX saml_relay_states_sso_provider_id_idx ON auth.saml_relay_states USING btree (sso_provider_id);


--
-- Name: sessions_not_after_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX sessions_not_after_idx ON auth.sessions USING btree (not_after DESC);


--
-- Name: sessions_oauth_client_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX sessions_oauth_client_id_idx ON auth.sessions USING btree (oauth_client_id);


--
-- Name: sessions_user_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX sessions_user_id_idx ON auth.sessions USING btree (user_id);


--
-- Name: sso_domains_domain_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX sso_domains_domain_idx ON auth.sso_domains USING btree (lower(domain));


--
-- Name: sso_domains_sso_provider_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX sso_domains_sso_provider_id_idx ON auth.sso_domains USING btree (sso_provider_id);


--
-- Name: sso_providers_resource_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX sso_providers_resource_id_idx ON auth.sso_providers USING btree (lower(resource_id));


--
-- Name: sso_providers_resource_id_pattern_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX sso_providers_resource_id_pattern_idx ON auth.sso_providers USING btree (resource_id text_pattern_ops);


--
-- Name: unique_phone_factor_per_user; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX unique_phone_factor_per_user ON auth.mfa_factors USING btree (user_id, phone);


--
-- Name: user_id_created_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX user_id_created_at_idx ON auth.sessions USING btree (user_id, created_at);


--
-- Name: users_email_partial_key; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX users_email_partial_key ON auth.users USING btree (email) WHERE (is_sso_user = false);


--
-- Name: INDEX users_email_partial_key; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON INDEX auth.users_email_partial_key IS 'Auth: A partial unique index that applies only when is_sso_user is false';


--
-- Name: users_instance_id_email_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX users_instance_id_email_idx ON auth.users USING btree (instance_id, lower((email)::text));


--
-- Name: users_instance_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX users_instance_id_idx ON auth.users USING btree (instance_id);


--
-- Name: users_is_anonymous_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX users_is_anonymous_idx ON auth.users USING btree (is_anonymous);


--
-- Name: webauthn_challenges_expires_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX webauthn_challenges_expires_at_idx ON auth.webauthn_challenges USING btree (expires_at);


--
-- Name: webauthn_challenges_user_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX webauthn_challenges_user_id_idx ON auth.webauthn_challenges USING btree (user_id);


--
-- Name: webauthn_credentials_credential_id_key; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX webauthn_credentials_credential_id_key ON auth.webauthn_credentials USING btree (credential_id);


--
-- Name: webauthn_credentials_user_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX webauthn_credentials_user_id_idx ON auth.webauthn_credentials USING btree (user_id);


--
-- Name: concorrente_forn_marca_unique; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX concorrente_forn_marca_unique ON public.concorrente USING btree (fornecedor_id, marca_concorrente) WHERE (ativo = 1);


--
-- Name: ix_realtime_subscription_entity; Type: INDEX; Schema: realtime; Owner: supabase_admin
--

CREATE INDEX ix_realtime_subscription_entity ON realtime.subscription USING btree (entity);


--
-- Name: messages_inserted_at_topic_index; Type: INDEX; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE INDEX messages_inserted_at_topic_index ON ONLY realtime.messages USING btree (inserted_at DESC, topic) WHERE ((extension = 'broadcast'::text) AND (private IS TRUE));


--
-- Name: subscription_subscription_id_entity_filters_action_filter_key; Type: INDEX; Schema: realtime; Owner: supabase_admin
--

CREATE UNIQUE INDEX subscription_subscription_id_entity_filters_action_filter_key ON realtime.subscription USING btree (subscription_id, entity, filters, action_filter);


--
-- Name: bname; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE UNIQUE INDEX bname ON storage.buckets USING btree (name);


--
-- Name: bucketid_objname; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE UNIQUE INDEX bucketid_objname ON storage.objects USING btree (bucket_id, name);


--
-- Name: buckets_analytics_unique_name_idx; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE UNIQUE INDEX buckets_analytics_unique_name_idx ON storage.buckets_analytics USING btree (name) WHERE (deleted_at IS NULL);


--
-- Name: idx_multipart_uploads_list; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE INDEX idx_multipart_uploads_list ON storage.s3_multipart_uploads USING btree (bucket_id, key, created_at);


--
-- Name: idx_objects_bucket_id_name; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE INDEX idx_objects_bucket_id_name ON storage.objects USING btree (bucket_id, name COLLATE "C");


--
-- Name: idx_objects_bucket_id_name_lower; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE INDEX idx_objects_bucket_id_name_lower ON storage.objects USING btree (bucket_id, lower(name) COLLATE "C");


--
-- Name: name_prefix_search; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE INDEX name_prefix_search ON storage.objects USING btree (name text_pattern_ops);


--
-- Name: vector_indexes_name_bucket_id_idx; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE UNIQUE INDEX vector_indexes_name_bucket_id_idx ON storage.vector_indexes USING btree (name, bucket_id);


--
-- Name: subscription tr_check_filters; Type: TRIGGER; Schema: realtime; Owner: supabase_admin
--

CREATE TRIGGER tr_check_filters BEFORE INSERT OR UPDATE ON realtime.subscription FOR EACH ROW EXECUTE FUNCTION realtime.subscription_check_filters();


--
-- Name: buckets enforce_bucket_name_length_trigger; Type: TRIGGER; Schema: storage; Owner: supabase_storage_admin
--

CREATE TRIGGER enforce_bucket_name_length_trigger BEFORE INSERT OR UPDATE OF name ON storage.buckets FOR EACH ROW EXECUTE FUNCTION storage.enforce_bucket_name_length();


--
-- Name: buckets protect_buckets_delete; Type: TRIGGER; Schema: storage; Owner: supabase_storage_admin
--

CREATE TRIGGER protect_buckets_delete BEFORE DELETE ON storage.buckets FOR EACH STATEMENT EXECUTE FUNCTION storage.protect_delete();


--
-- Name: objects protect_objects_delete; Type: TRIGGER; Schema: storage; Owner: supabase_storage_admin
--

CREATE TRIGGER protect_objects_delete BEFORE DELETE ON storage.objects FOR EACH STATEMENT EXECUTE FUNCTION storage.protect_delete();


--
-- Name: objects update_objects_updated_at; Type: TRIGGER; Schema: storage; Owner: supabase_storage_admin
--

CREATE TRIGGER update_objects_updated_at BEFORE UPDATE ON storage.objects FOR EACH ROW EXECUTE FUNCTION storage.update_updated_at_column();


--
-- Name: identities identities_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.identities
    ADD CONSTRAINT identities_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: mfa_amr_claims mfa_amr_claims_session_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_amr_claims
    ADD CONSTRAINT mfa_amr_claims_session_id_fkey FOREIGN KEY (session_id) REFERENCES auth.sessions(id) ON DELETE CASCADE;


--
-- Name: mfa_challenges mfa_challenges_auth_factor_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_challenges
    ADD CONSTRAINT mfa_challenges_auth_factor_id_fkey FOREIGN KEY (factor_id) REFERENCES auth.mfa_factors(id) ON DELETE CASCADE;


--
-- Name: mfa_factors mfa_factors_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_factors
    ADD CONSTRAINT mfa_factors_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: oauth_authorizations oauth_authorizations_client_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_authorizations
    ADD CONSTRAINT oauth_authorizations_client_id_fkey FOREIGN KEY (client_id) REFERENCES auth.oauth_clients(id) ON DELETE CASCADE;


--
-- Name: oauth_authorizations oauth_authorizations_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_authorizations
    ADD CONSTRAINT oauth_authorizations_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: oauth_consents oauth_consents_client_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_consents
    ADD CONSTRAINT oauth_consents_client_id_fkey FOREIGN KEY (client_id) REFERENCES auth.oauth_clients(id) ON DELETE CASCADE;


--
-- Name: oauth_consents oauth_consents_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_consents
    ADD CONSTRAINT oauth_consents_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: one_time_tokens one_time_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.one_time_tokens
    ADD CONSTRAINT one_time_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: refresh_tokens refresh_tokens_session_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.refresh_tokens
    ADD CONSTRAINT refresh_tokens_session_id_fkey FOREIGN KEY (session_id) REFERENCES auth.sessions(id) ON DELETE CASCADE;


--
-- Name: saml_providers saml_providers_sso_provider_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.saml_providers
    ADD CONSTRAINT saml_providers_sso_provider_id_fkey FOREIGN KEY (sso_provider_id) REFERENCES auth.sso_providers(id) ON DELETE CASCADE;


--
-- Name: saml_relay_states saml_relay_states_flow_state_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.saml_relay_states
    ADD CONSTRAINT saml_relay_states_flow_state_id_fkey FOREIGN KEY (flow_state_id) REFERENCES auth.flow_state(id) ON DELETE CASCADE;


--
-- Name: saml_relay_states saml_relay_states_sso_provider_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.saml_relay_states
    ADD CONSTRAINT saml_relay_states_sso_provider_id_fkey FOREIGN KEY (sso_provider_id) REFERENCES auth.sso_providers(id) ON DELETE CASCADE;


--
-- Name: sessions sessions_oauth_client_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.sessions
    ADD CONSTRAINT sessions_oauth_client_id_fkey FOREIGN KEY (oauth_client_id) REFERENCES auth.oauth_clients(id) ON DELETE CASCADE;


--
-- Name: sessions sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.sessions
    ADD CONSTRAINT sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: sso_domains sso_domains_sso_provider_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.sso_domains
    ADD CONSTRAINT sso_domains_sso_provider_id_fkey FOREIGN KEY (sso_provider_id) REFERENCES auth.sso_providers(id) ON DELETE CASCADE;


--
-- Name: webauthn_challenges webauthn_challenges_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.webauthn_challenges
    ADD CONSTRAINT webauthn_challenges_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: webauthn_credentials webauthn_credentials_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.webauthn_credentials
    ADD CONSTRAINT webauthn_credentials_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: objects objects_bucketId_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.objects
    ADD CONSTRAINT "objects_bucketId_fkey" FOREIGN KEY (bucket_id) REFERENCES storage.buckets(id);


--
-- Name: s3_multipart_uploads s3_multipart_uploads_bucket_id_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.s3_multipart_uploads
    ADD CONSTRAINT s3_multipart_uploads_bucket_id_fkey FOREIGN KEY (bucket_id) REFERENCES storage.buckets(id);


--
-- Name: s3_multipart_uploads_parts s3_multipart_uploads_parts_bucket_id_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.s3_multipart_uploads_parts
    ADD CONSTRAINT s3_multipart_uploads_parts_bucket_id_fkey FOREIGN KEY (bucket_id) REFERENCES storage.buckets(id);


--
-- Name: s3_multipart_uploads_parts s3_multipart_uploads_parts_upload_id_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.s3_multipart_uploads_parts
    ADD CONSTRAINT s3_multipart_uploads_parts_upload_id_fkey FOREIGN KEY (upload_id) REFERENCES storage.s3_multipart_uploads(id) ON DELETE CASCADE;


--
-- Name: vector_indexes vector_indexes_bucket_id_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.vector_indexes
    ADD CONSTRAINT vector_indexes_bucket_id_fkey FOREIGN KEY (bucket_id) REFERENCES storage.buckets_vectors(id);


--
-- Name: audit_log_entries; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.audit_log_entries ENABLE ROW LEVEL SECURITY;

--
-- Name: flow_state; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.flow_state ENABLE ROW LEVEL SECURITY;

--
-- Name: identities; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.identities ENABLE ROW LEVEL SECURITY;

--
-- Name: instances; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.instances ENABLE ROW LEVEL SECURITY;

--
-- Name: mfa_amr_claims; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.mfa_amr_claims ENABLE ROW LEVEL SECURITY;

--
-- Name: mfa_challenges; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.mfa_challenges ENABLE ROW LEVEL SECURITY;

--
-- Name: mfa_factors; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.mfa_factors ENABLE ROW LEVEL SECURITY;

--
-- Name: one_time_tokens; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.one_time_tokens ENABLE ROW LEVEL SECURITY;

--
-- Name: refresh_tokens; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.refresh_tokens ENABLE ROW LEVEL SECURITY;

--
-- Name: saml_providers; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.saml_providers ENABLE ROW LEVEL SECURITY;

--
-- Name: saml_relay_states; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.saml_relay_states ENABLE ROW LEVEL SECURITY;

--
-- Name: schema_migrations; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.schema_migrations ENABLE ROW LEVEL SECURITY;

--
-- Name: sessions; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.sessions ENABLE ROW LEVEL SECURITY;

--
-- Name: sso_domains; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.sso_domains ENABLE ROW LEVEL SECURITY;

--
-- Name: sso_providers; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.sso_providers ENABLE ROW LEVEL SECURITY;

--
-- Name: users; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.users ENABLE ROW LEVEL SECURITY;

--
-- Name: messages; Type: ROW SECURITY; Schema: realtime; Owner: supabase_realtime_admin
--

ALTER TABLE realtime.messages ENABLE ROW LEVEL SECURITY;

--
-- Name: buckets; Type: ROW SECURITY; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE storage.buckets ENABLE ROW LEVEL SECURITY;

--
-- Name: buckets_analytics; Type: ROW SECURITY; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE storage.buckets_analytics ENABLE ROW LEVEL SECURITY;

--
-- Name: buckets_vectors; Type: ROW SECURITY; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE storage.buckets_vectors ENABLE ROW LEVEL SECURITY;

--
-- Name: migrations; Type: ROW SECURITY; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE storage.migrations ENABLE ROW LEVEL SECURITY;

--
-- Name: objects; Type: ROW SECURITY; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

--
-- Name: s3_multipart_uploads; Type: ROW SECURITY; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE storage.s3_multipart_uploads ENABLE ROW LEVEL SECURITY;

--
-- Name: s3_multipart_uploads_parts; Type: ROW SECURITY; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE storage.s3_multipart_uploads_parts ENABLE ROW LEVEL SECURITY;

--
-- Name: vector_indexes; Type: ROW SECURITY; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE storage.vector_indexes ENABLE ROW LEVEL SECURITY;

--
-- Name: supabase_realtime; Type: PUBLICATION; Schema: -; Owner: postgres
--

CREATE PUBLICATION supabase_realtime WITH (publish = 'insert, update, delete, truncate');


ALTER PUBLICATION supabase_realtime OWNER TO postgres;

--
-- Name: SCHEMA auth; Type: ACL; Schema: -; Owner: supabase_admin
--

GRANT USAGE ON SCHEMA auth TO anon;
GRANT USAGE ON SCHEMA auth TO authenticated;
GRANT USAGE ON SCHEMA auth TO service_role;
GRANT ALL ON SCHEMA auth TO supabase_auth_admin;
GRANT ALL ON SCHEMA auth TO dashboard_user;
GRANT USAGE ON SCHEMA auth TO postgres;


--
-- Name: SCHEMA extensions; Type: ACL; Schema: -; Owner: postgres
--

GRANT USAGE ON SCHEMA extensions TO anon;
GRANT USAGE ON SCHEMA extensions TO authenticated;
GRANT USAGE ON SCHEMA extensions TO service_role;
GRANT ALL ON SCHEMA extensions TO dashboard_user;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT USAGE ON SCHEMA public TO postgres;
GRANT USAGE ON SCHEMA public TO anon;
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT USAGE ON SCHEMA public TO service_role;


--
-- Name: SCHEMA realtime; Type: ACL; Schema: -; Owner: supabase_admin
--

GRANT USAGE ON SCHEMA realtime TO postgres;
GRANT USAGE ON SCHEMA realtime TO anon;
GRANT USAGE ON SCHEMA realtime TO authenticated;
GRANT USAGE ON SCHEMA realtime TO service_role;
GRANT ALL ON SCHEMA realtime TO supabase_realtime_admin;


--
-- Name: SCHEMA storage; Type: ACL; Schema: -; Owner: supabase_admin
--

GRANT USAGE ON SCHEMA storage TO postgres WITH GRANT OPTION;
GRANT USAGE ON SCHEMA storage TO anon;
GRANT USAGE ON SCHEMA storage TO authenticated;
GRANT USAGE ON SCHEMA storage TO service_role;
GRANT ALL ON SCHEMA storage TO supabase_storage_admin WITH GRANT OPTION;
GRANT ALL ON SCHEMA storage TO dashboard_user;


--
-- Name: SCHEMA vault; Type: ACL; Schema: -; Owner: supabase_admin
--

GRANT USAGE ON SCHEMA vault TO postgres WITH GRANT OPTION;
GRANT USAGE ON SCHEMA vault TO service_role;


--
-- Name: FUNCTION email(); Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON FUNCTION auth.email() TO dashboard_user;


--
-- Name: FUNCTION jwt(); Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON FUNCTION auth.jwt() TO postgres;
GRANT ALL ON FUNCTION auth.jwt() TO dashboard_user;


--
-- Name: FUNCTION role(); Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON FUNCTION auth.role() TO dashboard_user;


--
-- Name: FUNCTION uid(); Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON FUNCTION auth.uid() TO dashboard_user;


--
-- Name: FUNCTION armor(bytea); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.armor(bytea) FROM postgres;
GRANT ALL ON FUNCTION extensions.armor(bytea) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.armor(bytea) TO dashboard_user;


--
-- Name: FUNCTION armor(bytea, text[], text[]); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.armor(bytea, text[], text[]) FROM postgres;
GRANT ALL ON FUNCTION extensions.armor(bytea, text[], text[]) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.armor(bytea, text[], text[]) TO dashboard_user;


--
-- Name: FUNCTION crypt(text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.crypt(text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.crypt(text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.crypt(text, text) TO dashboard_user;


--
-- Name: FUNCTION dearmor(text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.dearmor(text) FROM postgres;
GRANT ALL ON FUNCTION extensions.dearmor(text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.dearmor(text) TO dashboard_user;


--
-- Name: FUNCTION decrypt(bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.decrypt(bytea, bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.decrypt(bytea, bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.decrypt(bytea, bytea, text) TO dashboard_user;


--
-- Name: FUNCTION decrypt_iv(bytea, bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.decrypt_iv(bytea, bytea, bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.decrypt_iv(bytea, bytea, bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.decrypt_iv(bytea, bytea, bytea, text) TO dashboard_user;


--
-- Name: FUNCTION digest(bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.digest(bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.digest(bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.digest(bytea, text) TO dashboard_user;


--
-- Name: FUNCTION digest(text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.digest(text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.digest(text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.digest(text, text) TO dashboard_user;


--
-- Name: FUNCTION encrypt(bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.encrypt(bytea, bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.encrypt(bytea, bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.encrypt(bytea, bytea, text) TO dashboard_user;


--
-- Name: FUNCTION encrypt_iv(bytea, bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.encrypt_iv(bytea, bytea, bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.encrypt_iv(bytea, bytea, bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.encrypt_iv(bytea, bytea, bytea, text) TO dashboard_user;


--
-- Name: FUNCTION gen_random_bytes(integer); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.gen_random_bytes(integer) FROM postgres;
GRANT ALL ON FUNCTION extensions.gen_random_bytes(integer) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.gen_random_bytes(integer) TO dashboard_user;


--
-- Name: FUNCTION gen_random_uuid(); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.gen_random_uuid() FROM postgres;
GRANT ALL ON FUNCTION extensions.gen_random_uuid() TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.gen_random_uuid() TO dashboard_user;


--
-- Name: FUNCTION gen_salt(text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.gen_salt(text) FROM postgres;
GRANT ALL ON FUNCTION extensions.gen_salt(text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.gen_salt(text) TO dashboard_user;


--
-- Name: FUNCTION gen_salt(text, integer); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.gen_salt(text, integer) FROM postgres;
GRANT ALL ON FUNCTION extensions.gen_salt(text, integer) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.gen_salt(text, integer) TO dashboard_user;


--
-- Name: FUNCTION grant_pg_cron_access(); Type: ACL; Schema: extensions; Owner: supabase_admin
--

REVOKE ALL ON FUNCTION extensions.grant_pg_cron_access() FROM supabase_admin;
GRANT ALL ON FUNCTION extensions.grant_pg_cron_access() TO supabase_admin WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.grant_pg_cron_access() TO dashboard_user;


--
-- Name: FUNCTION grant_pg_graphql_access(); Type: ACL; Schema: extensions; Owner: supabase_admin
--

GRANT ALL ON FUNCTION extensions.grant_pg_graphql_access() TO postgres WITH GRANT OPTION;


--
-- Name: FUNCTION grant_pg_net_access(); Type: ACL; Schema: extensions; Owner: supabase_admin
--

REVOKE ALL ON FUNCTION extensions.grant_pg_net_access() FROM supabase_admin;
GRANT ALL ON FUNCTION extensions.grant_pg_net_access() TO supabase_admin WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.grant_pg_net_access() TO dashboard_user;


--
-- Name: FUNCTION hmac(bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.hmac(bytea, bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.hmac(bytea, bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.hmac(bytea, bytea, text) TO dashboard_user;


--
-- Name: FUNCTION hmac(text, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.hmac(text, text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.hmac(text, text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.hmac(text, text, text) TO dashboard_user;


--
-- Name: FUNCTION pg_stat_statements(showtext boolean, OUT userid oid, OUT dbid oid, OUT toplevel boolean, OUT queryid bigint, OUT query text, OUT plans bigint, OUT total_plan_time double precision, OUT min_plan_time double precision, OUT max_plan_time double precision, OUT mean_plan_time double precision, OUT stddev_plan_time double precision, OUT calls bigint, OUT total_exec_time double precision, OUT min_exec_time double precision, OUT max_exec_time double precision, OUT mean_exec_time double precision, OUT stddev_exec_time double precision, OUT rows bigint, OUT shared_blks_hit bigint, OUT shared_blks_read bigint, OUT shared_blks_dirtied bigint, OUT shared_blks_written bigint, OUT local_blks_hit bigint, OUT local_blks_read bigint, OUT local_blks_dirtied bigint, OUT local_blks_written bigint, OUT temp_blks_read bigint, OUT temp_blks_written bigint, OUT shared_blk_read_time double precision, OUT shared_blk_write_time double precision, OUT local_blk_read_time double precision, OUT local_blk_write_time double precision, OUT temp_blk_read_time double precision, OUT temp_blk_write_time double precision, OUT wal_records bigint, OUT wal_fpi bigint, OUT wal_bytes numeric, OUT jit_functions bigint, OUT jit_generation_time double precision, OUT jit_inlining_count bigint, OUT jit_inlining_time double precision, OUT jit_optimization_count bigint, OUT jit_optimization_time double precision, OUT jit_emission_count bigint, OUT jit_emission_time double precision, OUT jit_deform_count bigint, OUT jit_deform_time double precision, OUT stats_since timestamp with time zone, OUT minmax_stats_since timestamp with time zone); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pg_stat_statements(showtext boolean, OUT userid oid, OUT dbid oid, OUT toplevel boolean, OUT queryid bigint, OUT query text, OUT plans bigint, OUT total_plan_time double precision, OUT min_plan_time double precision, OUT max_plan_time double precision, OUT mean_plan_time double precision, OUT stddev_plan_time double precision, OUT calls bigint, OUT total_exec_time double precision, OUT min_exec_time double precision, OUT max_exec_time double precision, OUT mean_exec_time double precision, OUT stddev_exec_time double precision, OUT rows bigint, OUT shared_blks_hit bigint, OUT shared_blks_read bigint, OUT shared_blks_dirtied bigint, OUT shared_blks_written bigint, OUT local_blks_hit bigint, OUT local_blks_read bigint, OUT local_blks_dirtied bigint, OUT local_blks_written bigint, OUT temp_blks_read bigint, OUT temp_blks_written bigint, OUT shared_blk_read_time double precision, OUT shared_blk_write_time double precision, OUT local_blk_read_time double precision, OUT local_blk_write_time double precision, OUT temp_blk_read_time double precision, OUT temp_blk_write_time double precision, OUT wal_records bigint, OUT wal_fpi bigint, OUT wal_bytes numeric, OUT jit_functions bigint, OUT jit_generation_time double precision, OUT jit_inlining_count bigint, OUT jit_inlining_time double precision, OUT jit_optimization_count bigint, OUT jit_optimization_time double precision, OUT jit_emission_count bigint, OUT jit_emission_time double precision, OUT jit_deform_count bigint, OUT jit_deform_time double precision, OUT stats_since timestamp with time zone, OUT minmax_stats_since timestamp with time zone) FROM postgres;
GRANT ALL ON FUNCTION extensions.pg_stat_statements(showtext boolean, OUT userid oid, OUT dbid oid, OUT toplevel boolean, OUT queryid bigint, OUT query text, OUT plans bigint, OUT total_plan_time double precision, OUT min_plan_time double precision, OUT max_plan_time double precision, OUT mean_plan_time double precision, OUT stddev_plan_time double precision, OUT calls bigint, OUT total_exec_time double precision, OUT min_exec_time double precision, OUT max_exec_time double precision, OUT mean_exec_time double precision, OUT stddev_exec_time double precision, OUT rows bigint, OUT shared_blks_hit bigint, OUT shared_blks_read bigint, OUT shared_blks_dirtied bigint, OUT shared_blks_written bigint, OUT local_blks_hit bigint, OUT local_blks_read bigint, OUT local_blks_dirtied bigint, OUT local_blks_written bigint, OUT temp_blks_read bigint, OUT temp_blks_written bigint, OUT shared_blk_read_time double precision, OUT shared_blk_write_time double precision, OUT local_blk_read_time double precision, OUT local_blk_write_time double precision, OUT temp_blk_read_time double precision, OUT temp_blk_write_time double precision, OUT wal_records bigint, OUT wal_fpi bigint, OUT wal_bytes numeric, OUT jit_functions bigint, OUT jit_generation_time double precision, OUT jit_inlining_count bigint, OUT jit_inlining_time double precision, OUT jit_optimization_count bigint, OUT jit_optimization_time double precision, OUT jit_emission_count bigint, OUT jit_emission_time double precision, OUT jit_deform_count bigint, OUT jit_deform_time double precision, OUT stats_since timestamp with time zone, OUT minmax_stats_since timestamp with time zone) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pg_stat_statements(showtext boolean, OUT userid oid, OUT dbid oid, OUT toplevel boolean, OUT queryid bigint, OUT query text, OUT plans bigint, OUT total_plan_time double precision, OUT min_plan_time double precision, OUT max_plan_time double precision, OUT mean_plan_time double precision, OUT stddev_plan_time double precision, OUT calls bigint, OUT total_exec_time double precision, OUT min_exec_time double precision, OUT max_exec_time double precision, OUT mean_exec_time double precision, OUT stddev_exec_time double precision, OUT rows bigint, OUT shared_blks_hit bigint, OUT shared_blks_read bigint, OUT shared_blks_dirtied bigint, OUT shared_blks_written bigint, OUT local_blks_hit bigint, OUT local_blks_read bigint, OUT local_blks_dirtied bigint, OUT local_blks_written bigint, OUT temp_blks_read bigint, OUT temp_blks_written bigint, OUT shared_blk_read_time double precision, OUT shared_blk_write_time double precision, OUT local_blk_read_time double precision, OUT local_blk_write_time double precision, OUT temp_blk_read_time double precision, OUT temp_blk_write_time double precision, OUT wal_records bigint, OUT wal_fpi bigint, OUT wal_bytes numeric, OUT jit_functions bigint, OUT jit_generation_time double precision, OUT jit_inlining_count bigint, OUT jit_inlining_time double precision, OUT jit_optimization_count bigint, OUT jit_optimization_time double precision, OUT jit_emission_count bigint, OUT jit_emission_time double precision, OUT jit_deform_count bigint, OUT jit_deform_time double precision, OUT stats_since timestamp with time zone, OUT minmax_stats_since timestamp with time zone) TO dashboard_user;


--
-- Name: FUNCTION pg_stat_statements_info(OUT dealloc bigint, OUT stats_reset timestamp with time zone); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pg_stat_statements_info(OUT dealloc bigint, OUT stats_reset timestamp with time zone) FROM postgres;
GRANT ALL ON FUNCTION extensions.pg_stat_statements_info(OUT dealloc bigint, OUT stats_reset timestamp with time zone) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pg_stat_statements_info(OUT dealloc bigint, OUT stats_reset timestamp with time zone) TO dashboard_user;


--
-- Name: FUNCTION pg_stat_statements_reset(userid oid, dbid oid, queryid bigint, minmax_only boolean); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pg_stat_statements_reset(userid oid, dbid oid, queryid bigint, minmax_only boolean) FROM postgres;
GRANT ALL ON FUNCTION extensions.pg_stat_statements_reset(userid oid, dbid oid, queryid bigint, minmax_only boolean) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pg_stat_statements_reset(userid oid, dbid oid, queryid bigint, minmax_only boolean) TO dashboard_user;


--
-- Name: FUNCTION pgp_armor_headers(text, OUT key text, OUT value text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_armor_headers(text, OUT key text, OUT value text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_armor_headers(text, OUT key text, OUT value text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_armor_headers(text, OUT key text, OUT value text) TO dashboard_user;


--
-- Name: FUNCTION pgp_key_id(bytea); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_key_id(bytea) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_key_id(bytea) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_key_id(bytea) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_decrypt(bytea, bytea); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_decrypt(bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_decrypt(bytea, bytea, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea, text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea, text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea, text, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_decrypt_bytea(bytea, bytea); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_decrypt_bytea(bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_decrypt_bytea(bytea, bytea, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea, text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea, text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea, text, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_encrypt(text, bytea); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_encrypt(text, bytea) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt(text, bytea) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt(text, bytea) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_encrypt(text, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_encrypt(text, bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt(text, bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt(text, bytea, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_encrypt_bytea(bytea, bytea); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_encrypt_bytea(bytea, bytea) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt_bytea(bytea, bytea) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt_bytea(bytea, bytea) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_encrypt_bytea(bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_encrypt_bytea(bytea, bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt_bytea(bytea, bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt_bytea(bytea, bytea, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_sym_decrypt(bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_sym_decrypt(bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt(bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt(bytea, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_sym_decrypt(bytea, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_sym_decrypt(bytea, text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt(bytea, text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt(bytea, text, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_sym_decrypt_bytea(bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_sym_decrypt_bytea(bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt_bytea(bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt_bytea(bytea, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_sym_decrypt_bytea(bytea, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_sym_decrypt_bytea(bytea, text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt_bytea(bytea, text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt_bytea(bytea, text, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_sym_encrypt(text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_sym_encrypt(text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt(text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt(text, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_sym_encrypt(text, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_sym_encrypt(text, text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt(text, text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt(text, text, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_sym_encrypt_bytea(bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_sym_encrypt_bytea(bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt_bytea(bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt_bytea(bytea, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_sym_encrypt_bytea(bytea, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_sym_encrypt_bytea(bytea, text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt_bytea(bytea, text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt_bytea(bytea, text, text) TO dashboard_user;


--
-- Name: FUNCTION pgrst_ddl_watch(); Type: ACL; Schema: extensions; Owner: supabase_admin
--

GRANT ALL ON FUNCTION extensions.pgrst_ddl_watch() TO postgres WITH GRANT OPTION;


--
-- Name: FUNCTION pgrst_drop_watch(); Type: ACL; Schema: extensions; Owner: supabase_admin
--

GRANT ALL ON FUNCTION extensions.pgrst_drop_watch() TO postgres WITH GRANT OPTION;


--
-- Name: FUNCTION set_graphql_placeholder(); Type: ACL; Schema: extensions; Owner: supabase_admin
--

GRANT ALL ON FUNCTION extensions.set_graphql_placeholder() TO postgres WITH GRANT OPTION;


--
-- Name: FUNCTION uuid_generate_v1(); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_generate_v1() FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_generate_v1() TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_generate_v1() TO dashboard_user;


--
-- Name: FUNCTION uuid_generate_v1mc(); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_generate_v1mc() FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_generate_v1mc() TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_generate_v1mc() TO dashboard_user;


--
-- Name: FUNCTION uuid_generate_v3(namespace uuid, name text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_generate_v3(namespace uuid, name text) FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_generate_v3(namespace uuid, name text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_generate_v3(namespace uuid, name text) TO dashboard_user;


--
-- Name: FUNCTION uuid_generate_v4(); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_generate_v4() FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_generate_v4() TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_generate_v4() TO dashboard_user;


--
-- Name: FUNCTION uuid_generate_v5(namespace uuid, name text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_generate_v5(namespace uuid, name text) FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_generate_v5(namespace uuid, name text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_generate_v5(namespace uuid, name text) TO dashboard_user;


--
-- Name: FUNCTION uuid_nil(); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_nil() FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_nil() TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_nil() TO dashboard_user;


--
-- Name: FUNCTION uuid_ns_dns(); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_ns_dns() FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_ns_dns() TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_ns_dns() TO dashboard_user;


--
-- Name: FUNCTION uuid_ns_oid(); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_ns_oid() FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_ns_oid() TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_ns_oid() TO dashboard_user;


--
-- Name: FUNCTION uuid_ns_url(); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_ns_url() FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_ns_url() TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_ns_url() TO dashboard_user;


--
-- Name: FUNCTION uuid_ns_x500(); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_ns_x500() FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_ns_x500() TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_ns_x500() TO dashboard_user;


--
-- Name: FUNCTION graphql("operationName" text, query text, variables jsonb, extensions jsonb); Type: ACL; Schema: graphql_public; Owner: supabase_admin
--

GRANT ALL ON FUNCTION graphql_public.graphql("operationName" text, query text, variables jsonb, extensions jsonb) TO postgres;
GRANT ALL ON FUNCTION graphql_public.graphql("operationName" text, query text, variables jsonb, extensions jsonb) TO anon;
GRANT ALL ON FUNCTION graphql_public.graphql("operationName" text, query text, variables jsonb, extensions jsonb) TO authenticated;
GRANT ALL ON FUNCTION graphql_public.graphql("operationName" text, query text, variables jsonb, extensions jsonb) TO service_role;


--
-- Name: FUNCTION pg_reload_conf(); Type: ACL; Schema: pg_catalog; Owner: supabase_admin
--

GRANT ALL ON FUNCTION pg_catalog.pg_reload_conf() TO postgres WITH GRANT OPTION;


--
-- Name: FUNCTION get_auth(p_usename text); Type: ACL; Schema: pgbouncer; Owner: supabase_admin
--

REVOKE ALL ON FUNCTION pgbouncer.get_auth(p_usename text) FROM PUBLIC;
GRANT ALL ON FUNCTION pgbouncer.get_auth(p_usename text) TO pgbouncer;


--
-- Name: FUNCTION apply_rls(wal jsonb, max_record_bytes integer); Type: ACL; Schema: realtime; Owner: supabase_admin
--

GRANT ALL ON FUNCTION realtime.apply_rls(wal jsonb, max_record_bytes integer) TO postgres;
GRANT ALL ON FUNCTION realtime.apply_rls(wal jsonb, max_record_bytes integer) TO dashboard_user;
GRANT ALL ON FUNCTION realtime.apply_rls(wal jsonb, max_record_bytes integer) TO anon;
GRANT ALL ON FUNCTION realtime.apply_rls(wal jsonb, max_record_bytes integer) TO authenticated;
GRANT ALL ON FUNCTION realtime.apply_rls(wal jsonb, max_record_bytes integer) TO service_role;
GRANT ALL ON FUNCTION realtime.apply_rls(wal jsonb, max_record_bytes integer) TO supabase_realtime_admin;


--
-- Name: FUNCTION broadcast_changes(topic_name text, event_name text, operation text, table_name text, table_schema text, new record, old record, level text); Type: ACL; Schema: realtime; Owner: supabase_admin
--

GRANT ALL ON FUNCTION realtime.broadcast_changes(topic_name text, event_name text, operation text, table_name text, table_schema text, new record, old record, level text) TO postgres;
GRANT ALL ON FUNCTION realtime.broadcast_changes(topic_name text, event_name text, operation text, table_name text, table_schema text, new record, old record, level text) TO dashboard_user;


--
-- Name: FUNCTION build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]); Type: ACL; Schema: realtime; Owner: supabase_admin
--

GRANT ALL ON FUNCTION realtime.build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]) TO postgres;
GRANT ALL ON FUNCTION realtime.build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]) TO dashboard_user;
GRANT ALL ON FUNCTION realtime.build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]) TO anon;
GRANT ALL ON FUNCTION realtime.build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]) TO authenticated;
GRANT ALL ON FUNCTION realtime.build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]) TO service_role;
GRANT ALL ON FUNCTION realtime.build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]) TO supabase_realtime_admin;


--
-- Name: FUNCTION "cast"(val text, type_ regtype); Type: ACL; Schema: realtime; Owner: supabase_admin
--

GRANT ALL ON FUNCTION realtime."cast"(val text, type_ regtype) TO postgres;
GRANT ALL ON FUNCTION realtime."cast"(val text, type_ regtype) TO dashboard_user;
GRANT ALL ON FUNCTION realtime."cast"(val text, type_ regtype) TO anon;
GRANT ALL ON FUNCTION realtime."cast"(val text, type_ regtype) TO authenticated;
GRANT ALL ON FUNCTION realtime."cast"(val text, type_ regtype) TO service_role;
GRANT ALL ON FUNCTION realtime."cast"(val text, type_ regtype) TO supabase_realtime_admin;


--
-- Name: FUNCTION check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text); Type: ACL; Schema: realtime; Owner: supabase_admin
--

GRANT ALL ON FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text) TO postgres;
GRANT ALL ON FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text) TO dashboard_user;
GRANT ALL ON FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text) TO anon;
GRANT ALL ON FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text) TO authenticated;
GRANT ALL ON FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text) TO service_role;
GRANT ALL ON FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text) TO supabase_realtime_admin;


--
-- Name: FUNCTION is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]); Type: ACL; Schema: realtime; Owner: supabase_admin
--

GRANT ALL ON FUNCTION realtime.is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]) TO postgres;
GRANT ALL ON FUNCTION realtime.is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]) TO dashboard_user;
GRANT ALL ON FUNCTION realtime.is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]) TO anon;
GRANT ALL ON FUNCTION realtime.is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]) TO authenticated;
GRANT ALL ON FUNCTION realtime.is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]) TO service_role;
GRANT ALL ON FUNCTION realtime.is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]) TO supabase_realtime_admin;


--
-- Name: FUNCTION list_changes(publication name, slot_name name, max_changes integer, max_record_bytes integer); Type: ACL; Schema: realtime; Owner: supabase_admin
--

GRANT ALL ON FUNCTION realtime.list_changes(publication name, slot_name name, max_changes integer, max_record_bytes integer) TO postgres;
GRANT ALL ON FUNCTION realtime.list_changes(publication name, slot_name name, max_changes integer, max_record_bytes integer) TO dashboard_user;


--
-- Name: FUNCTION quote_wal2json(entity regclass); Type: ACL; Schema: realtime; Owner: supabase_admin
--

GRANT ALL ON FUNCTION realtime.quote_wal2json(entity regclass) TO postgres;
GRANT ALL ON FUNCTION realtime.quote_wal2json(entity regclass) TO dashboard_user;
GRANT ALL ON FUNCTION realtime.quote_wal2json(entity regclass) TO anon;
GRANT ALL ON FUNCTION realtime.quote_wal2json(entity regclass) TO authenticated;
GRANT ALL ON FUNCTION realtime.quote_wal2json(entity regclass) TO service_role;
GRANT ALL ON FUNCTION realtime.quote_wal2json(entity regclass) TO supabase_realtime_admin;


--
-- Name: FUNCTION send(payload jsonb, event text, topic text, private boolean); Type: ACL; Schema: realtime; Owner: supabase_admin
--

GRANT ALL ON FUNCTION realtime.send(payload jsonb, event text, topic text, private boolean) TO postgres;
GRANT ALL ON FUNCTION realtime.send(payload jsonb, event text, topic text, private boolean) TO dashboard_user;


--
-- Name: FUNCTION subscription_check_filters(); Type: ACL; Schema: realtime; Owner: supabase_admin
--

GRANT ALL ON FUNCTION realtime.subscription_check_filters() TO postgres;
GRANT ALL ON FUNCTION realtime.subscription_check_filters() TO dashboard_user;
GRANT ALL ON FUNCTION realtime.subscription_check_filters() TO anon;
GRANT ALL ON FUNCTION realtime.subscription_check_filters() TO authenticated;
GRANT ALL ON FUNCTION realtime.subscription_check_filters() TO service_role;
GRANT ALL ON FUNCTION realtime.subscription_check_filters() TO supabase_realtime_admin;


--
-- Name: FUNCTION to_regrole(role_name text); Type: ACL; Schema: realtime; Owner: supabase_admin
--

GRANT ALL ON FUNCTION realtime.to_regrole(role_name text) TO postgres;
GRANT ALL ON FUNCTION realtime.to_regrole(role_name text) TO dashboard_user;
GRANT ALL ON FUNCTION realtime.to_regrole(role_name text) TO anon;
GRANT ALL ON FUNCTION realtime.to_regrole(role_name text) TO authenticated;
GRANT ALL ON FUNCTION realtime.to_regrole(role_name text) TO service_role;
GRANT ALL ON FUNCTION realtime.to_regrole(role_name text) TO supabase_realtime_admin;


--
-- Name: FUNCTION topic(); Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON FUNCTION realtime.topic() TO postgres;
GRANT ALL ON FUNCTION realtime.topic() TO dashboard_user;


--
-- Name: FUNCTION _crypto_aead_det_decrypt(message bytea, additional bytea, key_id bigint, context bytea, nonce bytea); Type: ACL; Schema: vault; Owner: supabase_admin
--

GRANT ALL ON FUNCTION vault._crypto_aead_det_decrypt(message bytea, additional bytea, key_id bigint, context bytea, nonce bytea) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION vault._crypto_aead_det_decrypt(message bytea, additional bytea, key_id bigint, context bytea, nonce bytea) TO service_role;


--
-- Name: FUNCTION create_secret(new_secret text, new_name text, new_description text, new_key_id uuid); Type: ACL; Schema: vault; Owner: supabase_admin
--

GRANT ALL ON FUNCTION vault.create_secret(new_secret text, new_name text, new_description text, new_key_id uuid) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION vault.create_secret(new_secret text, new_name text, new_description text, new_key_id uuid) TO service_role;


--
-- Name: FUNCTION update_secret(secret_id uuid, new_secret text, new_name text, new_description text, new_key_id uuid); Type: ACL; Schema: vault; Owner: supabase_admin
--

GRANT ALL ON FUNCTION vault.update_secret(secret_id uuid, new_secret text, new_name text, new_description text, new_key_id uuid) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION vault.update_secret(secret_id uuid, new_secret text, new_name text, new_description text, new_key_id uuid) TO service_role;


--
-- Name: TABLE audit_log_entries; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.audit_log_entries TO dashboard_user;
GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.audit_log_entries TO postgres;
GRANT SELECT ON TABLE auth.audit_log_entries TO postgres WITH GRANT OPTION;


--
-- Name: TABLE custom_oauth_providers; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.custom_oauth_providers TO postgres;
GRANT ALL ON TABLE auth.custom_oauth_providers TO dashboard_user;


--
-- Name: TABLE flow_state; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.flow_state TO postgres;
GRANT SELECT ON TABLE auth.flow_state TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.flow_state TO dashboard_user;


--
-- Name: TABLE identities; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.identities TO postgres;
GRANT SELECT ON TABLE auth.identities TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.identities TO dashboard_user;


--
-- Name: TABLE instances; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.instances TO dashboard_user;
GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.instances TO postgres;
GRANT SELECT ON TABLE auth.instances TO postgres WITH GRANT OPTION;


--
-- Name: TABLE mfa_amr_claims; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.mfa_amr_claims TO postgres;
GRANT SELECT ON TABLE auth.mfa_amr_claims TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.mfa_amr_claims TO dashboard_user;


--
-- Name: TABLE mfa_challenges; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.mfa_challenges TO postgres;
GRANT SELECT ON TABLE auth.mfa_challenges TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.mfa_challenges TO dashboard_user;


--
-- Name: TABLE mfa_factors; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.mfa_factors TO postgres;
GRANT SELECT ON TABLE auth.mfa_factors TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.mfa_factors TO dashboard_user;


--
-- Name: TABLE oauth_authorizations; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.oauth_authorizations TO postgres;
GRANT ALL ON TABLE auth.oauth_authorizations TO dashboard_user;


--
-- Name: TABLE oauth_client_states; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.oauth_client_states TO postgres;
GRANT ALL ON TABLE auth.oauth_client_states TO dashboard_user;


--
-- Name: TABLE oauth_clients; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.oauth_clients TO postgres;
GRANT ALL ON TABLE auth.oauth_clients TO dashboard_user;


--
-- Name: TABLE oauth_consents; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.oauth_consents TO postgres;
GRANT ALL ON TABLE auth.oauth_consents TO dashboard_user;


--
-- Name: TABLE one_time_tokens; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.one_time_tokens TO postgres;
GRANT SELECT ON TABLE auth.one_time_tokens TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.one_time_tokens TO dashboard_user;


--
-- Name: TABLE refresh_tokens; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.refresh_tokens TO dashboard_user;
GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.refresh_tokens TO postgres;
GRANT SELECT ON TABLE auth.refresh_tokens TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE refresh_tokens_id_seq; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON SEQUENCE auth.refresh_tokens_id_seq TO dashboard_user;
GRANT ALL ON SEQUENCE auth.refresh_tokens_id_seq TO postgres;


--
-- Name: TABLE saml_providers; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.saml_providers TO postgres;
GRANT SELECT ON TABLE auth.saml_providers TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.saml_providers TO dashboard_user;


--
-- Name: TABLE saml_relay_states; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.saml_relay_states TO postgres;
GRANT SELECT ON TABLE auth.saml_relay_states TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.saml_relay_states TO dashboard_user;


--
-- Name: TABLE schema_migrations; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT SELECT ON TABLE auth.schema_migrations TO postgres WITH GRANT OPTION;


--
-- Name: TABLE sessions; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.sessions TO postgres;
GRANT SELECT ON TABLE auth.sessions TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.sessions TO dashboard_user;


--
-- Name: TABLE sso_domains; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.sso_domains TO postgres;
GRANT SELECT ON TABLE auth.sso_domains TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.sso_domains TO dashboard_user;


--
-- Name: TABLE sso_providers; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.sso_providers TO postgres;
GRANT SELECT ON TABLE auth.sso_providers TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.sso_providers TO dashboard_user;


--
-- Name: TABLE users; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.users TO dashboard_user;
GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.users TO postgres;
GRANT SELECT ON TABLE auth.users TO postgres WITH GRANT OPTION;


--
-- Name: TABLE webauthn_challenges; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.webauthn_challenges TO postgres;
GRANT ALL ON TABLE auth.webauthn_challenges TO dashboard_user;


--
-- Name: TABLE webauthn_credentials; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.webauthn_credentials TO postgres;
GRANT ALL ON TABLE auth.webauthn_credentials TO dashboard_user;


--
-- Name: TABLE pg_stat_statements; Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON TABLE extensions.pg_stat_statements FROM postgres;
GRANT ALL ON TABLE extensions.pg_stat_statements TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE extensions.pg_stat_statements TO dashboard_user;


--
-- Name: TABLE pg_stat_statements_info; Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON TABLE extensions.pg_stat_statements_info FROM postgres;
GRANT ALL ON TABLE extensions.pg_stat_statements_info TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE extensions.pg_stat_statements_info TO dashboard_user;


--
-- Name: TABLE associacao; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.associacao TO anon;
GRANT ALL ON TABLE public.associacao TO authenticated;
GRANT ALL ON TABLE public.associacao TO service_role;


--
-- Name: SEQUENCE associacao_associacao_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.associacao_associacao_id_seq TO anon;
GRANT ALL ON SEQUENCE public.associacao_associacao_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.associacao_associacao_id_seq TO service_role;


--
-- Name: TABLE att_promotor; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.att_promotor TO anon;
GRANT ALL ON TABLE public.att_promotor TO authenticated;
GRANT ALL ON TABLE public.att_promotor TO service_role;


--
-- Name: SEQUENCE att_promotor_att_promotor_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.att_promotor_att_promotor_id_seq TO anon;
GRANT ALL ON SEQUENCE public.att_promotor_att_promotor_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.att_promotor_att_promotor_id_seq TO service_role;


--
-- Name: TABLE att_vendedor; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.att_vendedor TO anon;
GRANT ALL ON TABLE public.att_vendedor TO authenticated;
GRANT ALL ON TABLE public.att_vendedor TO service_role;


--
-- Name: SEQUENCE att_vendedor_att_vendedor_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.att_vendedor_att_vendedor_id_seq TO anon;
GRANT ALL ON SEQUENCE public.att_vendedor_att_vendedor_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.att_vendedor_att_vendedor_id_seq TO service_role;


--
-- Name: TABLE categoria; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.categoria TO anon;
GRANT ALL ON TABLE public.categoria TO authenticated;
GRANT ALL ON TABLE public.categoria TO service_role;


--
-- Name: SEQUENCE categoria_categoria_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.categoria_categoria_id_seq TO anon;
GRANT ALL ON SEQUENCE public.categoria_categoria_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.categoria_categoria_id_seq TO service_role;


--
-- Name: TABLE central_compras; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.central_compras TO anon;
GRANT ALL ON TABLE public.central_compras TO authenticated;
GRANT ALL ON TABLE public.central_compras TO service_role;


--
-- Name: SEQUENCE central_compras_central_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.central_compras_central_id_seq TO anon;
GRANT ALL ON SEQUENCE public.central_compras_central_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.central_compras_central_id_seq TO service_role;


--
-- Name: TABLE cliente; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.cliente TO anon;
GRANT ALL ON TABLE public.cliente TO authenticated;
GRANT ALL ON TABLE public.cliente TO service_role;


--
-- Name: SEQUENCE cliente_cliente_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.cliente_cliente_id_seq TO anon;
GRANT ALL ON SEQUENCE public.cliente_cliente_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.cliente_cliente_id_seq TO service_role;


--
-- Name: TABLE cliente_fornecedor; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.cliente_fornecedor TO anon;
GRANT ALL ON TABLE public.cliente_fornecedor TO authenticated;
GRANT ALL ON TABLE public.cliente_fornecedor TO service_role;


--
-- Name: SEQUENCE cliente_fornecedor_cliente_fornecedor_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.cliente_fornecedor_cliente_fornecedor_id_seq TO anon;
GRANT ALL ON SEQUENCE public.cliente_fornecedor_cliente_fornecedor_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.cliente_fornecedor_cliente_fornecedor_id_seq TO service_role;


--
-- Name: TABLE comissao; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.comissao TO anon;
GRANT ALL ON TABLE public.comissao TO authenticated;
GRANT ALL ON TABLE public.comissao TO service_role;


--
-- Name: SEQUENCE comissao_comissao_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.comissao_comissao_id_seq TO anon;
GRANT ALL ON SEQUENCE public.comissao_comissao_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.comissao_comissao_id_seq TO service_role;


--
-- Name: TABLE comissao_pagamento; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.comissao_pagamento TO anon;
GRANT ALL ON TABLE public.comissao_pagamento TO authenticated;
GRANT ALL ON TABLE public.comissao_pagamento TO service_role;


--
-- Name: SEQUENCE comissao_pagamento_pagamento_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.comissao_pagamento_pagamento_id_seq TO anon;
GRANT ALL ON SEQUENCE public.comissao_pagamento_pagamento_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.comissao_pagamento_pagamento_id_seq TO service_role;


--
-- Name: TABLE concorrente; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.concorrente TO anon;
GRANT ALL ON TABLE public.concorrente TO authenticated;
GRANT ALL ON TABLE public.concorrente TO service_role;


--
-- Name: SEQUENCE concorrente_concorrente_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.concorrente_concorrente_id_seq TO anon;
GRANT ALL ON SEQUENCE public.concorrente_concorrente_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.concorrente_concorrente_id_seq TO service_role;


--
-- Name: TABLE configuracao; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.configuracao TO anon;
GRANT ALL ON TABLE public.configuracao TO authenticated;
GRANT ALL ON TABLE public.configuracao TO service_role;


--
-- Name: SEQUENCE configuracao_config_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.configuracao_config_id_seq TO anon;
GRANT ALL ON SEQUENCE public.configuracao_config_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.configuracao_config_id_seq TO service_role;


--
-- Name: TABLE contato_cliente; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.contato_cliente TO anon;
GRANT ALL ON TABLE public.contato_cliente TO authenticated;
GRANT ALL ON TABLE public.contato_cliente TO service_role;


--
-- Name: SEQUENCE contato_cliente_contato_cliente_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.contato_cliente_contato_cliente_id_seq TO anon;
GRANT ALL ON SEQUENCE public.contato_cliente_contato_cliente_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.contato_cliente_contato_cliente_id_seq TO service_role;


--
-- Name: TABLE contato_fornecedor; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.contato_fornecedor TO anon;
GRANT ALL ON TABLE public.contato_fornecedor TO authenticated;
GRANT ALL ON TABLE public.contato_fornecedor TO service_role;


--
-- Name: SEQUENCE contato_fornecedor_contato_fornecedor_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.contato_fornecedor_contato_fornecedor_id_seq TO anon;
GRANT ALL ON SEQUENCE public.contato_fornecedor_contato_fornecedor_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.contato_fornecedor_contato_fornecedor_id_seq TO service_role;


--
-- Name: TABLE contato_fornecedor_topico; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.contato_fornecedor_topico TO anon;
GRANT ALL ON TABLE public.contato_fornecedor_topico TO authenticated;
GRANT ALL ON TABLE public.contato_fornecedor_topico TO service_role;


--
-- Name: SEQUENCE contato_fornecedor_topico_cft_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.contato_fornecedor_topico_cft_id_seq TO anon;
GRANT ALL ON SEQUENCE public.contato_fornecedor_topico_cft_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.contato_fornecedor_topico_cft_id_seq TO service_role;


--
-- Name: TABLE contato_interacao; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.contato_interacao TO anon;
GRANT ALL ON TABLE public.contato_interacao TO authenticated;
GRANT ALL ON TABLE public.contato_interacao TO service_role;


--
-- Name: SEQUENCE contato_interacao_interacao_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.contato_interacao_interacao_id_seq TO anon;
GRANT ALL ON SEQUENCE public.contato_interacao_interacao_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.contato_interacao_interacao_id_seq TO service_role;


--
-- Name: TABLE contato_registro; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.contato_registro TO anon;
GRANT ALL ON TABLE public.contato_registro TO authenticated;
GRANT ALL ON TABLE public.contato_registro TO service_role;


--
-- Name: SEQUENCE contato_registro_contato_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.contato_registro_contato_id_seq TO anon;
GRANT ALL ON SEQUENCE public.contato_registro_contato_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.contato_registro_contato_id_seq TO service_role;


--
-- Name: TABLE contato_x_fornecedor; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.contato_x_fornecedor TO anon;
GRANT ALL ON TABLE public.contato_x_fornecedor TO authenticated;
GRANT ALL ON TABLE public.contato_x_fornecedor TO service_role;


--
-- Name: SEQUENCE contato_x_fornecedor_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.contato_x_fornecedor_id_seq TO anon;
GRANT ALL ON SEQUENCE public.contato_x_fornecedor_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.contato_x_fornecedor_id_seq TO service_role;


--
-- Name: TABLE fornecedor; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.fornecedor TO anon;
GRANT ALL ON TABLE public.fornecedor TO authenticated;
GRANT ALL ON TABLE public.fornecedor TO service_role;


--
-- Name: SEQUENCE fornecedor_fornecedor_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.fornecedor_fornecedor_id_seq TO anon;
GRANT ALL ON SEQUENCE public.fornecedor_fornecedor_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.fornecedor_fornecedor_id_seq TO service_role;


--
-- Name: TABLE historico_preco; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.historico_preco TO anon;
GRANT ALL ON TABLE public.historico_preco TO authenticated;
GRANT ALL ON TABLE public.historico_preco TO service_role;


--
-- Name: SEQUENCE historico_preco_hist_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.historico_preco_hist_id_seq TO anon;
GRANT ALL ON SEQUENCE public.historico_preco_hist_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.historico_preco_hist_id_seq TO service_role;


--
-- Name: TABLE interacao; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.interacao TO anon;
GRANT ALL ON TABLE public.interacao TO authenticated;
GRANT ALL ON TABLE public.interacao TO service_role;


--
-- Name: SEQUENCE interacao_interacao_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.interacao_interacao_id_seq TO anon;
GRANT ALL ON SEQUENCE public.interacao_interacao_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.interacao_interacao_id_seq TO service_role;


--
-- Name: TABLE linha; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.linha TO anon;
GRANT ALL ON TABLE public.linha TO authenticated;
GRANT ALL ON TABLE public.linha TO service_role;


--
-- Name: SEQUENCE linha_linha_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.linha_linha_id_seq TO anon;
GRANT ALL ON SEQUENCE public.linha_linha_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.linha_linha_id_seq TO service_role;


--
-- Name: TABLE marca; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.marca TO anon;
GRANT ALL ON TABLE public.marca TO authenticated;
GRANT ALL ON TABLE public.marca TO service_role;


--
-- Name: SEQUENCE marca_marca_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.marca_marca_id_seq TO anon;
GRANT ALL ON SEQUENCE public.marca_marca_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.marca_marca_id_seq TO service_role;


--
-- Name: TABLE mensagem_modelo; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.mensagem_modelo TO anon;
GRANT ALL ON TABLE public.mensagem_modelo TO authenticated;
GRANT ALL ON TABLE public.mensagem_modelo TO service_role;


--
-- Name: SEQUENCE mensagem_modelo_mensagem_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.mensagem_modelo_mensagem_id_seq TO anon;
GRANT ALL ON SEQUENCE public.mensagem_modelo_mensagem_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.mensagem_modelo_mensagem_id_seq TO service_role;


--
-- Name: TABLE meta_fornecedor; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.meta_fornecedor TO anon;
GRANT ALL ON TABLE public.meta_fornecedor TO authenticated;
GRANT ALL ON TABLE public.meta_fornecedor TO service_role;


--
-- Name: SEQUENCE meta_fornecedor_meta_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.meta_fornecedor_meta_id_seq TO anon;
GRANT ALL ON SEQUENCE public.meta_fornecedor_meta_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.meta_fornecedor_meta_id_seq TO service_role;


--
-- Name: TABLE meta_mix; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.meta_mix TO anon;
GRANT ALL ON TABLE public.meta_mix TO authenticated;
GRANT ALL ON TABLE public.meta_mix TO service_role;


--
-- Name: SEQUENCE meta_mix_meta_mix_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.meta_mix_meta_mix_id_seq TO anon;
GRANT ALL ON SEQUENCE public.meta_mix_meta_mix_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.meta_mix_meta_mix_id_seq TO service_role;


--
-- Name: TABLE mix_cliente; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.mix_cliente TO anon;
GRANT ALL ON TABLE public.mix_cliente TO authenticated;
GRANT ALL ON TABLE public.mix_cliente TO service_role;


--
-- Name: SEQUENCE mix_cliente_mix_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.mix_cliente_mix_id_seq TO anon;
GRANT ALL ON SEQUENCE public.mix_cliente_mix_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.mix_cliente_mix_id_seq TO service_role;


--
-- Name: TABLE negociacao; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.negociacao TO anon;
GRANT ALL ON TABLE public.negociacao TO authenticated;
GRANT ALL ON TABLE public.negociacao TO service_role;


--
-- Name: SEQUENCE negociacao_negociacao_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.negociacao_negociacao_id_seq TO anon;
GRANT ALL ON SEQUENCE public.negociacao_negociacao_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.negociacao_negociacao_id_seq TO service_role;


--
-- Name: TABLE pdv; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.pdv TO anon;
GRANT ALL ON TABLE public.pdv TO authenticated;
GRANT ALL ON TABLE public.pdv TO service_role;


--
-- Name: SEQUENCE pdv_pdv_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.pdv_pdv_id_seq TO anon;
GRANT ALL ON SEQUENCE public.pdv_pdv_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.pdv_pdv_id_seq TO service_role;


--
-- Name: TABLE pedido; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.pedido TO anon;
GRANT ALL ON TABLE public.pedido TO authenticated;
GRANT ALL ON TABLE public.pedido TO service_role;


--
-- Name: TABLE pedido_historico; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.pedido_historico TO anon;
GRANT ALL ON TABLE public.pedido_historico TO authenticated;
GRANT ALL ON TABLE public.pedido_historico TO service_role;


--
-- Name: SEQUENCE pedido_historico_historico_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.pedido_historico_historico_id_seq TO anon;
GRANT ALL ON SEQUENCE public.pedido_historico_historico_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.pedido_historico_historico_id_seq TO service_role;


--
-- Name: TABLE pedido_item; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.pedido_item TO anon;
GRANT ALL ON TABLE public.pedido_item TO authenticated;
GRANT ALL ON TABLE public.pedido_item TO service_role;


--
-- Name: SEQUENCE pedido_item_pedido_item_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.pedido_item_pedido_item_id_seq TO anon;
GRANT ALL ON SEQUENCE public.pedido_item_pedido_item_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.pedido_item_pedido_item_id_seq TO service_role;


--
-- Name: SEQUENCE pedido_pedido_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.pedido_pedido_id_seq TO anon;
GRANT ALL ON SEQUENCE public.pedido_pedido_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.pedido_pedido_id_seq TO service_role;


--
-- Name: TABLE pesquisa_foto; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.pesquisa_foto TO anon;
GRANT ALL ON TABLE public.pesquisa_foto TO authenticated;
GRANT ALL ON TABLE public.pesquisa_foto TO service_role;


--
-- Name: SEQUENCE pesquisa_foto_foto_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.pesquisa_foto_foto_id_seq TO anon;
GRANT ALL ON SEQUENCE public.pesquisa_foto_foto_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.pesquisa_foto_foto_id_seq TO service_role;


--
-- Name: TABLE pesquisa_preco; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.pesquisa_preco TO anon;
GRANT ALL ON TABLE public.pesquisa_preco TO authenticated;
GRANT ALL ON TABLE public.pesquisa_preco TO service_role;


--
-- Name: TABLE pesquisa_preco_item; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.pesquisa_preco_item TO anon;
GRANT ALL ON TABLE public.pesquisa_preco_item TO authenticated;
GRANT ALL ON TABLE public.pesquisa_preco_item TO service_role;


--
-- Name: SEQUENCE pesquisa_preco_item_pesquisa_item_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.pesquisa_preco_item_pesquisa_item_id_seq TO anon;
GRANT ALL ON SEQUENCE public.pesquisa_preco_item_pesquisa_item_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.pesquisa_preco_item_pesquisa_item_id_seq TO service_role;


--
-- Name: SEQUENCE pesquisa_preco_pesquisa_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.pesquisa_preco_pesquisa_id_seq TO anon;
GRANT ALL ON SEQUENCE public.pesquisa_preco_pesquisa_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.pesquisa_preco_pesquisa_id_seq TO service_role;


--
-- Name: TABLE produto; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.produto TO anon;
GRANT ALL ON TABLE public.produto TO authenticated;
GRANT ALL ON TABLE public.produto TO service_role;


--
-- Name: TABLE produto_codigo_cliente; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.produto_codigo_cliente TO anon;
GRANT ALL ON TABLE public.produto_codigo_cliente TO authenticated;
GRANT ALL ON TABLE public.produto_codigo_cliente TO service_role;


--
-- Name: SEQUENCE produto_codigo_cliente_produto_codigo_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.produto_codigo_cliente_produto_codigo_id_seq TO anon;
GRANT ALL ON SEQUENCE public.produto_codigo_cliente_produto_codigo_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.produto_codigo_cliente_produto_codigo_id_seq TO service_role;


--
-- Name: TABLE produto_concorrente; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.produto_concorrente TO anon;
GRANT ALL ON TABLE public.produto_concorrente TO authenticated;
GRANT ALL ON TABLE public.produto_concorrente TO service_role;


--
-- Name: SEQUENCE produto_concorrente_produto_concorrente_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.produto_concorrente_produto_concorrente_id_seq TO anon;
GRANT ALL ON SEQUENCE public.produto_concorrente_produto_concorrente_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.produto_concorrente_produto_concorrente_id_seq TO service_role;


--
-- Name: TABLE produto_concorrente_relacao; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.produto_concorrente_relacao TO anon;
GRANT ALL ON TABLE public.produto_concorrente_relacao TO authenticated;
GRANT ALL ON TABLE public.produto_concorrente_relacao TO service_role;


--
-- Name: SEQUENCE produto_concorrente_relacao_relacao_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.produto_concorrente_relacao_relacao_id_seq TO anon;
GRANT ALL ON SEQUENCE public.produto_concorrente_relacao_relacao_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.produto_concorrente_relacao_relacao_id_seq TO service_role;


--
-- Name: SEQUENCE produto_produto_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.produto_produto_id_seq TO anon;
GRANT ALL ON SEQUENCE public.produto_produto_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.produto_produto_id_seq TO service_role;


--
-- Name: TABLE promotor; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.promotor TO anon;
GRANT ALL ON TABLE public.promotor TO authenticated;
GRANT ALL ON TABLE public.promotor TO service_role;


--
-- Name: SEQUENCE promotor_promotor_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.promotor_promotor_id_seq TO anon;
GRANT ALL ON SEQUENCE public.promotor_promotor_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.promotor_promotor_id_seq TO service_role;


--
-- Name: TABLE representante; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.representante TO anon;
GRANT ALL ON TABLE public.representante TO authenticated;
GRANT ALL ON TABLE public.representante TO service_role;


--
-- Name: SEQUENCE representante_representante_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.representante_representante_id_seq TO anon;
GRANT ALL ON SEQUENCE public.representante_representante_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.representante_representante_id_seq TO service_role;


--
-- Name: TABLE tabela_preco; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.tabela_preco TO anon;
GRANT ALL ON TABLE public.tabela_preco TO authenticated;
GRANT ALL ON TABLE public.tabela_preco TO service_role;


--
-- Name: TABLE tabela_preco_item; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.tabela_preco_item TO anon;
GRANT ALL ON TABLE public.tabela_preco_item TO authenticated;
GRANT ALL ON TABLE public.tabela_preco_item TO service_role;


--
-- Name: SEQUENCE tabela_preco_item_tabela_preco_item_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.tabela_preco_item_tabela_preco_item_id_seq TO anon;
GRANT ALL ON SEQUENCE public.tabela_preco_item_tabela_preco_item_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.tabela_preco_item_tabela_preco_item_id_seq TO service_role;


--
-- Name: SEQUENCE tabela_preco_tabela_preco_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.tabela_preco_tabela_preco_id_seq TO anon;
GRANT ALL ON SEQUENCE public.tabela_preco_tabela_preco_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.tabela_preco_tabela_preco_id_seq TO service_role;


--
-- Name: TABLE usuario; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.usuario TO anon;
GRANT ALL ON TABLE public.usuario TO authenticated;
GRANT ALL ON TABLE public.usuario TO service_role;


--
-- Name: SEQUENCE usuario_usuario_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.usuario_usuario_id_seq TO anon;
GRANT ALL ON SEQUENCE public.usuario_usuario_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.usuario_usuario_id_seq TO service_role;


--
-- Name: TABLE vendedor; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.vendedor TO anon;
GRANT ALL ON TABLE public.vendedor TO authenticated;
GRANT ALL ON TABLE public.vendedor TO service_role;


--
-- Name: SEQUENCE vendedor_vendedor_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.vendedor_vendedor_id_seq TO anon;
GRANT ALL ON SEQUENCE public.vendedor_vendedor_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.vendedor_vendedor_id_seq TO service_role;


--
-- Name: TABLE visita_cliente; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.visita_cliente TO anon;
GRANT ALL ON TABLE public.visita_cliente TO authenticated;
GRANT ALL ON TABLE public.visita_cliente TO service_role;


--
-- Name: SEQUENCE visita_cliente_visita_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.visita_cliente_visita_id_seq TO anon;
GRANT ALL ON SEQUENCE public.visita_cliente_visita_id_seq TO authenticated;
GRANT ALL ON SEQUENCE public.visita_cliente_visita_id_seq TO service_role;


--
-- Name: TABLE messages; Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON TABLE realtime.messages TO postgres;
GRANT ALL ON TABLE realtime.messages TO dashboard_user;
GRANT SELECT,INSERT,UPDATE ON TABLE realtime.messages TO anon;
GRANT SELECT,INSERT,UPDATE ON TABLE realtime.messages TO authenticated;
GRANT SELECT,INSERT,UPDATE ON TABLE realtime.messages TO service_role;


--
-- Name: TABLE schema_migrations; Type: ACL; Schema: realtime; Owner: supabase_admin
--

GRANT ALL ON TABLE realtime.schema_migrations TO postgres;
GRANT ALL ON TABLE realtime.schema_migrations TO dashboard_user;
GRANT SELECT ON TABLE realtime.schema_migrations TO anon;
GRANT SELECT ON TABLE realtime.schema_migrations TO authenticated;
GRANT SELECT ON TABLE realtime.schema_migrations TO service_role;
GRANT ALL ON TABLE realtime.schema_migrations TO supabase_realtime_admin;


--
-- Name: TABLE subscription; Type: ACL; Schema: realtime; Owner: supabase_admin
--

GRANT ALL ON TABLE realtime.subscription TO postgres;
GRANT ALL ON TABLE realtime.subscription TO dashboard_user;
GRANT SELECT ON TABLE realtime.subscription TO anon;
GRANT SELECT ON TABLE realtime.subscription TO authenticated;
GRANT SELECT ON TABLE realtime.subscription TO service_role;
GRANT ALL ON TABLE realtime.subscription TO supabase_realtime_admin;


--
-- Name: SEQUENCE subscription_id_seq; Type: ACL; Schema: realtime; Owner: supabase_admin
--

GRANT ALL ON SEQUENCE realtime.subscription_id_seq TO postgres;
GRANT ALL ON SEQUENCE realtime.subscription_id_seq TO dashboard_user;
GRANT USAGE ON SEQUENCE realtime.subscription_id_seq TO anon;
GRANT USAGE ON SEQUENCE realtime.subscription_id_seq TO authenticated;
GRANT USAGE ON SEQUENCE realtime.subscription_id_seq TO service_role;
GRANT ALL ON SEQUENCE realtime.subscription_id_seq TO supabase_realtime_admin;


--
-- Name: TABLE buckets; Type: ACL; Schema: storage; Owner: supabase_storage_admin
--

REVOKE ALL ON TABLE storage.buckets FROM supabase_storage_admin;
GRANT ALL ON TABLE storage.buckets TO supabase_storage_admin WITH GRANT OPTION;
GRANT ALL ON TABLE storage.buckets TO service_role;
GRANT ALL ON TABLE storage.buckets TO authenticated;
GRANT ALL ON TABLE storage.buckets TO anon;
GRANT ALL ON TABLE storage.buckets TO postgres WITH GRANT OPTION;


--
-- Name: TABLE buckets_analytics; Type: ACL; Schema: storage; Owner: supabase_storage_admin
--

GRANT ALL ON TABLE storage.buckets_analytics TO service_role;
GRANT ALL ON TABLE storage.buckets_analytics TO authenticated;
GRANT ALL ON TABLE storage.buckets_analytics TO anon;


--
-- Name: TABLE buckets_vectors; Type: ACL; Schema: storage; Owner: supabase_storage_admin
--

GRANT SELECT ON TABLE storage.buckets_vectors TO service_role;
GRANT SELECT ON TABLE storage.buckets_vectors TO authenticated;
GRANT SELECT ON TABLE storage.buckets_vectors TO anon;


--
-- Name: TABLE objects; Type: ACL; Schema: storage; Owner: supabase_storage_admin
--

REVOKE ALL ON TABLE storage.objects FROM supabase_storage_admin;
GRANT ALL ON TABLE storage.objects TO supabase_storage_admin WITH GRANT OPTION;
GRANT ALL ON TABLE storage.objects TO service_role;
GRANT ALL ON TABLE storage.objects TO authenticated;
GRANT ALL ON TABLE storage.objects TO anon;
GRANT ALL ON TABLE storage.objects TO postgres WITH GRANT OPTION;


--
-- Name: TABLE s3_multipart_uploads; Type: ACL; Schema: storage; Owner: supabase_storage_admin
--

GRANT ALL ON TABLE storage.s3_multipart_uploads TO service_role;
GRANT SELECT ON TABLE storage.s3_multipart_uploads TO authenticated;
GRANT SELECT ON TABLE storage.s3_multipart_uploads TO anon;


--
-- Name: TABLE s3_multipart_uploads_parts; Type: ACL; Schema: storage; Owner: supabase_storage_admin
--

GRANT ALL ON TABLE storage.s3_multipart_uploads_parts TO service_role;
GRANT SELECT ON TABLE storage.s3_multipart_uploads_parts TO authenticated;
GRANT SELECT ON TABLE storage.s3_multipart_uploads_parts TO anon;


--
-- Name: TABLE vector_indexes; Type: ACL; Schema: storage; Owner: supabase_storage_admin
--

GRANT SELECT ON TABLE storage.vector_indexes TO service_role;
GRANT SELECT ON TABLE storage.vector_indexes TO authenticated;
GRANT SELECT ON TABLE storage.vector_indexes TO anon;


--
-- Name: TABLE secrets; Type: ACL; Schema: vault; Owner: supabase_admin
--

GRANT SELECT,REFERENCES,DELETE,TRUNCATE ON TABLE vault.secrets TO postgres WITH GRANT OPTION;
GRANT SELECT,DELETE ON TABLE vault.secrets TO service_role;


--
-- Name: TABLE decrypted_secrets; Type: ACL; Schema: vault; Owner: supabase_admin
--

GRANT SELECT,REFERENCES,DELETE,TRUNCATE ON TABLE vault.decrypted_secrets TO postgres WITH GRANT OPTION;
GRANT SELECT,DELETE ON TABLE vault.decrypted_secrets TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: auth; Owner: supabase_auth_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_auth_admin IN SCHEMA auth GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_auth_admin IN SCHEMA auth GRANT ALL ON SEQUENCES TO dashboard_user;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: auth; Owner: supabase_auth_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_auth_admin IN SCHEMA auth GRANT ALL ON FUNCTIONS TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_auth_admin IN SCHEMA auth GRANT ALL ON FUNCTIONS TO dashboard_user;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: auth; Owner: supabase_auth_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_auth_admin IN SCHEMA auth GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_auth_admin IN SCHEMA auth GRANT ALL ON TABLES TO dashboard_user;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: extensions; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA extensions GRANT ALL ON SEQUENCES TO postgres WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: extensions; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA extensions GRANT ALL ON FUNCTIONS TO postgres WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: extensions; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA extensions GRANT ALL ON TABLES TO postgres WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: graphql; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON SEQUENCES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON SEQUENCES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON SEQUENCES TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: graphql; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON FUNCTIONS TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON FUNCTIONS TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON FUNCTIONS TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON FUNCTIONS TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: graphql; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON TABLES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON TABLES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON TABLES TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: graphql_public; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON SEQUENCES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON SEQUENCES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON SEQUENCES TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: graphql_public; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON FUNCTIONS TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON FUNCTIONS TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON FUNCTIONS TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON FUNCTIONS TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: graphql_public; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON TABLES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON TABLES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON TABLES TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON SEQUENCES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON SEQUENCES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON SEQUENCES TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON FUNCTIONS TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON FUNCTIONS TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON FUNCTIONS TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON FUNCTIONS TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: public; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON FUNCTIONS TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON FUNCTIONS TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON FUNCTIONS TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON FUNCTIONS TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON TABLES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON TABLES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON TABLES TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: realtime; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA realtime GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA realtime GRANT ALL ON SEQUENCES TO dashboard_user;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: realtime; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA realtime GRANT ALL ON FUNCTIONS TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA realtime GRANT ALL ON FUNCTIONS TO dashboard_user;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: realtime; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA realtime GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA realtime GRANT ALL ON TABLES TO dashboard_user;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: storage; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON SEQUENCES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON SEQUENCES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON SEQUENCES TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: storage; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON FUNCTIONS TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON FUNCTIONS TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON FUNCTIONS TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON FUNCTIONS TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: storage; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON TABLES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON TABLES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON TABLES TO service_role;


--
-- Name: issue_graphql_placeholder; Type: EVENT TRIGGER; Schema: -; Owner: supabase_admin
--

CREATE EVENT TRIGGER issue_graphql_placeholder ON sql_drop
         WHEN TAG IN ('DROP EXTENSION')
   EXECUTE FUNCTION extensions.set_graphql_placeholder();


ALTER EVENT TRIGGER issue_graphql_placeholder OWNER TO supabase_admin;

--
-- Name: issue_pg_cron_access; Type: EVENT TRIGGER; Schema: -; Owner: supabase_admin
--

CREATE EVENT TRIGGER issue_pg_cron_access ON ddl_command_end
         WHEN TAG IN ('CREATE EXTENSION')
   EXECUTE FUNCTION extensions.grant_pg_cron_access();


ALTER EVENT TRIGGER issue_pg_cron_access OWNER TO supabase_admin;

--
-- Name: issue_pg_graphql_access; Type: EVENT TRIGGER; Schema: -; Owner: supabase_admin
--

CREATE EVENT TRIGGER issue_pg_graphql_access ON ddl_command_end
         WHEN TAG IN ('CREATE FUNCTION')
   EXECUTE FUNCTION extensions.grant_pg_graphql_access();


ALTER EVENT TRIGGER issue_pg_graphql_access OWNER TO supabase_admin;

--
-- Name: issue_pg_net_access; Type: EVENT TRIGGER; Schema: -; Owner: supabase_admin
--

CREATE EVENT TRIGGER issue_pg_net_access ON ddl_command_end
         WHEN TAG IN ('CREATE EXTENSION')
   EXECUTE FUNCTION extensions.grant_pg_net_access();


ALTER EVENT TRIGGER issue_pg_net_access OWNER TO supabase_admin;

--
-- Name: pgrst_ddl_watch; Type: EVENT TRIGGER; Schema: -; Owner: supabase_admin
--

CREATE EVENT TRIGGER pgrst_ddl_watch ON ddl_command_end
   EXECUTE FUNCTION extensions.pgrst_ddl_watch();


ALTER EVENT TRIGGER pgrst_ddl_watch OWNER TO supabase_admin;

--
-- Name: pgrst_drop_watch; Type: EVENT TRIGGER; Schema: -; Owner: supabase_admin
--

CREATE EVENT TRIGGER pgrst_drop_watch ON sql_drop
   EXECUTE FUNCTION extensions.pgrst_drop_watch();


ALTER EVENT TRIGGER pgrst_drop_watch OWNER TO supabase_admin;

--
-- PostgreSQL database dump complete
--

\unrestrict RsYbcl1jXdWZjb35Va0cF4ol0EDu3M29n0p3s2WMjRh7bcTlNtKYbSme3QcMDGL

