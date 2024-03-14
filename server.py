import time
import concurrent.futures as futures
import grpc
import berkeley_pb2_grpc
import berkeley_pb2


class TimeSyncServicer(berkeley_pb2_grpc.TimeSyncServicer):
    def __init__(self) -> None:
        super().__init__()
        self.clients = {}

    def GetTime(self, request, context):
        current_server_time_in_ms = time.time() * 1000
        return berkeley_pb2.TimeResponse(time=current_server_time_in_ms)

    def SendTimeToMaster(self, request, context):
        self.clients[request.port] = request.time
        average_time = sum(self.clients.values()) / len(self.clients)
        # result represents how much we need to adjust the client time based on
        # average of time
        result = average_time - self.clients[request.port]
        return berkeley_pb2.TimeResponse(time=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    berkeley_pb2_grpc.add_TimeSyncServicer_to_server(TimeSyncServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
