package models

import (
	"github.com/doug-martin/goqu/v9"
	_ "github.com/doug-martin/goqu/v9/dialect/postgres"
)

type QueryTimeRange struct {
	MinTimestamp int64 `json:"minTimestamp"`
	MaxTimestamp int64 `json:"maxTimestamp"`
}

func GetSQLBuilder() goqu.DialectWrapper {
	// look up the dialect
	return goqu.Dialect("postgres")
}
