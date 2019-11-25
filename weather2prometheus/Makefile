
build:
	docker build -t weather2prometheus .

push: build
	docker tag weather2prometheus cristi8/weather2prometheus
	docker push cristi8/weather2prometheus

run:
	docker run -d \
		--name=weather2prom \
		--net=host \
		--restart=always \
		-e DARKSKY_API_KEY \
		-e DARKSKY_GEO_NAME \
		-e DARKSKY_GEO_LOC \
		-e DARKSKY_UNITS \
		-e DARKSKY_QUERY_INTERVAL_MIN \
		-e LISTEN_HOST \
		-e LISTEN_ADDR \
		cristi8/weather2prometheus

stop:
	docker rm -f weather2prom
