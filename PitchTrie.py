from dataclasses import dataclass, field
import pandas as pd


@dataclass
class Pitch:
    type: str
    count = 0
    next_pitch: list=field(default_factory=[])

    def add_pitch(self): self.count += 1
    def get_pitch(self): return self.type
    def get_count(self): return self.count
    def add_next_pitch(self, pitch_): return self.next_pitch.append(pitch_)
    def get_next_pitches(self): return self.next_pitch
    def advance_pitch(self, next_pitch_):
        for pitch_ in self.next_pitch:
            if next_pitch_ == pitch_.get_pitch():
                return pitch_



@dataclass
class PitchTrie:
    pitch_df: pd.DataFrame
    pitch_sequence = Pitch('node')

    def find_pitches(self):
        for pitch_ in [x for x in self.pitch_df["pitch_type"].unique()]:
            self.pitch_sequence[pitch_] = Pitch(pitch_)
        
    def sequence(self):
        self.find_pitches()
        working_list = self.pitch_sequence
        for idx, row in self.pitch_df.iterrows():
            current_pitch = row["pitch_type"]
            if row["balls"] + row["strikes"] == 0:
                working_list = self.pitch_sequence
            # Use a next_pitch bool to escape the for loop...
            next_pitch = False
            for pitch_ in working_list.get_next_pitches():
                if current_pitch == pitch_.get_pitch():
                    working_list = pitch_
                    working_list.add_pitch()
                    next_pitch = True
                    break
                elif next_pitch == True:
                    break
            if next_pitch == False:
                working_list.add_next_pitch(Pitch(current_pitch))
                working_list = working_list.advance_pitch(current_pitch)
    
    # Need to figure out a way to print out the sequence...
    def get_sequence(self): 
        # Attempting to make a printable list out of the objects via recursion...
        def search_arrays(node, current_dict):
            for x in node.get_next_pitches():
                current_dict[x.get_pitch()] = {'count': x.get_count(), 'next_pitches': x.get_next_pitches()}
                current_dict = current_dict[x.get_pitch()]
                if len(current_dict['next_pitches']) != 0:
                    search_arrays(node, current_dict)
                else:
                    return current_dict

        temp_dict = {}
        for pitch_ in self.pitch_sequence.get_next_pitches():
            temp_dict[pitch_] = search_arrays(self.pitch_sequence, {})
        print(temp_dict)


# Let's make a test of the class
def test():
    pass