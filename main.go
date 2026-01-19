package main

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/StarNumber12046/reMarkacord/appload"
)

type Config struct {
	Token string
}

type DiscordBackend struct {
	config Config
}

func loadConfig() (Config, error) {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		return Config{}, err
	}

	configPath := filepath.Join(homeDir, ".config", "reMarkacord", ".env")
	file, err := os.Open(configPath)
	if err != nil {
		return Config{}, err
	}
	defer file.Close()

	config := Config{}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.SplitN(line, "=", 2)
		if len(parts) == 2 {
			key := strings.TrimSpace(parts[0])
			value := strings.TrimSpace(parts[1])
			if key == "DISCORD_TOKEN" {
				config.Token = value
			}
		}
	}

	if err := scanner.Err(); err != nil {
		return Config{}, err
	}

	return config, nil
}

func (db *DiscordBackend) HandleMessage(replier *appload.BackendReplier, message appload.Message) {
	fmt.Printf("Received message type: %d, contents: %s\n", message.MsgType, message.Contents)

	if message.MsgType == appload.MsgSystemTerminate {
		fmt.Println("Received termination message")
		os.Exit(0)
		return
	}

	// Stub for initialization
	if message.MsgType > 1000 {
		replier.SendMessage(200, "Init")
	}
}

func main() {
	config, err := loadConfig()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Warning: Could not load config: %v\n", err)
	} else {
		fmt.Println("Config loaded successfully")
	}

	backend := &DiscordBackend{
		config: config,
	}

	app, err := appload.NewAppLoad(backend)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error creating app: %v\n", err)
		os.Exit(1)
	}

	err = app.Run()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error running app: %v\n", err)
		os.Exit(1)
	}
}
