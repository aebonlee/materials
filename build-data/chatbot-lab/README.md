# 나만의 AI 챗봇 만들기 (실습 패키지)

문서를 읽고 답하는 **RAG 챗봇**을 각자 하나씩 만들어 배포합니다.
다 만들면 `https://<내아이디>.github.io/<저장소이름>/` 주소가 생기고, 그 주소로 누구나 씁니다.

**걸리는 시간: 2~4시간.** 설치할 프로그램은 없습니다 — 브라우저와 깃허브 계정만 있으면 됩니다.

## 무엇을 만드나

| 탭 | 하는 일 |
|---|---|
| 대화 | 주제를 정해 대화합니다. 대화마다 성격(시스템 프롬프트)·모델을 따로 줍니다 |
| 문서 | PDF·워드·엑셀을 올리면 잘라서 저장하고, 대화할 때 관련 대목을 찾아 씁니다 |
| 프롬프트 | 자주 쓰는 지시문을 모아 둡니다 |

만든 뒤 **주제별로 튜닝**하는 것이 이 실습의 목적입니다 — [`TUNING.md`](./TUNING.md) 를 보세요.

## 구조 — 왜 이렇게 나뉘어 있나

```
브라우저(내 화면)  →  Supabase Edge Function  →  Solar · OpenAI · Claude · Gemini
        ↕                      ↕
   내 Supabase 데이터베이스 (대화·문서)
```

**API 키는 브라우저에 두지 않습니다.** 브라우저에 두면 누구나 개발자도구로 꺼내 갑니다.
키는 Supabase 함수 안(서버)에만 두고, 브라우저는 그 함수를 부르기만 합니다.
**이 구조가 오늘 배우는 것 중 가장 중요한 부분입니다.**

---

# 만드는 순서

## 1단계 — 내 저장소 만들기 (10분)

1. 깃허브에서 새 저장소를 만듭니다. 이름은 자유입니다(예: `my-chatbot`).
   **Public 으로 만듭니다** — GitHub Pages 로 배포하려면 그게 간단합니다.
2. 받은 실습 파일을 그 저장소에 올립니다.
   - 웹에서 올릴 때는 **Add file → Upload files** 에 폴더째 끌어다 놓으면 됩니다.
3. `vite.config.ts` 를 열어 **저장소 이름으로 한 줄** 고칩니다.

   ```ts
   base: '/my-chatbot/',      // ← 내 저장소 이름
   ```

   > 이 줄이 틀리면 **화면이 하얗게** 뜹니다. 가장 많이 나오는 실수입니다.

## 2단계 — Supabase 프로젝트 만들기 (15분)

1. <https://supabase.com> 가입 → **New project**
   - 이름은 자유, 리전은 **Northeast Asia (Seoul)** 을 고르면 빠릅니다.
   - 데이터베이스 비밀번호는 적어 두세요(뒤에서 쓸 일은 없지만 분실하면 곤란합니다).
2. 프로젝트가 만들어지면 **Settings → API** 에서 두 값을 복사해 둡니다.
   - **Project URL**
   - **anon public** 키

> `anon` 키는 공개돼도 되는 키입니다. 브라우저에 들어갑니다.
> 옆에 있는 `service_role` 키는 **절대** 쓰지 않습니다 — 그건 모든 잠금을 여는 열쇠입니다.

## 3단계 — 표 만들기 (10분)

1. 왼쪽 메뉴 **SQL Editor** → **New query**
2. `supabase/sql/schema.sql` 파일을 통째로 복사해 붙여 넣고 **Run**
3. `Success` 가 뜨면 됩니다. **Table Editor** 에 표 다섯 개가 보입니다.

| 표 | 담는 것 |
|---|---|
| `bot_conversations` | 대화 목록 |
| `bot_messages` | 주고받은 말 |
| `bot_documents` | 올린 문서 |
| `bot_document_chunks` | 문서를 잘라 놓은 조각 + 임베딩 |
| `bot_prompts` | 저장해 둔 지시문 |

> 이 SQL 은 **여러 번 실행해도 안전**하게 쓰여 있습니다. 중간에 막히면 다시 돌려도 됩니다.

## 4단계 — 함수 두 개 올리기 (20분)

여기가 **키를 감추는 자리**입니다. 설치할 것 없이 브라우저에서 합니다.

1. 왼쪽 메뉴 **Edge Functions** → **Deploy a new function** → **Via Editor**
2. 이름을 **`bot-chat`** 으로 하고, `supabase/functions/bot-chat/index.ts` 내용을
   통째로 붙여 넣습니다 → **Deploy**
3. 같은 방법으로 **`bot-embed`** 도 올립니다 (`supabase/functions/bot-embed/index.ts`)

**이름을 정확히 그대로** 써야 합니다. 앱이 그 이름으로 부릅니다.

## 5단계 — 키를 함수에 넣기 (15분)

Supabase → **Edge Functions → Secrets** 에 넣습니다. **쓸 것만 넣으면 됩니다 — 넷 다 필요 없습니다.**

| Secrets 이름 | 키 받는 곳 | 언제 쓰나 |
|---|---|---|
| `SOLAR_API_KEY` | <https://console.upstage.ai> → API Keys | 한국어에 강함. **하나만 넣는다면 이것** |
| `OPENAI_API_KEY` | <https://platform.openai.com/api-keys> | **문서 검색(RAG)의 임베딩이 이 키를 씁니다** — 문서 탭을 쓰려면 필요 |
| `ANTHROPIC_API_KEY` | <https://console.anthropic.com/settings/keys> | Claude. 긴 글·꼼꼼한 지시 이행에 강함 |
| `GEMINI_API_KEY` | <https://aistudio.google.com/apikey> | 무료 구간이 있어 부담이 적음 |
| `BOT_CLIENT_TOKEN` | 직접 정함 | 아무 긴 문자열 하나 (예: `mybot-2026-abcdef`) |

대화 화면 위에서 **서비스와 모델을 골라** 대화마다 다르게 씁니다.
키가 없는 서비스를 고르면 **어느 키가 없는지 알려 주고 멈춥니다.**

> **모델 키는 여기에만 넣습니다.** 프런트엔드(.env)에 넣으면
> 빌드 결과에 그대로 남아 누구나 꺼내 갑니다.

## 6단계 — 앱에 내 프로젝트 알려 주기 (10분)

`.env.example` 을 복사해 `.env` 를 만들고 채웁니다.

```
VITE_SUPABASE_URL=https://내프로젝트.supabase.co
VITE_SUPABASE_ANON_KEY=(2단계에서 복사한 anon 키)
VITE_BOT_CLIENT_TOKEN=(5단계에서 정한 그 문자열과 똑같이)
```

**`BOT_CLIENT_TOKEN` 은 5단계 값과 글자 하나까지 같아야 합니다.** 다르면 함수가 거절합니다.

## 7단계 — 배포하기 (20분)

깃허브 저장소에서:

1. **Settings → Secrets and variables → Actions** 에 세 개를 등록합니다.
   `VITE_SUPABASE_URL` · `VITE_SUPABASE_ANON_KEY` · `VITE_BOT_CLIENT_TOKEN`
   (`.env` 는 깃허브에 안 올라가므로 빌드할 때 여기서 읽습니다)
2. `.github/workflows/deploy.yml` 이 이미 들어 있습니다. `main` 에 올리면 자동으로 빌드·배포됩니다.
3. **Settings → Pages** 에서 Source 가 **gh-pages** 브랜치인지 확인합니다.

몇 분 뒤 `https://<내아이디>.github.io/<저장소이름>/` 이 열립니다.

> 앱을 띄운 뒤에는 **「설정 방법」 탭**에 이 안내가 그대로 들어 있습니다.
> 실습 중에는 문서를 찾지 말고 그 탭을 보면 됩니다.

## 8단계 — 확인 (10분)

1. 대화 탭에서 **새 대화** → 아무거나 물어봅니다. 답이 오면 4·5단계가 맞은 것입니다.
2. 문서 탭에서 PDF 를 하나 올립니다. 조각 수가 표시되면 임베딩이 된 것입니다.
3. 그 문서를 켜고 문서 내용을 물어봅니다. **문서에 있는 말로 답하면 RAG 가 도는 것입니다.**

---

# 막혔을 때

| 증상 | 원인 |
|---|---|
| 화면이 하얗다 | `vite.config.ts` 의 `base` 가 저장소 이름과 다르다 (1단계) |
| "Supabase 설정이 없습니다" | `.env` 또는 깃허브 Actions Secrets 가 비었다 (6·7단계) |
| 답이 안 오고 401/403 | `BOT_CLIENT_TOKEN` 이 양쪽에서 다르다 (5·6단계) |
| 답이 안 오고 500 / "…KEY 가 서버에 없습니다" | 고른 서비스의 키를 Secrets 에 안 넣었다 (5단계) |
| 대화는 되는데 문서 답이 엉뚱하다 | 문서를 켜지 않았거나 조각이 안 만들어졌다 (8단계 2번) |
| 표가 없다고 나온다 | 3단계 SQL 을 안 돌렸다 |

**함수 쪽 오류는 Supabase → Edge Functions → 해당 함수 → Logs 에서 봅니다.**
어느 줄에서 멈췄는지 그대로 나옵니다.

---

# 알아 둘 것 — 이 앱은 로그인이 없습니다

`schema.sql` 은 **누구나 읽고 쓸 수 있게** 열려 있습니다. 주소를 아는 사람은
내 대화를 보고 지울 수도 있습니다. 실습에는 그게 편하지만, 실제로 쓰려면 잠가야 합니다.

**잠그는 방법**은 [`TUNING.md`](./TUNING.md) 의 「혼자만 쓰게 만들기」에 있습니다.
잠그는 것 자체가 좋은 실습입니다 — 열려 있을 때와 잠갔을 때를 직접 확인해 보세요.
