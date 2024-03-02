# The Urinal Protocol

Let's dive into the fascinating world of public restrooms. Every designer knows that an efficient design is a good design, and when it comes to restrooms for people who are willing to pee standing, there is nothing more space efficient than a row packed of urinals.

Most people that have used one of these probably never gave a second thought about how they picked which urinal to use. But there seems to be a [tacit consensus](https://www.youtube.com/shorts/ixe5SzlfWRk) about what is the [optimal choice every time](https://blog.xkcd.com/2009/09/02/urinal-protocol-vulnerability/).

The **Urinal Protocol and Etiquette Enforcement Department** (UPEED) wants to imbue this innate human behavior into the new AI models, and for that they need a training set. The intern working with UPEED created a dataset with the input scenarios, but his internship ended before he could finish writing the scenarios' outputs.

Now, the UPEED needs your help. In order to make a less awkward future for humans and robots alike, you have to complete the outputs for the training dataset.

## Input description

The input files have one line per scenario that consists of a series of zeroes and ones, where 0 means an unoccupied urinal and a 1 means an occupied one.

The maximum number of urinals per scenario will be one million (they really want to future-proof this!).

## Output description

One line per scenario in the input:

- The output for the scenario is the index of the optimal urinal to pick (the leftmost urinal is at index 0).
- The optimal urinal is an empty urinal that is the farthest away from any occupied urinal.
- In case there is a tie, ignore the closest occupied urinal for each candidate and consider the distance to the next closest occupied urinal as a tie breaker. Apply this rule until the tie is broken or there are no more urinals to consider.
- In case there is still a tie, for better privacy pick the one that is farthest away from the door (which is on the left of the row).
- If there are no empty urinals, the output is `N/A`.

## Example

Given the following input:

```output
10000
101
000100
0000000
1100111
110011
1010001000111
1111
```

The expected output would be:

```output
4
1
0
6
2
3
4
N/A
```
