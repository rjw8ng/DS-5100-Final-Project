import pandas as pd
import numpy as np
import random

class Die:
    
    def __init__(self, face):
        self.face = face
        self.weight = [1.0 for i in face]
        self.df = pd.DataFrame({"face": self.face, "weight": self.weight})
    
    def change_weight(self, face_value, new_weight):
        '''
        Takes two arguments: the face value to be changed and the new weight.
        Changes the weights value of the face inputted.
        
        '''
        
        if face_value not in self.df["face"].values:
            print("Face not in DataFrame!")
        else:
            try: 
                self.df.loc[(self.df["face"]==face_value)] = [face_value, float(new_weight)]
                
            except:
                print("Weight value cannot be converted to float!")
                
    def roll(self, amount = 1):
        '''
        Takes a parameter of how many times the die is to be rolled.
        Returns a list of outcomes.
        
        '''
        
        lst = [i for i in self.df["weight"]]
        sm = sum(lst)
        p = [x / sm for x in lst]
        
        result = np.random.choice([i for i in self.df["face"]], amount, p = p)
        
        return result
    
    def show(self):
        '''
        Returns the dataframe created in the initializer.
        '''
        return self.df
    
class Game:
    
    def __init__(self, die_object):
        self.die_object = die_object
    
    def play(self, turns):
        new_df = pd.DataFrame(columns = ["Roll_Number", "Die", "Roll"])
        
        counter = 0
        for i in self.die_object:
            
            temp_df = pd.DataFrame()
            
            output_list = i.roll(turns)
            length = len(output_list)
            
            
            temp_df["Roll_Number"] = [int(j) for j in range(1, length+1)]
            temp_df["Die"] = [counter for k in range(1, length+1)]
            temp_df["Roll"] = output_list
            
            new_df = pd.concat([new_df, temp_df], ignore_index=True)
            counter += 1
        
        new_df["Roll Number"] = new_df['Roll_Number']
        new_df = new_df[["Roll_Number", "Roll Number", "Die", "Roll"]]
        
        return new_df.set_index('Roll_Number')
        
    def show_game(self, dataframe, form = 'wide'):
        
        if form != 'wide' and form != 'narrow':
            print("Set second arguement to either 'wide' or 'narrow'!")
            
        elif form == 'wide':
            return dataframe.pivot(index = "Roll Number", columns = "Die", values = "Roll")
        else:
            return dataframe.set_index(["Die", "Roll Number"]) 
        
class Analyzer:
    
    def __init__(self, result):
        self.result = result
        self.jackpot_result = pd.DataFrame({"Roll Number": [],"Value": []})
        
    def jackpot(self):
        '''
        Returns an integer for the number times to the user.
        Stores the results as a dataframe of jackpot results in a public attribute.
        
        '''
        self.jackpot_df = pd.DataFrame({"Roll Number": [],"Value": []})
        
        self.jackpot_count = 0
        
        turns = max(self.result["Roll Number"])
        
        for i in range(1, turns + 1):
            lst = [j for j in self.result[self.result["Roll Number"]==i]["Roll"]]
            
            counts = lst.count(lst[0])
            list_length = len(lst)
            
            if counts == list_length:
                self.jackpot_df.loc[len(self.jackpot_df)] = [i, lst[0]]
                self.jackpot_count += 1
            else:
                pass
            
        self.jackpot_result = self.jackpot_df
        
        return self.jackpot_count
                   
    def combo(self):
        '''
        Compute the distinct combinations of faces rolled, along with their counts.
        Stores the results as a dataframe in a public attribute.
        
        '''
        self.combo_df = pd.DataFrame()
        
        temp_lst = [i for i in self.result["Roll"]]
        temp_lst = sorted(list(set(temp_lst)))
        
        columns = []
        for i in range(1, len(set(self.result["Die"]))+1):
            columns.append(i) 
            self.combo_df[i] = ""
        self.combo_df["count"] = ""
        
        temp_dict = {}
        
        turns = max(self.result["Roll Number"])
        
        for i in range(1, turns + 1):
            lst = [str(j) for j in self.result[self.result["Roll Number"] == i]["Roll"]]
            
            lst = sorted(lst)
            lst_string = " ".join(lst)
            
            if lst_string in temp_dict:
                temp_dict[lst_string] += 1
            else:
                temp_dict[lst_string] = 1 
        
        for key, value in temp_dict.items():
            lst_values = key.split(" ")
            df_lst = [i for i in lst_values]
            df_lst.append(value)
            self.combo_df.loc[len(self.combo_df)] = df_lst
        
        self.combo_df = self.combo_df.sort_values(by = columns)
        
        return self.combo_df.set_index(columns) 
        
            
    def face_counts_per_roll(self):
        '''
        Compute how many times a given face is rolled in each event.
        Stores the results as a dataframe in a public attribute.
        
        '''
        
        turns = max(self.result["Roll Number"])
        distinct_outcomes = set(self.result["Roll"])
        distinct_outcomes = sorted([i for i in distinct_outcomes])
        
        df = pd.DataFrame()
        
        for i in distinct_outcomes:
            df[i] = ""
        
        for i in range(1, turns + 1):
            lst = [j for j in self.result[self.result["Roll Number"] == i]["Roll"]]
            
            temp_list = []
            for j in distinct_outcomes:
                temp_list.append(lst.count(j))
            
            df.loc[len(df)] = temp_list
        
        return df
