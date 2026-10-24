# crawler_pipeline.py의 def fetch … return res.text를 이것으로 바꿉니다
def fetch(url: str, retries: int = 3) -> str:
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            if res.status_code == 429:
                print(f'  429 too many requests — {attempt}회차, 5초 대기')
                time.sleep(5)
                continue
            res.raise_for_status()
            return res.text
        except requests.RequestException as e:
            last_error = e
            print(f'  요청 실패({attempt}/{retries}): {e}')
            time.sleep(2 * attempt)      # 갈수록 더 오래 쉰다
    raise RuntimeError(f'{url} 수집 실패') from last_error
