from django.shortcuts import render, redirect, get_object_or_404
from . import forms, models
import os
import pandas as pd
from django.conf import settings
import plotly.express as px
from plotly.offline import plot
from django.utils.timezone import now
from django.core.exceptions import ValidationError
import json
from math import isnan
from django.db.models import Count
from collections import defaultdict


def home(request):
    # Get the counts of people who received training categorized by type
    counts_dict = get_training_received_counts()
    context = {
        "counts_dict": counts_dict,
    }
    return render(request, "index.html", context)


def upload_data(request):
    if request.method == "POST":
        form = forms.UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            return redirect("process_data", pk=uploaded_file.pk)
    else:
        form = forms.UploadFileForm()
    context = {
        "form": form,
    }
    return render(request, "upload_data.html", context)


def process_data(request):
    return render(request, "success.html")


def clean_data(df):
    # replacing NaN with empty strings
    df = df.fillna("")
    return df


def save_data_to_db(df, uploaded_file):
    cleaned_data = models.CleanedData(data=df.to_dict(orient="records"), uploaded_file=uploaded_file)
    cleaned_data.save()




def visualize_data(request, pk):
    cleaned_data = models.CleanedData.objects.get(pk=pk)
    df = pd.DataFrame(cleaned_data.data)
    
    # Calculate insights
    training_received_counts = df['Training Received '].value_counts().to_dict()
    form_of_land_access_counts = df['Form of land access'].value_counts().to_dict()

    # Example visualization using Plotly
    if 'Training Received ' in df.columns:
        fig = px.histogram(df, x='Training Received ')
        plot_div = plot(fig, output_type='div')
    else:
        plot_div = "Column 'Training Received ' not found in the data"

    context = {
        'plot_div': plot_div,
        'training_received_counts': training_received_counts,
        'form_of_land_access_counts': form_of_land_access_counts,
    }

    return render(request, 'visualization.html', context)


def profile(request):
    return render(request, "profile.html")


def signout(request):
    return render(request, "signin.html")




# def upload_file(request):
#     if request.method == 'POST':
#         form = forms.UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             excel_file = request.FILES['file']
#             if excel_file.name.endswith('.xlsx'):
#                 df = pd.read_excel(excel_file)
#                 for index, row in df.iterrows():
#                     models.DataOne.objects.create(
#                         baseline_ID=row['Baseline_ID'],
#                         name=row['HHH name'],
#                         training_received=row['Training Received '],
#                         form_of_land_access=row['Form of land access'],
#                         source_of_seed=row['Source of seed'],
#                         main_channel_of_selling=row['Main channel of selling '],
#                         major_transition_method=row['Major transtion method'],
#                         main_outlet=row['Main outlet'],
#                         distance_to_market_km=row['Distance to market (km)'],
#                         major_transport_means=row['Major ransport means'],
#                         transport_cost=row['Transport cost']
#                     )
#                 return render(request, 'success.html')
#             else:
#                 context = {'form': form, 'error': 'Please upload a valid Excel file.'}
#                 return render(request, 'upload.html', context)
#     else:
#         form = forms.UploadFileForm()

#     context = {
#         "form": form,
#     }
#     return render(request, 'upload.html', context)


# import pandas as pd
# import numpy as np  # Import numpy for NaN values

# def upload_file(request):
#     if request.method == 'POST':
#         form = forms.UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             excel_file = request.FILES['file']
#             if excel_file.name.endswith('.xlsx'):
#                 df = pd.read_excel(excel_file)
                
#                 # Replace NaN values with 0
#                 df.fillna(0, inplace=True)

#                 for index, row in df.iterrows():
#                     models.DataOne.objects.create(
#                         baseline_ID=row['Baseline_ID'],
#                         name=row['HHH name'],
#                         training_received=row['Training Received '],
#                         form_of_land_access=row['Form of land access'],
#                         source_of_seed=row['Source of seed'],
#                         main_channel_of_selling=row['Main channel of selling '],
#                         major_transition_method=row['Major transtion method'],
#                         main_outlet=row['Main outlet'],
#                         distance_to_market_km=row['Distance to market (km)'],
#                         major_transport_means=row['Major ransport means'],
#                         transport_cost=row['Transport cost']
#                     )
#                 return render(request, 'success.html')
#             else:
#                 context = {'form': form, 'error': 'Please upload a valid Excel file.'}
#                 return render(request, 'upload.html', context)
#     else:
#         form = forms.UploadFileForm()

#     context = {
#         "form": form,
#     }
#     return render(request, 'upload.html', context)


def upload_file(request):
    if request.method == 'POST':
        form = forms.UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            if excel_file.name.endswith('.xlsx'):
                df = pd.read_excel(excel_file)

                # Replace NaN values with 0
                df.fillna(0, inplace=True)
                
                for index, row in df.iterrows():
                    baseline_id = row['Baseline_ID']
                    # Check if the record already exists
                    obj, created = models.DataOne.objects.get_or_create(baseline_ID=baseline_id)
                    # Update fields with new values
                    obj.name = row['HHH name']
                    obj.training_received = row['Training Received ']
                    obj.form_of_land_access = row['Form of land access']
                    obj.source_of_seed = row['Source of seed']
                    obj.main_channel_of_selling = row['Main channel of selling ']
                    obj.major_transition_method = row['Major transtion method']
                    obj.main_outlet = row['Main outlet']
                    obj.distance_to_market_km = row['Distance to market (km)']
                    obj.major_transport_means = row['Major ransport means']
                    obj.transport_cost = row['Transport cost']
                    # Save the object
                    obj.save()
                return redirect('process_data')
            else:
                context = {'form': form, 'error': 'Please upload a valid Excel file.'}
                return render(request, 'upload_data.html', context)
    else:
        form = forms.UploadFileForm()

    context = {
        "form": form,
    }
    return render(request, 'upload_data.html', context)


# def get_training_received_counts():
#     # Query to count the number of people who received training by type
#     training_received_counts = models.DataOne.objects.values('training_received').annotate(count=Count('training_received'))

#     # Dictionary to store the counts
#     counts_dict = {
#         'farmer': 0,
#         'consumer': 0,
#         'agro_input_dear': 0
#     }

#     # Update the counts dictionary with the results
#     for item in training_received_counts:
#         if item['training_received'] == 'Farmer':
#             counts_dict['Farmer'] = item['count']
#         elif item['training_received'] == 'Consumer ':
#             counts_dict['Consumer'] = item['count']
#         elif item['training_received'] == 'Agro input dear':
#             counts_dict['Agro input dear'] = item['count']

#     # print(f"Counts dictionary: {counts_dict}")
#     # print(f"Training received counts: {training_received_counts}")

#     return counts_dict


def get_training_received_counts():
    # Query to count the number of people who received training by type
    training_received_counts = models.DataOne.objects.values('training_received').annotate(count=Count('training_received'))

    # Initialize a dictionary to store the counts with renamed keys
    counts_dict = defaultdict(int)

    # Update the counts dictionary with the results
    for item in training_received_counts:
        if item['training_received'] == 'Farmer':
            counts_dict['farmer'] += item['count']
        elif item['training_received'] == 'Consumer ':
            counts_dict['consumer'] += item['count']
        elif item['training_received'] == 'Agro input dear':
            counts_dict['agro_input_dear'] += item['count']

    # Convert the defaultdict back to a regular dict if needed
    counts_dict = dict(counts_dict)
    print(f"counts dictionary: {counts_dict}")

    return counts_dict


# def upload_file(request):
#     if request.method == 'POST':
#         form = forms.UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             excel_file = request.FILES['file']
#             if excel_file.name.endswith('.xlsx'):
#                 df = pd.read_excel(excel_file)

#                 # Replace NaN values with 0
#                 df.fillna(0, inplace=True)
                
#                 for index, row in df.iterrows():
#                     baseline_id = row['Baseline_ID']
#                     # Check if the record already exists
#                     obj, created = models.DataOne.objects.get_or_create(baseline_ID=baseline_id)
#                     # Update fields with new values
#                     obj.name = row['HHH name']
#                     obj.training_received = row['Training Received ']
#                     obj.form_of_land_access = row['Form of land access']
#                     obj.source_of_seed = row['Source of seed']
#                     obj.main_channel_of_selling = row['Main channel of selling ']
#                     obj.major_transition_method = row['Major transtion method']
#                     obj.main_outlet = row['Main outlet']
#                     obj.distance_to_market_km = row['Distance to market (km)']
#                     obj.major_transport_means = row['Major ransport means']
#                     obj.transport_cost = row['Transport cost']
#                     # Save the object
#                     obj.save()

#                 # Get the counts of people who received training categorized by type
#                 counts_dict = get_training_received_counts()

#                 # Pass the counts to the template
#                 return render(request, 'success.html', {'counts_dict': counts_dict})
#             else:
#                 context = {'form': form, 'error': 'Please upload a valid Excel file.'}
#                 return render(request, 'upload_data.html', context)
#     else:
#         form = forms.UploadFileForm()

#     context = {
#         "form": form,
#     }
#     return render(request, 'upload_data.html', context)