import psycopg2

def importFile(xml_str, xml_file):
    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(user="is",
                                    password="is",
                                    host="is-db",
                                    port="5432",
                                    database="is")

        cursor = connection.cursor()

        # Adicionei a lógica para criar o arquivo temporário dentro da função insert
        with open("/data/csvtoxml.xml", "w") as xml_file:
            xml_file.write(xml_str)

        # Agora, lemos o conteúdo do arquivo temporário e executamos a inserção no banco de dados
        with open('/data/csvtoxml.xml', 'r', encoding='utf-8') as xml_file:
            conteudo_xml = xml_file.read()

        # Adicionamos mensagens de log
        print("File read successfully.")
        print("Inserting into the database...")

        cursor.execute("INSERT INTO imported_documents (file_name, xml) VALUES (%s, %s) ON CONFLICT (file_name) DO NOTHING;", ("output", conteudo_xml))

        connection.commit()

        # Adicionamos uma mensagem de log indicando o término da inserção no banco de dados
        print("Database insertion complete.")

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:
        if connection:
            cursor.close()
            connection.close()

    return "Sucesso!"
