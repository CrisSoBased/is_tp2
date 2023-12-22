package main

import (
	"database/sql"
	"fmt"
	"log"
	"time"

	"github.com/streadway/amqp"
	_ "github.com/lib/pq"
)

const (
	dbUser      = "is"
	dbPassword  = "is"
	dbName      = "is"
	dbHost      = "db-xml"
	rabbitMQURL = "amqp://is:is@rabbitmq:5672/is"
	queueName   = "tasks"
)

func connectDB() *sql.DB {
	connStr := fmt.Sprintf("user=%s password=%s dbname=%s host=%s sslmode=disable",
		dbUser, dbPassword, dbName, dbHost)

	db, err := sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal("Erro ao conectar ao banco de dados:", err)
	}

	err = db.Ping()
	if err != nil {
		log.Fatal("Erro ao fazer ping no banco de dados:", err)
	}

	return db
}

func sendToBroker(fileName string, taskType string) {
	conn, err := amqp.Dial(rabbitMQURL)
	if err != nil {
		log.Fatalf("Erro ao se conectar ao RabbitMQ: %s", err)
	}
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		log.Fatalf("Erro ao abrir o canal: %s", err)
	}
	defer ch.Close()

	q, err := ch.QueueDeclare(
		queueName,
		true,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		log.Fatalf("Erro ao declarar a fila: %s", err)
	}

	body := fmt.Sprintf("Tarefa para o arquivo: %s, Tipo: %s", fileName, taskType)
	err = ch.Publish(
		"",
		q.Name,
		false,
		false,
		amqp.Publishing{
			DeliveryMode: amqp.Persistent,
			ContentType:  "text/plain",
			Body:         []byte(body),
		})
	if err != nil {
		log.Fatalf("Erro ao publicar a mensagem: %s", err)
	}

	fmt.Println("Mensagem enviada para o RabbitMQ com sucesso!")
}

func hasNewEntity() bool {
	//logica
	return true
}

func hasNewLocation() bool {
	//logica
	return true
}

func checkNewXMLFilesEvery60Seconds(db *sql.DB) {
	fmt.Println("Verificando novos arquivos XML a cada 60 segundos:")

	ticker := time.NewTicker(60 * time.Second)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			query := `
				SELECT file_name, created_on
				FROM imported_documents
				WHERE created_on > $1
			`

			// Define o limite de tempo para 60 segundos atrás
			sixtySecondsAgo := time.Now().Add(-60 * time.Second)

			rows, err := db.Query(query, sixtySecondsAgo)
			if err != nil {
				log.Fatal("Erro ao executar a consulta:", err)
			}

			for rows.Next() {
				var fileName string
				var createdOn time.Time
				err := rows.Scan(&fileName, &createdOn)
				if err != nil {
					log.Fatal("Erro ao escanear o resultado da consulta:", err)
				}

				fmt.Printf("Novo arquivo XML encontrado: Nome do arquivo: %s, Criado em: %s\n", fileName, createdOn)
				// Enviar para o RabbitMQ
				if hasNewEntity {
					task = "Nova entidade."
				}else{
					task = "Atualização de dados geograficos."
				}
				sendToBroker(fileName, task)
			}

			if err := rows.Err(); err != nil {
				log.Fatal("Erro durante a iteração dos resultados:", err)
			}

			rows.Close()
		}
	}
}

func main() {
	db := connectDB()
	defer db.Close()

	checkNewXMLFilesEvery60Seconds(db)
}
