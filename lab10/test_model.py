# coding=utf-8

import gensim
import io

print "Loading model..."
model = gensim.models.Word2Vec.load("wiki.pl.text.model")
print "Model loaded"

word_vectors = model.wv
del model

morfosyntactic_cases = {
    u'singular_plural_noun': [
        {
            'positive': [u'kot', u'psy'],
            'negative': [u'pies']
        },
        {
            'positive': [u'głowa', u'nogi'],
            'negative': [u'noga']
        },
        {
            'positive': [u'krzesło', u'stoły'],
            'negative': [u'stół']
        },
        {
            'positive': [u'piwo', u'wina'],
            'negative': [u'wino']
        },
        {
            'positive': [u'drzewa', u'kwiaty'],
            'negative': [u'kwiat']
        }
    ],
    u'present_past_verb': [
        {
            'positive': [u'jestem', u'jest'],
            'negative': [u'był']
        },
        {
            'positive': [u'chodzi', u'spał'],
            'negative': [u'śpi']
        },
        {
            'positive': [u'mówi', u'słuchał'],
            'negative': [u'słucha']
        },
        {
            'positive': [u'pisze', u'czytała'],
            'negative': [u'czyta']
        },
        {
            'positive': [u'rozmawia', u'patrzyła'],
            'negative': [u'patrzy']
        }
    ],
    u'genitive_nominative_noun': [
        {
            'positive': [u'kota', u'pies'],
            'negative': [u'psa']
        },
        {
            'positive': [u'domu', u'samochód'],
            'negative': [u'samochodu']
        },
        {
            'positive': [u'wody', u'powietrze'],
            'negative': [u'powietrza']
        },
        {
            'positive': [u'księżyca', u'słońce'],
            'negative': [u'słońca']
        },
        {
            'positive': [u'cię', u'ja'],
            'negative': [u'mnie']
        }
    ]
}

semantic_cases = {
    u'noun_type': [
        {
            'positive': [u'stół', u'zwierzę'],
            'negative': [u'kot']
        },
        {
            'positive': [u'człowiek', u'rzecz'],
            'negative': [u'zabawka']
        },
        {
            'positive': [u'dom', u'roślina'],
            'negative': [u'jabłoń']
        },
        {
            'positive': [u'kot', u'pojazd'],
            'negative': [u'samochód']
        },
        {
            'positive': [u'woda', u'jedzenie'],
            'negative': [u'makaron']
        }
    ],
    u'noun_association': [
        {
            'positive': [u'francja', u'pierogi'],
            'negative': [u'polska']
        },
        {
            'positive': [u'mrówka', u'leń'],
            'negative': [u'kot']
        },
        {
            'positive': [u'włochy', u'wódka'],
            'negative': [u'polska']
        },
        {
            'positive': [u'belgia', u'ser'],
            'negative': [u'szwajcaria']
        },
        {
            'positive': [u'kot', u'przyjaciel'],
            'negative': [u'pies']
        }
    ],
    u'part_whole': [
        {
            'positive': [u'mieszkaniec', u'ciało'],
            'negative': [u'głowa']
        },
        {
            'positive': [u'obywatel', u'dłoń'],
            'negative': [u'palec']
        },
        {
            'positive': [u'koło', u'zeszyt'],
            'negative': [u'kartka']
        },
        {
            'positive': [u'państwo', u'kraj'],
            'negative': [u'województwo']
        },
        {
            'positive': [u'słowo', u'alfabet'],
            'negative': [u'litera']
        }
    ]
}


def process(output_file, cases):
    print "Saving results to {} ...".format(output_file)
    with io.open(output_file, 'w', encoding='utf-8') as f:
        for case in cases:
            f.write(u'===========================\n')
            f.write(case)
            f.write(u'\n')
            for d in cases[case]:
                result = word_vectors.most_similar(
                    positive=d['positive'],
                    negative=d['negative'],
                    topn=5,
                )
                f.write(d['positive'][0])
                f.write(u' - ')
                f.write(d['negative'][0])
                f.write(u' + ')
                f.write(d['positive'][1])
                f.write(u':\n')
                for word, value in result:
                    f.write(word)
                    f.write(u': {}\n'.format(value))
                f.write(u'\n')


process('results/morfosyntactic.txt', morfosyntactic_cases)
process('results/semantic.txt', semantic_cases)
