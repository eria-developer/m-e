from django.shortcuts import render, redirect, get_object_or_404
from . import forms, models
import os
import pandas as pd
from django.conf import settings
import plotly.express as px
from plotly.offline import plot


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
    # data cleaning logic
    df = df.dropna()
    return df


def save_data_to_db(df, uploaded_file):
    cleaned_data = models.CleanedData(data=df.to_dict(orient="records"), uploaded_file=uploaded_file)
    cleaned_data.save()


def visualize_data(request, pk):
    cleaned_data = models.CleanedData.objects.get(pk=pk)
    df = pd.DataFrame(cleaned_data.data)
    
    # Calculate insights
    gender_counts = df['Res_gen'].value_counts().to_dict()
    marital_status_counts = df['Marital_status'].value_counts().to_dict()

    # Example visualization using Plotly
    if 'Res_age' in df.columns:
        fig = px.histogram(df, x='Res_age')
        plot_div = plot(fig, output_type='div')
    else:
        plot_div = "Column 'Res_age' not found in the data"

    context = {
        'plot_div': plot_div,
        'gender_counts': gender_counts,
        'marital_status_counts': marital_status_counts,
    }

    return render(request, 'visualization.html', context)


def profile(request):
    return render(request, "profile.html")


def signout(request):
    return render(request, "signin.html")