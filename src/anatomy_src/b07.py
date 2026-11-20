import sys;sys.path.insert(0,'/tmp/claude-0/-home-claude/6c68019e-cd2e-53f9-8137-25a894479233/scratchpad/an');from mk import I
CIR=("원 위의 점과 정점의 거리",[r"중심까지 거리 $d$, 반지름 $r$이면 원 위의 점까지 거리는 $|d-r|$부터 $d+r$까지."])
DOT1=("한 방향과의 내적은 일차식",[r"$\vec{\mathrm{AQ}}\cdot\vec v$는 Q의 좌표에 대한 일차식. 원 위에서의 최대·최소는 (중심에서의 값) $\pm r|\vec v|$."])

I('추가30·기하-11',"예상 오답 — (가)를 수직 조건으로만 읽고 P, R의 위치를 정하지 못하는 경우 · 무게중심 대신 외심을 중심으로 잡은 경우",
 ["(가)의 $(\\vec{\\mathrm{PB}}+\\vec{\\mathrm{PQ}})\\cdot\\vec{\\mathrm{BC}}=0$은 ‘P에서 BQ의 중점으로 가는 벡터가 BC에 수직’, 즉 **$\\overline{\\mathrm{PB}}=\\overline{\\mathrm{PQ}}$인 이등변삼각형**입니다.",
  "(나)로 Q가 정해지고, 마지막 조건은 삼각형 PQR의 **무게중심 G**를 중심으로 하는 원. A에서 그 원까지의 거리 범위를 구하면 끝입니다."],
 {'C1':("삼각형",r"$\overline{\mathrm{AB}}=\overline{\mathrm{AC}}=10$, $\overline{\mathrm{BC}}=12$. B$(0,0)$, C$(12,0)$, A$(6,8)$."),
  'C3':("(가) 이등변 조건",r"$\vec{\mathrm{PB}}+\vec{\mathrm{PQ}}=2\vec{\mathrm{PK}}$(K: BQ의 중점) $\perp$ BC → $\overline{\mathrm{PB}}=\overline{\mathrm{PQ}}$. R도 같은 방식."),
  'C4':("(나) 길이 비",r"$\overline{\mathrm{PQ}}=\frac56q$, $\overline{\mathrm{QR}}=\frac56(12-q)$ → $q=8$."),
  'C5':("묻는 것",r"$3|\vec{\mathrm{XG}}|=4$: G 중심 반지름 $\frac43$인 원. $M=\overline{\mathrm{AG}}+\frac43$, $m=\overline{\mathrm{AG}}-\frac43$.")},
 [("중점 벡터와 수직",[r"$\vec{\mathrm{PB}}+\vec{\mathrm{PQ}}=2\vec{\mathrm{PK}}$. 이것이 BQ에 수직이면 P는 BQ의 수직이등분선 위."]),
  ("세 벡터의 합 → 무게중심",[r"$\vec{\mathrm{XP}}+\vec{\mathrm{XQ}}+\vec{\mathrm{XR}}=3\vec{\mathrm{XG}}$."]),CIR],
 [("(가) → 이등변",['C3']),("좌표 설정",['C1']),("P, Q, R을 $q$로",['C3']),("(나)로 $q=8$",['C4']),("무게중심 원",['C5']),("$\\overline{\\mathrm{AG}}$",['C5']),("답",['C5'])],
 [("(가)를 수선의 발로 읽기",'C3',[r"‘$\vec{\mathrm{PB}}+\vec{\mathrm{PQ}}$가 BC에 수직’을 바로 해석하지 못하면 P, R을 정할 수 없습니다. 중점 벡터로 바꾸는 것이 열쇠."]),
  ("$M^2+m^2=2(d^2+r^2)$",'C5',[r"$(d+r)^2+(d-r)^2=2(d^2+r^2)$. $d$를 루트로 구하지 않아도 됩니다."])],
 [("변형 · $|\\vec{\\mathrm{PQ}}|=|\\vec{\\mathrm{QR}}|$",[r"$\overline{\mathrm{AB}}=\overline{\mathrm{AC}}=10$, $\overline{\mathrm{BC}}=12$인 삼각형 ABC에서 선분 AB 위의 점 P, 선분 BC 위의 점 Q, 선분 CA 위의 점 R가 $(\vec{\mathrm{PB}}+\vec{\mathrm{PQ}})\cdot\vec{\mathrm{BC}}=0$, $(\vec{\mathrm{RC}}+\vec{\mathrm{RQ}})\cdot\vec{\mathrm{BC}}=0$, $|\vec{\mathrm{PQ}}|=|\vec{\mathrm{QR}}|$를 만족시킨다. $|\vec{\mathrm{XP}}+\vec{\mathrm{XQ}}+\vec{\mathrm{XR}}|=4$인 점 X에 대하여 $|\vec{\mathrm{AX}}|$의 최댓값을 $M$, 최솟값을 $m$이라 할 때, $9(M^2+m^2)$의 값을 구하시오."],544,r"$q=6$: P$(3,4)$, Q$(6,0)$, R$(9,4)$, G$\left(6,\tfrac83\right)$, $\overline{\mathrm{AG}}=\tfrac{16}3$. $2\left(\tfrac{256}9+\tfrac{16}9\right)=\tfrac{544}9$.")],
 "$(\\vec{\\mathrm{PB}}+\\vec{\\mathrm{PQ}})\\perp\\overline{\\mathrm{BQ}}$이면 이등변. 세 벡터의 합은 무게중심.")

I('추가30·기하-12',"예상 오답 **80** — (나)를 무시하고 원 위의 최댓값 $(중심값)+40$으로 계산한 경우",
 ["(가) $\\vec{\\mathrm{PQ}}\\cdot(\\vec{\\mathrm{PQ}}-\\vec{\\mathrm{BC}})=0$ → Q는 P와 $\\mathrm{P}+\\vec{\\mathrm{BC}}$를 지름 양 끝으로 하는 원 위. P가 대각선 BD를 따라 움직이면 원이 미끄러집니다.",
  "(나) ‘직사각형 안’ 제한 때문에 최댓값은 원의 접점이 아니라 **꼭짓점 C**에서 납니다. 최솟값은 제한에 걸리지 않는지 확인합니다."],
 {'C2':("움직이는 점 P",r"P$(8s,6s)$, $0\le s\le1$."),
  'C3':("(가) 지름 원",r"중심 $\mathrm P+(4,0)$, 반지름 $4$."),
  'C4':("(나) 범위 제한",r"Q는 직사각형 안 또는 위. 최댓값·최솟값 후보가 이 제한을 만족하는지 확인."),
  'C5':("묻는 것",r"$\vec{\mathrm{AQ}}\cdot\vec{\mathrm{AC}}=8x-6y+36$.")},
 [("$\\vec v\\cdot(\\vec v-\\vec w)=0$ → 지름 원",[r"$\vec{\mathrm{PQ}}\perp\vec{\mathrm{P'Q}}$ ($\vec{\mathrm{PP'}}=\vec w$) → PP'을 지름으로 하는 원."]),DOT1],
 [("지름 원",['C3']),("내적을 일차식으로",['C5']),("최댓값은 꼭짓점 C",['C4']),("최솟값",['C2','C4']),("답",['C5'])],
 [("범위 제한 (나)",'C4',[r"원만 보면 최댓값이 더 커 보이지만 그 점은 직사각형 밖입니다. 직사각형 안에서 $8x-6y$의 최댓값은 C에서 $64$, 그 C가 실제 어떤 원 위에 오는지($s=\frac{16}{25}$) 확인해야 합니다."]),
  ("최솟값의 점이 안쪽인지",'C4',[r"$s=0$일 때의 최소점 $\left(\frac45,\frac{12}5\right)$이 직사각형 안이라 제한에 걸리지 않습니다."])],
 [("변형 · $\\vec{\\mathrm{AD}}$와의 내적",[r"좌표평면에서 $\overline{\mathrm{AB}}=6$, $\overline{\mathrm{BC}}=8$인 직사각형 ABCD의 선분 BD 위를 움직이는 점 P에 대하여 점 Q가 $\vec{\mathrm{PQ}}\cdot(\vec{\mathrm{PQ}}-\vec{\mathrm{BC}})=0$을 만족시키고 직사각형 ABCD의 내부 또는 둘레 위에 있다. $\vec{\mathrm{AQ}}\cdot\vec{\mathrm{AD}}$의 최댓값과 최솟값의 차를 구하시오."],64,r"$\vec{\mathrm{AD}}=(8,0)$, 값 $=8x$. Q의 $x$좌표는 $0$(P$=$B일 때 B)부터 $8$(C 등)까지.")],
 "원 위의 최대·최소도 ‘범위 제한’이 있으면 경계(꼭짓점)에서 날 수 있다.")

I('추가30·기하-13',"예상 오답 **216** — Q를 P 그대로 두고 $x$ 범위를 계산한 경우",
 ["$|\\vec{\\mathrm{XB}}+\\vec{\\mathrm{XC}}|=|\\vec{\\mathrm{XB}}-\\vec{\\mathrm{XC}}|$ → BC를 지름으로 하는 원. $3\\vec{\\mathrm{PQ}}=\\vec{\\mathrm{PA}}+\\vec{\\mathrm{PC}}$를 위치벡터로 정리하면 $\\mathrm Q=\\frac{\\mathrm P+\\mathrm A+\\mathrm C}3$, 즉 삼각형 PAC의 무게중심.",
  "구하는 내적은 Q의 $x$좌표의 일차식 → P의 $x$좌표 범위로 귀결됩니다."],
 {'C2':("수직 조건",r"$\vec{\mathrm{XB}}\cdot\vec{\mathrm{XC}}=0$ → 지름 BC 원."),
  'C5':("Q의 정의",r"$3(\mathrm Q-\mathrm P)=(\mathrm A-\mathrm P)+(\mathrm C-\mathrm P)$ → $\mathrm Q=\frac13(\mathrm P+\mathrm A+\mathrm C)$."),
  'C6':("묻는 것",r"$\vec{\mathrm{DQ}}\cdot\vec{\mathrm{DA}}=24-2x$ (P의 $x$좌표).")},
 [("벡터식 → 위치벡터",[r"$\vec{\mathrm{PQ}}=\mathrm Q-\mathrm P$로 모두 바꾸면 Q가 P의 일차식으로 나옵니다."]),DOT1],
 [("$S$는 원",['C2']),("Q의 위치",['C5']),("좌표",['C5']),("내적을 $x$로",['C6']),("범위와 곱",['C6'])],
 [("Q는 축소·이동된 점",'C5',[r"Q의 자취는 원 $S$를 $\frac13$로 축소·이동한 원. 그래도 내적은 P의 $x$좌표 하나로 정해집니다."])],
 [("변형 · 네 점의 무게중심",[r"한 변의 길이가 $6$인 정사각형 ABCD에서 $|\vec{\mathrm{XB}}+\vec{\mathrm{XC}}|=|\vec{\mathrm{XB}}-\vec{\mathrm{XC}}|$를 만족시키는 점 X가 나타내는 도형 위의 점 P에 대하여 $4\vec{\mathrm{PQ}}=\vec{\mathrm{PA}}+\vec{\mathrm{PC}}+\vec{\mathrm{PD}}$를 만족시키는 점을 Q라 할 때, $\vec{\mathrm{DQ}}\cdot\vec{\mathrm{DA}}$의 최댓값과 최솟값의 곱을 구하시오."],972,r"Q$=\frac14(\mathrm P+\mathrm A+\mathrm C+\mathrm D)$, $x_Q=\frac{x+12}4$, 내적 $=36-\frac32x\in[27,36]$.")],
 "벡터식은 위치벡터로 바꿔 Q를 P로 나타낸다. 한 방향과의 내적은 한 좌표의 범위.")

I('추가30·기하-14',"예상 오답 **78** — 최솟값을 꼭짓점끼리의 거리로 계산한 경우",
 ["$\\vec{\\mathrm{PQ}}+\\vec{\\mathrm{OF}}=\\vec{\\mathrm{PW}}$ ($\\mathrm W=\\mathrm Q+\\vec{\\mathrm{OF}}$)로 보면 ‘삼각형 CDE를 평행이동한 삼각형’과 ‘삼각형 AOB’ 사이의 거리 문제입니다.",
  "최댓값은 꼭짓점끼리, 최솟값은 꼭짓점과 **변** 사이(수선)에서 나옵니다."],
 {'C2':("여섯 점",r"삼각형 AOB와 삼각형 CDE, 평행이동 벡터 $\vec{\mathrm{OF}}=(4,1)$."),
  'C4':("묻는 것",r"$|\vec{\mathrm{PW}}|^2$의 최댓값과 최솟값의 합.")},
 [("평행이동으로 벡터 합 정리",[r"$\vec{\mathrm{OQ}}+\vec{\mathrm{OF}}$는 Q를 $(4,1)$만큼 옮긴 점. 도형 전체를 옮겨 생각합니다."]),
  ("두 도형 사이 거리",[r"최대: 꼭짓점 쌍 비교. 최소: 한 도형의 꼭짓점에서 다른 도형의 변까지 수선(발이 변 위에 있을 때)."])],
 [("평행이동",['C2','C4']),("최댓값",['C4']),("최솟값",['C4']),("답",['C4'])],
 [("최솟값은 꼭짓점-꼭짓점이 아님",'C4',[r"$(5,3)$과 가장 가까운 꼭짓점 A$(6,0)$의 거리는 $\sqrt{10}$. 빗변까지의 수선 $\sqrt2$가 더 짧습니다."])],
 [("변형 · $\\mathrm F(5,1)$",[r"좌표평면 위에 여섯 점 A$(6,0)$, B$(0,6)$, C$(1,2)$, D$(1,4)$, E$(3,4)$, F$(5,1)$이 있다. 삼각형 AOB의 변 위를 움직이는 점 P와 삼각형 CDE의 변 위를 움직이는 점 Q에 대하여 $|\vec{\mathrm{PQ}}+\vec{\mathrm{OF}}|^2$의 최댓값을 $M$, 최솟값을 $m$이라 할 때, $2(M+m)$의 값을 구하시오."],187,r"옮긴 삼각형 $(6,3)$, $(6,5)$, $(8,5)$. $M=8^2+5^2=89$, $m=\left(\tfrac{3}{\sqrt2}\right)^2=\tfrac92$.")],
 "벡터 합은 평행이동으로. 두 도형 사이 최소 거리는 꼭짓점과 변 사이의 수선.")

I('추가30·기하-15',"예상 오답 **17** — 최솟값을 묻는데 $13+4$를 쓴 경우 · 방향 제한을 확인하지 않은 경우",
 ["$|\\vec{\\mathrm{PF}}|+8$은 쌍곡선의 정의로 $|\\vec{\\mathrm{PF'}}|$. 그래서 Q는 F'에서 P 방향으로 길이 $4$인 점, 자취는 반지름 $4$인 원의 **일부**(오른쪽 가지 방향만).",
  "A 방향이 그 허용 범위(기울기 $|k|<\\frac34$) 안인지 확인해야 $13-4$를 쓸 수 있습니다."],
 {'C1':("쌍곡선",r"$a=4$, $c=5$. 오른쪽 가지 위의 점 P: $\overline{\mathrm{PF'}}-\overline{\mathrm{PF}}=8$."),
  'C2':("벡터 조건",r"$\vec{\mathrm{F'Q}}=4\cdot\dfrac{\vec{\mathrm{F'P}}}{|\vec{\mathrm{F'P}}|}$."),
  'C4':("묻는 것",r"A$(7,5)$에서 Q까지 거리의 최솟값.")},
 [("쌍곡선의 정의",[r"$|\overline{\mathrm{PF'}}-\overline{\mathrm{PF}}|=2a$."]),
  ("초점을 지나는 직선과 한 가지",[r"F'을 지나는 직선이 오른쪽 가지와 만나려면 기울기의 절댓값이 점근선 기울기 $\frac34$보다 작아야 합니다."])],
 [("정의로 바꾸기",['C1','C2']),("단위벡터의 4배",['C2']),("자취",['C2']),("방향 제한",['C1']),("A의 방향 확인",['C4']),("답",['C4'])],
 [("허용 방향",'C1',[r"Q의 자취는 원 전체가 아니라 기울기 $|k|<\frac34$인 방향의 호. $\vec{\mathrm{F'A}}$의 기울기 $\frac5{12}$가 범위 안이라 등호가 성립합니다."])],
 [("변형 · 계수 3",[r"쌍곡선 $\frac{x^2}{16}-\frac{y^2}9=1$의 두 초점 F$(5,0)$, F'$(-5,0)$과 $x$좌표가 양수인 쌍곡선 위의 점 P에 대하여 점 Q가 $(|\vec{\mathrm{PF}}|+8)\vec{\mathrm{F'Q}}=3\vec{\mathrm{F'P}}$를 만족시킨다. 점 A$(7,5)$에 대하여 $|\vec{\mathrm{AQ}}|$의 최솟값을 구하시오."],10,r"$|\vec{\mathrm{F'Q}}|=3$, $|\vec{\mathrm{AF'}}|=13$, 방향 허용 → $13-3$.")],
 "$\\overline{\\mathrm{PF}}+2a$는 다른 초점까지의 거리. 자취가 호이면 방향이 허용 범위인지 확인.")
