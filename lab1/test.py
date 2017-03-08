import os

from guess_lang import guess
from lang_ngrams import lang_ngrams

test_samples = {
    "en1.txt": "en",
    "en2.txt": "en",
    "en3.txt": "en",
    "pl1.txt": "pl",
    "pl2.txt": "pl",
    "pl3.txt": "pl",
    "it1.txt": "it",
    "it2.txt": "it",
    "it3.txt": "it",
    "de1.txt": "de",
    "de2.txt": "de",
    "de3.txt": "de",
    "es1.txt": "es",
    "es2.txt": "es",
    "es3.txt": "es",
    "fl1.txt": "fl",
    "fl2.txt": "fl",
    "fl3.txt": "fl",
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
