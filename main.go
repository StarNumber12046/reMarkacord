package main

import (
	"fmt"
	"os"
	"github.com/StarNumber12046/reMarkacord/appload"
)

type DiscordBackend struct {}

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
	backend := &DiscordBackend{}

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
