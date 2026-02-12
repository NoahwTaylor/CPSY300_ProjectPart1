FROM python:3.14.2

WORKDIR D:\diet_analysis

COPY data_analysis.py .

COPY All_Diets.csv .

RUN pip install pandas
RUN pip install seaborn
RUN pip install matplotlib

RUN mkdir -p visualizations


CMD ["python3", "data_analysis.py"]
