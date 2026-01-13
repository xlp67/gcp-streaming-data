import argparse
import logging
import json
import datetime
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, SetupOptions, StandardOptions
from google.cloud import bigtable

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

class ParseAndFilterFn(beam.DoFn):
    def process(self, element):
        try:
            record = json.loads(element.decode("utf-8"))
            if not record:
                return

            record['processed_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            yield record

        except (json.JSONDecodeError, ValueError) as e:
            logging.error(f"Erro de Parse: {e}")

class WriteToBigtable(beam.DoFn):
    def __init__(self, project_id, instance_id, table_id):
        self.project_id = project_id
        self.instance_id = instance_id
        self.table_id = table_id
        self.batcher = None
        self.table = None

    def setup(self):
        client = bigtable.Client(project=self.project_id, admin=False)
        instance = client.instance(self.instance_id)
        self.table = instance.table(self.table_id)
        self.batcher = self.table.mutations_batcher(flush_count=100, max_mutation_bytes=1048576)

    def process(self, element):
        try:
            row_key = f"{element['sensor_id']}#{element['timestamp']}".encode('utf-8')
            row = self.table.row(row_key)
            cf_id = "cf1"
            for key, value in element.items():
                row.set_cell(
                    cf_id,
                    key.encode('utf-8'),
                    str(value).encode('utf-8') 
                )
            self.batcher.mutate(row)

        except Exception as e:
            logging.error(f"Erro ao adicionar no batch: {e}")

    def finish_bundle(self):
        if self.batcher:
            self.batcher.flush()

    def teardown(self):
        if self.batcher:
            self.batcher.flush()

def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--project_id', required=True)
    parser.add_argument('--subscription', required=True)
    parser.add_argument('--bigtable_instance', required=True)
    parser.add_argument('--bigtable_table', required=True)
    known_args, pipeline_args = parser.parse_known_args(argv)
    options = PipelineOptions(pipeline_args)
    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = known_args.project_id
    options.view_as(StandardOptions).streaming = True
    options.view_as(SetupOptions).save_main_session = True
    with beam.Pipeline(options=options) as p:
        (
            p
            | "ReadPubSub" >> beam.io.ReadFromPubSub(subscription=known_args.subscription)
            | "ProcessElement" >> beam.ParDo(ParseAndFilterFn())
            | "WriteToBigtable" >> beam.ParDo(WriteToBigtable(
                project_id=known_args.project_id,
                instance_id=known_args.bigtable_instance,
                table_id=known_args.bigtable_table
            ))
        )

if __name__ == "__main__":
    run()