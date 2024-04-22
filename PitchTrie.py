from dataclasses import dataclass
import pandas as pd

# Need multiple instances of the Pitch class
class Pitch:
    def __init__(self, name, seq):
        self.name = name
        self.seq = name
        self.count = 1
        self.next_pitch = []

    def add_pitch(self): self.count += 1
    def get_pitch(self): return self.name
    def get_seq(self): return self.seq
    def get_count(self): return self.count
    def add_next_pitch(self, pitch_): self.next_pitch.append(pitch_)
    def get_next_pitches(self): return self.next_pitch
    def advance_pitch(self, next_pitch_):
        for pitch_ in self.next_pitch:
            if next_pitch_ == pitch_.get_pitch():
                return pitch_



@dataclass
class PitchTrie:
    pitch_df: pd.DataFrame
    pitch_sequence = Pitch('node', '')

    def sequence(self):
        working_list = self.pitch_sequence
        seq_str = ''
        for idx, row in self.pitch_df.iterrows():
            current_pitch = row["pitch_type"]
            if row["balls"] + row["strikes"] == 0:
                working_list = self.pitch_sequence
                seq_str = ''
            seq_str += current_pitch
            next_pitch = False
            for pitch_ in working_list.get_next_pitches():
                if (current_pitch == pitch_.get_pitch()) and (seq_str == pitch_.get_seq()):
                    pitch_.add_pitch()
                    next_pitch = True
                    working_list = working_list.advance_pitch(current_pitch)
                    break
            # Use a next_pitch bool to escape the for loop...
            if next_pitch == False:
                working_list.add_next_pitch(Pitch(current_pitch, seq_str))
                working_list = working_list.advance_pitch(current_pitch)
    
    # Need to figure out a way to print out the sequence...
    def get_sequence(self): 
        def traverse_objects(nodes, temp_dict_):
            for node in nodes.get_next_pitches():
                working_list = node
                temp_dict_[node.get_pitch()] = {'count': node.get_count(), 'next_pitches': {f'{next_pitch.get_pitch()}': {} for next_pitch in node.get_next_pitches()}}
                if len(node.get_next_pitches()) == 0:
                    return temp_dict_
                else:
                    traverse_objects(working_list, temp_dict_[node.get_pitch()])

        temp_dict = {}
        for pitch_ in self.pitch_sequence.get_next_pitches():
            temp_dict[pitch_.get_pitch()] = traverse_objects(self.pitch_sequence, {})
        print(temp_dict)



# Let's make a test of the class
def test(temp_sequence):
    test_trie = PitchTrie(temp_sequence)
    test_trie.sequence()
    test_trie.get_sequence()

if __name__ == "__main__":
    # lookup from pybaseball takes some time... maybe save to a .csv down the road to speed this up
    from pybaseball import playerid_lookup, statcast_pitcher
    cole_id = playerid_lookup('cole', 'gerrit')
    cole_sequence = cole_id["key_mlbam"][0]

    cole_v_boston = statcast_pitcher('2023-08-19', '2023-08-21', cole_sequence)
    cole_v_boston.head()
    # the df is in reverse chronological order, first row is the last pitch he threw... gotta reverse it
    test(cole_v_boston.iloc[::-1])