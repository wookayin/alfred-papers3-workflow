.PHONY: deploy

deploy:
	pip install py-applescript --force-reinstall --upgrade -I --target .
	rm -rf *.dist-info/
