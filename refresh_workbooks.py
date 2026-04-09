import os
import csv
import datetime
import time
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

    # 로그 파일 설정
    log_file = 'refresh_log.csv'
    file_exists = os.path.isfile(log_file)

    # Tableau 인증 설정
    tableau_auth = TSC.PersonalAccessTokenAuth(
        token_name,
        token_value,
        site_id=site_id
    )
    # API 버전 3.4 이상 필요 (Workbook Refresh 지원)
    server = TSC.Server(server_url, use_server_version=False)
    server.version = '3.4'
    # SSL 인증서 검증 문제 발생 시 아래 설정 (보안 주의)
    server.add_http_options({'verify': False})

    with server.auth.sign_in(tableau_auth):
        # 모든 워크북 조회
        all_workbooks = list(TSC.Pager(server.workbooks))
        
        refresh_results = []

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
                    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"[{start_time}] Triggering refresh: {workbook.name}")
                    
                    # 추출 새로고침 작업 요청
                    job = server.workbooks.refresh(workbook.id)
                    
                    # 작업 완료 대기 (기본적으로 성공/실패까지 대기)
                    job_status = server.jobs.wait_for_job(job.id)
                    
                    end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    success = "Success" if job_status.finish_code == 0 else f"Failed({job_status.finish_code})"
                    
                    print(f"[{end_time}] Result: {success} (Job ID: {job.id})")
                    
                    # 결과 저장
                    refresh_results.append({
                        'Workbook Name': workbook.name,
                        'Workbook ID': workbook.id,
                        'Start Time': start_time,
                        'End Time': end_time,
                        'Status': success,
                        'Job ID': job.id
                    })
                
            except Exception as e:
                print(f"Error processing {workbook.name}: {e}")

        # CSV 파일에 결과 기록 (추가 모드)
        if refresh_results:
            keys = refresh_results[0].keys()
            with open(log_file, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                if not file_exists:
                    writer.writeheader()
                writer.writerows(refresh_results)
            print(f"\nRefresh results logged to {log_file}")


if __name__ == "__main__":
    main()
