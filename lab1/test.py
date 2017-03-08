import os

from guess_lang import guess
from lang_ngrams import lang_ngrams

from corpus_definitions import languages_set

test_samples = {
    "en1_l.txt": "en",
    "en2_l.txt": "en",
    "en3_s.txt": "en",
    "pl1_l.txt": "pl",
    "pl2_l.txt": "pl",
    "pl3_s.txt": "pl",
    "it1_l.txt": "it",
    "it2_l.txt": "it",
    "it3_s.txt": "it",
    "de1_l.txt": "de",
    "de2_l.txt": "de",
    "de3_s.txt": "de",
    "es1_l.txt": "es",
    "es2_l.txt": "es",
    "es3_s.txt": "es",
    "fl1_l.txt": "fl",
    "fl2_l.txt": "fl",
    "fl3_s.txt": "fl",
}

test_samples_dir = "test_samples"
samples_num = len(test_samples)

metrics = ["cosine", "taxi", "euclidean", "max"]
languages = languages_set()

n_range = range(2, 6)

generate_lang_ngrams = False
if generate_lang_ngrams:
    for n in n_range:
        print "Generating {}-grams...".format(n)
        lang_ngrams(n)

process_by_metric = False
if process_by_metric:
    for metric in metrics:
        print "Processing metric {}".format(metric)

        with open(os.path.join("test_results", "test_{}.txt".format(metric)), 'w') as fn:
            fn.write("n,\%\n")
            for n in n_range:

                success = 0
                for test_sample in test_samples:
                    input_file = os.path.join(test_samples_dir, test_sample)
                    best_language = guess(input_file, metric, n)

                    if best_language == test_samples[test_sample]:
                        success += 1

                accuracy = (success / float(samples_num))
                print "All percent: {}".format(accuracy)
                fn.write("{},{}\n".format(n, accuracy))

process_by_lang = True
if process_by_lang:
    for metric in metrics:

        with open(os.path.join("test_results", "test_{}_bylang.txt".format(metric)), 'w') as fn:
            fn.write("lang,precision,recall,f1,accuracy\n")

            for lang in languages:

                true_positives = 0
                true_negatives = 0
                false_negatives = 0
                false_positives = 0

                for n in n_range:

                    for sample in test_samples:

                        input_file = os.path.join(test_samples_dir, sample)
                        guessed_language = guess(input_file, metric, n)

                        if test_samples[sample] == lang:
                            if guessed_language == test_samples[sample]:
                                true_positives += 1
                            else:
                                false_negatives += 1
                        else:
                            if guessed_language == test_samples[sample]:
                                true_negatives += 1
                            else:
                                false_positives += 1

                precision = true_positives / float(true_positives + false_positives)
                recall = true_positives / float(true_positives + false_negatives)
                f1 = 2 * ((precision * recall) / float(precision + recall))
                accuracy = (true_positives + true_negatives) / float(
                    true_positives + false_positives + true_negatives + false_negatives)

                fn.write("{},{},{},{},{}\n".format(lang, precision, recall, f1, accuracy))
