# middleware.py

from datetime import datetime
import subprocess
from django.contrib.auth import logout
from django.contrib import messages
import os
from django.utils.translation import gettext_lazy as _


import logging
logger = logging.getLogger(__name__)

DEMO_DELAY = os.getenv('DEMO_DELAY_SECONDS')

class SessionExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request
        response = self.get_response(request)

        # Check if the session has expired
        if 'expiry_time' in request.session:
            expiry_time = request.session.get('expiry_time') # str format
            logger.info(f"EXPIRY TIME -> {expiry_time}")
            expiry_time = datetime.strptime(expiry_time.replace('"',''),"%Y-%m-%d %H:%M:%S.%f") # datetime format
            current_time = datetime.now()
            # logger.info(f"current_time.timestamp() -> {current_time.timestamp()} / expiry_time.timestamp() -> {expiry_time.timestamp()}")
            logger.info(f"remaining time before session expires: {int(expiry_time.timestamp()-current_time.timestamp())} seconds")
            if current_time.timestamp() > expiry_time.timestamp():
                # Session has expired, execute the script
                try:
                    #subprocess.run(['./fake_data_test.sh'], check=True)
                    logout(request)
                    messages.WARNING(_("You were logged out of the demo session."))
                    logger.info(f"User logged out of demo session after {int(int(DEMO_DELAY)/60)} mins.")
                except subprocess.CalledProcessError as e:
                    # Handle script execution errors
                    pass

        return response
