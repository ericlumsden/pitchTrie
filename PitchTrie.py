from dataclasses import dataclass, field
import json
import pandas as pd
import pydot

# Need multiple instances of the Pitch class
class Pitch:
    def __init__(self, name, seq):
        self.name = name
        self.seq = seq
        self.count = 1
        self.next_pitch = []

    def add_pitch(self): self.count += 1
    def get_pitch(self): return self.name
    def get_seq(self): return self.seq
    def get_count(self): return self.count
    def add_next_pitch(self, pitch_): self.next_pitch.append(pitch_)
    def get_next_pitches(self): return self.next_pitch
    def advance_pitch(self, next_pitch_, next_seq_):
        if next_seq_ == None:
            return 
        for pitch_ in self.next_pitch:
            if (next_pitch_ == pitch_.get_pitch()) and (next_seq_ == pitch_.get_seq()):
                return pitch_
    # to make conversion to json easier...
    def dictionize(self): return {'count': self.count, 'next_pitches': {}}
    # recursive nature of collecting data can happen right here in the Pitch class
    def jsonify(self):
        temp_dict = self.dictionize()
        for next_pitch in self.get_next_pitches():
            temp_dict['next_pitches'][next_pitch.get_pitch()] = next_pitch.jsonify()
        return temp_dict



@dataclass
class PitchTrie:
    pitch_df: pd.DataFrame
    pitch_sequence = Pitch('node', '')
    seq_dict: dict=field(default_factory=lambda: {})

    def sequence(self):
        working_list = self.pitch_sequence
        seq_str = '' # seq_str keeps track of the pitch sequence to make sure the pitch object affected isn't an instance of that pitch in a different sequence
        for idx, row in self.pitch_df.iterrows():
            current_pitch = row["pitch_type"]
            if row["balls"] + row["strikes"] == 0:
                working_list = self.pitch_sequence
                seq_str = ''
            seq_str += current_pitch
            # Use a next_pitch bool to escape the for loop...
            next_pitch = False
            for pitch_ in working_list.get_next_pitches():
                if (current_pitch == pitch_.get_pitch()) and (seq_str == pitch_.get_seq()):
                    pitch_.add_pitch()
                    next_pitch = True
                    working_list = working_list.advance_pitch(current_pitch, seq_str)
                    break
            if next_pitch == False:
                working_list.add_next_pitch(Pitch(current_pitch, seq_str))
                working_list = working_list.advance_pitch(current_pitch, seq_str)

    def graph_node(self, graph, prev_node, node):
        graph.add_edge(pydot.Edge(f"{prev_node.get_pitch()} (count: {prev_node.get_count()}, seq: {prev_node.get_seq()})", f"{node.get_pitch()} (count: {node.get_count()}, seq: {node.get_seq()})"))

    def traverse_trie(self, graph, prev_node):
        if len(prev_node.get_next_pitches()) == 0:
            pass
        for node in prev_node.get_next_pitches():
            self.graph_node(graph, prev_node, node)
            self.traverse_trie(graph, node)

    def graph_sequence(self, title='PitchTrie'):
        for first_pitch in self.pitch_sequence.get_next_pitches():
            graph = pydot.Dot(graph_type='graph')
            self.traverse_trie(graph, first_pitch)
            graph.write_png(f'{title}_firstPitch_{first_pitch.get_pitch()}.png')
    
    def json_transform(self, file_name='PitchTrie-json'):
        temp_dict = self.pitch_sequence.jsonify()
        with open(f"{file_name}.json", "w") as f:
            json.dump(temp_dict, f, indent=4)
        



# Let's make a test of the class
def test(temp_sequence):
    test_trie = PitchTrie(temp_sequence)
    test_trie.sequence()
    test_trie.graph_sequence(title='ColeTest')
    test_trie.json_transform(file_name='ColeTest')


if __name__ == "__main__":
    # lookup from pybaseball takes some time... maybe save to a .csv down the road to speed this up
    from pybaseball import playerid_lookup, statcast_pitcher
    cole_id = playerid_lookup('cole', 'gerrit')
    cole_sequence = cole_id["key_mlbam"][0]

    cole_v_boston = statcast_pitcher('2023-08-19', '2023-08-21', cole_sequence)
    cole_v_boston.head()
    # the df is in reverse chronological order, first row is the last pitch he threw... gotta reverse it
    test(cole_v_boston.iloc[::-1])