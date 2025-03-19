import boto3
import requests
import traceback
from .cloudwatch_logger import setup_logger

REGION = "us-east-1"

def get_instance_metadata(path):
    """Obtém metadados da instância EC2 usando IMDSv2 ou IMDSv1"""
    try:
        # 🔹 Tenta primeiro com IMDSv2
        token_url = "http://169.254.169.254/latest/api/token"
        headers = {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
        response = requests.put(token_url, headers=headers, timeout=5)

        if response.status_code == 200:
            token = response.text.strip()
            metadata_url = f"http://169.254.169.254/latest/meta-data/{path}"
            headers = {"X-aws-ec2-metadata-token": token}
            response = requests.get(metadata_url, headers=headers, timeout=5)

            if response.status_code == 200:
                return response.text.strip()

        print("IMDSv2 falhou. Tentando IMDSv1...")

    except requests.RequestException:
        print("Erro ao obter metadados usando IMDSv2.")

    # 🔹 Se IMDSv2 falhar, tenta IMDSv1
    try:
        response = requests.get(f"http://169.254.169.254/latest/meta-data/{path}", timeout=5)
        if response.status_code == 200:
            return response.text.strip()
    except requests.RequestException:
        print("Erro ao obter metadados usando IMDSv1.")

    return None

def get_cluster_id():
    """Obtém o Cluster ID a partir do nó-mestre do EMR."""
    try:
        print("Obtendo o ID da instância do nó-mestre...")
        instance_id = get_instance_metadata("instance-id")
        if not instance_id:
            print("Não foi possível obter o Instance ID.")
            return None

        print(f"Instance ID obtido: {instance_id}")

        # Obtém o Cluster ID a partir das tags da instância EC2
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
