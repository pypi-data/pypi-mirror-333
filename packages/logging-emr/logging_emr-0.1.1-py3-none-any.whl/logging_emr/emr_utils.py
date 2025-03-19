import boto3
import requests
import traceback
from .cloudwatch_logger import setup_logger

REGION = "us-east-1"

def get_cluster_id():
    """Obtém o Cluster ID a partir do nó-mestre do EMR, usando IMDSv2."""
    try:
        print("Obtendo o ID da instância do nó-mestre...")

        # Obtém o token para autenticação na API de metadados (IMDSv2)
        token_url = "http://169.254.169.254/latest/api/token"
        headers = {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}  # Token válido por 6 horas
        response = requests.put(token_url, headers=headers, timeout=5)

        if response.status_code != 200:
            print(f"Erro ao obter token de metadados, status HTTP: {response.status_code}")
            return None

        token = response.text.strip()

        # Obtém o Instance ID usando o token
        instance_id_url = "http://169.254.169.254/latest/meta-data/instance-id"
        headers = {"X-aws-ec2-metadata-token": token}
        response = requests.get(instance_id_url, headers=headers, timeout=5)

        if response.status_code != 200:
            print(f"Erro ao obter Instance ID, status HTTP: {response.status_code}")
            return None

        instance_id = response.text.strip()
        if not instance_id:
            print("Instance ID retornou vazio.")
            return None

        # Obtém Cluster ID a partir das tags da instância EC2
        ec2_client = boto3.client("ec2", region_name=REGION)
        response = ec2_client.describe_instances(InstanceIds=[instance_id])

        tags = response["Reservations"][0]["Instances"][0].get("Tags", [])
        for tag in tags:
            if tag["Key"] == "aws:elasticmapreduce:job-flow-id":
                return tag["Value"]

        print("Cluster ID não encontrado nas tags.")
        return None
    except Exception as e:
        print(f"Erro ao obter Cluster ID: {e}")
        print(traceback.format_exc())
        return None

def get_cluster_name(emr_client, cluster_id):
    """Obtém o nome do cluster a partir do ID."""
    try:
        response = emr_client.describe_cluster(ClusterId=cluster_id)
        tags = response['Cluster'].get('Tags', [])

        for tag in tags:
            if tag['Key'] == 'Name':
                return tag["Value"]

        print("Cluster não possui a tag 'Name'.")
        return None
    except Exception as e:
        print(f"Erro ao obter nome do cluster: {e}")
        print(traceback.format_exc())
        return None

def get_current_step_name(emr_client, cluster_id):
    """Obtém o nome da step em execução no momento."""
    try:
        print(f"Obtendo step em execução no cluster {cluster_id}...")

        response = emr_client.list_steps(ClusterId=cluster_id)
        
        # Filtra a primeira step que está em execução
        running_steps = [step for step in response["Steps"] if step["Status"]["State"] in ("PENDING", "RUNNING")]
        
        if running_steps:
            step_name = running_steps[0]["Name"]
            print(f"Step em execução encontrada: {step_name}")
            return step_name.lower()

        print("Nenhuma step em execução encontrada.")
        return "unknown_step"

    except Exception as e:
        print(f"Erro ao obter step atual: {e}")
        print(traceback.format_exc())
        return "unknown_step"

def setup_logging_for_emr():
    """Configura automaticamente o logger para CloudWatch no EMR, identificando o Cluster ID e a Step atual."""
    try:
        emr_client = boto3.client('emr', region_name=REGION)
        
        cluster_id = get_cluster_id()
        if not cluster_id:
            print("Não foi possível identificar o cluster.")
            return None

        cluster_name = get_cluster_name(emr_client, cluster_id)
        if not cluster_name:
            print("Cluster não possui a tag 'Name'.")
            return None

        step_name = get_current_step_name(emr_client, cluster_id)

        print(f"Cluster identificado: {cluster_name} (ID: {cluster_id}), Step atual: {step_name}")

        # Configura o logger automaticamente com os valores obtidos
        return setup_logger(logprocessorname=cluster_name, logstepname=step_name)

    except Exception as e:
        print(f"Erro ao configurar logging no EMR: {e}")
        print(traceback.format_exc())
        return None
