import subprocess
from time import time
import csv

python_dir = r'?????\python.exe'

with open(r"problem_set.txt", 'r') as fp: res = eval(fp.read())
ai = r'test_one_problem.py'
timeout_sec = 60

score = []
for i in range(len(res)):
    print("testing problem", i)
    ok = True
    try:
        t = time()
        r = subprocess.run([python_dir, r'eval_env.py', str(i)], capture_output=True, timeout=timeout_sec)
        if r.returncode != 0: raise "code raised error"
        t = time()-t
        score.append({'problem': i, 'status': 'completed', 'run_time': round(t,4),
                      'score': 1 / int(str(r.stdout).split(r'\n')[-2].split(r'\r')[0])*1000})
    except subprocess.TimeoutExpired as e:
        score.append({'problem': i, 'status': 'timeout', 'run_time': float('nan'), 'score': 0})
    except:
        score.append({'problem': i, 'status': 'error', 'run_time': float('nan'), 'score': 0})
    print('result:', score[-1])

with open('people.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, score[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(score)
