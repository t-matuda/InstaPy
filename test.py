""" Quickstart script for InstaPy usage """

# imports
from instapy import InstaPy
from instapy import smart_run
from instapy import set_workspace
from instapy.util import get_full_name
import sys

# set workspace folder at desired location (default is at your home folder)
set_workspace(path=None)

# get an InstaPy session!
insta_username = sys.argv[1]  # <- enter username here
insta_password = sys.argv[2]  # <- enter password here
session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=False,
                  bypass_suspicious_attempt=True)

with smart_run(session):
    result = session.grab_followers('kaba_proj', 10)
    print(result)