from application.containers import ApplicationContainer


def main():
    container = ApplicationContainer()
    container.init_resources()
    return container


if __name__ == "__main__":
    main()

