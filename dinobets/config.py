from dotenv import load_dotenv
import os

load_dotenv()

NETWORK = os.getenv('NETWORK', 'test')
# API_ROOT = 'https://bittensor.dinobets.io' if NETWORK == 'finney' else 'https://stagingbittensor.dinobets.io'
API_ROOT = 'http://localhost:5001'
SEVER_SEED = os.getenv('SERVER_SEED', '4F8D2EF3C9E109F9E8A8B52B872')
