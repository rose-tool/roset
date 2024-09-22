grammar_%:
	antlr4 -Dlanguage=Python3 -visitor -o "../src/rs4lk/grammar/$(shell echo $* | awk '{print tolower($0)}')" $*.g4
	rm ../src/rs4lk/grammar/$(shell echo $* | awk '{print tolower($0)}')/*.tokens
	rm ../src/rs4lk/grammar/$(shell echo $* | awk '{print tolower($0)}')/*.interp
	touch ../src/rs4lk/grammar/$(shell echo $* | awk '{print tolower($0)}')/__init__.py
