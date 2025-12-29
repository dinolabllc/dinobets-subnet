from dotenv import load_dotenv
import os

load_dotenv()

NETWORK = os.getenv('NETWORK', 'test')
API_ROOT = 'https://bittensor.dinobets.io' if NETWORK == 'finney' else 'https://stagingbittensor.dinobets.io'
SEVER_SEED = os.getenv('SERVER_SEED', '19c7cd7a575130d3d7c93bbbd3e50296ac7d4b8fc608347009bde24eef19b798')
