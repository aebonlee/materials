-- chatbot-lab (개인 AI 챗봇) 스키마
-- 대표가 Supabase SQL Editor에서 직접 실행 (§3.7 — 이 리포에는 anon 키만 있어 DDL 불가)
-- 재실행 안전: IF NOT EXISTS / DROP POLICY IF EXISTS 선행
--
-- 접근 제어 결정(2026-08-27 대표 확정): 로그인 게이트 없음, 사이트 URL을 비공개로 관리하는 것으로 갈음.
-- ⚠️ 단, anon 키는 dreamitbiz 전 사이트가 공유하는 "공개" 키입니다(§3.2). 이 SQL이 만드는 정책은
--    bot_ 테이블을 anon 역할에 전면 개방하므로, 이 anon 키를 아는 사람은(=어떤 dreamitbiz 사이트든
--    번들을 열어보면 누구나) chatbot-lab 사이트 URL을 몰라도 이 테이블을 REST API로 직접 조회/기록할
--    수 있습니다. 실제 비용이 드는 OpenAI/Solar 호출은 Edge Function 뒤에 있어 안전하지만,
--    대화 기록·프롬프트 라이브러리 자체의 기밀성이 필요해지면 로그인 게이트(§3.3 3종) 추가를 고려할 것.

create extension if not exists vector;

-- 1) 대화방
create table if not exists public.bot_conversations (
  id uuid primary key default gen_random_uuid(),
  title text not null default '새 대화',
  mode text not null default 'general' check (mode in ('general', 'qa', 'summary', 'report')),
  system_prompt text not null default '',
  provider text not null default 'openai' check (provider in ('openai', 'solar')),
  model text not null default 'gpt-4.1-mini',
  use_rag boolean not null default false,
  rag_document_ids uuid[] not null default '{}',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- 2) 메시지
create table if not exists public.bot_messages (
  id uuid primary key default gen_random_uuid(),
  conversation_id uuid not null references public.bot_conversations(id) on delete cascade,
  role text not null check (role in ('user', 'assistant', 'system')),
  content text not null,
  context jsonb,
  created_at timestamptz not null default now()
);

create index if not exists bot_messages_conversation_idx
  on public.bot_messages (conversation_id, created_at);

-- 3) 업로드 문서 (원본 파일은 저장하지 않고, 클라이언트에서 추출한 텍스트만 청크로 보관)
create table if not exists public.bot_documents (
  id uuid primary key default gen_random_uuid(),
  filename text not null,
  file_type text not null check (file_type in ('pdf', 'docx', 'xlsx', 'txt')),
  char_count integer not null default 0,
  chunk_count integer not null default 0,
  status text not null default 'processing' check (status in ('processing', 'ready', 'failed')),
  error_message text,
  created_at timestamptz not null default now()
);

-- 4) 문서 청크 + 임베딩 (OpenAI text-embedding-3-small = 1536차원)
create table if not exists public.bot_document_chunks (
  id uuid primary key default gen_random_uuid(),
  document_id uuid not null references public.bot_documents(id) on delete cascade,
  chunk_index integer not null,
  content text not null,
  embedding vector(1536),
  created_at timestamptz not null default now(),
  unique (document_id, chunk_index)
);

create index if not exists bot_document_chunks_embedding_idx
  on public.bot_document_chunks
  using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);

-- 5) 재사용 프롬프트 라이브러리
create table if not exists public.bot_prompts (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  content text not null,
  category text not null default 'general' check (category in ('general', 'qa', 'summary', 'report', 'custom')),
  is_pinned boolean not null default false,
  usage_count integer not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- updated_at 자동 갱신 트리거 함수 (§3.7 — search_path 고정)
create or replace function public.bot_set_updated_at()
returns trigger
language plpgsql
set search_path = public
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists bot_conversations_set_updated_at on public.bot_conversations;
create trigger bot_conversations_set_updated_at
  before update on public.bot_conversations
  for each row execute function public.bot_set_updated_at();

drop trigger if exists bot_prompts_set_updated_at on public.bot_prompts;
create trigger bot_prompts_set_updated_at
  before update on public.bot_prompts
  for each row execute function public.bot_set_updated_at();

-- 벡터 유사도 검색 RPC (Edge Function이 service role로 호출)
create or replace function public.bot_match_chunks(
  query_embedding vector(1536),
  match_count integer default 6,
  doc_ids uuid[] default null
)
returns table (
  id uuid,
  document_id uuid,
  chunk_index integer,
  content text,
  similarity float
)
language sql
stable
set search_path = public
as $$
  select
    c.id,
    c.document_id,
    c.chunk_index,
    c.content,
    1 - (c.embedding <=> query_embedding) as similarity
  from public.bot_document_chunks c
  where c.embedding is not null
    and (doc_ids is null or array_length(doc_ids, 1) is null or c.document_id = any(doc_ids))
  order by c.embedding <=> query_embedding
  limit greatest(match_count, 1);
$$;

-- RLS: 로그인 게이트가 없으므로 anon에게 전면 개방 (위 경고 참고)
alter table public.bot_conversations enable row level security;
alter table public.bot_messages enable row level security;
alter table public.bot_documents enable row level security;
alter table public.bot_document_chunks enable row level security;
alter table public.bot_prompts enable row level security;

drop policy if exists bot_conversations_all on public.bot_conversations;
create policy bot_conversations_all on public.bot_conversations
  for all to anon, authenticated using (true) with check (true);

drop policy if exists bot_messages_all on public.bot_messages;
create policy bot_messages_all on public.bot_messages
  for all to anon, authenticated using (true) with check (true);

drop policy if exists bot_documents_all on public.bot_documents;
create policy bot_documents_all on public.bot_documents
  for all to anon, authenticated using (true) with check (true);

drop policy if exists bot_document_chunks_all on public.bot_document_chunks;
create policy bot_document_chunks_all on public.bot_document_chunks
  for all to anon, authenticated using (true) with check (true);

drop policy if exists bot_prompts_all on public.bot_prompts;
create policy bot_prompts_all on public.bot_prompts
  for all to anon, authenticated using (true) with check (true);

-- match 함수는 RLS 정책 평가용이 아니라 앱이 직접 호출하는 함수라 anon EXECUTE 유지(§3.7 표의 "판정 함수"와는 다른 케이스지만 동일 취지)
grant execute on function public.bot_match_chunks(vector, integer, uuid[]) to anon, authenticated;

-- 기본 프롬프트 4종 시드 (이미 있으면 건너뜀)
insert into public.bot_prompts (title, content, category, is_pinned)
select * from (values
  ('일반 대화', '너는 이애본 대표의 개인 업무 비서야. 간결하고 정확하게, 필요하면 단계별로 답해줘.', 'general', true),
  ('문서 기반 Q&A', '아래 제공되는 문서 발췌를 근거로만 답변해. 근거가 없으면 "문서에서 확인되지 않음"이라고 명시하고, 답변 끝에 참고한 문서/청크 번호를 표기해줘.', 'qa', true),
  ('문서 요약', '제공된 문서(또는 대화 내용)를 핵심 위주로 요약해줘. 목차형 소제목 + 불릿으로 구성하고, 마지막에 3줄 총평을 붙여줘.', 'summary', true),
  ('보고서 작성', '제공된 자료를 바탕으로 보고서 초안을 작성해줘. 구성: 1) 개요 2) 주요 내용(소제목별) 3) 시사점/제안 4) 결론. 문어체·개조식 혼용, 근거 없는 수치는 만들어내지 마.', 'report', true)
) as v(title, content, category, is_pinned)
where not exists (select 1 from public.bot_prompts p where p.title = v.title);
