import re
import requests

def print_table(win):
    row_format ='{:>3} <= p < {:>3} : {:>5}   {:>6}%'
    for i in range(10):
        a = str(i*10)
        b = str((i+1)*10)
        if win[i] + win[9-i] == 0:
            c = '0.0'        
            d = 'N/A'
        else:
            c = round(float(win[i]) * 100 / (win[i] + win[9-i]),2)
            d = (c - (float(i) + 5) / 10) / ((float(i) + 5) / 10)
        print row_format.format(a, *[b,str(win[i]),c])

def print_dict(dict):
    for k, v in dict.iteritems():
        print('\nBest of ' + str(k))    
        row_format ='{:>3} <= p < {:>3} : {:>5}   {:>6}%'
        print(v)
        print_table(v)

        
dict = {}
try: 
    for match_id in range(3000, 5000):
        try:
            r = requests.get('https://csgolounge.com/match?m=' + str(match_id)).text
            m_format = r.split('Best of ')[1][0]
            html = re.split('<div class="team" style="[^"]*"></div>', r)
            fst_team = html[1].split('</span>')[0]
            snd_team = html[2].split('</span>')[0]
            fst_team_name = fst_team.split('</b>')[0].split('<b>')[1]
            snd_team_name = snd_team.split('</b>')[0].split('<b>')[1]
            fst_team_winp = fst_team.split('</i>')[0].split('<i>')[1]
            fst_team_winp = int(fst_team_winp[:len(fst_team_winp)-1])
            snd_team_winp = snd_team.split('</i>')[0].split('<i>')[1]
            snd_team_winp = int(snd_team_winp[:len(snd_team_winp)-1])
            if m_format not in dict.keys():
                dict[m_format] = [0] * 10
            if '(win)' in fst_team_name:
                dict[m_format][fst_team_winp / 10] += 1
            elif '(win)' in snd_team_name:
                dict[m_format][snd_team_winp / 10] += 1
            if match_id % 10 == 0: print_dict(dict)
        except:
            pass
finally:
    print_dict(dict)

            
