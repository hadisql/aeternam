# middleware.py

from datetime import datetime
import subprocess
from django.contrib.auth import logout


class SessionExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request
        response = self.get_response(request)

        # Check if the session has expired
        if 'test' in request.session:
            expiry_time = request.session.get('expiry_time') # str format
            print(f"EXPIRY TIME -> {expiry_time}")
            expiry_time = datetime.strptime(expiry_time.replace('"',''),"%Y-%m-%d %H:%M:%S.%f") # datetime format
            current_time = datetime.now()
            print(f"current_time.timestamp() -> {current_time.timestamp()} / expiry_time.timestamp() -> {expiry_time.timestamp()}")
            if current_time.timestamp() > expiry_time.timestamp():
                # Session has expired, execute the script
                try:
                    #subprocess.run(['./fake_data_test.sh'], check=True)
                    logout(request)
                except subprocess.CalledProcessError as e:
                    # Handle script execution errors
                    pass

        return response
