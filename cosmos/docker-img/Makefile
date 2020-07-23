IMAGE_NAME=ms-cosmos
CONTAINER_NAME=demo

build:
	docker build --compress --network=host --build-arg DART_DB=$(DART_TEST_DB) --build-arg DART_USERNAME=$(DART_USERNAME) --build-arg DART_PASSWORD=$(DART_PASSWORD) --force-rm --tag $(IMAGE_NAME) .

deploy:
	docker run --tty --interactive --detach --name $(CONTAINER_NAME) --network=host --ipc=host --env DART_DB=$(DART_TEST_DB) --env DART_USERNAME=$(DART_USERNAME) --env DART_PASSWORD=$(DART_PASSWORD) --env DISPLAY=$(DISPLAY) --volume $(XAUTH):/root/.Xauthority --volume /var/run/postgresql/.s.PGSQL.5432:/var/run/postgresql/.s.PGSQL.5432 $(IMAGE_NAME)

clean:
	docker container prune -f

start:
	docker start --attach --interactive $(CONTAINER_NAME)

attach:
	docker attach $(CONTAINER_NAME)
