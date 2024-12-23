# Spotify_Data_Pipeline
This end-to-end pipeline will fetch data using the Spotify API and AWS Lambda scheduled daily using an Event Trigger and store it as a CSV in AWS S3 Bucket. This data will then be transformed using a Jupyter Notebook and sent to a Postgres database staging table. The staging tables have defined Functions and Triggers that are activated once the data is inserted into their respective tables based on Snowflake schema design.

Pipeline Design
![Spotify Data Pipeline](https://github.com/user-attachments/assets/b4ed2571-e162-41ce-816f-a06614257084)

Databse Table ERD
![Postgre Table ERD](https://github.com/user-attachments/assets/ceda1c7e-5be4-4908-a162-7ae33768c310)
