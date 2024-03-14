import sys
from berkeley import BerkeleyAlgorithm


def main(port: int):
    # Inicia a conexão com o servidor
    server_address = "localhost:50051"
    berkeley_algorithm = BerkeleyAlgorithm(port)
    berkeley_algorithm.start(server_address)


if __name__ == "__main__":
    port = sys.argv[1]
    if port is None:
        print("No port was defined.\nEx.: python client.py xxxx")
        exit(1)
    main(int(port))
