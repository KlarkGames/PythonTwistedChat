from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

names = []
previous_messages =""

class Client(Protocol):
    ip: str = None
    login: str = None
    factory: 'Chat'

    def __init__(self, factory):
        """
        Инициализация фабрики клиента
        :param factory:
        """
        self.factory = factory

    def connectionMade(self):
        """
        Обработчик подключения нового клиента
        """
        global previous_messages

        self.ip = self.transport.getHost().host

        self.factory.clients.append(self)

        print(f"Client connected: {self.ip}")

        self.transport.write("Welcome to the chat v0.1\n\n".encode())
        self.transport.write(previous_messages.encode())

    def dataReceived(self, data: bytes):
        """
        Обработчик нового сообщения от клиента
        :param data:
        """
        message = data.decode().replace('\n', '')
        global names

        if self.login is not None:
            server_message = f"{self.login}: {message}"
            self.factory.notify_all_users(server_message)

            print(server_message)
        else:
            if message.startswith("login:"):
                self.login = message.replace("login:", "")

                if names.count(self.login)!=0:
                    self.transport.write("This Login is buzy(\n".encode('utf8'))
                    reactor.callLater(0.5, self.transport.loseConnection)
                else:
                    names.append(self.login)

                    notification = f"New user connected: {self.login}"

                    self.factory.notify_all_users(notification)
                    print(notification)
            else:
                print("Error: Invalid client login")

    def connectionLost(self, reason=None):
        """
        Обработчик отключения клиента
        :param reason:
        """
        self.factory.clients.remove(self)
        print(f"Client disconnected: {self.ip}")


class Chat(Factory):
    clients: list

    def __init__(self):
        """
        Инициализация сервера
        """
        self.clients = []
        print("*" * 10, "\nStart server \nCompleted [OK]")

    def startFactory(self):
        """
        Запуск процесса ожидания новых клиентов
        :return:
        """
        print("\n\nStart listening for the clients...")

    def buildProtocol(self, addr):
        """
        Инициализация нового клиента
        :param addr:
        :return:
        """
        return Client(self)

    def notify_all_users(self, data: str):
        """
        Отправка сообщений всем текущим пользователям
        :param data:
        :return:
        """
        global previous_messages

        for user in self.clients:
            user.transport.write(f"{data}\n".encode())
        previous_messages+=(f"{data}\n")


if __name__ == '__main__':
    reactor.listenTCP(14377, Chat())
    reactor.run()