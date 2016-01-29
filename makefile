all: webserver.py
	cp webserver.py webserver
	chmod 755 webserver

clean: webserver
	rm webserver
