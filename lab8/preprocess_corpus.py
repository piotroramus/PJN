import re

corpus_file = 'resources/potop/potop.txt'
out_file = 'resources/potop/potop_preprocessed.txt'

with open(corpus_file, 'rb') as f:
    content = f.read().decode('utf-8')

    content = re.sub(r'\s+', '', content, flags=re.UNICODE)

    with open(out_file, 'wb') as out:
        out.write(content.encode('utf-8'))
