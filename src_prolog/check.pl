%!       https://www.swi-prolog.org/pldoc/man?section=preddesc
% ?     At call time, the argument must be bound to a partial term
%       (a term which may or may not be ground) satisfying some
%       (informal) type specification. Note that an unbound variable
%       is a partial term. Think of the argument as either providing
%       input or accepting output or being used for both input and
%       output. For example, in stream_property(S, reposition(Bool)),
%       the reposition part of the term provides input and the
%       unbound-at-call-time Bool variable accepts output.
% +     At call time, the argument must be instantiated to a term
%       satisfying some (informal) type specification. The
%       argument needs not necessarily be ground. For example, the
%       term [_] is a list, although its only member is the anonymous
%       variable, which is always unbound (and thus nonground).
% -	Argument is an output argument. It may or may not be bound at
%	call-time. If the argument is bound at call time, the goal
%	behaves as if the argument were unbound, and then unified with
%	that term after the goal succeeds. This is what is called being
%	steadfast: instantiation of output arguments at call-time does
%	not change the semantics of the predicate, although
%	optimizations may be performed. For example, the goal
%	findall(X, Goal, [T]) is good style and equivalent to
%	findall(X, Goal, Xs), Xs = [T]50 Note that any determinism
%	specification, e.g., det, only applies if the argument is
%	unbound. For the case where the argument is bound or involved in
%	constraints, det effectively becomes semidet, and multi
%	effectively becomes nondet.
% lists			https://www.swi-prolog.org/pldoc/man?section=lists
% solution_sequences	https://www.swi-prolog.org/pldoc/man?section=solutionsequences

%! oggetto della verifica
:- module(verify,
          [ bgp_transit/3,              % ?AS, ?From, ?StartsTier1
            bgp_transits/2,             % ?AS, -Set
            rir_transit/2,              % ?As, ?From
            rir_transits/2,             % ?AS, -Set
            unexpected_bgp_transit/2,   % ?AS, ?From
            expected_bgp_transit/2      % ?AS, ?From
          ]).
:- use_module(library(lists)).
:- use_module(library(solution_sequences)).

%! roba mia
:- use_module(rir).
:- use_module(bgp).

%!  bgp_transit(?AS, ?From, ?StartsTier1) is nondet.
%	https://www.swi-prolog.org/pldoc/man?section=preddesc
%nondet	A non-deterministic predicate is the most general
%	case and no claims are made on the number of solutions
%	(which may be zero, i.e., the predicate may fail) and
%	whether or not the predicate leaves a choicepoint on
%	the last solution.
%
%   True when the AS path ends with [From,As].
%
%   @arg StartsTier1 is `true` if the left-most entry of the AS-Path is
%   a tier-1 AS.

bgp_transit(AS, From, StartsTier1) :-
    bgp_record(Prefix, _Origin, ASPath, AS),
    ASPath = [Left|_],
    address_family(Prefix, Family),
    starts_tier_1(Left, Family, StartsTier1),
    reverse(ASPath, RevPath),
    (   member(From0, RevPath),
        From0 \== AS
    ->  From = From0
    ).

address_family(Prefix, Family),
    sub_atom(Prefix, _, _, _, :) =>
    Family = ipv6.
address_family(_Prefix, Family) =>
    Family = ipv4.

starts_tier_1(Left, Family, Truth),
    tier_1(Left, Family, _Name) =>
    Truth = true.
starts_tier_1(_Left, _Family, Truth) =>
    Truth = false.

tier_1(6762,  _,    'Sparkle').
tier_1(12956, _,    'Telefonica').
tier_1(2914,  _,    'NTT').
tier_1(3356,  _,    'Lumen').
tier_1(6453,  _,    'TATA').
tier_1(701,   _,    'Verizon').
tier_1(6461,  _,    'Zayo').
tier_1(3257,  _,    'GTT').
tier_1(1299,  _,    'Arelion').
tier_1(3491,  _,    'PCCW').
tier_1(7018,  _,    'AT&T').
tier_1(3320,  _,    'DTAG').
tier_1(5511,  _,    'Orange').
tier_1(6830,  _,    'Liberty Global').
tier_1(7922,  _,    'Comcast').
tier_1(174,   _,    'Cogent').
tier_1(6939,  ipv6, 'HE').

%!  bgp_transits(?AS, -Set) is nondet.
%
%   True when Set is the set of incomming ASes to AS.
% https://www.swi-prolog.org/pldoc/doc_for?object=setof/3

bgp_transits(AS, Set) :-
    setof(From, bgp_transit(AS, From, _), Set).

%!  rir_transit(?As, ?From) is nondet.

rir_transit(As, From) :-
    import(As, _Family, From, any).

%!  rir_transits(?AS, -Set) is nondet.

rir_transits(AS, Set) :-
    setof(From, rir_transit(AS, From), Set).

%!  unexpected_bgp_transit(?AS, ?From) is nondet.
%
%   True when the BGP table says From  talks   to  AS,  but there is no
%   corresponding import in the RIR database.
% https://www.swi-prolog.org/pldoc/doc_for?object=distinct/1

unexpected_bgp_transit(AS, From) :-
    distinct(unexpected_bgp_transit_(AS, From)).

unexpected_bgp_transit_(AS, From) :-
    bgp_transit(AS, From, false),       % ignore tier-1 at left of AS-Path
    \+ rir_transit(AS, From).

%!  expected_bgp_transit(?AS, ?From) is nondet.
%
%   True when we  have  a  transit  import   in  the  RIR  data  but  no
%   corresponding BGP entry.

expected_bgp_transit(AS, From) :-
    distinct(expected_bgp_transit_(AS, From)).

expected_bgp_transit_(AS, From) :-
    rir_transit(AS, From),
    \+ bgp_transit(AS, From, _).        % false?
