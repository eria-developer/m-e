# from PIL import Image
# from io import BytesIO
# import tempfile
# from . import forms, models
from .views import get_form_of_land_counts, get_source_of_seed_counts, get_training_received_counts, get_transport_means_counts
# import os
# from django.core.files.storage import default_storage
# from django.shortcuts import render
# from django.http import FileResponse, HttpResponse
# from weasyprint import HTML
# from django.template.loader import render_to_string
# from.models import DataOne
# from django.db.models import Count
# from collections import defaultdict
# import json


# # def generate_report(request):
# #     # Get the counts of people who received training categorized by type
# #     counts_dict = get_training_received_counts()
# #     form_of_land_access = get_form_of_land_counts()
# #     source_of_seed = get_source_of_seed_counts()
# #     transport_means = get_transport_means_counts()

# #     # Pie chart configuration
# #     # Aggregate transport means data
# #     transport_data = models.DataOne.objects.values('major_transport_means').annotate(count=Count('major_transport_means')).order_by('-count')

# #     # Prepare data for the pie chart
# #     piechart_labels = [entry['major_transport_means'] for entry in transport_data]
# #     piechart_counts = [entry['count'] for entry in transport_data]

# #     # Doughnut chart configuration
# #     # Aggregate for main channel of selling
# #     channel_of_selling_data = models.DataOne.objects.values('main_channel_of_selling').annotate(count=Count('main_channel_of_selling')).order_by('-count')

# #     # Prepare data for the doughnut chart
# #     doughnut_labels = [entry['main_channel_of_selling'] for entry in channel_of_selling_data]
# #     doughnut_counts = [entry['count'] for entry in channel_of_selling_data]

# #     # Major transition method
# #     major_transition_method = models.DataOne.objects.values('major_transition_method').annotate(count=Count('major_transition_method')).order_by('-count')

# #     # Prepare data for the doughnut chart
# #     major_transition_method_labels = [entry['major_transition_method'] for entry in major_transition_method]
# #     major_transition_method_counts = [entry['count'] for entry in major_transition_method]


# #     context = {
# #         "counts_dict": clean_dictionary(counts_dict),
# #         "form_of_land_access": clean_dictionary(form_of_land_access),
# #         "source_of_seed": clean_dictionary(source_of_seed),
# #         "transport_means": clean_dictionary(transport_means),
# #         "piechart_labels_json": json.dumps(piechart_labels),
# #         "piechart_counts_json": json.dumps(piechart_counts),
# #         "doughnut_labels": doughnut_labels,
# #         "doughnut_counts": doughnut_counts,
# #         "major_transition_method_labels": major_transition_method_labels,
# #         "major_transition_method_counts": major_transition_method_counts,
# #     }

# #     # Render the template to a PDF
# #     with default_storage.open('temporary_file.pdf', 'wb') as temp_file:
# #         html_string = render_to_string("generate_pdf.html", context)
# #         HTML(string=html_string).write_pdf(temp_file)

# #     # Read the PDF file into memory
# #     with open(temp_file.name, 'rb') as pdf_file:
# #         pdf_content = pdf_file.read()

# #     # Create an HTTP response with the PDF content and inline disposition
# #     response = HttpResponse(pdf_content, content_type='application/pdf')
# #     response['Content-Disposition'] = 'inline; filename="generate_pdf.pdf"'

# #     return response

# def generate_report(request):
#     # Get the counts of people who received training categorized by type
#     counts_dict = get_training_received_counts()
#     form_of_land_access = get_form_of_land_counts()
#     source_of_seed = get_source_of_seed_counts()
#     transport_means = get_transport_means_counts()

#     # Pie chart configuration
#     # Aggregate transport means data
#     transport_data = models.DataOne.objects.values('major_transport_means').annotate(count=Count('major_transport_means')).order_by('-count')

#     # Prepare data for the pie chart
#     piechart_labels = [entry['major_transport_means'] for entry in transport_data]
#     piechart_counts = [entry['count'] for entry in transport_data]

#     # Doughnut chart configuration
#     # Aggregate for main channel of selling
#     channel_of_selling_data = models.DataOne.objects.values('main_channel_of_selling').annotate(count=Count('main_channel_of_selling')).order_by('-count')

#     # Prepare data for the doughnut chart
#     doughnut_labels = [entry['main_channel_of_selling'] for entry in channel_of_selling_data]
#     doughnut_counts = [entry['count'] for entry in channel_of_selling_data]

#     # Major transition method
#     major_transition_method = models.DataOne.objects.values('major_transition_method').annotate(count=Count('major_transition_method')).order_by('-count')

#     # Prepare data for the doughnut chart
#     major_transition_method_labels = [entry['major_transition_method'] for entry in major_transition_method]
#     major_transition_method_counts = [entry['count'] for entry in major_transition_method]

#     context = {
#         "counts_dict": clean_dictionary(counts_dict),
#         "form_of_land_access": clean_dictionary(form_of_land_access),
#         "source_of_seed": clean_dictionary(source_of_seed),
#         "transport_means": clean_dictionary(transport_means),
#         "piechart_labels_json": json.dumps(piechart_labels),
#         "piechart_counts_json": json.dumps(piechart_counts),
#         "doughnut_labels": doughnut_labels,
#         "doughnut_counts": doughnut_counts,
#         "major_transition_method_labels": major_transition_method_labels,
#         "major_transition_method_counts": major_transition_method_counts,
#     }

#     # Render the template to HTML
#     html_string = render_to_string("generate_pdf.html", context)

#     # Convert HTML to PDF using WeasyPrint
#     pdf_file_path = 'temporary_file.pdf'
#     HTML(string=html_string).write_pdf(target=pdf_file_path)

#     # Read the PDF file into memory
#     with open(pdf_file_path, 'rb') as pdf_file:
#         pdf_content = pdf_file.read()

#     # Create an HTTP response with the PDF content and inline disposition
#     response = HttpResponse(pdf_content, content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; filename="generate_pdf.pdf"'

#     return response


# def clean_key(key):
#     """Remove underscores from the key."""
#     return key.replace('_', ' ')

# def clean_dictionary(dictionary):
#     """Clean up the keys in a dictionary by removing underscores."""
#     return {clean_key(k): v for k, v in dictionary.items()}


# import matplotlib.pyplot as plt
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

# def generate_pie_chart(labels, sizes, chart_path):
#     fig, ax = plt.subplots()
#     ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
#     ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#     plt.savefig(chart_path)
#     plt.close()

def generate_report(request):
    # Get the counts of people who received training categorized by type
    counts_dict = get_training_received_counts()
    form_of_land_access = get_form_of_land_counts()
    source_of_seed = get_source_of_seed_counts()
    transport_means = get_transport_means_counts()

    # Pie chart configuration
    # Aggregate transport means data
    transport_data = DataOne.objects.values('major_transport_means').annotate(count=Count('major_transport_means')).order_by('-count')

    # Prepare data for the pie chart
    piechart_labels = [entry['major_transport_means'] for entry in transport_data]
    piechart_counts = [entry['count'] for entry in transport_data]

    # Doughnut chart configuration
    # Aggregate for main channel of selling
    channel_of_selling_data = DataOne.objects.values('main_channel_of_selling').annotate(count=Count('main_channel_of_selling')).order_by('-count')

    # Prepare data for the doughnut chart
    doughnut_labels = [entry['main_channel_of_selling'] for entry in channel_of_selling_data]
    doughnut_counts = [entry['count'] for entry in channel_of_selling_data]

    # Major transition method
    major_transition_method = DataOne.objects.values('major_transition_method').annotate(count=Count('major_transition_method')).order_by('-count')

    # Prepare data for the doughnut chart
    major_transition_method_labels = [entry['major_transition_method'] for entry in major_transition_method]
    major_transition_method_counts = [entry['count'] for entry in major_transition_method]

    # Create charts directory if it does not exist
    charts_dir = os.path.join(settings.MEDIA_ROOT, 'charts')
    os.makedirs(charts_dir, exist_ok=True)

    # Paths to save charts
    pie_chart_path = os.path.join(charts_dir, 'transport_means_pie_chart.png')
    doughnut_chart_path = os.path.join(charts_dir, 'channel_of_selling_doughnut_chart.png')
    transition_method_chart_path = os.path.join(charts_dir, 'major_transition_method_doughnut_chart.png')

    # Generate charts
    # generate_pie_chart(piechart_labels, piechart_counts, pie_chart_path)
    # generate_pie_chart(doughnut_labels, doughnut_counts, doughnut_chart_path)
    # generate_pie_chart(major_transition_method_labels, major_transition_method_counts, transition_method_chart_path)

    context = {
        "counts_dict": clean_dictionary(counts_dict),
        "form_of_land_access": clean_dictionary(form_of_land_access),
        "source_of_seed": clean_dictionary(source_of_seed),
        "transport_means": clean_dictionary(transport_means),
        "pie_chart_path": pie_chart_path,
        "doughnut_chart_path": doughnut_chart_path,
        "transition_method_chart_path": transition_method_chart_path,
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
