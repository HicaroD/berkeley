import time
import grpc
import berkeley_pb2, berkeley_pb2_grpc


class BerkeleyAlgorithm:
    def __init__(self, client_port: int) -> None:
        self.client_port = client_port

    def adjust_client_clock(self, server_address):
        with grpc.insecure_channel(server_address) as channel:
            stub = berkeley_pb2_grpc.TimeSyncStub(channel)

            server_time_in_ms = stub.GetTime(berkeley_pb2.Empty())
            current_client_time_in_ms = time.time() * 1000

            delta = current_client_time_in_ms - server_time_in_ms.time
            delta = stub.SendTimeToMaster(
                berkeley_pb2.TimeRequest(
                    port=self.client_port,
                    time=current_client_time_in_ms,
                )
            )
            adjustment = current_client_time_in_ms + delta.time
            self.adjust_client_clock_based_on_server_time(adjustment)

    def adjust_client_clock_based_on_server_time(self, adjustment):
        print(f"Clock adjusted with value {adjustment} in the port {self.client_port}")
