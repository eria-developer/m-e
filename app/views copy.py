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


def home(request):
    return render(request, "index.html")


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


def process_data(request, pk):
    uploaded_file = get_object_or_404(models.UploadedFile, pk=pk)
    file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.file.name)

    # reading the excel file 
    df = pd.read_excel(file_path)

    # cleaning the data 
    df_cleaned = clean_data(df)

    # saving the cleaned data to the db
    save_data_to_db(df_cleaned, uploaded_file)
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