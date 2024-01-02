package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
	"strconv"
	"database/sql"
	"encoding/json"
	"bytes"
	"github.com/streadway/amqp"
)


const (
	rabbitMQURL = "amqp://is:is@rabbitmq:5672/is"
	queueName   = "new_entity"
	apiURL      = "http://api-entities/players"

	dbUser     = "is"
	dbPassword = "is"
	dbName     = "is"
	dbHost     = "db-rel"
)



type PlayerData struct {
	
	Name          string `json:"name"`
	Age           int    `json:"age"`
	Overall       int    `json:"overall"`
	Position      string `json:"position"`
	Pace          int    `json:"pace"`
	Shooting      int    `json:"shooting"`
	Passing       int    `json:"passing"`
	Dribbling     int    `json:"dribbling"`
	Defending     int    `json:"defending"`
	Physicality   int    `json:"physicality"`
	Acceleration  int 	 `json:"acceleration"`
	Sprint        int    `json:"sprint"`
	Positioning   int    `json:"positioning"`
	Finishing     int    `json:"finishing"`
	Shot          int    `json:"shot"`
	Long          int    `json:"long"`
	Volleys       int    `json:"volleys"`
	Penalties     int    `json:"penalties"`
	Vision        int    `json:"vision"`
	Crossing      int    `json:"crossing"`
	Free          int    `json:"free"`
	Curve         int    `json:"curve"`
	Agility       int    `json:"agility"`
	Balance       int    `json:"balance"`
	Reactions     int    `json:"reactions"`
	Ball          int    `json:"ball"`
	Composure     int    `json:"composure"`
	Interceptions int    `json:"interceptions"`
	Heading       int    `json:"heading"`
	Def           int    `json:"def"`
	Standing      int    `json:"standing"`
	Sliding       int    `json:"sliding"`
	Jumping       int    `json:"jumping"`
	Stamina       int    `json:"stamina"`
	Strength      int    `json:"strength"`
	Aggression    int    `json:"aggression"`
	AttWorkRate   string `json:"att_work_rate"`
	DefWorkRate   string `json:"def_work_rate"`
	PreferredFoot string `json:"preferred_foot"`
	WeakFoot      int    `json:"weak_foot"`
	SkillMoves    int    `json:"skill_moves"`
	URL           string `json:"url"`
	Gender        string `json:"gender"`
	GK            int    `json:"gk"`

	IdClub   string `json:"id_club"`
	IdNation string `json:"id_nation"`
}


func waitForService() {
	url := "http://api-entities:8080/clubs"
	maxRetries := 10
	retryInterval := 2 * time.Second

	for i := 0; i < maxRetries; i++ {
		_, err := http.Get(url)
		if err == nil {
			return
		}

		log.Printf("Error connecting to service: %v. Retrying...", err)
		time.Sleep(retryInterval)
	}

	log.Fatal("Failed to connect to the service after multiple retries.")
}

func convertStringToInt(s string) (int, error) {
    return strconv.Atoi(s)
}




func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func insertnation(nationname string) (string, error){

	url := "http://api-entities:8080/nations"

	// Cria o objeto JSON com o nome do clube
	createNationto := map[string]string{
		"name": nationname,
	}

	jsonData, err := json.Marshal(createNationto)
	if err != nil {
		return "", fmt.Errorf("Erro ao converter para JSON: %v", err)
	}

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return "", fmt.Errorf("Erro ao fazer a solicitação HTTP: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("A solicitação à API falhou com o status: %v", resp.Status)
	}

	var result map[string]string
	err = json.NewDecoder(resp.Body).Decode(&result)
	if err != nil {
		return "", fmt.Errorf("Erro ao decodificar a resposta JSON: %v", err)
	}
	

	return result["id"], nil




}

func checkIfNationIsThere(nationname string) string {
    url := "http://api-entities:8080/nations"

    // Faz a solicitação GET
    resp, err := http.Get(url)
    if err != nil {
        return "nop" // ou qualquer valor padrão que você deseje
    }
    defer resp.Body.Close()

    // Decodifica o JSON diretamente
    var nations []map[string]interface{}
    var idnation = "nop"

    decoder := json.NewDecoder(resp.Body)
    err = decoder.Decode(&nations)
    if err != nil {
        return "nop" // ou qualquer valor padrão que você deseje
    }

    for _, nation := range nations {
        if name, ok := nation["name"].(string); ok && name == nationname {
            // Encontrou correspondência, definir idnation
            idnation = nation["id"].(string)
            break
        }
    }

    return idnation
}










func connectToRabbitMQ() (*amqp.Connection, *amqp.Channel) {
	conn, err := amqp.Dial(rabbitMQURL)
	failOnError(err, "Failed to connect to RabbitMQ")
	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")

	return conn, ch
}

func consumeMessages(ch *amqp.Channel) <-chan amqp.Delivery {
	msgs, err := ch.Consume(
		queueName,
		"",
		true,
		false,
		false,
		false,
		nil,
	)
	failOnError(err, "Failed to register a consumer")

	return msgs
}


func connectDB() *sql.DB {
	connStr := fmt.Sprintf("host=%s dbname=%s user=%s password=%s sslmode=disable",
		dbHost, dbName, dbUser, dbPassword)

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


func handleTask(msg amqp.Delivery)  {
	
	/*defer func() {
		// Sinalize que esta goroutine de processamento de mensagens foi concluída
		doneChan <- struct{}{}
	}()*/

	log.Printf("Received task: New Entity")

	var playerData PlayerData
	err := json.Unmarshal(msg.Body, &playerData)
	if err != nil {
		log.Printf("Error decoding JSON: %v", err)
		return
	}
	


	
	
	if checkIfClubIsThere(playerData.IdClub) == "nop" {
		inserttheclub(playerData.IdClub)
	}
		
	idClub := checkIfClubIsThere(playerData.IdClub)
	playerData.IdClub = idClub

	if checkIfNationIsThere(playerData.IdNation) == "nop" {
		insertnation(playerData.IdNation)
	}
	
	idNation := checkIfNationIsThere(playerData.IdNation)
	playerData.IdNation = idNation
	

	

	// Criar JSON para o jogador
	playerJSON, err := json.Marshal(playerData)
	if err != nil {
		log.Printf("Error encoding player JSON: %v", err)
		return
	}

	//log.Printf("Player JSON: %s", string(playerJSON))

	// Fazer chamada para a API HTTP
	url := "http://api-entities:8080/players"
	resp, err := http.Post(url, "application/json", bytes.NewBuffer(playerJSON))
	if err != nil {
		log.Printf("Error making HTTP request: %v", err)
		return
	}
	defer resp.Body.Close()

	log.Printf("API response: %v", resp.Status)

	//msg.Ack(false)



}


func inserttheclub(clubname string) (string, error) {
	url := "http://api-entities:8080/clubs"

	// Cria o objeto JSON com o nome do clube
	createClubDto := map[string]string{
		"name": clubname,
	}

	jsonData, err := json.Marshal(createClubDto)
	if err != nil {
		return "", fmt.Errorf("Erro ao converter para JSON: %v", err)
	}

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return "", fmt.Errorf("Erro ao fazer a solicitação HTTP: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := ioutil.ReadAll(resp.Body)
		log.Printf("A solicitação à API falhou com o status: %v\nResponse Body: %s", resp.Status, body)
		return "", fmt.Errorf("A solicitação à API falhou com o status: %v", resp.Status)
	}

	var result map[string]string
	err = json.NewDecoder(resp.Body).Decode(&result)
	if err != nil {
		return "", fmt.Errorf("Erro ao decodificar a resposta JSON: %v", err)
	}

	return result["id"], nil
}

func checkIfClubIsThere(clubname string) string {
    /*
	apiUrl := os.Getenv("API_ENTITIES_URL")
	url := fmt.Sprintf("http://%s/clubs", apiUrl)
	*/
    // Faz a solicitação GET
    resp, err := http.Get("http://api-entities:8080/clubs")
    if err != nil {
        log.Fatalln(err)
    } else {
		log.Printf("deu a google ")

	} 
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        body, _ := ioutil.ReadAll(resp.Body)
        log.Printf("A solicitação à API falhou com o status: %v\nResponse Body: %s", resp.Status, body)
    }

    // Decodifica o JSON diretamente
    var clubs []map[string]interface{}
    var idclub = "nop"

    decoder := json.NewDecoder(resp.Body)
    err = decoder.Decode(&clubs)
    if err != nil {
        log.Printf("Erro ao decodificar a resposta JSON: %v", err)
        return "nop" // ou qualquer valor padrão que você deseje
    }

    for _, club := range clubs {
        if name, ok := club["name"].(string); ok && name == clubname {
            // Encontrou correspondência, definir idclub
            idclub = club["id"].(string)
            break
        }
    }

    return idclub
}






var (
	shutdownChan    = make(chan struct{})
	workersDoneChan = make(chan struct{})
)

func main() {
	// Aguarde até que o serviço esteja disponível
	waitForService()

	conn, ch := connectToRabbitMQ()
	defer conn.Close()
	defer ch.Close()

	msgs := consumeMessages(ch)

	fmt.Println("Migrator is waiting for tasks. To exit press CTRL+C")

	// Aguarde sinal para encerrar
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)

	for {
		select {
		case msg, ok := <-msgs:
			if !ok {
				log.Println("No more messages. Shutting down.")
				return
			}
			handleTask(msg)
		case <-sigChan:
			log.Println("Received interrupt signal. Shutting down.")
			return
		}
	}
}
