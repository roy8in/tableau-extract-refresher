# Tableau Extract Refresh Automation

GitHub Actions와 Python을 사용하여 Tableau Cloud/Server의 데이터 추출(Extract)을 자동으로 새로고침하는 프로젝트입니다.

## 1. 사전 준비 사항

### Tableau 개인 액세스 토큰(PAT) 생성
1. Tableau Server/Cloud 로그인 후 **내 콘텐츠 설정** > **설정** > **개인 액세스 토큰** 이동.
2. 새 토큰 생성 후 **Token Name**과 **Token Value**를 안전한 곳에 기록.

### Site ID 확인
* Tableau Cloud URL: `https://.../#/site/{SITE_ID}/home`
* 위 URL 구조에서 `{SITE_ID}`에 해당하는 문자열이 Site ID입니다.

---

## 2. GitHub Secrets 설정

GitHub 저장소의 `Settings` > `Secrets and variables` > `Actions` 메뉴에서 **New repository secret**을 클릭하여 다음 4개 항목을 추가합니다.

| Secret Name | 설명 | 예시 |
| :--- | :--- | :--- |
| `TABLEAU_SERVER_URL` | Tableau 접속 URL | `https://prod-apnortheast-a.online.tableau.com` |
| `TABLEAU_TOKEN_NAME` | PAT 이름 | `automation-token` |
| `TABLEAU_TOKEN_VALUE` | PAT 값 | `p+QWERTY12345...` |
| `TABLEAU_SITE_ID` | 사이트 식별자 | `mycompany` |

---

## 3. 로컬 개발 설정

로컬 환경에서 스크립트를 테스트하고 실행하려면 다음 단계를 따르세요.

### 가상 환경 및 패키지 설치
1. 가상 환경 생성: `python -m venv .venv`
2. 가상 환경 활성화:
   - **Windows**: `.\.venv\Scripts\activate`
   - **Mac/Linux**: `source .venv/bin/activate`
3. 의존성 패키지 설치: `pip install -r requirements.txt`

### 환경 변수 설정 (.env)
루트 디렉토리에 `.env` 파일을 생성하고 아래 내용을 입력합니다.
```env
TABLEAU_SERVER_URL=your-server-url
TABLEAU_TOKEN_NAME=your-token-name
TABLEAU_TOKEN_VALUE=your-token-value
TABLEAU_SITE_ID=your-site-id
```

### 스크립트 실행
```bash
python refresh_workbooks.py
```

---

## 4. 사용 방법 (GitHub Actions)

### 자동 실행
* `.github/workflows/tableau_refresh.yml`에 설정된 `cron` 주기에 따라 매일 정해진 시간에 자동 실행됩니다.

### 수동 실행
1. GitHub 저장소 상단의 **Actions** 탭으로 이동합니다.
2. 좌측 워크플로우 목록에서 **Tableau Extract Refresh Automation**을 선택합니다.
3. 오른쪽의 **Run workflow** 버튼을 클릭하여 즉시 실행합니다.

---

## 5. 파일 구성

* `.github/workflows/tableau_refresh.yml`: 자동화 스케줄링 설정.
* `refresh_workbooks.py`: 추출 새로고침 메인 로직.
* `requirements.txt`: 의존성 라이브러리 목록.
* `.env`: 로컬용 환경 변수 파일 (Git ignore 권장).

---

## 6. 참고 사항

* **추출 전용**: '데이터 추출' 방식의 워크북만 새로고침 가능합니다. 라이브 연결은 스킵됩니다.
* **로그 확인**: 실행 결과는 GitHub Actions의 **Run history**에서 확인할 수 있습니다.
* **비동기 작업**: 새로고침 요청 후 즉시 종료되며, 실제 완료는 서버 상태에 따라 다를 수 있습니다.
