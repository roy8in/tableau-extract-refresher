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

## 3. 파일 구성

본 저장소는 다음과 같이 구성되어야 합니다.

* `.github/workflows/tableau_refresh.yml`: 자동화 스케줄링 설정 (매일 한국 시간 오전 9시).
* `refresh_workbooks.py`: 추출 새로고침을 실행하는 메인 로직.
* `requirements.txt`: 의존성 라이브러리 목록 (`tableau-server-client`).

---

## 4. 사용 방법

### 자동 실행
* `.github/workflows/tableau_refresh.yml`에 설정된 `cron` 주기에 따라 매일 정해진 시간에 자동 실행됩니다.

### 수동 실행
1. GitHub 저장소 상단의 **Actions** 탭으로 이동합니다.
2. 좌측 워크플로우 목록에서 **Tableau Extract Refresh Automation**을 선택합니다.
3. 오른쪽의 **Run workflow** 버튼을 클릭하여 즉시 실행합니다.

---

## 5. 참고 사항

* **추출 전용**: 이 스크립트는 '데이터 추출(Extract)' 방식의 워크북만 새로고침할 수 있습니다. 라이브 연결 워크북은 스킵됩니다.
* **로그 확인**: 실행 결과 및 오류 메시지는 GitHub Actions의 **Run history**에서 실시간으로 확인할 수 있습니다.
* **비동기 작업**: 스크립트는 서버에 새로고침 요청을 보낸 후 즉시 종료됩니다. 실제 데이터 업데이트 완료 시점은 서버의 Backgrounder 작업 상태에 따라 다를 수 있습니다.