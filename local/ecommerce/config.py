import socket
import os
from typing import List

ORDER_SERVICE = os.getenv("ORDER_SERVICE")
PROUDCT_SERVICE = os.getenv("PROUDCT_SERVICE")
CUSTOMER_SERVICE = os.getenv("CUSTOMER_SERVICE")

def host():    
    
    container_hostname = None
    container_ip = None

    try :
        container_hostname = socket.gethostname()    
        container_ip = socket.gethostbyname(container_hostname)
    except :
        pass
    host_ip = os.environ.get('HOST_IP')
    host_name = os.environ.get('HOST_NAME')
    
    return {
            "container_ip": container_ip,
            "container_hostname": container_hostname,
            "host_ip": host_ip,
            "host_name": host_name,
           }

def create_dict_from_rows(rows: List[tuple], columns: List[str]) -> List[dict]:
    return [dict(zip(columns, row)) for row in rows]