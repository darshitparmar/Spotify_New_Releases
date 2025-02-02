# Spotify_New_Releases
The Spotify New Releases data pipeline will fetch all new albums released and store them in an **S3 Bucket** as a CSV file, then push it downstream to **Postgres Database**. It is automated to run daily using **AWS Lambda**, **Event Triggers**, **PySpark**, and **PLSQL Functions and Triggers**.

## Pipeline Design
![Spotify Data Pipeline](https://github.com/user-attachments/assets/b4ed2571-e162-41ce-816f-a06614257084)

## Databse Table ERD
![Postgre Table ERD](https://github.com/user-attachments/assets/ceda1c7e-5be4-4908-a162-7ae33768c310)
