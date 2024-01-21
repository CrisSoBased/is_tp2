import os
import uuid
import re
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from utils.db_access import DBAccess
from utils.csv_to_xml_converter import CSVtoXMLConverter




CSV_INPUT_PATH = "/csv"
XML_OUTPUT_PATH = "/xml"
NUM_XML_PARTS = int(os.environ['NUM_XML_PARTS'])




def get_csv_files_in_input_folder():
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(CSV_INPUT_PATH) for f in filenames if
            os.path.splitext(f)[1] == '.csv']




def generate_unique_file_name(directory):
    j = f"{directory}/{str(uuid.uuid4())}.xml"
    j = re.sub(r'/xml\d+/', '/xml/', j)
    return j




def convert_csv_to_xml(in_path, out_path, i):
    converter = CSVtoXMLConverter(in_path, i)
    with open(out_path, "w") as file:
        file.write(converter.to_xml_str(i))

class CSVHandler(FileSystemEventHandler):
    def __init__(self, input_path, output_path):
        super().__init__()
        self._output_path = output_path

    def convert_csv(self, csv_path):
        if csv_path in self.get_converted_files():
            return

        print(f"Novo arquivo CSV detectado: '{csv_path}'")
        file_size = Path(csv_path).stat().st_size

        for i in range(NUM_XML_PARTS):
            name = f"{self._output_path}{str(i)}"
            print(f"Novo nome : '{name}'")
            xml_path = generate_unique_file_name(name)
            convert_csv_to_xml(csv_path, xml_path, i)
            print(f"Novo arquivo XML gerado: '{xml_path}'")

            db_access = DBAccess()
            db_access.convert_document(csv_path, xml_path, file_size)

            with open(xml_path, encoding='utf-8') as file:
                data = file.read()

            db_access.import_xml_document(xml_path, data)

    def get_converted_files(self):
        csv_files = []
        db_access = DBAccess()
        files = db_access.get_converted_files()

        for file in files:
            csv_files.append(file)
        return csv_files

def scan_existing_files(csv_handler):
    for file in get_csv_files_in_input_folder():
        csv_handler.convert_csv(file)

def main():

    csv_handler = CSVHandler(CSV_INPUT_PATH, XML_OUTPUT_PATH)

    # Executa a verificação de arquivos existentes antes de iniciar o loop
    scan_existing_files(csv_handler)

    # Cria o observador de arquivos
    observer = Observer()

    # Associa o manipulador CSVHandler ao observador
    observer.schedule(csv_handler, path=CSV_INPUT_PATH, recursive=True)

    # Inicia o observador
    observer.start()

    try:
        # Mantém o programa em execução
        while True:
            pass
    except KeyboardInterrupt:
        # Encerra o observador quando o usuário pressiona Ctrl+C
        observer.stop()

    # Aguarda a conclusão do observador
    observer.join()

if __name__ == "__main__":
    main()