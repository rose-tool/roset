grammar_%:
	cd grammars; antlr4 -Dlanguage=Python3 -visitor -o "../src/rs4lk/parser/$(shell echo $* | sed 's/.*/\L&/')/antlr4" $*.g4
	rm src/rs4lk/parser/$(shell echo $* | sed 's/.*/\L&/')/antlr4/*.tokens
	rm src/rs4lk/parser/$(shell echo $* | sed 's/.*/\L&/')/antlr4/*.interp
