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

func isNewEntity(db *sql.DB, fileName string) bool {
	query := `
		SELECT EXISTS (
			SELECT 1
			FROM imported_documents
			WHERE file_name = $1
		)
	`

	var exists bool
	err := db.QueryRow(query, fileName).Scan(&exists)
	if err != nil {
		log.Fatal("Erro ao verificar existência da entidade:", err)
	}

	return !exists
}

func checkNewXMLFiles(db *sql.DB) {
	query := `
		SELECT file_name, created_on
		FROM imported_documents
		WHERE created_on > $1
	`

	umDiaAtras := time.Now().Add(-24 * time.Hour)

	rows, err := db.Query(query, umDiaAtras)
	if err != nil {
		log.Fatal("Erro ao executar a consulta:", err)
	}
	defer rows.Close()

	fmt.Println("Verificando novos arquivos XML carregados nas últimas 24 horas:")

	for rows.Next() {
		var fileName string
		var createdOn time.Time
		err := rows.Scan(&fileName, &createdOn)
		if err != nil {
			log.Fatal("Erro ao escanear o resultado da consulta:", err)
		}

		if isNewEntity(db, fileName) {
			sendToBroker(fileName, "Importar nova entidade")
		} else {
			sendToBroker(fileName, "Atualização de dados geográficos")
		}
	}

	if err := rows.Err(); err != nil {
		log.Fatal("Erro durante a iteração dos resultados:", err)
	}
}

func main() {
	db := connectDB()
	defer db.Close()

	checkNewXMLFiles(db)
}
