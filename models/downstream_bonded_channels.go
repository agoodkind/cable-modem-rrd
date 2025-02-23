package models

import (
	"context"
	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

type DownstreamBondedChannels struct {
	Channel        int64     `json:"channel"`        // bigint
	LockedStatus   string    `json:"lockedStatus"`   // text
	Modulation     string    `json:"modulation"`     // text
	ChannelID      int64     `json:"channelId"`      // bigint
	Frequency      int64     `json:"frequency"`      // bigint
	Power          float32   `json:"power"`          // real
	SNR            float32   `json:"snr"`            // real
	Correctables   int64     `json:"correctables"`   // bigint
	Uncorrectables int64     `json:"uncorrectables"` // bigint
	Timestamp      int64     `json:"timestamp"`      // bigint (assumed as UNIX timestamp)
	ID             uuid.UUID `json:"id"`             // uuid = uuid_generate_v4()
}

// GetDownstreamBondedChannels returns the DownstreamBondedChannels object from the database
// TODO convert to generic function for rest of tables
func queryDownstreamBondedChannels(pool *pgxpool.Pool, whereString string, args pgx.NamedArgs) ([]DownstreamBondedChannels, error) {
	query := `SELECT * FROM downstream_bonded_channels ` + whereString

	rows, err := pool.Query(context.Background(), query, args)
	collectRows, err := pgx.CollectRows(rows, pgx.RowToStructByPos[DownstreamBondedChannels])

	if err != nil {
		return nil, err
	}

	return collectRows, nil
}

func GetDownstreamBondedChannels(pool *pgxpool.Pool) ([]DownstreamBondedChannels, error) {
	return queryDownstreamBondedChannels(pool, "LIMIT 100", pgx.NamedArgs{})
}
