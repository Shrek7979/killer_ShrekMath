import json,sys
R='/home/claude/ks/site/data/'
a,b=int(sys.argv[1]),int(sys.argv[2])
for n in range(a,b+1):
    d=json.load(open(f'{R}{n}.json',encoding='utf-8'))
    print(f"=== #{n} {d['id']} | {d['subject']} {d['type']} ★{d['stars']} | 답 {d['answer']} | {d['topic']}")
    for c in d['conds']: print(f"  {c['id']}: {c['text']}")
    for s in d['steps']: print(f"  [{s['n']}] {s['text']}")
