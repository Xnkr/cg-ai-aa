import pandas as pd
match_test = pd.read_csv('Testmatches.csv')
deliv_test = pd.read_csv('TestDeliveries.csv')

uniq_ids = match_test.match_id.unique()
sub = pd.DataFrame(uniq_ids)
sub.columns = ["match_id"]

innings = [1,2]
sub = match_test[["match_id","team1"]]

entries = []
for idx in sub["match_id"]:
    for inning in innings:
        try:
            bat = (deliv_test[(deliv_test["match_id"] == idx) & (deliv_test["inning"] == inning)]["batting_team"].unique().tolist())[0]
        except IndexError:
            continue
        entries.append([idx,inning,bat,sum(deliv_test[(deliv_test["match_id"] == idx) & (deliv_test["inning"] == inning)]["total_runs"])])
           
batting_table = pd.DataFrame(entries,columns=['match_id','innings','batting_team','inning_score'])

for idx in sub["match_id"]:
    try:
        in1_score = batting_table[(batting_table["match_id"] == idx) & (batting_table["innings"] == innings[0])]["inning_score"].tolist()[0]
        in2_score = batting_table[(batting_table["match_id"] == idx) & (batting_table["innings"] == innings[1])]["inning_score"].tolist()[0]
        if in1_score > in2_score:
            winning = batting_table[(batting_table["match_id"] == idx) & (batting_table["innings"] == innings[0])]["batting_team"].tolist()[0]
            if sub[sub["match_id"] == idx]["team1"].tolist()[0] == winning:
                sub.loc[sub["match_id"] == idx,"team_1_win_flag"] = 1
            else:
                sub.loc[sub["match_id"] == idx,"team_1_win_flag"] = 0
        elif in1_score < in2_score:
            winning = batting_table[(batting_table["match_id"] == idx) & (batting_table["innings"] == innings[1])]["batting_team"].tolist()[0]
            if sub[sub["match_id"] == idx]["team1"].tolist()[0] == winning:
                sub.loc[sub["match_id"] == idx,"team_1_win_flag"] = 1
            else:
                sub.loc[sub["match_id"] == idx,"team_1_win_flag"] = 0
        
        else:
            sub.loc[sub["match_id"] == idx,"team_1_win_flag"] = 0
    except IndexError:
        sub.loc[sub["match_id"] == idx,"team_1_win_flag"] = 0
        continue

final_sub = sub[['match_id','team_1_win_flag']]
print(final_sub.head())
final_sub.to_csv('AAsub.csv',index=False)