# 주제별로 튜닝하기

기본 틀은 하나지만, **몇 군데만 바꾸면 전혀 다른 챗봇**이 됩니다.
아래는 "무엇을 바꾸면 무엇이 달라지는가"를 손대는 순서대로 적은 것입니다.

> 하나 바꾸고 **한 번 써 보고** 다음으로 갑니다. 여러 개를 한꺼번에 바꾸면
> 좋아졌는지 나빠졌는지 알 수 없습니다.

---

## 1. 성격 정하기 — 가장 큰 차이가 나는 곳

**대화마다** 시스템 프롬프트를 따로 줍니다. 화면에서 바로 고칠 수 있어 코드를 안 건드립니다.

- 대화 탭 → 대화 선택 → 위쪽 **시스템 프롬프트** 칸

같은 문서를 물어도 이 한 칸으로 답이 달라집니다.

| 주제 | 이렇게 써 봅니다 |
|---|---|
| 사내 규정 안내 | `너는 우리 회사 규정 안내 담당이야. 반드시 올려둔 문서에 있는 내용으로만 답하고, 문서에 없으면 "규정 문서에 없습니다"라고 말해. 답 끝에 근거가 된 대목을 한 줄 인용해.` |
| 장비 정비 도우미 | `너는 굴착기 정비 보조야. 증상을 들으면 확인할 것을 위험한 것부터 순서대로 알려 줘. 확실하지 않으면 추측하지 말고 무엇을 더 확인해야 하는지 물어봐.` |
| 보고서 초안 | `너는 보고서 작성 보조야. 결론을 먼저 쓰고, 근거를 세 가지로 정리하고, 마지막에 다음에 할 일을 적어. 문장은 짧게.` |
| 신입 교육 | `너는 신입사원 교육 담당이야. 중학생도 이해할 비유를 하나 들고 설명해. 전문 용어를 쓰면 괄호로 뜻을 붙여.` |

**잘 듣는 프롬프트의 공통점 세 가지**

1. **역할**을 준다 — "너는 ○○ 담당이야"
2. **모르는 경우**를 정해 준다 — "문서에 없으면 없다고 말해" ← 지어내는 것을 막는 핵심
3. **형식**을 정해 준다 — "세 줄로", "표로", "근거를 인용해"

자주 쓰는 것은 **프롬프트 탭**에 저장해 두고 새 대화에 붙여 씁니다.

## 2. 모델 바꾸기

`src/features/chat/ChatHeader.tsx` 위쪽:

```ts
openai: ['gpt-4.1-mini', 'gpt-4.1', 'gpt-4o-mini', 'gpt-4o'],
solar:  ['solar-pro2', 'solar-mini'],
```

- **`solar-pro2`** — 한국어 문서에 강합니다. 이 실습의 기본값입니다.
- **`solar-mini`** — 빠르고 쌉니다. 단순 분류·요약에 씁니다.
- 목록에 모델을 더하려면 이 배열에 이름만 넣으면 화면 선택지에 나옵니다.

같은 질문을 **모델만 바꿔 두 번** 던져 보세요. 어디서 차이가 나는지가 보입니다.

## 3. 문서를 어떻게 자를지 — 답의 품질이 여기서 갈립니다

`src/features/documents/chunk.ts`

```ts
const CHUNK_SIZE = 1000      // 조각 하나의 글자 수
const CHUNK_OVERLAP = 150    // 앞 조각과 겹치는 만큼
```

| 바꾸면 | 이렇게 됩니다 |
|---|---|
| 조각을 **작게**(400~600) | 딱 맞는 대목을 잘 찾지만, 앞뒤 맥락이 잘려 답이 단편적이 됩니다 |
| 조각을 **크게**(1500~2000) | 맥락은 살지만 관계없는 내용이 섞여 들어옵니다 |
| 겹침을 **늘리면** | 문장이 조각 경계에서 잘리는 문제가 줄지만 저장량이 늘어납니다 |

**규정·매뉴얼처럼 조항이 짧으면 작게, 서술형 보고서면 크게.** 정답은 없고 문서에 달렸습니다.
바꾼 뒤에는 **문서를 지우고 다시 올려야** 새 기준으로 잘립니다.

## 4. 몇 조각을 참고할지

`supabase/functions/bot-chat/index.ts`

```ts
match_count: 6,      // 질문마다 문서에서 가져올 조각 수
```

- **줄이면**(3~4) 초점이 또렷해지지만 필요한 대목을 놓칠 수 있습니다.
- **늘리면**(8~10) 놓칠 확률은 줄지만 관계없는 내용이 섞이고 느려지고 비용이 듭니다.

고친 뒤에는 **함수를 다시 배포**해야 반영됩니다(Edge Functions → 편집 → Deploy).

## 5. 이름과 첫인상

- `index.html` 의 `<title>` — 브라우저 탭에 뜨는 이름
- `src/features/chat/MessageList.tsx` — 대화가 비었을 때 보이는 안내 문구
- `src/index.css` — 색. 맨 위 색 변수만 바꿔도 분위기가 달라집니다

**주제에 맞는 이름을 붙이는 것만으로 완성도가 올라갑니다.**
「My Chat」보다 「정비 매뉴얼 도우미」가 낫습니다.

---

## 혼자만 쓰게 만들기 (권장)

기본 SQL 은 **누구나 읽고 쓸 수 있게** 열려 있습니다. 실습에는 편하지만,
주소를 아는 사람이 내 대화를 보고 지울 수 있습니다.

**먼저 열려 있다는 것을 직접 확인해 보세요.** 다른 브라우저(시크릿 창)로 내 주소를 열면
내 대화가 그대로 보입니다. 그게 지금 상태입니다.

잠그려면 Supabase **SQL Editor** 에서 아래를 실행합니다.

```sql
-- 로그인한 사람만 쓰게 한다 (비로그인 anon 은 막힌다)
drop policy if exists bot_conversations_all on public.bot_conversations;
create policy bot_conversations_all on public.bot_conversations
  for all to authenticated using (true) with check (true);

drop policy if exists bot_messages_all on public.bot_messages;
create policy bot_messages_all on public.bot_messages
  for all to authenticated using (true) with check (true);

drop policy if exists bot_documents_all on public.bot_documents;
create policy bot_documents_all on public.bot_documents
  for all to authenticated using (true) with check (true);

drop policy if exists bot_document_chunks_all on public.bot_document_chunks;
create policy bot_document_chunks_all on public.bot_document_chunks
  for all to authenticated using (true) with check (true);

drop policy if exists bot_prompts_all on public.bot_prompts;
create policy bot_prompts_all on public.bot_prompts
  for all to authenticated using (true) with check (true);
```

**이것만 하면 앱이 멈춥니다.** 지금 앱에는 로그인 화면이 없어서 아무도 `authenticated` 가
아니기 때문입니다. 그래서 **로그인 붙이기가 다음 과제**가 됩니다 —
Supabase Auth 로 구글 로그인 한 개를 붙이면 됩니다.

> 잠그고 → 멈추는 것을 보고 → 로그인을 붙여 다시 살리는 것,
> 이 순서를 밟아 보는 것이 이 실습에서 가장 남는 부분입니다.

---

## 더 해 볼 것

- **문서마다 태그를 붙이고** 대화에서 그 태그만 검색하게 하기 (`bot_documents` 에 열 추가)
- **답의 근거를 화면에 보여 주기** — 함수가 이미 어떤 조각을 썼는지 돌려줍니다
- **대화 내보내기** — 워드로 내보내는 기능이 이미 들어 있습니다(`exportDocx.ts`). 형식을 바꿔 보세요
- **주제별 시작 질문 3개**를 첫 화면에 버튼으로 두기 — 처음 쓰는 사람이 훨씬 편해집니다
