import os
import tableauserverclient as TSC
from dotenv import load_dotenv


def main():
    # .env 파일 로드 (로컬 개발용)
    load_dotenv()

    # 환경 변수 로드
    server_url = os.environ.get('TABLEAU_SERVER_URL')
    token_name = os.environ.get('TABLEAU_TOKEN_NAME')
    token_value = os.environ.get('TABLEAU_TOKEN_VALUE')
    site_id = os.environ.get('TABLEAU_SITE_ID')

    # Tableau 인증 설정
    tableau_auth = TSC.PersonalAccessTokenAuth(
        token_name,
        token_value,
        site_id=site_id
    )
    server = TSC.Server(server_url, use_server_version=True)
    # SSL 인증서 검증 문제 발생 시 아래 주석 해제 (보안 주의)
    # server.add_http_options({'verify': False})

    with server.auth.sign_in(tableau_auth):
        # 모든 워크북 조회 (페이지네이션 활용)
        all_workbooks = list(TSC.Pager(server.workbooks))

        for workbook in all_workbooks:
            try:
                # 데이터 연결 정보 로드
                server.workbooks.populate_connections(workbook)
                
                # PostgreSQL 연결 포함 여부 확인 ('postgres')
                is_postgres = any(
                    conn.connection_type == 'postgres' 
                    for conn in workbook.connections
                )

                if is_postgres:
                    # 추출 새로고침 작업 요청
                    job = server.workbooks.refresh(workbook.id)
                    print(f"Refresh triggered: {workbook.name} (Job ID: {job.id})")
                else:
                    # PostgreSQL이 아닌 경우 스킵
                    # print(f"Skipping: {workbook.name} (Not a PostgreSQL connection)")
                    pass

            except TSC.ServerResponseError as e:
                # 추출 항목이 없는 워크북(Live 연결 등)은 403 에러 발생 가능
                if e.code == '403002':
                    print(f"Skipping: {workbook.name} (No extract found)")
                else:
                    print(f"Error processing {workbook.name}: {e}")


if __name__ == "__main__":
    main()
