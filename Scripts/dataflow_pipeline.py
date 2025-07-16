import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions, GoogleCloudOptions, SetupOptions
import json

class ParseMessageFn(beam.DoFn):
    def process(self, element):
        data = json.loads(element.decode("utf-8"))
        yield {
            "user_id": data["user_id"],
            "action": data["action"],
            "timestamp": data["timestamp"]
        }

PROJECT_ID = "bootcampproject-5-465900"
REGION = "us-central1"
BUCKET = "stream-raw-backup-bootcampproject-5-465900"
TOPIC = f"projects/{PROJECT_ID}/topics/stream-topic"
BQ_TABLE = f"{PROJECT_ID}:stream_dataset.stream_table"
TEMPLATE_PATH = f"gs://{BUCKET}/templates/streaming_dataflow_template.json"

options = PipelineOptions(
    streaming=True,
    project=PROJECT_ID,
    region=REGION,
    job_name="streaming-dataflow-job",
    temp_location=f"gs://{BUCKET}/temp",
    save_main_session=True,
    template_location=TEMPLATE_PATH   # Add this line to create template
)

options.view_as(StandardOptions).runner = "DataflowRunner"
options.view_as(SetupOptions).save_main_session = True
gcp_options = options.view_as(GoogleCloudOptions)
gcp_options.labels = {"env": "prod", "team": "bootcamp"}
gcp_options.staging_location = f"gs://{BUCKET}/staging"

with beam.Pipeline(options=options) as p:
    (
        p
        | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(topic=TOPIC)
        | "Parse JSON" >> beam.ParDo(ParseMessageFn())
        | "Write to BigQuery" >> beam.io.WriteToBigQuery(
            BQ_TABLE,
            schema="user_id:STRING, action:STRING, timestamp:STRING",
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
        )
    )

if __name__ == "__main__":
    import apache_beam as beam
    from apache_beam.runners.dataflow import DataflowRunner
    from apache_beam.options.pipeline_options import PipelineOptions

    options = PipelineOptions([
        "--runner=DataflowRunner",
        "--project=bootcampproject-5-465900",
        "--region=us-central1",
        "--staging_location=gs://stream-raw-backup-bootcampproject-5-465900/staging",
        "--temp_location=gs://stream-raw-backup-bootcampproject-5-465900/temp",
        "--template_location=gs://stream-raw-backup-bootcampproject-5-465900/templates/streaming-template.json",
        "--save_main_session",
        "--streaming"
    ])

    p = beam.Pipeline(options=options)
    # Your pipeline code here (already defined above)
    ...
    p.run()
