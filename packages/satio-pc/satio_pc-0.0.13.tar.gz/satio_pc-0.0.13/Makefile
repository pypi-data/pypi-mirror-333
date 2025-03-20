.PHONY: docker
clean: clean-build clean-pyc

clean-build:
	-rm -fr dist
	-rm -rf build
	-rm -rf satio_pc/satio_pc.egg-info
	-rm -rf satio_pc.egg-info

clean-pyc:
	sudo find . -name '*.pyc' -exec rm -f {} +
	sudo find . -name '*.pyo' -exec rm -f {} +
	sudo find . -name '*~' -exec rm -f {} +
	sudo find . -name '__pycache__' -exec rm -fr {} +

VERSION = $(shell python -c "from staio_pc._version import __version__; print(__version__)")

WHL_FOLDER=/data/users/Public/$(USER)/wheels
setup: clean
	hatch build -t wheel
	rm -rf build

copy:
	$(eval WHL=$(shell ls dist))
	cp dist/${WHL} ${WHL_FOLDER}/${WHL}

build: setup copy

hadoop: build
	$(eval WHL=$(shell ls dist))
	-hadoop fs -rm /tapdata/worldcover/dist/${WHL}
	hadoop fs -copyFromLocal ./dist/${WHL} /tapdata/worldcover/dist/${WHL}

awssync:
	aws s3 sync satio-pc s3://vito-worldcover-public/repos/satio-pc --exclude ".*/*"