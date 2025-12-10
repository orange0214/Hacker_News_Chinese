-- Create a function to search documents by vector similarity
create or replace function match_documents (
  query_embedding vector(1536),
  match_threshold float,
  match_count int,
  filter jsonb default '{}'
)
returns table (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    document_chunks.id,
    document_chunks.content,
    document_chunks.metadata,
    1 - (document_chunks.embedding <=> query_embedding) as similarity
  from document_chunks
  where 1 - (document_chunks.embedding <=> query_embedding) > match_threshold
  and document_chunks.metadata @> filter
  order by document_chunks.embedding <=> query_embedding
  limit match_count;
end;
$$;