# https://www.swi-prolog.org/pldoc/man?section=projectfiles
# run.pl   Use this file to start the application. Normally it loads
#          load.pl in silent-mode, and calls one of the starting
#          predicates from load.pl.
#          https://www.swi-prolog.org/pldoc/man?section=cmdline

PLFILES=rir.pl bgp.pl main.pl check.pl

verify: $(PLFILES) Makefile
	swipl --no-pce -o $@ -c main.pl

clean:
	rm -f *~

distclean: clean
	rm -f verify
