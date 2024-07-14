## AF_INET stands for "Address Family - Internet" and indicates the socket is using IPv4 addresses
## What is IPv4? What's the difference between IPv6?
## -> Address Length:
## -> IPv4 uses 32-bit addresses which allow for 4.3 billion unique addresses, typiacll written as `192.168.0.1` format
## -> IPv6 uses 128-bit addresses which allow for 340 undecillion unique addresses and are written in hexadecimal separated by colons `2001:0db8:85a3:0000:0000:8a2e:0370:7334`
## -> Configuration:
## -> IPv4 often requires manual configuration or DHCP (Dynamic Host Configuration Protocol) for address assignment
## -> IPv6 supports auto-configuration allowing devices to generate their own IP addresses using Stateless Address Autoconfiguration (SLAAC) pr DCHPv6
## -> Header Complexity:
## -> IPv4 header is 20-60 bytes long and containes 12 fields
## -> IPv6 header is 40 bytes long with 8 fields, designed to be simpler and more efficient
## -> Security:
## -> IPv4 security is optional and implemented through the IPsec suite, but not universally used
## -> IPv6 HAS to use IPsec offering built-in security features for authentication and encryption
## -> Broadcast:
## -> IPv4 uses broadcast addresses to send packets to all devices on a subnet
## -> IPv6 replaces broadcast with multicast, improving networking efficiency and reducing unnecessary traffic
## -> Fragmentation:
## -> IPv4 routers and sendig hostrs can fragment packages
## -> IPv6 only the sending host can fragment packages, routers do not perform fragmentation
## When to use IPv4 over IPv6?
## -> For IPv4, use it when: compatibility with older devices and networks are required, workling in an envrionmnt where IPv4 infrastructure is already well established
## -> For IPv6, use it when: building new network infastructure or future-proofing existing networkings, dealing with IP address shortages and the limitatinos of NAT, needing improcved security features and more efficient routing, ensuring compatibility with modern devices and services that require IPv6
## -> Many services offer a dual approach
## socket is the actual socket object used to establish connections
## SOCK_STREAM indicates the the socket will use TCP (Transmission Control Protocol) which provides a reliable, ordered and error-checked de;ocery of a stream of data between applications
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

## TCP server
class Server():
    def __init__(self, host, port):
        self.host = host ## Store host server will listen
        self.port = port ## Store port server will listen
        self.sock = socket(AF_INET, SOCK_STREAM) ## Creates a new socket using IPv4 (AF_INET) and TCP (SOCK_STREAM)
        ## How do you know what size to make a buffer?
        ## -> Common buffer sizes are 512 bytes, 1024 bytes (1 KB) and 2048 bytes (2 KB), these are often chosen since the align well with the typical Maximum Transmission Unit (MTU) sizes on the internet
        ## -> Expecting larger chgunks of data (ex. file transfers, media streaming etc.) then you might choose larger buffer sizes to redice the number of `recv` calls
        ## -> For smaller messages (ex. chat messages, commands etc.) a smaller buffer size is probably fine
        ## -> On fast and reliable networks (ex. a local area network), larger buffer sizes can be more efficient
        ## -> On slower or less reliable networking (ex. the internet), smaller buffer sizes help manage retransmissinos and error handling more effectively
        ## -> Operating system can also influence optimal buffer size based on how they handle memory and I/O operations
        ## -> 1024 is often fine for short messages where it can handle messages in a single read and not being large enough to waste memory
        ## -> If you might receive larger datas at times, you can create a loop to check that all the data has been received first
        self.buffer = 1024 ## Defines a buffer size of 1024 for receiving messages
        self.clients = {} ## Tracks connected clients
        self.addrs = {} ## Tracks clients addresses

    def serverStart(self):
        self.sock.bind((self.host, self.port)) ## Binds the socket to the specified host and port
        self.sock.listen(5) ## Tells the socket to start listening for incoming conenctinos, the number 5 os a backlog parameter which specifies the maximum number of queued connectinos, if it's full new connectinos may be refused
        print("We're connected! *high-fives*")

        ## Get chat started
        while True:
            try:
                clientSocket, clientAddress = self.sock.accept()
                print(f"Connection recieved from {clientAddress}")

                self.clients[clientSocket] = clientAddress ## Make multiple clients join the server and register in the client dict
                self.addrs[clientAddress] = clientSocket

                Thread(target=self.handling, args=(clientSocket,)).start()
            except Exception as e:
                print(f"{e}: Connection closed")

    ## Message and display them in terminal
    def handling(self, clientSocket):
        while True:
            msg = clientSocket.recv(self.buffer).decode("utf8")
            print(clientSocket)

            if msg:
                print(f"{msg} received!")
                self.sendTexts(msg)

    def sendTexts(self, msg):
        for socket in self.clients:
            try:
                socket.send(bytes(msg, "utf8"))
            except Exception as e:
                print(e)

## Ensures server starts only if script is running directly
if __name__ == "__main__":
    try:
        Server("localhost", 8000).serverStart() ## Creates an instance of the `Server` class with "localhost" as the host and 8000 as the port, then calls `serverStart` to start the server
    except KeyboardInterrupt:
        print("Closed Connection")
