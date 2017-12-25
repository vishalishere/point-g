clean:
	rm -rf ./website/data/json/*

init:
	env/bin/python initial.py

update:
	env/bin/python build_content_index.py

data:
	env/bin/python build_data.py

sync:
	aws s3 sync ./website/ s3://phleaks.com/

server:
	cd website/ && python -m SimpleHTTPServer
