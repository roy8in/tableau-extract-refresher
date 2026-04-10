import os
import datetime
import tableauserverclient as TSC
from dotenv import load_dotenv
import urllib3

# Disable SSL warnings for environments with self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def refresh_aqi_workbook():
    load_dotenv()
    server_url = os.environ.get('TABLEAU_SERVER_URL')
    token_name = os.environ.get('TABLEAU_TOKEN_NAME')
    token_value = os.environ.get('TABLEAU_TOKEN_VALUE')
    site_id = os.environ.get('TABLEAU_SITE_ID')

    # Write the target name to test refresh
    target_name = "AQI"

    if not all([server_url, token_name, token_value]):
        print("Missing environment variables. Please check your .env file.")
        return

    tableau_auth = TSC.PersonalAccessTokenAuth(token_name, token_value, site_id=site_id)
    server = TSC.Server(server_url, use_server_version=False)
    server.version = '3.4'
    server.add_http_options({'verify': False})

    try:
        with server.auth.sign_in(tableau_auth):
            print(f"Searching for workbook: {target_name}")
            all_workbooks = list(TSC.Pager(server.workbooks))
            target_wb = next((wb for wb in all_workbooks if wb.name == target_name), None)
            
            if not target_wb:
                print(f"Workbook '{target_name}' not found on the server.")
                return

            start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{start_time}] Found workbook: {target_wb.name} (ID: {target_wb.id})")
            print(f"Triggering refresh for '{target_name}' only...")

            job = server.workbooks.refresh(target_wb.id)
            print(f"Refresh job submitted (Job ID: {job.id}). Waiting for completion...")
            
            job_status = server.jobs.wait_for_job(job.id)
            end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            status = "Success" if job_status.finish_code == 0 else f"Failed({job_status.finish_code})"
            print(f"[{end_time}] Refresh Job {job.id} finished with status: {status}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    refresh_aqi_workbook()
