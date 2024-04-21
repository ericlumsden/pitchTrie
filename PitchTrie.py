from dataclasses import dataclass, field
import pandas as pd


@dataclass
class Pitch:
    type: str
    count = 0
    next_pitch: list=field(default_factory=[])

    def add_pitch(self): self.count += 1
    def get_pitch(self): self.type
    def add_next_pitch(self, pitch_): self.next_pitch.append(pitch_)
    def get_next_pitches(self): self.next_pitch



@dataclass
class PitchTrie:
    pitch_df: pd.DataFrame
    pitch_sequence = Pitch('node')
    pitches: list=[]

    def find_pitches(self):
        self.pitches = [x for x in self.pitch_df["pitch_type"].unique()]
        for pitch_ in self.pitches:
            self.pitch_sequence[pitch_] = Pitch(pitch_)
        
    def sequence(self):
        self.find_pitches()
        working_list = self.pitch_sequence
        for idx, row in self.pitch_df.iterrows():
            current_pitch = row["pitch_type"]
            if row["balls"] + row["strikes"] == 0:
                working_list = self.pitch_sequence
            next_pitch = False
            for pitch_ in working_list.get_next_pitches():
                if current_pitch == pitch_.get_pitch():
                    working_list = pitch_
                    working_list.add_pitch()
                    working_list = working_list
                    next_pitch = True
            if next_pitch == False:
                working_list.add_next_pitch(Pitch(current_pitch))
    
    def get_sequence(self): print(self.pitch_sequence)