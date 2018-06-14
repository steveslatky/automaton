---
title: Kanye West Text Song Generator 
author: Stephen Slatky
geometry: margin=0.5in
numbersections: true
---

# Author Notes

I am sorry I could not work on the Cybernetic Automata. After working on it 
for many hours in the start of the term and taking a little break from it. 
Everyone I knew kept asking me questions about the project. "How to do this, 
What does this line mean, why is this project so stupid". I could not stand the project
any more. I would sit down to work and just hate every moment thinking about it. I was 
so tired of it and all the people around me asking questions. 

This song generator project was my escape. I have many more ideas that I want to do with this
and I found the love in programming again after so many school projects hindered it. 

So I am sorry I could not finish the CFA, but I hope the effort I put into this
makes up for it. I loved every moment of your class. It was the best CS class 
I have been in. You broke the normal school system and I love it. 

# How to run 

## Requirements

Python3

## Commands

python3 markov_chain.py

output save in ./songs/n.txt

# What is it? 

Have you ever wanted a new song by an artist but did not want to wait? 
Well I have the solution for you... kind of. I hope that artist is Kanye
West.

This application will take in a group of song lyrics and output a new song
based on the inputted lyrics from [genius](https://genius.com/). This new song will have it's own structure.

# Example output

The songs can be found in the folder songs. There is a note on top indicating what
version (1-5) it is and what *improvement* was made in that version

# How does it work?

## Markov Chains Everywhere! 

### Lyric Markov Chain

The program will take in a folder with sanitized lyrics and find 
the connections between the words. Right now it only does probability 
based on the next word. It does not care what words came before. 

#### How it generates lines

It will choose a word at random to start the line. It will then have 
a probability to choose any word connected to the current word. 
The more times it has seen it in the the inputted lyrics. 

If the current word has no connections to it, the line will just 
end and more on to the next, picking a new word at random. 

#### Improvements

* Have an idea of part of speech E.G. Nouns, adjectives, verbs
* Make prior words have an affect on probability

### Structure Markov Chain

This is where I tried to get creative a bit. In the input files there are tags
for what section of the song it is. E.G. [Chorus], [Verse]. The program will
parse through and count the amount of times it sees a tag. It will also count
the number of lines of each section. It will average the numbers out over
all the songs in the input folder. 


#### How It Generates Sections

In my program a chorus is repeated lines. Verses are new lyrics and you 
probably will not see repeated lines in these sections. Right now there 
are only these two tags. 

With this simple structure of Chorus and Verses it will choose what to start
with based off of the probability of each. It will then flip flop between 
the two based off the number of lines each section was found to be on average. 

#### Improvements

* Read in more tags
* With more tags a more complex structure where it does not just flip flop. 


# Does it do what was intended!? 

**Kind of** 

The songs it makes will not trick any human. There are a few lines that
are pretty good and will make you laugh, but that is mostly it. 

I think with more work and with some of the improvements stated above 
I could get close to tricking someone. Or at least be better than it is. 

## More improvements 

* Have a bigger source of songs. Right now there are only 8 songs
I had to import each song by hand because I did not want to write a
web scrapper at the moment and wanted to focus more on the AI side. 

# Does it show Classical Conditioning 

Kinda. It does *learn* in some way on how songs work but it does not get
stimulus. I do not count the inputted songs as stimulus really. Although 
if more songs are inputted it will change how the song is generated slightly. 

## Could Classical Conditioning be added? 

At the state it is in I don't believe I could add a real classical 
conditioning system with time and strengths. The word strength has 
some sense of conditioning but it is not *smart* in any real sense. 
It does not learn over time. With more lyrics it will get more chances
to get good lines. But that is about it. 

Maybe with an part of speech it would be able to learn and have a 
conditioning. Or if there is a system to tell what is a good line 
and what is a bad line. It could make more connections. I don't 
know how I would design that at this point. 
