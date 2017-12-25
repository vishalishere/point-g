clean:
	rm -rf ./website/data/json/*

init:
	env/bin/python initial.py

update:
	env/bin/python build_content_index.py

data:
	env/bin/python build_data.py

server:
	cd website/ && python -m SimpleHTTPServer
