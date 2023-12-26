import asyncio
import time
import uuid

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from utils.db_access import DBAccess
from pathlib import Path
from utils.csv_to_xml_converter import CSVtoXMLConverter


NUM_XML_PARTS = int(os.environ.get("NUM_XML_PARTS", 1))

def get_csv_files_in_input_folder():
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(CSV_INPUT_PATH) for f in filenames if
            os.path.splitext(f)[1] == '.csv']
#alterei aqui
def generate_unique_file_name(directory, part_number):
    return f"{directory}/{str(uuid.uuid4())}_part{part_number}.xml"

def convert_csv_to_xml(in_path, out_paths, num_parts):
    converter = CSVtoXMLConverter(in_path)
    
    # Calculate the number of rows to include in each part
    total_rows = len(converter.data)
    rows_per_part = total_rows // num_parts
    remaining_rows = total_rows % num_parts

    # Iterate over the parts and write the XML content to each file
    start_index = 0
    for part, out_path in enumerate(out_paths):
        end_index = start_index + rows_per_part + (1 if part < remaining_rows else 0)
        part_data = converter.data[start_index:end_index]

        with open(out_path, "w") as file:
            file.write(CSVtoXMLConverter.data_to_xml(part_data))

        start_index = end_index

class CSVHandler(FileSystemEventHandler):
    def __init__(self, input_path, output_path):
        self._output_path = output_path
        self._input_path = input_path

        # generate file creation events for existing files
        for file in [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_path) for f in filenames]:
            event = FileCreatedEvent(os.path.join(CSV_INPUT_PATH, file))
            event.event_type = "created"
            self.dispatch(event)

    async def convert_csv(self, csv_path):
        # here we avoid converting the same file again
        # !TODO: check converted files in the database
        if csv_path in await self.get_converted_files():
            return

        print(f"new file to convert: '{csv_path}'")

        # we generate a unique file name for the XML file
        #alterei aqui
        xml_paths = [generate_unique_file_name(self._output_path, part) for part in range(1, NUM_XML_PARTS + 1)]

        #alterei aqui
        convert_csv_to_xml(csv_path, xml_paths, NUM_XML_PARTS)
        
        for xml_path in xml_paths:
            print(f"new xml file generated: '{xml_path}'")

            # get the file size
            file_size = Path(csv_path).stat().st_size
            # import the document to the db
            db_access = DBAccess()
            db_access.convert_document(csv_path, xml_path, file_size)
            # !TODO: we should store the XML document into the imported_documents table
            #open the file to send the xml data
            with open(xml_path, encoding='latin-1') as file:
                data = file.read()
            
            # import the file into the db
            db_access.import_xml_document(xml_path, data)

    async def get_converted_files(self):
        csv_files = []
        # !TODO: you should retrieve from the database the files that were already converted before
        db_access = DBAccess()
        files = db_access.get_converted_files()

        for file in files:
            csv_files.append(file)
        return csv_files

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            asyncio.run(self.convert_csv(event.src_path))


if __name__ == "__main__":

    CSV_INPUT_PATH = "/csv"
    XML_OUTPUT_PATH = "/xml"

    # create the file observer
    observer = Observer()
    observer.schedule(
        CSVHandler(CSV_INPUT_PATH, XML_OUTPUT_PATH),
        path=CSV_INPUT_PATH,
        recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
