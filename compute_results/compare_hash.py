import hashlib

file1 = "output_grid_search/2024-06-18 10:58:29.907386/qualitas_corpus_n_gram_4_qr_18-06-24_10-58-41.csv"
file2 = "output_grid_search/2024-06-18 10:58:29.907386/qualitas_corpus_n_gram_4_qr_18-06-24_10-58-41.csv"
#file2 = "output_grid_search/2024-07-09 18:16:44.537017/1_nS_4_cS_6_qrN_8_qrT2_8_qrT1_8_qrO_8_boN_-1_boT2_-1_boT1_-1_boOr_-1_simT_20%,40%,60%,80%_56738460-5bbd-4528-a165-9bc05f8f6eef.csv"

def generate_hash(text):
    hash_obj = hashlib.sha256()
    hash_obj.update(text.encode('utf-8'))
    return hash_obj.hexdigest()

def compare_hashes(hash1, hash2):
    if hash1 == hash2:
        return "The hashes are identical."
    else:
        return "The hashes are different."

def main():
    text1 = open(file1, 'r').read()
    text2 = open(file2, 'r').read()

    hash1 = generate_hash(text1)
    hash2 = generate_hash(text2)

    print(f"Hash of the first text: {hash1}")
    print(f"Hash of the second text: {hash2}")

    result = compare_hashes(hash1, hash2)
    print(result)

if __name__ == "__main__":
    main()
