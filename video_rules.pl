% Main content type classifications
content_type(Text, tutorial) :- matches_tutorial(Text).
content_type(Text, educational) :- matches_educational(Text).
content_type(Text, entertainment) :- matches_entertainment(Text).
content_type(Text, coding) :- matches_coding(Text).
content_type(Text, cooking) :- matches_cooking(Text).

% Tutorial patterns
matches_tutorial(Text) :-
    (contains(Text, 'how to') ;
     contains(Text, 'step by step') ;
     contains(Text, 'guide') ;
     contains(Text, 'learn how')),
    (contains(Text, 'first') ;
     contains(Text, 'then') ;
     contains(Text, 'next') ;
     contains(Text, 'finally')).

% Educational patterns
matches_educational(Text) :-
    (contains(Text, 'learn') ;
     contains(Text, 'understand') ;
     contains(Text, 'concept') ;
     contains(Text, 'study')),
    (contains(Text, 'explain') ;
     contains(Text, 'explore') ;
     contains(Text, 'examine')).

% Entertainment patterns
matches_entertainment(Text) :-
    contains(Text, 'fun') ;
    contains(Text, 'amazing') ;
    contains(Text, 'awesome') ;
    contains(Text, 'incredible') ;
    contains(Text, 'watch').

% Coding patterns
matches_coding(Text) :-
    (contains(Text, 'code') ;
     contains(Text, 'programming') ;
     contains(Text, 'function') ;
     contains(Text, 'class')),
    (contains(Text, 'implement') ;
     contains(Text, 'debug') ;
     contains(Text, 'build')).

% Cooking patterns
matches_cooking(Text) :-
    (contains(Text, 'recipe') ;
     contains(Text, 'cook') ;
     contains(Text, 'ingredient')),
    (contains(Text, 'prepare') ;
     contains(Text, 'mix') ;
     contains(Text, 'heat')).

% Helper predicate for pattern matching
contains(Text, Pattern) :-
    sub_string(Text, _, _, _, Pattern).