### Streaming:

    python -m grpc_tools.protoc --proto_path=. ./digestor.proto --python_out=. --grpc_python_out=.

Start server:

    python digestor_server.py
    
Run client: 

    python
    from digestor_client import DigestorClient
    currs_client = DigestorClient()
    currs_client.get_streaming_digest('This is a sample test where I get streaming responses')
