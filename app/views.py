from django.shortcuts import render, redirect, get_object_or_404
from . import forms, models
import os
import pandas as pd
from django.conf import settings
# import plotly.express as px
# from plotly.offline import plot
from django.utils.timezone import now
from django.core.exceptions import ValidationError
import json
from math import isnan
from django.db.models import Count
from collections import defaultdict
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import AuthenticationForm


def user_signup(request):
    if request.method == "POST":
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = forms.CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "user_signup.html", context)


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "signin.html", context)



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

    # doughnu chart configuration
    # aggregate for main channel of selling
    channel_of_selling_data = models.DataOne.objects.values('main_channel_of_selling').annotate(count=Count('main_channel_of_selling')).order_by('-count')

    # preparing data for the doughnut
    doughnut_labels = [entry['main_channel_of_selling'] for entry in channel_of_selling_data]
    doughnut_counts = [entry['count'] for entry in channel_of_selling_data]

    # major transition method 
    major_transition_method = models.DataOne.objects.values('major_transition_method').annotate(count=Count('major_transition_method')).order_by('-count')

    # preparing data for the doughnut
    major_transition_method_labels = [entry['major_transition_method'] for entry in major_transition_method]
    major_transition_method_counts = [entry['count'] for entry in major_transition_method]


    context = {
        "counts_dict": counts_dict,
        "form_of_land_access": form_of_land_access,
        "source_of_seed": source_of_seed,
        "transport_means": transport_means,
        "piechart_labels": piechart_labels,
        "piechart_counts": piechart_counts,
        "doughnut_labels": doughnut_labels,
        "doughnut_counts": doughnut_counts,
        "major_transition_method_labels": major_transition_method_labels,
        "major_transition_method_counts": major_transition_method_counts,
    }
    return render(request, "index.html", context)


def process_data(request):
    return render(request, "success.html")


def clean_data(df):
    # replacing NaN with empty strings
    df = df.fillna("")
    return df


def save_data_to_db(df, uploaded_file):
    cleaned_data = models.CleanedData(data=df.to_dict(orient="records"), uploaded_file=uploaded_file)
    cleaned_data.save()


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
    # print(f"counts dictionary: {counts_dict}")

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
    # print(f"counts dictionary: {form_of_land_access_counts}")

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
    # print(f"counts dictionary: {source_of_seed_counts}")

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
    # print(f"counts dictionary: {transport_means_counts}")

    return counts_dict

def get_main_channel_of_selling_counts():
    # Query to count the number of people who received training by type
    main_channel_of_selling_counts = models.DataOne.objects.values('main_channel_of_selling').annotate(count=Count('main_channel_of_selling'))

    # Initialize a dictionary to store the counts with renamed keys
    counts_dict = defaultdict(int)

    # Update the counts dictionary with the results
    for item in main_channel_of_selling_counts:
        if item['main_channel_of_selling'] == 'Directly to consumer (village sale)':
            counts_dict['Directly to consumer (village sale)'] += item['count']
        elif item['main_channel_of_selling'] == 'To–primary wholesaler–secondary wholesaler–  retailer– consumer (distant market)':
            counts_dict['To–primary wholesaler–secondary wholesaler–  retailer– consumer (distant market)'] += item['count']
        elif item['main_channel_of_selling'] == 'To retailer–consumer (local sale)':
            counts_dict['To retailer–consumer (local sale)'] += item['count']
        elif item['main_channel_of_selling'] == 'To broker–retailer–consumer':
            counts_dict['To broker–retailer–consumer'] += item['count']
        elif item['main_channel_of_selling'] == 'To Trader–broker–retailer–consumer.':
            counts_dict['To Trader–broker–retailer–consumer.'] += item['count']

    # Convert the defaultdict back to a regular dict if needed
    counts_dict = dict(counts_dict)

    return counts_dict

def get_main_outlet_counts():
    # Query to count the number of people who received training by type
    main_outlet_counts = models.DataOne.objects.values('main_outlet').annotate(count=Count('main_outlet'))

    # Initialize a dictionary to store the counts with renamed keys
    counts_dict = defaultdict(int)

    # Update the counts dictionary with the results
    for item in main_outlet_counts:
        if item['main_outlet'] == 'At gazetted market within the sub county':
            counts_dict['At gazetted market within the sub county'] += item['count']
        elif item['main_outlet'] == 'At the farmgate':
            counts_dict['At the farmgate'] += item['count']

    # Convert the defaultdict back to a regular dict if needed
    counts_dict = dict(counts_dict)

    return counts_dict

def get_distance_to_market_analysis():
    # Define the ranges
    distance_ranges = {
        '0-2': (0, 2),
        '3-5': (3, 5),
        '6-10': (6, 10),
        '11-15': (11, 15),
        '16-20': (16, 20),
        '21-25': (21, 25),
        '26-30': (26, 30),
    }
    
    # Initialize a dictionary to store the counts for each range
    distance_counts = defaultdict(int)
    
    # Fetch all records
    all_records = models.DataOne.objects.all()
    
    # Iterate through the records and categorize them
    for record in all_records:
        distance = record.distance_to_market_km
        if distance is not None:  # Check if distance is not None
            for range_name, (min_val, max_val) in distance_ranges.items():
                if min_val <= distance <= max_val:
                    distance_counts[range_name] += 1
                    break

    # Convert the defaultdict back to a regular dict
    distance_counts = dict(distance_counts)
    
    return distance_counts

def get_transport_cost_analysis():
    # Define the ranges
    transport_cost_ranges = {
        '1-5000': (1, 5000),
        '5001-10000': (5001, 10000),
        '10001-15000': (10001, 15000),
        '15001-20000': (15001, 20000),
        '20001-25000': (20001, 25000),
        '25001-50000': (25001, 50000),
        '50001-100000': (50001, 100000),
    }
    
    # Initialize a dictionary to store the counts for each range
    transport_cost_counts = defaultdict(int)
    
    # Fetch all records
    all_records = models.DataOne.objects.all()
    
    # Iterate through the records and categorize them
    for record in all_records:
        cost = record.transport_cost
        if cost is not None:  # Check if transport cost is not None
            for range_name, (min_val, max_val) in transport_cost_ranges.items():
                if min_val <= cost <= max_val:
                    transport_cost_counts[range_name] += 1
                    break

    # Convert the defaultdict back to a regular dict
    transport_cost_counts = dict(transport_cost_counts)
    
    return transport_cost_counts
