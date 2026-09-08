// 앱 안에서 바로 보는 설정 안내. 실습 중에 문서를 따로 찾지 않아도 되게 화면에 둔다.
// 값은 아무것도 저장하지 않는다 — 읽기 전용 안내다.

type KeyInfo = {
  name: string
  secret: string
  where: string
  url: string
  note: string
}

const KEYS: KeyInfo[] = [
  {
    name: 'Solar (업스테이지)',
    secret: 'SOLAR_API_KEY',
    where: 'console.upstage.ai → API Keys',
    url: 'https://console.upstage.ai',
    note: '한국어 문서에 강합니다. 이 실습의 기본값이라 하나만 넣는다면 이것을 권합니다.',
  },
  {
    name: 'OpenAI',
    secret: 'OPENAI_API_KEY',
    where: 'platform.openai.com → API keys',
    url: 'https://platform.openai.com/api-keys',
    note: '문서 검색(RAG)에 쓰는 임베딩이 이 키를 씁니다. 문서 탭을 쓰려면 이 키가 있어야 합니다.',
  },
  {
    name: 'Claude (Anthropic)',
    secret: 'ANTHROPIC_API_KEY',
    where: 'console.anthropic.com → API keys',
    url: 'https://console.anthropic.com/settings/keys',
    note: '긴 글을 다루거나 지시를 꼼꼼히 따라야 할 때 좋습니다. 비싼 모델이니 실습에는 haiku 로 시작해 보세요.',
  },
  {
    name: 'Gemini (Google)',
    secret: 'GEMINI_API_KEY',
    where: 'aistudio.google.com → API keys',
    url: 'https://aistudio.google.com/apikey',
    note: '무료 사용 구간이 있어 부담이 적습니다. 이미지·긴 문서에 강합니다.',
  },
]

const STEPS: { title: string; body: React.ReactNode }[] = [
  {
    title: '1. Supabase 프로젝트 만들기',
    body: (
      <>
        <a href="https://supabase.com" target="_blank" rel="noreferrer">
          supabase.com
        </a>{' '}
        → New project. 리전은 <b>Northeast Asia (Seoul)</b> 이 빠릅니다.
        <br />
        만들어지면 <b>Settings → API</b> 에서 <code>Project URL</code> 과 <code>anon public</code> 키를 복사해 둡니다.
        <br />
        <b>옆에 있는 service_role 키는 절대 쓰지 않습니다</b> — 모든 잠금을 여는 열쇠입니다.
      </>
    ),
  },
  {
    title: '2. 표 만들기',
    body: (
      <>
        <b>SQL Editor → New query</b> 에 <code>supabase/sql/schema.sql</code> 을 통째로 붙여 넣고 Run.
        <br />
        <b>Table Editor</b> 에 표가 다섯 개 보이면 된 것입니다. 여러 번 실행해도 안전합니다.
      </>
    ),
  },
  {
    title: '3. 함수 두 개 올리기',
    body: (
      <>
        <b>Edge Functions → Deploy a new function → Via Editor</b>
        <br />
        이름을 <code>bot-chat</code> 으로 하고 <code>supabase/functions/bot-chat/index.ts</code> 를 붙여 넣습니다.
        같은 방법으로 <code>bot-embed</code> 도 올립니다.
        <br />
        <b>이름을 정확히 그대로</b> 써야 합니다 — 앱이 그 이름으로 부릅니다. 설치할 프로그램은 없습니다.
      </>
    ),
  },
  {
    title: '4. 키를 함수에 넣기',
    body: (
      <>
        <b>Edge Functions → Secrets</b> 에 아래 표의 이름 그대로 넣습니다.
        <br />
        여기에 넣은 값은 <b>서버 안에만</b> 있고 브라우저로 내려가지 않습니다.
        <br />
        <b>넷 다 넣을 필요 없습니다</b> — 쓸 것만 넣으면 됩니다.
      </>
    ),
  },
  {
    title: '5. 앱에 내 프로젝트 알려 주기',
    body: (
      <>
        <code>.env.example</code> 을 복사해 <code>.env</code> 를 만들고 1번에서 복사한 두 값을 넣습니다.
        <br />
        <code>VITE_BOT_CLIENT_TOKEN</code> 은 아무 긴 문자열이나 정하고, Secrets 의{' '}
        <code>BOT_CLIENT_TOKEN</code> 과 <b>글자 하나까지 같게</b> 맞춥니다.
        <br />
        깃허브로 배포할 때는 같은 세 값을 <b>Settings → Secrets and variables → Actions</b> 에도 등록합니다.
      </>
    ),
  },
]

export function SetupGuide() {
  return (
    <div className="setup-guide">
      <h2>설정하는 법</h2>
      <p className="setup-lead">
        이 챗봇은 <b>내 Supabase</b> 위에서 돕니다. 아래 다섯 단계를 마치면 내 주소로 열립니다.
        <br />
        막히면 <b>Edge Functions → 해당 함수 → Logs</b> 에 어디서 멈췄는지 그대로 나옵니다.
      </p>

      <ol className="setup-steps">
        {STEPS.map((s) => (
          <li key={s.title}>
            <h3>{s.title}</h3>
            <p>{s.body}</p>
          </li>
        ))}
      </ol>

      <h3>API 키 네 가지</h3>
      <p className="setup-lead">
        <b>키는 반드시 Supabase Secrets 에만 넣습니다.</b> 프런트엔드(.env)에 넣으면 빌드 결과에 그대로 남아
        누구나 꺼내 갈 수 있습니다. 이 앱이 함수를 거쳐 부르는 이유가 그것입니다.
      </p>

      <table className="setup-table">
        <thead>
          <tr>
            <th>서비스</th>
            <th>Secrets 이름</th>
            <th>키 받는 곳</th>
            <th>언제 쓰나</th>
          </tr>
        </thead>
        <tbody>
          {KEYS.map((k) => (
            <tr key={k.secret}>
              <td>{k.name}</td>
              <td>
                <code>{k.secret}</code>
              </td>
              <td>
                <a href={k.url} target="_blank" rel="noreferrer">
                  {k.where}
                </a>
              </td>
              <td>{k.note}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <p className="setup-note">
        대화 화면 위쪽에서 <b>서비스와 모델을 골라</b> 대화마다 다르게 쓸 수 있습니다. 같은 질문을 서비스만
        바꿔 두 번 던져 보면 차이가 보입니다. 고른 서비스의 키가 없으면 <b>어느 키가 없는지</b> 알려 주고 멈춥니다.
      </p>

      <h3>막혔을 때</h3>
      <table className="setup-table">
        <thead>
          <tr>
            <th>증상</th>
            <th>원인</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>화면이 하얗다</td>
            <td>
              <code>vite.config.ts</code> 의 <code>base</code> 가 저장소 이름과 다릅니다
            </td>
          </tr>
          <tr>
            <td>“Supabase 설정이 없습니다”</td>
            <td>
              <code>.env</code> 또는 깃허브 Actions Secrets 가 비었습니다 (5단계)
            </td>
          </tr>
          <tr>
            <td>답이 안 오고 401 / 403</td>
            <td>
              <code>BOT_CLIENT_TOKEN</code> 이 Secrets 와 <code>.env</code> 에서 다릅니다
            </td>
          </tr>
          <tr>
            <td>“…KEY 가 서버에 없습니다”</td>
            <td>고른 서비스의 키를 Secrets 에 안 넣었습니다 (4단계)</td>
          </tr>
          <tr>
            <td>문서 답이 엉뚱하다</td>
            <td>문서를 켜지 않았거나 임베딩용 OPENAI_API_KEY 가 없습니다</td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}
