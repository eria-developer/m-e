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
    form_of_land_access = get_form_of_land_counts()
    source_of_seed = get_source_of_seed_counts()
    transport_means = get_transport_means_counts()

#    piechart configuration
    # Aggregate transport means data
    transport_data = models.DataOne.objects.values('major_transport_means').annotate(count=Count('major_transport_means')).order_by('-count')

    # Prepare data for the pie chart
    piechart_labels = [entry['major_transport_means'] for entry in transport_data]
    piechart_counts = [entry['count'] for entry in transport_data]

    context = {
        "counts_dict": counts_dict,
        "form_of_land_access": form_of_land_access,
        "source_of_seed": source_of_seed,
        "transport_means": transport_means,
        "piechart_labels": piechart_labels,
        "piechart_counts": piechart_counts,
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


def get_form_of_land_counts():
    # Query to count the number of people who received training by type
    form_of_land_access_counts = models.DataOne.objects.values('form_of_land_access').annotate(count=Count('form_of_land_access'))

    # Initialize a dictionary to store the counts with renamed keys
    counts_dict = defaultdict(int)

    # Update the counts dictionary with the results
    for item in form_of_land_access_counts:
        if item['form_of_land_access'] == 'Own land':
            counts_dict['own_land'] += item['count']
        elif item['form_of_land_access'] == 'Hired land':
            counts_dict['hired_land'] += item['count']
        elif item['form_of_land_access'] == 'Family land':
            counts_dict['family_land'] += item['count']

    # Convert the defaultdict back to a regular dict if needed
    counts_dict = dict(counts_dict)
    print(f"counts dictionary: {form_of_land_access_counts}")

    return counts_dict


def get_source_of_seed_counts():
    # Query to count the number of people who received training by type
    source_of_seed_counts = models.DataOne.objects.values('source_of_seed').annotate(count=Count('source_of_seed'))

    # Initialize a dictionary to store the counts with renamed keys
    counts_dict = defaultdict(int)

    # Update the counts dictionary with the results
    for item in source_of_seed_counts:
        if item['source_of_seed'] == 'Agrodealer':
            counts_dict['agrodealer'] += item['count']
        elif item['source_of_seed'] == 'Fellow farmer':
            counts_dict['fellow_farmer'] += item['count']

    # Convert the defaultdict back to a regular dict if needed
    counts_dict = dict(counts_dict)
    print(f"counts dictionary: {source_of_seed_counts}")

    return counts_dict


def get_transport_means_counts():
    # Query to count the number of people who received training by type
    transport_means_counts = models.DataOne.objects.values('major_transport_means').annotate(count=Count('major_transport_means'))

    # Initialize a dictionary to store the counts with renamed keys
    counts_dict = defaultdict(int)

    # Update the counts dictionary with the results
    for item in transport_means_counts:
        if item['major_transport_means'] == 'Motorcycle':
            counts_dict['motorcycle'] += item['count']
        elif item['major_transport_means'] == 'Tukutuku':
            counts_dict['tukutuku'] += item['count']
        elif item['major_transport_means'] == 'Bicycle':
            counts_dict['bicycle'] += item['count']
        elif item['major_transport_means'] == 'Walking on foot':
            counts_dict['walking_on_foot'] += item['count']
        elif item['major_transport_means'] == 'Track':
            counts_dict['track'] += item['count']

    # Convert the defaultdict back to a regular dict if needed
    counts_dict = dict(counts_dict)
    print(f"counts dictionary: {transport_means_counts}")

    return counts_dict







