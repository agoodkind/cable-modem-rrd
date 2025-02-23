package models

type QueryTimeRange struct {
	MinTimestamp int64 `json:"minTimestamp"`
	MaxTimestamp int64 `json:"maxTimestamp"`
}
