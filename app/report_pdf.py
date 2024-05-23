from . import forms, models
from .views import get_form_of_land_counts, get_source_of_seed_counts, get_training_received_counts, get_transport_means_counts, get_main_channel_of_selling_counts, get_main_outlet_counts, get_distance_to_market_analysis, get_transport_cost_analysis
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from .models import DataOne
from django.db.models import Count
import json


def generate_report(request):
    # Get the counts of people who received training categorized by type
    total_records = models.DataOne.objects.all().count()
    counts_dict = get_training_received_counts()
    form_of_land_access = get_form_of_land_counts()
    source_of_seed = get_source_of_seed_counts()
    transport_means = get_transport_means_counts()
    main_channel_of_selling = get_main_channel_of_selling_counts()
    main_outlet = get_main_outlet_counts()
    distance_to_market = get_distance_to_market_analysis()
    transport_cost = get_transport_cost_analysis()
    print(total_records)


    context = {
        "counts_dict": clean_dictionary(counts_dict),
        "form_of_land_access": clean_dictionary(form_of_land_access),
        "source_of_seed": clean_dictionary(source_of_seed),
        "transport_means": clean_dictionary(transport_means),
        "total_records": total_records,
        "main_channel_of_selling": main_channel_of_selling,
        "main_outlet": main_outlet,
        "distance_to_market": distance_to_market,
        "transport_cost": transport_cost,
    }

    # Render the template to a PDF
    html_string = render_to_string("generate_pdf.html", context)
    html = HTML(string=html_string)
    pdf_content = html.write_pdf()

    # Create an HTTP response with the PDF content and inline disposition
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="generate_pdf.pdf"'

    return response

def clean_key(key):
    """Remove underscores from the key."""
    return key.replace('_', ' ')

def clean_dictionary(dictionary):
    """Clean up the keys in a dictionary by removing underscores."""
    return {clean_key(k): v for k, v in dictionary.items()}
