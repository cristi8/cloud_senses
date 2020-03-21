
build:
	docker build -t air2prometheus .


start: build
	docker run -d \
		--name=air2prom \
		--net=host \
		--restart=always \
		-e AIR_IP \
		-e AIR_TOKEN \
		-e AIR_DID \
		-e LISTEN_HOST \
		-e LISTEN_ADDR \
		air2prometheus


stop:
	docker rm -f air2prom
