import os
import tableauserverclient as TSC
from dotenv import load_dotenv

def compare_workbooks(success_name, fail_name):
    load_dotenv()
    auth = TSC.PersonalAccessTokenAuth(os.environ['TABLEAU_TOKEN_NAME'], os.environ['TABLEAU_TOKEN_VALUE'], os.environ['TABLEAU_SITE_ID'])
    server = TSC.Server(os.environ['TABLEAU_SERVER_URL'], use_server_version=False)
    server.version = '3.4'
    server.add_http_options({'verify': False})

    with server.auth.sign_in(auth):
        all_workbooks = list(TSC.Pager(server.workbooks))
        success_wb = next((wb for wb in all_workbooks if wb.name == success_name), None)
        fail_wb = next((wb for wb in all_workbooks if wb.name == fail_name), None)

        for name, wb in [(success_name, success_wb), (fail_name, fail_wb)]:
            print(f"\n=== Analyzing {name} ===")
            if not wb:
                print("Not found.")
                continue
            
            server.workbooks.populate_connections(wb)
            print(f"Number of connections: {len(wb.connections)}")
            for i, conn in enumerate(wb.connections):
                print(f"Connection #{i+1}:")
                print(f"  - Type: {conn.connection_type}")
                print(f"  - Server: {conn.server_address}")
                print(f"  - Username: {conn.username}")
                print(f"  - Is Published Data Source: {True if conn.datasource_id else False}")
                if conn.datasource_id:
                    ds = server.datasources.get_by_id(conn.datasource_id)
                    print(f"  - Data Source Name: {ds.name}")
                    print(f"  - Data Source Project: {ds.project_name}")
                    print(f"  - Data Source has Extract: {ds.has_extracts}")

if __name__ == "__main__":
    compare_workbooks("AQI", "Global Air Quality")
