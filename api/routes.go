package routes

import (
	"cable-modem-rrd/models"
	"github.com/jackc/pgx/v5/pgxpool"
	"log"

	"github.com/gin-gonic/gin"
	"net/http"
)

type RequestHandler struct {
	datastore models.Datastore
}

func NewRequestHandler(dbPool *pgxpool.Pool) *RequestHandler {
	return &RequestHandler{datastore: models.NewDatastore(dbPool)}
}

func (r *RequestHandler) DownstreamRowsTODO(ctx *gin.Context) {
	channels, err := models.GetDownstreamBondedChannels(r.datastore.Pool())
	if err != nil {
		return
	}
	ctx.JSON(http.StatusOK, channels)
}

func (r *RequestHandler) Home(ctx *gin.Context) {
	ctx.HTML(http.StatusOK, "index.html", gin.H{
		"title": "Stop being poor",
	})
}

func Init() {
	router := gin.Default()

	dbPool, _, err := models.NewDBPool(models.DatabaseConfig{
		Username: "agoodkind",
		Password: "2020560",
		Hostname: "localhost",
		Port:     "5432",
		DBName:   "cm_data",
	})

	if err != nil {
		log.Fatalf("unexpected error while tried to connect to database: %v\n", err)
	}

	defer dbPool.Close()

	handler := NewRequestHandler(dbPool)
	router.GET("/downstream", handler.DownstreamRowsTODO)
	// TODO make configurable
	router.Run(":6969")

}
