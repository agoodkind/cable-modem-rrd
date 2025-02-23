package models

import (
	"context"
	"fmt"
	"github.com/doug-martin/goqu/v9"
	"math"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

type DownstreamBondedChannels struct {
	Channel        int64     `json:"channel" db:"channel"`               // bigint
	LockedStatus   string    `json:"lockedStatus" db:"locked_status"`    // text
	Modulation     string    `json:"modulation" db:"modulation"`         // text
	ChannelID      int64     `json:"channelId" db:"channel_id"`          // bigint
	Frequency      int64     `json:"frequency" db:"frequency"`           // bigint
	Power          float32   `json:"power" db:"power"`                   // real
	SNR            float32   `json:"snr" db:"snr"`                       // real
	Correctables   int64     `json:"correctables" db:"correctables"`     // bigint
	Uncorrectables int64     `json:"uncorrectables" db:"uncorrectables"` // bigint
	Timestamp      int64     `json:"timestamp" db:"timestamp"`           // bigint (assumed as UNIX timestamp)
	ID             uuid.UUID `json:"id" db:"id"`                         // uuid = uuid_generate_v4()
}

/**
 * Calculate the limit based on the max channel value
 * the limit returned will be a multiple of numChannels
 */
func calculateLimit(pool *pgxpool.Pool, builder *goqu.SelectDataset, baseLimit *uint) (*goqu.SelectDataset, error) {
	var numChannels uint
	maxChannelSQL, _, _ := builder.Select(goqu.MAX("channel")).ToSQL()
	if err := pool.QueryRow(context.Background(), maxChannelSQL).Scan(&numChannels); err != nil {
		return nil, fmt.Errorf("failed to get max channel: %w", err)
	}

	const maxLimit uint = 1024
	limit := numChannels
	if nil != baseLimit {
		if (*baseLimit * numChannels) > maxLimit {
			limit = uint(math.Floor(float64(1024)/float64(numChannels))) * numChannels
		} else {
			limit = *baseLimit * numChannels
		}
	}

	return builder.Limit(limit), nil
}

// GetDownstreamBondedChannels returns the DownstreamBondedChannels object from the database
func queryTable(pool *pgxpool.Pool, table string, baseLimit, minTS, maxTS *uint) ([]DownstreamBondedChannels, error) {

	// TODO accept any table
	baseBuilder := GetSQLBuilder().From(table)
	builder := baseBuilder

	builder = builder.Select(&DownstreamBondedChannels{})

	builder, err := calculateLimit(pool, baseBuilder, baseLimit)
	if err != nil {
		return nil, fmt.Errorf("failed to calculate limit: %v", err)
	}

	if minTS != nil {
		builder = builder.Where(goqu.C("timestamp").Gte(*minTS))
	}
	if maxTS != nil {
		builder = builder.Where(goqu.C("timestamp").Lte(*maxTS))
	}

	//query, args, _ := builder.Order(goqu.C("timestamp").Desc()).Prepared(true).ToSQL()
	queryPrepped, _, _ := builder.Order(goqu.C("timestamp").Desc()).ToSQL()
	rows, err := pool.Query(context.Background(), queryPrepped)
	if err != nil {
		return nil, fmt.Errorf("failed to query db: %v", err)
	}

	records, err := pgx.CollectRows(rows, pgx.RowToStructByName[DownstreamBondedChannels])
	if err != nil {
		return nil, fmt.Errorf("failed to collect rows: %v", err)
	}
	return records, nil
}

func GetDownstreamBondedChannels(pool *pgxpool.Pool) ([]DownstreamBondedChannels, error) {
	return queryTable(pool, "downstream_bonded_channels", nil, nil, nil)
}
