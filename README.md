# demo

정적 HTML을 GitHub Pages로 호스팅하는 저장소.

- 배포 URL: https://dohyeon-kr.github.io/demo/
- 배포 방식: GitHub Actions (`.github/workflows/deploy.yml`)
- 트리거: `main` 브랜치 push, 또는 Actions 탭에서 수동 실행

## 구조

```
index.html            홈
404.html              Not Found 페이지
.nojekyll             Jekyll 처리 비활성화 (_ 로 시작하는 파일/폴더 보존)
.github/workflows/    Pages 배포 워크플로
```

저장소 루트 전체가 아티팩트로 업로드된다. HTML/CSS/JS/이미지를 루트에 추가하면
그대로 서빙된다. 링크는 상대 경로(`./assets/...`)를 쓸 것 — 사이트가
`/demo/` 하위 경로에 배포되므로 절대 경로(`/assets/...`)는 깨진다.

## 로컬 확인

```bash
python3 -m http.server 8000
```
