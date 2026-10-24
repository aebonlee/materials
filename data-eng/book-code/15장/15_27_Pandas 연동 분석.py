# 1단계(분위수 경계) — roundtrip.py 끝에 이어 붙입니다
q = top['spend'].quantile([0.33, 0.66]).tolist()
print('경계값 후보:', [round(x) for x in q])

top['grade2'] = pd.cut(top['spend'],
                       bins=[0, q[0], q[1], float('inf')],
                       labels=['B', 'A', 'S'])
print(top['grade2'].value_counts())
