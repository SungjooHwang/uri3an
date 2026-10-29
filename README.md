# URI3AN Lab website

이화여자대학교 도시정보지능화연구실(URBAN Informatics and Intelligent Infrastructure Lab) 홈페이지입니다. GitHub Pages로 배포합니다.

## 내용 고치기
- 뉴스, 멤버, 교수 소개: `content/site.json`
- 논문·특허·소프트웨어: `content/publications.json`
- 연구과제: `content/research.json` (`img`는 `assets/img/research/` 안의 파일 이름)
- 강의: `content/teaching.json`
- 사진: `assets/img/` (news, members, research)

고친 뒤 `python3 tools/build.py`를 실행하면 루트의 HTML 6개가 다시 만들어집니다. HTML을 직접 고치지 마세요.
