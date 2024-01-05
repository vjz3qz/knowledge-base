-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- Create user table
CREATE TABLE users (
  id VARCHAR(64) PRIMARY KEY,
  name VARCHAR(100),
  role VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- create component table
CREATE TABLE components (
  id VARCHAR(64) PRIMARY KEY,
  title VARCHAR(100),
  description TEXT,
  location TEXT,
  text_search_vector TSVECTOR
);

-- Create media table
CREATE TABLE media (
  id VARCHAR(64) PRIMARY KEY,
  author VARCHAR(100),
  created_at TIMESTAMP,
  title VARCHAR(100),
  description TEXT,
  component_ids TEXT[],
  image_ids TEXT[],
  video_ids TEXT[],
  document_ids TEXT[],
  text_search_vector TSVECTOR,
  -- FOREIGN KEY (author) REFERENCES users(id)
);

-- Create the tsvector index for the media table
CREATE INDEX media_text_search_vector_idx ON media USING GIN(text_search_vector);

-- Create the trigger function for media table
CREATE OR REPLACE FUNCTION update_media_fts() RETURNS trigger AS $$
BEGIN
  NEW.text_search_vector = to_tsvector('english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.description, ''));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger for INSERT and UPDATE on media table
CREATE TRIGGER media_fts_trigger
BEFORE INSERT OR UPDATE ON media
FOR EACH ROW EXECUTE FUNCTION update_media_fts();

-- Create the tsvector index for the component table
CREATE INDEX component_text_search_vector_idx ON components USING GIN(text_search_vector);

-- Create the trigger function for component table
CREATE OR REPLACE FUNCTION update_component_fts() RETURNS trigger AS $$
BEGIN
  NEW.text_search_vector = to_tsvector('english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.description, '') || ' ' || COALESCE(NEW.location, ''));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger for INSERT and UPDATE on component table
CREATE TRIGGER component_fts_trigger
BEFORE INSERT OR UPDATE ON components
FOR EACH ROW EXECUTE FUNCTION update_component_fts();

-- Create component_media_association table
CREATE TABLE component_media_association (
  component_id VARCHAR(64),
  media_id VARCHAR(64),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (component_id, media_id),
  FOREIGN KEY (component_id) REFERENCES components(id),
  FOREIGN KEY (media_id) REFERENCES media(id)
);

-- Create embedding table
CREATE TABLE embeddings (
  id VARCHAR(64) PRIMARY KEY,
  content TEXT,
  metadata jsonb,
  embedding vector(1536) 
);

-- Create a function to search for content
create function match_embeddings (
  query_embedding vector (1536),
  filter jsonb default '{}'
) returns table (
  id VARCHAR(64),
  content text,
  metadata jsonb,
  similarity float
) language plpgsql as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    1 - (embeddings.embedding <=> query_embedding) as similarity
  from embeddings
  where metadata @> filter
  order by embeddings.embedding <=> query_embedding;
end;
$$;

-- -- Create embedding table
-- CREATE TABLE embeddings (
--   id VARCHAR(64) PRIMARY KEY,
--   content TEXT,
--   media_id VARCHAR(64),
--   file_type VARCHAR(50),
--   file_id VARCHAR(64),
--   embedding vector(1536),
--   FOREIGN KEY (media_id) REFERENCES media(id)
-- );

-- -- Create a function to search for content with column filters
-- CREATE FUNCTION match_embeddings (
--   query_embedding vector(1536),
--   filter jsonb DEFAULT '{}'
-- ) RETURNS TABLE (
--   id VARCHAR(64),
--   content TEXT,
--   media_id VARCHAR(64),
--   file_type VARCHAR(50),
--   file_id VARCHAR(64),

--   similarity FLOAT
-- ) LANGUAGE plpgsql AS $$
-- BEGIN
--   RETURN QUERY
--   SELECT
--     id,
--     content,
--     media_id,
--     file_type,
--     file_id,
--     1 - (embeddings.embedding <=> query_embedding) AS similarity
--   FROM embeddings
--   WHERE media_id IS NOT NULL
--     AND file_type IS NOT NULL
--     AND file_id IS NOT NULL
--     AND embeddings.embedding IS NOT NULL
--     AND media_id <> ''
--     AND file_type <> ''
--     AND file_id <> ''
--     AND media_id = filter->>'media_id'
--     AND file_type = filter->>'file_type'
--     AND file_id = filter->>'file_id'
--   ORDER BY embeddings.embedding <=> query_embedding;
-- END;
-- $$;