import io
import math
import os

import django
import pandas as pd
import requests
from celery import shared_task
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dhishnaserver.settings")

django.setup()

from home.models import Event, Registration, CA


# Set the Django settings module


def fetch_and_update():
    today = timezone.now()
    events = Event.objects.filter(end_date__gt=today)
    for event in events:
        excel_file_url = "https://www.yepdesk.com/rest/event/attendees/export?&eventid=" + event.yep_id
        response = requests.get(excel_file_url)
        if response.status_code == 200:
            excel_data = response.content
            df = pd.read_excel(io.BytesIO(excel_data))

            for index, row in df.iloc[event.last_processed:].iterrows():
                booking_id = row['BOOKING ID']
                ticket_id = row['TICKET ID']
                name = row['NAME']
                email = row['EMAIL']
                phone = row['PHONE']
                status = row['PAYMENT STATUS']
                no = row['NO OF TICKETS PURCHASED']
                total = row['TOTAL PAYMENT'].split(" ")[0]
                referral = None
                if 'REFERRAL CODE' in df.columns and isinstance(row['REFERRAL CODE'], str):
                    referral = row['REFERRAL CODE']
                    if referral.startswith('#'):
                        referral = referral[1:]
                    referral = referral.upper()

                registration = Registration(
                    booking_id=booking_id,
                    ticket_id=ticket_id,
                    event=event,
                    name=name,
                    email=email,
                    phone=phone,
                    number_of_tickets=no,
                    payment_status=status,
                    total_payment=total,
                    referral=referral
                )
                registration.save()
            event.last_processed = df.shape[0]
            event.save()
    sql_query = "SELECT id, referral, SUM(number_of_tickets) AS total_tickets_sold FROM home_registration where referral IS NOT NULL GROUP BY referral, id ;"

    # Execute the query
    selected_data = Registration.objects.raw(sql_query)

    # Iterate through the selected data
    for registration in selected_data:
        cas = CA.objects.filter(referral__iexact=registration.referral)
        if cas:
            ca = cas[0]
            ca.points = registration.total_tickets_sold
            ca.save()


if __name__ == "__main__":
    fetch_and_update()
