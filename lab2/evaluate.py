from metrics import longest_common_substring_metric


def load_clusters(input_file):
    clusters = dict()
    cluster_num = 0
    with open(input_file, 'r') as f:
        for line in f:
            if line.startswith('#'):
                cluster_num += 1
                continue
            if line == '\n':
                continue
            if cluster_num in clusters:
                clusters[cluster_num].append(line)
            else:
                clusters[cluster_num] = [line]
    return clusters


def load_centroids(input_file):
    centroids = dict()
    with open(input_file, 'r') as f:
        for line in f:
            k, v = line.split(":")
            k, v = int(k), v.strip()
            centroids[k] = v
    return centroids


def compute_centorids(clusters, output_file, metric):
    cluster_num = len(clusters)
    with open(output_file, 'w') as f:
        for i in xrange(1, cluster_num + 1):
            print "Processing cluster {}...".format(i)
            centroid = None
            min_dist = 99999999999
            num_of_vectors = len(clusters[i])
            for m in xrange(num_of_vectors):
                sum_dist = 0
                for n in xrange(num_of_vectors):
                    if n != m:
                        sum_dist += metric(clusters[i][m], clusters[i][n])
                if sum_dist < min_dist:
                    min_dist = sum_dist
                    centroid = clusters[i][m]
            f.write("{}: {}".format(i, centroid))


def match_clusters(reference_centroids, computed_clusters, metric, threshold, out_file):
    matching_clusters = dict()
    with open(out_file, 'w') as f:
        f.write("#ref_cluster_id: compute_cluster_id")
        for rc in reference_centroids:
            print "Matching ref cluster {}...".format(rc)
            best_fitting_id = -1
            best_fitting_max = -1
            for cc_list in computed_clusters:
                fitting_entries = 0
                for cc in computed_clusters[cc_list]:
                    if metric(reference_centroids[rc], cc) < threshold:
                        fitting_entries += 1
                if fitting_entries > best_fitting_max:
                    best_fitting_id = cc_list
                    best_fitting_max = fitting_entries
            matching_clusters[rc] = best_fitting_id
            f.write("{}: {}\n".format(rc, best_fitting_id))

    return matching_clusters


computed_clusters = load_clusters('out_levenshtein_0_5.txt')

# only for the first time
perform_centroids_computing = False
if perform_centroids_computing:
    reference_clusters = load_clusters('resources/clusters_pp.txt')
    compute_centorids(reference_clusters, 'resources/ref_centroids.txt', longest_common_substring_metric)
ref_centroids = load_centroids('resources/ref_centroids.txt')

match_clusters(ref_centroids, computed_clusters, longest_common_substring_metric, 0.5, 'resources/matching_cluster.txt')
