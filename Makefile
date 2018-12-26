build:
	python setup.py sdist

publish:
	twine upload dist/*

test:
	nosetests -v .

deploy: build publish
