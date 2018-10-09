import pandas as pd

NOUN_TAGS = [pos.lower() for pos in [
    'ND1', 'NN', 'NN1', 'NN2', 'NNA', 'NNB', 'NNL1', 'NNL2', 'NNO', 'NNO2', 'NNT1', 'NNT2', 'NNU', 'NNU1', 'NNU2', 'NP',
    'NP1', 'NP2', 'NPD1', 'NPD2', 'NPM1', 'NPM2',
]]
ADJ_TAGS = [pos.lower() for pos in ['JJ', 'JJR', 'JJT', 'JK']]

SENTENCE_END_WORDS = ['.', '?', '!']


def just_words(df):
    """
    remove all punctuation from given DataFrame
    :param file_data: DataFrame
    :return: DataFrame
    """
    df = df.query('POS != "y"').query('POS != "\\""')
    return df[df["POS"].notnull()]


def get_ttr(df):
    """
    get the type token ratio
    :param df: Input DataFrame
    :type df: pd.DataFrame()
    :type return: float
    """
    words = just_words(df)
    number_unique = len(words.word.unique())
    number_all = len(words)
    ttr = number_unique / number_all
    return ttr


def get_nouniness(df):
    """
    get the nouniness
    :param df: Input DataFrame
    :type df: pd.DataFrame()
    :type return: float
    """
    df = just_words(df)
    number_all = len(df)
    # create DataFrame of just nouns
    just_nouns = df[df['POS'].isin(NOUN_TAGS)]
    nouniness = len(just_nouns)/number_all # TODO: normalization
    return nouniness


def get_mean_word_len(df):
    """
    get the mean word length
    :param df: Input DataFrame
    :type df: pd.DataFrame()
    :type return: float
    """
    df = just_words(df)
    number_all = len(df)
    # add new column to DataFrame for length of word
    df['word_length'] = df['word'].str.len()
    # add up all word lengths
    total_length = df['word_length'].sum()
    return total_length/number_all


def get_mean_sentence_len(df):
    """
    get the mean sentence length
    :param df: Input DataFrame
    :type df: pd.DataFrame()
    :type return: float
    """
    sentences = [
        []
    ]
    index = 0
    # convert DataFrame to a list
    rows = df.values

    for word, lemma, pos in rows:
        # check if item is punctuation
        # the word in SENTENCE_END_WORDS is because
        #  the ! was not counting as end punctuation
        if pos == 'y' or word == '"' or word in SENTENCE_END_WORDS:
            # check if item is end punctuation
            if word in SENTENCE_END_WORDS:
                # End of sentence. Move to next sentence
                index += 1
                sentences.append([])
        else:
            # Add word to sentence
            sentences[index].append(word)

    sentence_lengths = [len(l) for l in sentences]
    total_sentence_length = sum(sentence_lengths)
    mean_sentence_length = total_sentence_length/len(sentence_lengths)

    return mean_sentence_length


def get_np_info(df):
    """
    get the mean and max np
    :param df: Input DataFrame
    :type df: pd.DataFrame()
    :type return: float
    """
    noun_phrases = [
        []
    ]
    index = 0
    # convert DataFrame to a list
    rows = df.values

    for word, _, pos in rows:
        # check if item is noun or adjective
        if pos in NOUN_TAGS or pos in ADJ_TAGS:
            # add word to current phrase
            noun_phrases[index].append(word)
        else:
            # increase index and add a new list
            index += 1
            noun_phrases.append([])

    np_lengths = [len(l) for l in noun_phrases]
    total_np_length = sum(np_lengths)
    mean_np = total_np_length/len(np_lengths)

    max_np = max(np_lengths)

    # same as before, if you return two vars like this you can also assign them to two vars where you call it
    return mean_np, max_np


def get_sub_conj(df):
    """
    get the mean word length
    :param df: Input DataFrame
    :type df: pd.DataFrame()
    :type return: float
    """
    df = just_words(df)
    number_all = len(df)
    # create DataFrame of just subordinating conjunctions
    num_sub_conj = len(df.query('POS == "cs"'))
    return num_sub_conj/number_all
