%! ansi_term	https://www.swi-prolog.org/pldoc/doc/_SWI_/library/ansi_term.pl
% lists		https://www.swi-prolog.org/pldoc/man?section=lists
% main		https://www.swi-prolog.org/pldoc/man?section=main

:- module(main,
          []).
:- use_module(library(ansi_term)).
:- use_module(library(lists)).
:- use_module(library(main)).
%! roba mia, file bgp.pl che si occupa della tabella BGP,
% rir.pl che parsa l'oggetto aut-num in RIR DB e check.pl
% che confronta gli insiemi
:- use_module(bgp).
:- use_module(rir).
:- use_module(check).

%! https://www.swi-prolog.org/pldoc/man?predicate=initialization/1
:- initialization(main, main).

%! https://www.swi-prolog.org/pldoc/man?predicate=argv_options/3
opt_type(bgp, bgp, file(read)).
opt_type(rir, rir, file(read)).

%! https://www.swi-prolog.org/pldoc/doc_for?object=opt_help/2
opt_help(bgp, "BGP file to read").
opt_help(rir, "RIR file to read").

%! https://www.swi-prolog.org/pldoc/doc_for?object=argv_options/3
% https://www.swi-prolog.org/pldoc/doc_for?object=argv_usage/1
% https://www.swi-prolog.org/pldoc/man?predicate=halt/1

main(Argv) :-
    argv_options(Argv, Positional, Options),
    (   Positional == []
    ->  rir_load(Options),
        bgp_load(Options),
        compare_rir_to_bgp
    ;   argv_usage(debug),
        halt(1)
    ).

%! https://www.swi-prolog.org/pldoc/doc_for?object=member/2
% https://www.swi-prolog.org/pldoc/man?section=forall2
rir_load(Options) :-
    forall(member(rir(File), Options),
           rir_read(File)).

bgp_load(Options) :-
    forall(member(bgp(File), Options),
           bgp_read(File)).

%! https://www.swi-prolog.org/pldoc/doc_for?object=ansi_format/3

compare_rir_to_bgp :-
    \+ unexpected_bgp_transit(_, _),
    \+ expected_bgp_transit(_, _),
    !,
    ansi_format(comment,
                'Excellent work, what declared in the RIR DB matches what \c
                was found on the Internet (and vice versa).~n', []).
compare_rir_to_bgp :-
    report_unexpected_bgp_transits,
    report_expected_bgp_transits.


report_unexpected_bgp_transits :-
    unexpected_bgp_transit(_, _),
    !,
    forall(setof(From, unexpected_bgp_transit(AS, From), Set),
           report_unexpected_bgp_transits(AS, Set)).
report_unexpected_bgp_transits :-
    ansi_format(comment,
                'Excellent work, what was found on the Internet matches what \c
                 was declared in the RIR DB.~n', []).

report_unexpected_bgp_transits(AS, Set) :-
    ansi_format(bold, 'Transit for AS~w detected on the Internet but not \c
                       declared in the RIR DB.~n', [AS]),
    forall(member(From, Set),
           ansi_format(warning, '~t~4|AS~w~n', [From])).

report_expected_bgp_transits :-
    expected_bgp_transit(_,_),
    !,
    forall(setof(From, expected_bgp_transit(AS, From), Set),
           report_expected_bgp_transits(AS, Set)).
report_expected_bgp_transits :-
    ansi_format(comment,
                'Excellent work, what declared in the RIR DB matches what \c
                 was found on the Internet.~n', []).

report_expected_bgp_transits(AS, Set) :-
    ansi_format(bold, 'Transit for AS~w declared in the RIR DB but \c
                       not detected in the Internet.~n', [AS]),
    forall(member(From, Set),
           ansi_format(warning, '~t~4|AS~w~n', [From])).
