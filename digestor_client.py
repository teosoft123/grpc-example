import grpc

import digestor_pb2
import digestor_pb2_grpc


class DigestorClient(object):
    """
    Client for accessing the gRPC functionality
    """

    def __init__(self):
        # configure the host and the
        # the port to which the client should connect
        # to.
        self.host = 'localhost'
        self.server_port = 46001

        # instantiate a communication channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        # bind the client to the server channel
        self.stub = digestor_pb2_grpc.DigestorStub(self.channel)

    def get_digest(self, message):
        """
        Client function to call the rpc for GetDigest
        """
        to_digest_message = digestor_pb2.DigestMessage(ToDigest=message)
        return self.stub.GetDigestor(to_digest_message)

    # function to invoke our newly implemented RPC
    def get_streaming_digest(self, message):
        """
        Client function to call the rpc for GetDStream
        """
        to_digest_message = digestor_pb2.DigestMessage(ToDigest=message)
        digested_words = self.stub.GetDStream(to_digest_message)
        for digested_word in digested_words:
            print(digested_word)


dc = DigestorClient()
dc.get_streaming_digest("Goodbye, cruel world.")
