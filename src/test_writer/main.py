import os
import argparse
from dotenv import load_dotenv
from test_writer.test_writer_crew import TestWriterCrew


# Load .env file for OpenAI key and other config
load_dotenv()

# Create required directories
os.makedirs('memory', exist_ok=True)
os.makedirs('temp', exist_ok=True)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to file or folder to test")
    parser.add_argument("--test-command", help="Command to run test (optional)", default=None)
    return parser.parse_args()

def run():
    args = parse_args()
    crew = TestWriterCrew()

    if os.path.isfile(args.path):
        crew.run_file(args.path, args.test_command)
    elif os.path.isdir(args.path):
        crew.run_folder(args.path, args.test_command)
    else:
        print(f"❌ Path does not exist: {args.path}")

if __name__ == "__main__":
    run()
