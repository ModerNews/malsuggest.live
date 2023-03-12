DROP FUNCTION IF EXISTS clear_stale_cache_function();
CREATE OR REPLACE FUNCTION clear_stale_cache_function() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
        DELETE FROM cache WHERE recorded_at < CURRENT_DATE - interval '1 week';
        RETURN NULL;
END;
    $$;

CREATE TRIGGER clear_stale_cache
    AFTER INSERT ON cache
    EXECUTE FUNCTION clear_stale_cache_function();