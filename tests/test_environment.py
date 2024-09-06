import sys
import numpy
import requests

def test_environment():
    # Print Python version
    print(f"Python Version: {sys.version}")

    # Check if numpy is installed
    try:
        import numpy
        print(f"NumPy Version: {numpy.__version__}")
    except ImportError:
        print("NumPy is not installed.")

    # Check if requests is installed
    try:
        import requests
        print(f"Requests Version: {requests.__version__}")
    except ImportError:
        print("Requests is not installed.")

if __name__ == "__main__":
    test_environment()
