import concurrent.futures as futures
import grpc
import berkeley_pb2_grpc
import berkeley_pb2
import time


class TimeSyncServicer(berkeley_pb2_grpc.TimeSyncServicer):
    def __init__(self, server_port: int) -> None:
        super().__init__()
        self.server_port = server_port
        self.clients = {}

    def SendTimeToMaster(self, request, context):
        # Atualizando o tempo do servidor para utilizarmos na média
        self.clients[self.server_port] = time.time() * 1000
        # Atualizando o tempo do cliente para utilizarmos na média
        self.clients[request.port] = request.time
        # Pega o tempo médio dos clientes
        average_time = sum(self.clients.values()) / len(self.clients)
        # Fazemos a média menos o tempo atual do cliente para sabermos o
        # o quanto o cliente atual deve ajustar seu relógio
        result = average_time - self.clients[request.port]
        # Retorna o ajuste para o cliente
        return berkeley_pb2.TimeResponse(time=result)


def serve():
    # Inicia o servidor na porta 50051
    server_port = 50051
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    berkeley_pb2_grpc.add_TimeSyncServicer_to_server(
        TimeSyncServicer(server_port=server_port), server
    )
    server.add_insecure_port("[::]:50051")
    print("Server is running on port 50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
