import hashlib
import time
from concurrent import futures

import grpc

import digestor_pb2
import digestor_pb2_grpc


class DigestorServicer(digestor_pb2_grpc.DigestorServicer):
    """
    gRPC server for Digestor Service
    """

    def __init__(self, *args, **kwargs):
        self.server_port = 46001

    def GetDigestor(self, request, context):
        """
        Implementation of the rpc GetDigest declared in the proto
        file above.
        """
        # get the string from the incoming request
        to_be_digested = request.ToDigest

        # digest and get the string representation
        # from the digestor
        hasher = hashlib.sha256()
        hasher.update(to_be_digested.encode())
        digested = hasher.hexdigest()

        # print the output here
        print(digested)

        result = {'Digested': digested, 'WasDigested': True}

        return digestor_pb2.DigestedMessage(**result)

    # code specific to our new service
    def GetDStream(self, request, context):
        """
        RPC for getting streaming digests
        """
        # get the sentence that needs to be processed
        to_be_digested_message = request.ToDigest

        # get all the words in the sentence
        word_list = to_be_digested_message.split(' ')

        for word in word_list:
            yield digestor_pb2.DigestedMessage(**self.get_hash(word))

    def get_hash(self, data):
        """
        Class function for returning the hash of a function
        """
        hasher = hashlib.sha256()
        hasher.update(data.encode())
        digested = hasher.hexdigest()
        return {'Digested': digested, 'WasDigested': True}

    def start_server(self):
        """
        Function which actually starts the gRPC server, and preps
        it for serving incoming connections
        """
        # declare a server object with desired number
        # of thread pool workers.
        digestor_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        # This line can be ignored
        digestor_pb2_grpc.add_DigestorServicer_to_server(DigestorServicer(), digestor_server)

        # bind the server to the port defined above
        digestor_server.add_insecure_port('[::]:{}'.format(self.server_port))

        # start the server
        digestor_server.start()
        print('Digestor Server running ...')

        try:
            # need an infinite loop since the above
            # code is non blocking, and if I don't do this
            # the program will exit
            while True:
                time.sleep(60 * 60 * 60)
        except KeyboardInterrupt:
            digestor_server.stop(0)
            print('Digestor Server Stopped ...')


curr_server = DigestorServicer()
curr_server.start_server()
