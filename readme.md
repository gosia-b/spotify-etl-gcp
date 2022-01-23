Project based on a series of [YouTube videos](https://www.youtube.com/watch?v=dvviIUKwH7o&list=WL&index=2) + automated by moving to GCP.  
In `useful_links.md` I keep videos and documentation that helped me.

# Overview
Folder `cloud_functions` contains files to upload to Google Cloud Functions.  
In my case, this function is invoked once a day by a Cloud Scheduler job.  
It connects to Spotify API and gets the data about songs I played in last 24 hours. Then saves this data to a MySQL database set up in Cloud SQL.  

<p align="center">
<img width="100%" src="https://raw.githubusercontent.com/gosia-b/spotify-etl/master/gcp_architecture.PNG">
</p>

# Connection to the database
- Cloud Functions can connect to Cloud SQL over private IP, via a Serverless VPC Access connector (which must be in the same VPC network as the Cloud SQL instance).
- You can connect to Cloud SQL from a local machine using a database client over public IP.
