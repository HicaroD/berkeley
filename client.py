from berkeley import BerkeleyAlgorithm


def main():
    server_address = "localhost:50051"
    berkeley_algorithm = BerkeleyAlgorithm()
    delta = berkeley_algorithm.get_adjusted_clock(server_address)
    berkeley_algorithm.adjust_client_clock_based_on_server_time(delta)
    print("Clock synchronized successfully!")


if __name__ == "__main__":
    main()
