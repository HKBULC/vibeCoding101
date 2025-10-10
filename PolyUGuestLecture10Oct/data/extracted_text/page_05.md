# Page 05

Multimedia Tools and Applications (2023) 82:3713–3744                                      3717


with the use of a vocabulary. For example, in case of token drived, stemming results in “driv”,
whereas lemmatization attempts to return the correct basic form either drive or drived
depending on the context it is used.

d) Syntactic

After PoS tagging done at lexical level, words are grouped to phrases and phrases are grouped
to form clauses and then phrases are combined to sentences at syntactic level. It emphasizes the
correct formation of a sentence by analyzing the grammatical structure of the sentence. The
output of this level is a sentence that reveals structural dependency between words. It is also
known as parsing which uncovers the phrases that convey more meaning in comparison to the
meaning of individual words. Syntactic level examines word order, stop-words, morphology
and PoS of words which lexical level does not consider. Changing word order will change the
dependency among words and may also affect the comprehension of sentences. For example,
in the sentences “ram beats shyam in a competition” and “shyam beats ram in a competition”,
only syntax is different but convey different meanings [139]. It retains the stopwords as
removal of them changes the meaning of the sentence. It doesn’t support lemmatization and
stemming because converting words to its basic form changes the grammar of the sentence. It
focuses on identification on correct PoS of sentences. For example: in the sentence “frowns on
his face”, “frowns” is a noun whereas it is a verb in the sentence “he frowns”.

e) Semantic

On a semantic level, the most important task is to determine the proper meaning of a sentence.
To understand the meaning of a sentence, human beings rely on the knowledge about language
and the concepts present in that sentence, but machines can’t count on these techniques.
Semantic processing determines the possible meanings of a sentence by processing its logical
structure to recognize the most relevant words to understand the interactions among words or
different concepts in the sentence. For example, it understands that a sentence is about
“movies” even if it doesn’t comprise actual words, but it contains related concepts such as
“actor”, “actress”, “dialogue” or “script”. This level of processing also incorporates the
semantic disambiguation of words with multiple senses (Elizabeth D. Liddy, 2001) [68]. For
example, the word “bark” as a noun can mean either as a sound that a dog makes or outer
covering of the tree. The semantic level examines words for their dictionary interpretation or
interpretation is derived from the context of the sentence. For example: the sentence “Krishna
is good and noble.” This sentence is either talking about Lord Krishna or about a person
“Krishna”. That is why, to get the proper meaning of the sentence, the appropriate interpre-
tation is considered by looking at the rest of the sentence [44].

f) Discourse

While syntax and semantics level deal with sentence-length units, the discourse level of NLP
deals with more than one sentence. It deals with the analysis of logical structure by making
connections among words and sentences that ensure its coherence. It focuses on the properties
of the text that convey meaning by interpreting the relations between sentences and uncovering
linguistic structures from texts at several levels (Liddy,2001) [68]. The two of the most
common levels are: Anaphora Resolution and Coreference Resolution. Anaphora resolution
