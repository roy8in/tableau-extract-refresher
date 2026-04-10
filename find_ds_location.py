import os
import tableauserverclient as TSC
from dotenv import load_dotenv

def find_datasource_by_id(ds_id):
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
        try:
            # ID로 직접 데이터 원본 정보 가져오기
            ds = server.datasources.get_by_id(ds_id)
            print(f"--- Data Source Found ---")
            print(f"Name: {ds.name}")
            print(f"Project Name: {ds.project_name}")
            print(f"Project ID: {ds.project_id}")
            print(f"Owner ID: {ds.owner_id}")
            print(f"Webpage URL: {server_url}/#/site/{site_id}/datasources/{ds.id}")
            
            print("\nCheck if password is embedded:")
            server.datasources.populate_connections(ds)
            for conn in ds.connections:
                print(f"  - Connection Type: {conn.connection_type}")
                print(f"  - Username: {conn.username}")
                print(f"  - Password Embedded: {conn.embed_password}")

        except Exception as e:
            print(f"Error finding data source: {e}")

if __name__ == "__main__":
    # 아까 진단 결과에서 나온 Published Data Source ID
    find_datasource_by_id("9e48b2ce-0508-4894-aa95-7e23afab493f")
