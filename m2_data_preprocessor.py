"""
13.06.2024

This file helps to preprocess data taken from the Building Educational
Applications 2019 Shared Task: Grammatical Error Correction
(https://www.cl.cam.ac.uk/research/nl/bea2019st/) where the data corresponds
to the m2 scheme.

Example of m2 entry as block:

S When I was younger I used to say that I wanted to be a teacher , a saleswoman and even a butcher .. I do n't know why .
A 4 4|||M:PUNCT|||,|||REQUIRED|||-NONE-|||0
A 22 23|||R:PUNCT|||.|||REQUIRED|||-NONE-|||0

In M2 format, lines starting with "S" represent original sentences, and lines
starting with "A" represent edit annotations. Each annotation line includes
the start and end token offsets of the edit, the error type, and the
tokenized  correction string. The next two fields are historical and can be
disregarded  (refer to the CoNLL-2013 shared task), while the final field
indicates the  annotator ID.
"""


class DataPreprocessor:
    """
    This class consists of several methods to extract source and target
    lists of tokens where the source contains grammatical errors and
    the target corresponds to a corrected version. For each file that is
    read, the processed data is stored in the class' attributes.
    """

    def __init__(self):
        """
        src_tokens and tgt_tokens are used to store lists with corrected
        tokens when m2 file is provided through read_m2_data().
        """
        self.raw_m2_entries = []
        self.data = []

    def read_m2_data(self, path):
        """
        Reads file input through the generator method read_m2_entry and appends
        each block in file to self.raw_data.

        Args:
            path: str, file path
        """
        for block in self.read_m2_entry(path):

            self.raw_m2_entries.append(block)

        self.create_sentence_tuples()

    def read_m2_entry(self, path):
        """
        This is a generator method that yields the blocks from the source as
        dictionaries.

        Args:
            path: str, file path
        """
        with open(path, "r") as open_file:

            block = []

            for line in open_file:
                if line.strip() == "":
                    if block:
                        # Yield each block
                        yield self.parse_block_to_dict(block)

                        # Reset block after empty line
                        block = []
                else:
                    block.append(line.strip())

            # If there's any remaining block, it is also yielded
            if block:

                yield self.parse_block_to_dict(block)

    @staticmethod
    def parse_block_to_dict(block):
        """
        For each block as list a dictionary is created with the first
        element from the block, that is, the first line as key, and the
        following lines as values. These lines correspond to the corrections
        for the given first line.

        Arg:
            block, list: a list containing the m2 entries for each sentence

        Return:
            dict: key of the dictionary is the sentence "S" where each
            following line corresponds to the annotation.
        """
        block_dict = {}

        for line in block:

            # S indicates in m2 the original sentence
            if line[0] == "S":
                block_dict.update({line[2:]: []})

            # Lines that don't start with S are annotations
            else:

                for key in block_dict.keys():

                    annotation = line[2:].split("|||")
                    positions = [int(e) for e in annotation[0].split()]

                    block_dict[key].append([positions, annotation[2]])

        return block_dict

    def create_sentence_tuples(self):
        """
        Transforms the raw m2 data into two lists where the original
        sentence is matched with a corrected one.
        """
        for entry in self.raw_m2_entries:
            for sentence, corrections in entry.items():

                correction = self.apply_corrections_to_sentence(corrections,
                                                                sentence)

                self.data.append({"src": sentence,
                                  "tgt": " ".join(correction)})

    @staticmethod
    def apply_corrections_to_sentence(corrections, sentence):
        """
        Takes a list of corrections and applies them to a given sentence.
        Changes are dynamically stored so that multiple correction can be
        applied at the correct position. The implementation is inspired by
        insertion sort.

        Args:
            corrections, list: This list contains entries of corrections
            where each correction is itself a list with one entry for
            positions of the correction and one with the proposed corrected
            token(s).

            sentence, str: This is the original sentence from the data.

        Return:
            list: A list of tokens where all corrections are incorporated.
        """

        sentence = sentence.split()
        previous_change = 0  # Tracks positional changes from each correction

        for correction in corrections:

            pos1, pos2 = correction[0]  # Two integers for positions
            corrected_token = correction[1]

            #  noop sentences have -NONE- and should not be changed.
            if corrected_token != "-NONE-":

                pos1 = pos1 + previous_change
                pos2 = pos2 + previous_change

                if pos1 != pos2:

                    # Delete elements within range of positions
                    del sentence[pos1:pos2]

                    # Check that correction is not just deletion of tokens
                    if corrected_token != "":
                        sentence.insert(pos1, corrected_token)
                        previous_change += 1

                    previous_change += pos1-pos2

                else:

                    # Insert the corrected token at the specified position
                    sentence.insert(pos1, corrected_token)
                    previous_change += 1

        return sentence


if __name__ == "__main__":

    # File names from BEA 2019

    A_train = "A.train.gold.bea19.m2"
    B_train = "B.train.gold.bea19.m2"
    C_train = "C.train.gold.bea19.m2"

    A_dev = "A.dev.gold.bea19.m2"
    B_dev = "B.dev.gold.bea19.m2"
    C_dev = "C.dev.gold.bea19.m2"

    training_raw_data = [A_train, B_train, C_train]
    validation_raw_data = [A_dev, B_dev, C_dev]

    # Path to data of current project

    hard_path = "data/m2/"

    # Preprocessing training data

    preprocessor_training = DataPreprocessor()

    for file in training_raw_data:
        preprocessor_training.read_m2_data(hard_path + file)

    print(len(preprocessor_training.data))
    print(preprocessor_training.data[5:6])

    # Preprocessing validation data

    preprocessor_val = DataPreprocessor()

    for file in validation_raw_data:
        preprocessor_val.read_m2_data(hard_path + file)

    #print(len(preprocessor_val.data))
    #print(preprocessor_val.data[10:15])

