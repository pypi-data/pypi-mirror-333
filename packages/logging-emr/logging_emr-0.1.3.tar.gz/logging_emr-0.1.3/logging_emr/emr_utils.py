#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pyspark import SparkContext
from pyspark.sql.session import SparkSession
import boto3
import requests
import traceback
import sys

# Inicializa o Spark
sc = SparkContext.getOrCreate()
spark = SparkSession.builder.master("yarn").enableHiveSupport().getOrCreate()

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
                print(f"Cluster ID encontrado: {tag['Value']}")
                return tag["Value"]

        print("Cluster ID não encontrado nas tags da instância.")
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

def ensure_log_group_exists(logs_client, log_group_name):
    """Verifica se o log group existe, e cria caso não exista"""
    try:
        response = logs_client.describe_log_groups(logGroupNamePrefix=log_group_name)
        log_groups = [group["logGroupName"] for group in response.get("logGroups", [])]

        if log_group_name not in log_groups:
            print(f"Log group '{log_group_name}' não encontrado. Criando...")
            logs_client.create_log_group(logGroupName=log_group_name)
            logs_client.put_retention_policy(logGroupName=log_group_name, retentionInDays=30)
            print(f"Log group '{log_group_name}' criado com sucesso!")
        else:
            print(f"Log group '{log_group_name}' já existe.")

    except Exception as e:
        print(f"Erro ao verificar/criar log group: {e}")
        print(traceback.format_exc())

def ensure_log_stream_exists(logs_client, log_group_name, log_stream_name):
    """Verifica se o log stream existe, e cria caso não exista"""
    try:
        response = logs_client.describe_log_streams(logGroupName=log_group_name, logStreamNamePrefix=log_stream_name)
        log_streams = [stream["logStreamName"] for stream in response.get("logStreams", [])]

        if log_stream_name not in log_streams:
            print(f"Log stream '{log_stream_name}' não encontrado. Criando...")
            logs_client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
            print(f"Log stream '{log_stream_name}' criado com sucesso!")
        else:
            print(f"Log stream '{log_stream_name}' já existe.")

    except Exception as e:
        print(f"Erro ao verificar/criar log stream: {e}")
        print(traceback.format_exc())

def main():
    try:
        print("Inicializando clientes boto3...")
        emr_client = boto3.client('emr', region_name=REGION)
        logs_client = boto3.client('logs', region_name=REGION)

        cluster_id = get_cluster_id()
        if not cluster_id:
            print("Não foi possível identificar o cluster.")
            return

        cluster_name = get_cluster_name(emr_client, cluster_id)
        if not cluster_name:
            print("Cluster não possui a tag 'Name'.")
            return

        step_name = get_current_step_name(emr_client, cluster_id)

        print(f"Cluster identificado: {cluster_name} (ID: {cluster_id}), Step atual: {step_name}")

        # Garante que o log group e o log stream existam
        ensure_log_group_exists(logs_client, cluster_name)
        ensure_log_stream_exists(logs_client, cluster_name, step_name)

        print("Configuração de logging concluída!")

    except Exception as e:
        print(f"Erro no processo principal: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
