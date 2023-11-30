%!	basics	https://www.swi-prolog.org/pldoc/doc/_SWI_/library/dcg/basics.pl
%	apply	https://www.swi-prolog.org/pldoc/man?section=apply
%	debug	https://www.swi-prolog.org/pldoc/man?section=debug
%	lists	https://www.swi-prolog.org/pldoc/man?section=lists
%	readutilhttps://www.swi-prolog.org/pldoc/man?section=readutil
%	bgp	read input file, clean records, define bgp input record (4 fields)
% +     At call time, the argument must be instantiated to a term
%       satisfying some (informal) type specification. The
%       argument needs not necessarily be ground. For example, the
%       term [_] is a list, although its only member is the anonymous
%       variable, which is always unbound (and thus nonground).


:- module(bgp,
          [ bgp_read/1,                 % leggi il file in input +File
            bgp_clean/0,
            bgp_record/4                % ciascun record e' costituito di 4 campi: Prefix, Origin, ASPath, AS
          ]).
:- use_module(library(dcg/basics)).
:- use_module(library(apply)).
:- use_module(library(debug)).
:- use_module(library(lists)).
:- use_module(library(readutil)).

%!  bgp_record(Prefix:atom, Origin:atom, ASPath:list(integer), AS:integer)
%
%   @arg AS is the last element of ASPath, added to speedup search.
% https://www.swi-prolog.org/pldoc/doc_for?object=(dynamic)/1
% https://www.swi-prolog.org/pldoc/doc_for?object=f(integer/1)

:- dynamic
    bgp_record/4.

%!  bgp_clean
%
%   Delete all known BGP records

bgp_clean :-
    retractall(bgp_record(_,_,_,_)).

%!  bgp_read(+File)
%
%   Read a BGP file.
% https://www.swi-prolog.org/pldoc/doc_for?object=read_file_to_string/3
% https://www.swi-prolog.org/pldoc/doc_for?object=split_string/4
% https://www.swi-prolog.org/pldoc/doc_for?object=foldl/4 
% https://www.swi-prolog.org/pldoc/doc_for?object=print_message/2
% https://www.swi-prolog.org/pldoc/doc_for?object=debug/3

bgp_read(File) :-
    read_file_to_string(File, String, []),
    split_string(String, "\n", "", Lines),
    foldl(bgp_line, Lines, #{line:0, file:File}, _).

bgp_line(Line, State0, State),
    split_string(Line, "|", "|", ["="|Fields]) =>
    inc_line(State0, State1),
    (   phrase(bgp_fields(State1, State), Fields)
    ->  true
    ;   print_message(error, bgp_line(State1, Line))
    ).
bgp_line(Line, State0, State),
    split_string(Line, "", " \t", [""]) => % blank line
    inc_line(State0, State).

inc_line(State0, State) :-
    Line1 is State0.line+1,
    State = State0.put(line, Line1).

%! https://www.swi-prolog.org/pldoc/doc_for?object=once/1
%  https://www.swi-prolog.org/pldoc/doc_for?object=assertz/1
%  https://www.swi-prolog.org/pldoc/doc_for?object=atom_string/2
%  https://www.swi-prolog.org/pldoc/doc_for?object=string_codes/2
%  https://www.swi-prolog.org/pldoc/doc_for?object=phrase/2
%  https://www.swi-prolog.org/pldoc/doc_for?object=f(integer/1)

bgp_fields(State, State) -->
    prefix(Prefix),
    as_path(ASPath),
    origin(Origin),
    (   ["i"]
    ->  []
    ;   [X],
        { debug(bgp, '~w:~w: Unexpected field: ~p',
                [State.file, State.line, X])
        }
    ),
    remainder(_),
    !,
    { once(append(_, [AS], ASPath)),
      assertz(bgp_record(Prefix, Origin, ASPath, AS))
    }.

prefix(Prefix) -->
    [PrefixS],
    { atom_string(Prefix, PrefixS) }.

as_path(Path) -->
    [S],
    { string_codes(S, Codes),
      phrase(as_list(Path), Codes)
    }.

as_list([H|T]) -->
    integer(H),
    (   white
    ->  whites,
        as_list(T)
    ;   {T=[]}
    ).

origin(Origin) -->
    [OriginS],
    { atom_string(Origin, OriginS) }.

		 /*******************************
		 *             MESSAGES		*
		 *******************************/

:- multifile prolog:message//1.

prolog:message(bgp_line(State, String)) -->
    [ 'Invalid BGP record ~w:~w: ~s'-[State.file, State.line, String] ].
