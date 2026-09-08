import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// ⚠️ 여기를 여러분의 저장소 이름으로 바꾸세요.
//    https://<아이디>.github.io/<저장소이름>/ 로 서비스되므로 base 가 하위 경로여야 합니다.
//    예) 저장소가 my-chatbot 이면  base: '/my-chatbot/'
//    이 값이 틀리면 화면이 하얗게 뜨고 콘솔에 파일 404 가 납니다.
export default defineConfig({
  base: '/chatbot-lab/',
  plugins: [react()],
})
