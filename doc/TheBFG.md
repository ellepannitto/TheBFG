# The Big Friendly Graph

## Introduction

This project consists in developing a solution to extract Generalized Event Knowledge (GEK) from a parsed corpus (such as the University of Hamburg's dependency-parsed DepCC corpus (https://www.inf.uni-hamburg.de/en/inst/ab/lt/resources/data/depcc.html).

We consider the dependencies (either basic dependencies or enhanced ones) as a tool to get access to relations between lexical items. Basic dependencies and enhanced dependencies have the same status. One is not more important than the other. What matters are the frequency of the relations that unite lexical items with each other.


## Example

> The tall student reads the black book while the teacher speaks about history

### How to build subsets:
* for each nominal or verbal head, take all its dependants and generate all possible subsets from this group
* in order to take into account potentially interesting relations between dependants of different heads, we generate pairs formed by two items belonging to different groups. These relations are generic association relations (not labeled with syntactic paths). The idea is that they are useful to activate nieghbouring events

From the example, we can extract 4 heads, and so 4 groups are formed:
* read + student, book, speak
* student + tall
* book + black
* speak + teacher, history


* Hence, from point 1 we get (each of this subset is labeled with syntactic relations):
Group 1:
--- subsets with 2 elements ---
('book', 'speak')
('read', 'speak')
('student', 'book')
('read', 'book')
('student', 'read')
('student', 'speak')

--- subsets with 3 elements ---
('student', 'read', 'book')
('student', 'book', 'speak')
('student', 'read', 'speak')
('read', 'book', 'speak')

--- subsets with 4 elements ---
('student', 'read', 'book', 'speak')

Group 2:
--- subsets with 2 elements ---
('student', 'tall')

Group 3:
--- subsets with 2 elements ---
('book', 'black')

Group 4:
--- subsets with 2 elements ---
('teacher', 'history')
('speak', 'teacher')
('speak', 'history')

--- subsets with 3 elements ---
('speak', 'teacher', 'history')

* From point 2 we get unlabeled generic pairs of associated items:

('read', 'tall')
('read', 'black')
('read', 'teacher')
('read', 'history')

('student', 'black')
('student', 'teacher')
('student', 'history')

('book', 'tall')
('book', 'teacher')
('book', 'history')

('speak', 'tall')
('speak', 'black')

('tall', 'black')
('tall', 'teacher')
('tall', 'history')

('black', 'teacher')
('black', 'history')


## Pseudocode
Here is what we propose to do:

We carry out the processing of the parsed corpus in several steps.

Step 1: calculate general statistics for all potential GEK relations.

The statistics count the number of times a 'relationship' appears.

A relationship can be drawn between two items (pairs), three items (triads), four items, etc.

* For all sentences:
    * Take the graph composed by the elements (i.e., nodes) of that sentence (elements are related to each other by dependencies):
	    * Take all subsets of elements (nodes) in the graph:
		    * For each subset:
		    	* Count the relation (whether it is a pair, a trio, etc.), while keeping the order of the elements in the relation.     


Note: this step might be computionally consuming. It could become a stumbling block.



Step 2: remove unfrequent/irrelevant construction

Some thinking need here to occur to set a proper threshold and mechanism to filter unfrequent/irrelevant construction.

Some constructions might be relevant (e.g., an idiomatic expression as "kick the bucket").

In order to set that filter, human eyes/judgments might be needed.

Because several thresholds or mechanisms might be used, Step 2 might lead to different products (i.e., sets of statistics).





## History of the project

Originally, it was thought that, on the basis of intuition, we would a priori (i.e., immediately) filter out certain types of dependencies from the parsed corpus and only keep a specific set of dependencies (subj, obj, iobj, prep, conj, adv, adj, etc.). However it seems safer to be first agnostic about what is relevant. For that reason, Step 1, that processes the parsed corpus, keeps all dependencies. It does not matter whether the dependency is local or distant (i.e., enhanced): they are considered as the same. We do not weight dependencies (e.g., local dependencies receiving a higher weight than distance dependencies).

Note, however that Step 1 is not (like was suggested earlier) producing the "most general statistics". This step is not "innocent" indeed (to be discussed later).

During a second step, we examine the frequencies of dependencies, and keep the most frequent ones.



