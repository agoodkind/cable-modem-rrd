package cmd

import (
	"fmt"
	"os"

	"gopkg.in/yaml.v3"
)

// Config represents the structure of the config.yml file
type Config struct {
	DB struct {
		Host     string `yaml:"host"`
		Port     int    `yaml:"port"`
		User     string `yaml:"user"`
		Password string `yaml:"password"`
		DBName   string `yaml:"dbname"`
	} `yaml:"db"`
	Modem struct {
		Host     string `yaml:"host"`
		Port     int    `yaml:"port"`
		Password string `yaml:"password"`
	} `yaml:"modem"`
	Logging struct {
		File   string `yaml:"file"`
		Level  string `yaml:"level"`
		Format string `yaml:"format,omitempty"`
	} `yaml:"logging"`
}

// ParseConfig reads and parses the YAML config file at the given path
func ParseConfig(configPath string) (*Config, error) {
	// Check if file exists
	if _, err := os.Stat(configPath); os.IsNotExist(err) {
		return nil, fmt.Errorf("config file does not exist: %s", configPath)
	}

	// Read file
	data, err := os.ReadFile(configPath)
	if err != nil {
		return nil, fmt.Errorf("error reading config file: %v", err)
	}

	// Parse YAML
	var config Config
	if err := yaml.Unmarshal(data, &config); err != nil {
		return nil, fmt.Errorf("error parsing config file: %v", err)
	}

	return &config, nil
}

func Execute() error {
	// Check if config file path is provided
	// if len(os.Args) < 2 {
	// 	return fmt.Errorf("Usage: program <config_file_path>")
	// }

	return nil
}

// func asdasd() {
// 	// Check if config file path is provided
// 	if len(os.Args) < 2 {
// 		log.Fatal("Usage: program <config_file_path>")
// 	}

// 	configPath := os.Args[1]
// 	config, err := ParseConfig(configPath)
// 	if err != nil {
// 		log.Fatalf("Failed to parse config: %v", err)
// 	}

// 	// Example: Print the parsed config
// 	fmt.Printf("Database: %s@%s:%d/%s\n", 
// 		config.DB.User, config.DB.Host, config.DB.Port, config.DB.DBName)
// 	fmt.Printf("Modem: %s:%d\n", config.Modem.Host, config.Modem.Port)
// 	fmt.Printf("Log file: %s (Level: %s)\n", config.Logging.File, config.Logging.Level)
// }