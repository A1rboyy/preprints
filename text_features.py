import textstat

def calculate_text_features(text):

    return {

        "word_count":
            len(text.split()),

        "sentence_count":
            textstat.sentence_count(text),

        "flesch_reading_ease":
            textstat.flesch_reading_ease(text),

        "gunning_fog":
            textstat.gunning_fog(text),

        "flesch_kincaid_grade":
            textstat.flesch_kincaid_grade(text),

        "avg_sentence_length":
            textstat.avg_sentence_length(text),

        "avg_letter_per_word":
            textstat.avg_letter_per_word(text),

        "lexicon_count":
            textstat.lexicon_count(text)
    }