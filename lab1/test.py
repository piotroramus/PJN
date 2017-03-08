import os

from guess_lang import guess
from lang_ngrams import lang_ngrams

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

n_range = range(2, 15)

generate_lang_ngrams = False
if generate_lang_ngrams:
    for n in n_range:
        print "Generating {}-grams...".format(n)
        lang_ngrams(n)

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

            all_percent = (success / float(samples_num))
            print "All percent: {}".format(all_percent)
            fn.write("{},{}\n".format(n, all_percent))
