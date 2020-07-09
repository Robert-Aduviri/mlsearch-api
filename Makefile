.PHONY: run deploy undeploy init

run:
	export FLASK_DEBUG=True; export FLASK_DEVELOPMENT=True; python main.py

deploy:
	time zappa deploy dev

undeploy:
	time zappa undeploy dev

init:
	zappa init

