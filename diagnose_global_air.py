import os
import tableauserverclient as TSC
from dotenv import load_dotenv

def diagnose_workbook(target_name):
    load_dotenv()
    server_url = os.environ.get('TABLEAU_SERVER_URL')
    token_name = os.environ.get('TABLEAU_TOKEN_NAME')
    token_value = os.environ.get('TABLEAU_TOKEN_VALUE')
    site_id = os.environ.get('TABLEAU_SITE_ID')

    tableau_auth = TSC.PersonalAccessTokenAuth(token_name, token_value, site_id=site_id)
    server = TSC.Server(server_url, use_server_version=False)
    server.version = '3.4'
    server.add_http_options({'verify': False})

    with server.auth.sign_in(tableau_auth):
        all_workbooks = list(TSC.Pager(server.workbooks))
        target_wb = next((wb for wb in all_workbooks if wb.name == target_name), None)
        
        if not target_wb:
            print(f"Workbook '{target_name}' not found.")
            return

        print(f"--- Diagnosing Workbook: {target_wb.name} (ID: {target_wb.id}) ---")
        server.workbooks.populate_connections(target_wb)
        
        for i, conn in enumerate(target_wb.connections):
            print(f"\nConnection #{i+1}:")
            print(f"  - ID: {conn.id}")
            print(f"  - Type: {conn.connection_type}")
            print(f"  - Server Address: {conn.server_address}")
            print(f"  - Port: {conn.server_port}")
            print(f"  - Username: {conn.username}")
            # Check if it's a published data source
            if conn.datasource_id:
                print(f"  - Link to Published Data Source ID: {conn.datasource_id}")
                # Try to fetch the data source details
                try:
                    ds = server.datasources.get_by_id(conn.datasource_id)
                    print(f"  - Data Source Name: {ds.name}")
                    server.datasources.populate_connections(ds)
                    for ds_conn in ds.connections:
                        print(f"    * DS Connection Type: {ds_conn.connection_type}")
                        print(f"    * DS Server: {ds_conn.server_address}")
                        print(f"    * DS Username: {ds_conn.username}")
                except Exception as e:
                    print(f"    * Could not fetch data source info: {e}")
            else:
                print("  - Embedded Data Source (Not published separately)")

if __name__ == "__main__":
    diagnose_workbook("Global Air Quality")
