AUTHOR="Dmitri McGuckin"
DESCRIPTION="A modification of the cosmos docker image customized for oresat mission server."
CONTAINER=cosmos
LOCAL_IMAGE=ms-cosmos
REMOTE_IMAGE=dmitrimcguuckin/$(LOCAL_IMAGE):latest

IMAGE=$(REMOTE_IMAGE)
USE_LOCAL_BUILD=1
START_INTERACTIVE_MODE=1

build:
	$(info Using Arguments: ($(DART_DB), $(DART_USERNAME), $(DART_PASSWORD), $(LOCAL_IMAGE)))
	docker build \
		--compress \
		--network=host \
		--build-arg DART_DB=$(DART_DB) \
		--build-arg DART_USERNAME=$(DART_USERNAME) \
		--build-arg DART_PASSWORD=$(DART_PASSWORD) \
		--force-rm \
		--tag $(LOCAL_IMAGE) .

run:
ifeq ($(USE_LOCAL_BUILD), 1)
	$(info Prioritizing local build)
	$(eval IMAGE=$(LOCAL_IMAGE))
endif

ifeq ($(START_INTERACTIVE_MODE), 1)
	$(info Interactive mode enabled)
	$(eval FLAGS=--interactive)
endif

	docker run \
		--tty $(FLAGS) \
		--detach \
		--name $(CONTAINER) \
		--network=host \
		--ipc=host \
		--env DART_DB=$(DART_DB) \
		--env DART_USERNAME=$(DART_USERNAME) \
		--env DART_PASSWORD=$(DART_PASSWORD) \
		--env DISPLAY=$(DISPLAY) \
		--volume $(PG_SOCKET):$(PG_SOCKET) \
		--volume $(XAUTH):/root/.Xauthority \
		$(IMAGE)

deploy:
	docker commit -a $(AUTHOR) -m $(DESCRIPTION) $(CONTAINER) $(REMOTE_IMAGE)
	docker push $(REMOTE_IMAGE)

kill:
	docker container kill $(CONTAINER)

clean:
	docker container prune -f

start:
	docker start --attach --interactive $(CONTAINER)

attach:
	docker attach $(CONTAINER)
