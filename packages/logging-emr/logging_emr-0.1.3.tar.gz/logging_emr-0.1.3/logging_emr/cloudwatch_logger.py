import logging
import boto3
import sys
from datetime import datetime
import traceback

REGION = "us-east-1"

class CloudWatchHandler(logging.Handler):
    """Handler para envio de logs ao AWS CloudWatch"""

    def __init__(self, log_group: str, log_stream: str, region_name="us-east-1"):
        super().__init__()
        self.client = boto3.client("logs", region_name=region_name)
        self.log_group = log_group
        self.log_stream = log_stream

        # 🔹 Garante que o log group e log stream existam antes de enviar logs
        self.ensure_log_group_exists()
        self.ensure_log_stream_exists()

    def ensure_log_group_exists(self):
        """Verifica se o log group existe, e cria caso não exista"""
        try:
            response = self.client.describe_log_groups(logGroupNamePrefix=self.log_group)
            log_groups = [group["logGroupName"] for group in response.get("logGroups", [])]

            if self.log_group not in log_groups:
                print(f"Log group '{self.log_group}' não encontrado. Criando...")
                self.client.create_log_group(logGroupName=self.log_group)
                self.client.put_retention_policy(logGroupName=self.log_group, retentionInDays=30)
                print(f"Log group '{self.log_group}' criado com sucesso!")
            else:
                print(f"Log group '{self.log_group}' já existe.")

        except Exception as e:
            print(f"Erro ao verificar/criar log group: {e}")
            print(traceback.format_exc())

    def ensure_log_stream_exists(self):
        """Verifica se o log stream existe, e cria caso não exista"""
        try:
            response = self.client.describe_log_streams(
                logGroupName=self.log_group, logStreamNamePrefix=self.log_stream
            )

            log_streams = [stream["logStreamName"] for stream in response.get("logStreams", [])]

            if self.log_stream not in log_streams:
                print(f"Log stream '{self.log_stream}' não encontrado. Criando...")
                self.client.create_log_stream(logGroupName=self.log_group, logStreamName=self.log_stream)
                print(f"Log stream '{self.log_stream}' criado com sucesso!")
            else:
                print(f"Log stream '{self.log_stream}' já existe.")

        except self.client.exceptions.ResourceNotFoundException:
            print(f"Erro: Log group '{self.log_group}' não encontrado no CloudWatch.")
        except Exception as e:
            print(f"Erro ao verificar/criar log stream: {e}")
            print(traceback.format_exc())

    def get_sequence_token(self):
        """Obtém o sequence token necessário para enviar logs"""
        try:
            response = self.client.describe_log_streams(
                logGroupName=self.log_group, logStreamNamePrefix=self.log_stream
            )
            streams = response.get("logStreams", [])
            if streams:
                return streams[0].get("uploadSequenceToken")
        except Exception as e:
            print(f"Erro ao obter sequence token: {e}")
        return None

    def emit(self, record):
        """Envia os logs automaticamente para o CloudWatch"""
        try:
            message = self.format(record)
            timestamp = int(datetime.utcnow().timestamp() * 1000)
            log_event = {
                "logEvents": [{"timestamp": timestamp, "message": message}]
            }
            sequence_token = self.get_sequence_token()
            if sequence_token:
                log_event["sequenceToken"] = sequence_token

            self.client.put_log_events(
                logGroupName=self.log_group,
                logStreamName=self.log_stream,
                **log_event
            )
        except Exception as e:
            print(f"Erro ao enviar log: {e}")

def setup_logger(logprocessorname, logstepname):
    """Configura o logger para envio de logs ao AWS CloudWatch"""

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("ProcessorLogger")

    cloudwatch_handler = CloudWatchHandler(logprocessorname, logstepname)
    logger.addHandler(cloudwatch_handler)

    # Tratamento de exceções globais
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.error("Exceção não tratada", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception

    return logger
