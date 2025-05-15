from modules import *
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
SERVER_IP = os.getenv("SERVER_IP")

def main():
    print(SERVER_IP)

if __name__ == "__main__":
    main()