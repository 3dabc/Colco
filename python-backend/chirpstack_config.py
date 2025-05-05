import grpc
from chirpstack_api.as_pb.external import api

# ChirpStack gRPC server configuration
CHIRPSTACK_SERVER = "localhost:8080"  # Replace with your ChirpStack server address
CHIRPSTACK_API_TOKEN = "your_api_token_here"  # Replace with your API token

def get_chirpstack_client():
    # Create gRPC channel
    channel = grpc.insecure_channel(CHIRPSTACK_SERVER)

    # Add authentication metadata
    def auth_interceptor(metadata, callback):
        metadata.append(("authorization", f"Bearer {CHIRPSTACK_API_TOKEN}"))
        callback(metadata, None)

    # Create gRPC client with interceptor
    client = grpc.intercept_channel(channel, grpc.metadata_call_credentials(auth_interceptor))
    return api.ApplicationServiceStub(client)