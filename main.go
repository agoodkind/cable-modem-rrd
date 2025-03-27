package main

import (
	"os"

	"cable-modem-rrd/cmd"
)

func main() {
	if err := cmd.Execute(); err != nil {
		os.Exit(1)
	}
	// routes.Init()
}
