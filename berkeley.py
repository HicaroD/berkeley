import time
import grpc
import berkeley_pb2, berkeley_pb2_grpc

INTERVAL = 3


class BerkeleyAlgorithm:
    def __init__(self, client_port: int) -> None:
        self.client_port = client_port

    def start(self, server_address):
        # Loop que irá executar o método que o cliente se conecta com
        # o servidor periodicamente (a cada 3 segundos)
        while 1:
            time.sleep(INTERVAL)
            self.adjust_client_clock(server_address)

    def adjust_client_clock(self, server_address):
        with grpc.insecure_channel(server_address) as channel:
            stub = berkeley_pb2_grpc.TimeSyncStub(channel)
            # Pega o tempo atual do cliente em milissegundo
            current_client_time_in_ms = time.time() * 1000
            # Envia para o servidor a porta do cliente atual e seu tempo
            delta = stub.SendTimeToMaster(
                berkeley_pb2.TimeRequest(
                    port=self.client_port,
                    time=current_client_time_in_ms,
                )
            )
            # Soma ao tempo do cliente o delta (o tempo de ajuste recebido
            # do cliente)
            adjustment = current_client_time_in_ms + delta.time
            print(
                f"Clock adjusted with value {adjustment} in the port {self.client_port}"
            )
