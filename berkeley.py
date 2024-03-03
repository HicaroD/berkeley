import time
import grpc
import berkeley_pb2, berkeley_pb2_grpc


class BerkeleyAlgorithm:
    def get_adjusted_clock(self, server_address):
        with grpc.insecure_channel(server_address) as channel:
            stub = berkeley_pb2_grpc.TimeSyncStub(channel)
            response = stub.GetTime(berkeley_pb2.Empty())
            local_time_in_ms = int(time.time() * 1000)
            delta = response.time - local_time_in_ms
            return delta

    def adjust_client_clock_based_on_server_time(self, delta):
        current_time_in_ms = int(time.time() * 1000)
        new_client_clock_time = current_time_in_ms + delta
        print(f"Client time set to {new_client_clock_time} ms")
