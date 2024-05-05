from datetime import datetime
import random


def generate_po_number(vendor_id):

    random_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
    po_number = f"po_{vendor_id}_{random_number}"
    return po_number


def format_date(sdate=None):
    if sdate == None:
        return sdate

    return datetime.strptime(sdate, "%d-%m-%Y")


