AUTHOR="Dmitri McGuckin"
DESCRIPTION="A modification of the cosmos docker image customized for oresat mission server."
IMAGE_NAME=ms-cosmos
CONTAINER_NAME=cosmos
REMOTE_CONTAINER_NAME=dmitrimcguuckin/$(IMAGE_NAME):latest

build:
	docker build --compress --network=host --build-arg DART_DB=$(DART_TEST_DB) --build-arg DART_USERNAME=$(DART_USERNAME) --build-arg DART_PASSWORD=$(DART_PASSWORD) --force-rm --tag $(IMAGE_NAME) .

run:
	docker run --tty --interactive --detach --name $(CONTAINER_NAME) --network=host --ipc=host --env DART_DB=$(DART_TEST_DB) --env DART_USERNAME=$(DART_USERNAME) --env DART_PASSWORD=$(DART_PASSWORD) --env DISPLAY=$(DISPLAY) --volume $(XAUTH):/root/.Xauthority --volume /var/run/postgresql/.s.PGSQL.5432:/var/run/postgresql/.s.PGSQL.5432 $(IMAGE_NAME)

deploy:
	docker commit -a $(AUTHOR) -m $(DESCRIPTION) $(CONTAINER_NAME) $(REMOTE_CONTAINER_NAME)
	docker push $(REMOTE_CONTAINER_NAME)

clean:
	docker container prune -f

start:
	docker start --attach --interactive $(CONTAINER_NAME)

attach:
	docker attach $(CONTAINER_NAME)
