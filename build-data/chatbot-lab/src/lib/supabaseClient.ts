import { createClient } from '@supabase/supabase-js'

// 여러분의 Supabase 프로젝트 값을 .env 에 넣습니다.
//   VITE_SUPABASE_URL       프로젝트 URL      (Settings → API)
//   VITE_SUPABASE_ANON_KEY  anon public 키    (Settings → API)
//
// 일부러 기본값을 두지 않았습니다. 값이 없으면 조용히 남의 프로젝트에 붙는 대신
// 여기서 바로 멈추고 무엇이 빠졌는지 알려 줍니다.
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!SUPABASE_URL || !SUPABASE_ANON_KEY) {
  throw new Error(
    'Supabase 설정이 없습니다. .env 파일에 VITE_SUPABASE_URL 과 VITE_SUPABASE_ANON_KEY 를 넣으세요. ' +
      '(.env.example 을 복사해 .env 로 만들면 됩니다)',
  )
}

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)
