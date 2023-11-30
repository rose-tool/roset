%!	https://www.swi-prolog.org/pldoc/man?section=preddesc
% ?	At call time, the argument must be bound to a partial term
%	(a term which may or may not be ground) satisfying some
%	(informal) type specification. Note that an unbound variable
%	is a partial term. Think of the argument as either providing
%	input or accepting output or being used for both input and
%	output. For example, in stream_property(S, reposition(Bool)),
%	the reposition part of the term provides input and the
%	unbound-at-call-time Bool variable accepts output.
% +	At call time, the argument must be instantiated to a term
%	satisfying some (informal) type specification. The
%	argument needs not necessarily be ground. For example, the
%	term [_] is a list, although its only member is the anonymous
%	variable, which is always unbound (and thus nonground).

:- module(rir,
          [ rir_read/1,                  % leggi il file di input +File 
            rir_clean/0,
            import/4,                    % campi dall'input ?AS, ?Family, ?From, ?Accept
            export/4,                    % campi dall'input ?AS, ?Family, ?To, ?Announce
            as_member/2                  % campi dall'input ?Set, ?AS
          ]).

%! https://www.swi-prolog.org/pldoc/man?section=apply
% https://www.swi-prolog.org/pldoc/man?section=readutil
% https://www.swi-prolog.org/pldoc/man?section=basics
:- use_module(library(apply)).
:- use_module(library(readutil)).
:- use_module(library(dcg/basics)).

%! https://www.swi-prolog.org/pldoc/doc_for?object=(meta_predicate)/1
:- meta_predicate
    phrase_string(//, +),
    phrase_string_err(//, +, +).

%!  rir_read(+File)
%
%   Read a RIR file, populating import/4   and  export/4 facts. Existing
%   facts are __not__ removed.
% https://www.swi-prolog.org/pldoc/doc_for?object=read_file_to_string/3
% https://www.swi-prolog.org/pldoc/doc_for?object=split_string/4
% https://www.swi-prolog.org/pldoc/doc_for?object=foldl/4

rir_read(File) :-
    read_file_to_string(File, String, []),
    split_string(String, "\n", "", Lines),
    foldl(rir_line, Lines, #{line:0, file:File}, _).

%! https://www.swi-prolog.org/pldoc/doc_for?object=sub_string/5
% https://www.swi-prolog.org/pldoc/doc_for?object=sub_atom/5
% https://www.swi-prolog.org/pldoc/doc_for?object=split_string/4

rir_line(Line, State0, State),
    sub_string(Line, B, _, A, ":") =>
    sub_atom(Line, 0, B, _, Field),
    sub_atom(Line, _, A, 0, Value0),
    split_string(Value0, "", " \t", [Value]),
    inc_line(State0, State1),
    rir_line(Field, Value, State1, State).
rir_line(Line, State0, State),
    split_string(Line, "", " \t", [""]) => % blank line
    inc_line(State0, State).
rir_line(Line, State0, State),
    split_string(Line, "%", " \t", [""|_]) => % comment line
    inc_line(State0, State).

inc_line(State0, State) :-
    Line1 is State0.line+1,
    State = State0.put(line, Line1).

%! https://www.swi-prolog.org/pldoc/doc_for?object=string_concat/3
% https://www.swi-prolog.org/pldoc/doc_for?object=number_string/2
rir_line('aut-num', AS, State0, State) =>
    string_concat("AS", NumS, AS),
    number_string(ASNum, NumS),
    State = State0.put(#{about:ASNum, type:as}).
rir_line('as-set', Value, State0, State) =>
    atom_string(Set, Value),
    State = State0.put(#{about:Set, type:set}).
rir_line(import, Import, State0, State) =>
    (   phrase_string_err(parse_import(From, Accept), Import, State0)
    ->  import(ipv4, From, Accept, State0, State)
    ;   State = State0
    ).
rir_line('mp-import', Import, State0, State) =>
    (   phrase_string_err(parse_mp_import(Family, From, Accept), Import, State0)
    ->  import(Family, From, Accept, State0, State)
    ;   State = State0
    ).
rir_line(export, Export, State0, State) =>
    (   phrase_string_err(parse_export(To, Announce), Export, State0)
    ->  export(ipv4, To, Announce, State0, State)
    ;   State = State0
    ).
rir_line('mp-export', Export, State0, State) =>
    (   phrase_string_err(parse_mp_export(Family, To, Announce), Export, State0)
    ->  export(Family, To, Announce, State0, State)
    ;   State = State0
    ).
rir_line('members', Line, State0, State) =>
    (   phrase_string_err(as(Member), Line, State0)
    ->  add_as_set_member(Member, State0, State)
    ;   State = State0
    ).
rir_line('member-of', Line, State0, State) =>
    (   phrase_string_err(as_set(Set), Line, State0)
    ->  add_to_as_set(Set, State0, State)
    ;   State = State0
    ).

%! https://www.swi-prolog.org/pldoc/man?section=format-predicates
% https://www.swi-prolog.org/pldoc/doc_for?object=print_message/2
% Ignored fields
rir_line(Field,  _Line, State0, State), ignored(Field) => State = State0.
rir_line(Field, Value, State0, State) =>
    State = State0,
    format(string(Line), '~w: ~w', [Field,Value]),
    print_message(error, rir_line(State, Line)).

%!  ignored(?Field)
%
%   True when Field is ignored. We list them explicitly. If you want to
%   ignore any unknown field, uncomment ignored(_).

%! ignored(_).                           % uncomment to ignore all unknown
ignored('abuse-c').
ignored('address').
ignored('admin-c').
ignored('as-block').
ignored('as-name').
ignored('country').
ignored('created').
ignored('descr').
ignored('export-via').
ignored('fax-no').
ignored('last-modified').
ignored('mnt-by').
ignored('mnt-ref').
ignored('nic-hdl').
ignored('org').
ignored('org-name').
ignored('org-type').
ignored('organisation').
ignored('person').
ignored('phone').
ignored('remarks').
ignored('source').
ignored('status').
ignored('tech-c').

%!  parse_import(-From, -Accept)// is det
%	https://www.swi-prolog.org/pldoc/man?section=preddesc
% det	(A deterministic predicate always succeeds exactly once
%	and does not leave a choicepoint.)
%
%   Parse the value of an "import: ..." line.
% esempio https://www.swi-prolog.org/pldoc/doc_for?object=parse_url/2

parse_import(From, Accept) -->
    kw(from), as(From),
    opt_endpoints,
    opt_action,
    kw(accept), accept(Accept),
    opt_semicolon.

opt_endpoints -->
    ip(_), kw(at), ip(_),
    !.
opt_endpoints -->
    [].

opt_action -->
    kw(action), pref(_), semicolon,
    !.
opt_action -->
    [].

opt_semicolon -->
    semicolon,
    !.
opt_semicolon -->
    [].

semicolon --> whites, ";", whites.

%!  parse_mp_import(-Family, -From, -Accept)// is det.

parse_mp_import(Family, From, Accept) -->
    kw(afi),
    family(Family),
    parse_import(From, Accept).

%!  parse_export(-To, -Announce)// is det.
%
%   Parse the value of an "export: ..." line.

parse_export(To, Announce) -->
    kw(to), as(To),
    opt_endpoints,
    opt_action,
    kw(announce), announce(Announce),
    (";" -> [] ; []).

%!  parse_mp_export(-Family, -To, -Announce)// is det.

parse_mp_export(Family, To, Announce) -->
    kw(afi),
    family(Family),
    parse_export(To, Announce).


		 /*******************************
		 *          PARSER UTILS	*
		 *******************************/

family(ipv4) -->
    kw_nw(ipv4), !, ".", cast(_).
family(ipv6) -->
    kw_nw(ipv6), ".", cast(_).

as(From) -->
    as, integer(From).

as --> kw_nw(as).

pref(Pref) -->
    "pref", whites, "=", whites, integer(Pref).

announce(To) -->
    accept(To).

accept(any) -->
    kw(any),
    !.
accept(as(List)) -->
    as_list(List),
    {List \== []},
    !.
accept(set(Set)) -->
    as_set(Set).

as_set(Set) -->
    string(Codes),
    (   white
    ;   eos
    ),
    !,
    { atom_codes(Set, Codes)
    }.

as_list([H|T]) -->
    as_or_as_set(H),
    whites,
    !,
    (   semicolon
    ->  {T=[]}
    ;   eos
    ->  {T=[]}
    ;   opt_and,
        as_list(T)
    ).
as_list([]) -->
    whites.

as_or_as_set(AS) -->
    as(AS),
    !.
as_or_as_set(set(AS)) -->
    as_set(AS).

opt_and -->
    kw(and),
    !.
opt_and -->
    whites.

cast(unicast) --> nw_kw(unicast), !.
cast(multicast) --> nw_kw(multicast).

ip(IP) -->
    whites,
    int256(A), ".", int256(B), ".", int256(C), ".", int256(D),
    whites,
    { format(atom(IP), '~w.~w.~w.~w', [A,B,C,D])
    }.

int256(A) -->
    integer(A),
    { between(0, 255, A) }.

kw(KeyWord) -->
    kw_nw(KeyWord),
    \+ csymc(_),
    whites.

csymc(C) -->
    [C],
    { code_type(C, csym) }.

kw_nw(KeyWord) -->                       % keyword, no whites
    { atom_codes(KeyWord, Codes)
    },
    whites,
    string_lwr(Codes).

nw_kw(KeyWord) -->                       % no whites, keyword
    { atom_codes(KeyWord, Codes)
    },
    string_lwr(Codes),
    white, whites.

string_lwr([]) -->
    [].
string_lwr([H|T]) -->
    [C],
    { code_type(H, to_lower(C)) },
    string_lwr(T).

% https://www.swi-prolog.org/pldoc/doc_for?object=print_message/3
phrase_string_err(DCG, String, State) :-
    (   phrase_string(DCG, String)
    ->  true
    ;   print_message(error, rir_line(State, String)),
        fail
    ).

%!  phrase_string(:DCG, +String)
% https://www.swi-prolog.org/pldoc/doc_for?object=string_codes/2

phrase_string(DCG, String) :-
    string_codes(String, Codes),
    phrase(DCG, Codes).

		 /*******************************
		 *             DATA		*
		 *******************************/

%!  import(?AS, ?Family, ?From, ?Accept)
%
%   AS accepts connections for Family from From.  Accept is one of
%
%     - any
%     - as(list(AS))
%     - set(Name)

%!  export(?AS, ?Family, ?To, ?Announce)
%
%   AS exports to To. Announce  uses  the   same  rules  as Accept` from
%   import/4.

%!  as_member(?Set, ?AS)
%
%   True when AS is a member of Set.

:- dynamic
    import/4,
    export/4,
    as_member/2.

%!  rir_clean
%
%   Clear rir database

rir_clean :-
    retractall(import(_,_,_,_)),
    retractall(export(_,_,_,_)),
    retractall(as_member(_,_)).

import(Family, From, Accept, State0, State),
    #{about:ASNum, type:as} :< State0 =>
    State = State0,
    assertz(import(ASNum, Family, From, Accept)).

export(Family, To, Announce, State0, State),
    #{about:ASNum, type:as} :< State0 =>
    State = State0,
    assertz(export(ASNum, Family, To, Announce)).

add_as_set_member(Member, State0, State),
    #{about:Set, type:set} :< State0 =>
    State = State0,
    assertz(as_member(Set, Member)).

add_to_as_set(Set, State0, State),
    #{about:ASNum, type:as} :< State0 =>
    State = State0,
    assertz(as_member(Set, ASNum)).


		 /*******************************
		 *             MESSAGES		*
		 *******************************/
%! https://github.com/SWI-Prolog/swipl/blob/master/boot/messages.pl
:- multifile prolog:message//1.

prolog:message(rir_line(State, String)) -->
    [ 'Invalid RIR line ~w:~w: ~s'-[State.file, State.line, String] ].
