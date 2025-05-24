NAME="swagger-validator"
VERSION=1.0.0

all:
	docker build -q --tag=$(NAME):$(VERSION) .
	docker tag $(NAME):$(VERSION) $(NAME):latest
