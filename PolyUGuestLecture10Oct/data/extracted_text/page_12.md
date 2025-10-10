# Page 12

3724                                            Multimedia Tools and Applications (2023) 82:3713–3744


the users in prioritizing their messages based on the emotions attached with the message. Seal
et al. (2020) [120] proposed an efficient emotion detection method by searching emotional
words from a pre-defined emotional keyword database and analyzing the emotion words,
phrasal verbs, and negation words. Their proposed approach exhibited better performance than
recent approaches.
    Semantic Role Labeling (SRL) works by giving a semantic role to a sentence. For example,
in the PropBank (Palmer et al., 2005) [100] formalism, one assigns roles to words that are
arguments of a verb in the sentence. The precise arguments depend on the verb frame and if
multiple verbs exist in a sentence, it might have multiple tags. State-of-the-art SRL systems
comprise several stages: creating a parse tree, identifying which parse tree nodes represent the
arguments of a given verb, and finally classifying these nodes to compute the corresponding
SRL tags.
    Event discovery in social media feeds (Benson et al.,2011) [13], using a graphical model to
analyze any social media feeds to determine whether it contains the name of a person or name
of a venue, place, time etc. The model operates on noisy feeds of data to extract records of
events by aggregating multiple information across multiple messages, despite the noise of
irrelevant noisy messages and very irregular message language, this model was able to extract
records with a broader array of features on factors.
    We first give insights on some of the mentioned tools and relevant work done before
moving to the broad applications of NLP.

3.2 Applications of NLP

Natural Language Processing can be applied into various areas like Machine Translation,
Email Spam detection, Information Extraction, Summarization, Question Answering etc. Next,
we discuss some of the areas with the relevant work done in those directions.

a) Machine Translation

As most of the world is online, the task of making data accessible and available to all is a
challenge. Major challenge in making data accessible is the language barrier. There are a
multitude of languages with different sentence structure and grammar. Machine Translation is
generally translating phrases from one language to another with the help of a statistical engine
like Google Translate. The challenge with machine translation technologies is not directly
translating words but keeping the meaning of sentences intact along with grammar and tenses.
The statistical machine learning gathers as many data as they can find that seems to be parallel
between two languages and they crunch their data to find the likelihood that something in
Language A corresponds to something in Language B. As for Google, in September 2016,
announced a new machine translation system based on artificial neural networks and Deep
learning. In recent years, various methods have been proposed to automatically evaluate
machine translation quality by comparing hypothesis translations with reference translations.
Examples of such methods are word error rate, position-independent word error rate (Tillmann
et al., 1997) [138], generation string accuracy (Bangalore et al., 2000) [8], multi-reference
word error rate (Nießen et al., 2000) [95], BLEU score (Papineni et al., 2002) [101], NIST
score (Doddington, 2002) [35] All these criteria try to approximate human assessment and
often achieve an astonishing degree of correlation to human subjective evaluation of fluency
and adequacy (Papineni et al., 2001; Doddington, 2002) [35, 101].
