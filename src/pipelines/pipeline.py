import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import os

TOPIC_ID = f"projects/{os.getenv('PROJECT_ID')}/subscriptions/iot-sub"
BUCKET = "gs://seu-bucket-de-saida"

options = PipelineOptions(
    runner='DataflowRunner',
    project=os.getenv('PROJECT_ID'),
    temp_location=f'{BUCKET}/temp',
    region='us-central1',
    streaming=True 
)

class WriteToBigtableFn(beam.DoFn):
    def __init__(self, project_id, instance_id, table_id):
        self.project_id = project_id
        self.instance_id = instance_id
        self.table_id = table_id

    def process(self, element):
        from google.cloud import bigtable
        client = bigtable.Client(project=self.project_id, admin=True)
        instance = client.instance(self.instance_id)
        table = instance.table(self.table_id)

        row_key = "sensor_data_#1".encode() 
        row = table.direct_row(row_key)
        row.set_cell("cf1", "raw_data".encode(), element.encode())
        row.commit()
        yield element

with beam.Pipeline(options=options) as p:
    raw_data = (
        p
        | 'ReadFromPubSub' >> beam.io.ReadFromPubSub(subscription=TOPIC_ID)
        | 'Decode' >> beam.Map(lambda x: x.decode('utf-8'))
    )

    # Caminho 1: Salvar no Google Cloud Storage (Texto)
    raw_data | 'WriteToGCS' >> beam.io.WriteToText(f'{BUCKET}/output/iot_log')

    # Caminho 2: Salvar no Bigtable
    # raw_data | 'WriteToBT' >> beam.ParDo(WriteToBigtableFn(project_id, 'iot-instance', 'iot-data'))