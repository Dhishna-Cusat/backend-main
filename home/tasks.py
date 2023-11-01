import pandas as pd
import io
import requests
from celery import shared_task

from .models import Event


import os
import django
from dhishnaserver import settings  # Replace 'your_project_name' with your actual project name

# Set the Django settings module


@shared_task
def fetch_and_update():
    # Your task logic here
    pass



if __name__ == "__main__":

    # excel_file_url = "https://www.yepdesk.com/rest/event/attendees/export?&eventid=65292bac46e0fb0001c6f6c7"
    #
    # response = requests.get(excel_file_url)
    #
    # if response.status_code == 200:
    #     excel_data = response.content
    #
    #     with open("sample.xlsx", "wb") as f:
    #         f.write(excel_data)
    #
    #     df = pd.read_excel(io.BytesIO(excel_data))
    #
    # else:
    #     print("Failed to download the file.")
    # df = pd.read_excel("sample.xlsx")
    pass

