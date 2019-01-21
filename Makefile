build:
	docker build -t seb/style_transfert .

run:
	docker run -it --rm -v $$(pwd):/root/workspace seb/style_transfert bash