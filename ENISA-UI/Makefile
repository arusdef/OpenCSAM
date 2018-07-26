default: build

NAME=webapp
REGISTRY=enisa2018
REF=$(shell git rev-parse --short HEAD)

push: build push.tag push.latest

push.tag:
	docker tag $(NAME) $(REGISTRY)/$(NAME):$(REF)
	docker push $(REGISTRY)/$(NAME):$(REF)

push.latest:
	docker tag $(NAME) $(REGISTRY)/$(NAME):latest
	docker push $(REGISTRY)/$(NAME):latest

build:
	docker build -t $(NAME) .

run:
	docker run -it --rm --name $(NAME) -p 4200:4200 $(NAME)

.PHONY: build push push.tag push.latest