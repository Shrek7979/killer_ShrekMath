import sys;sys.path.insert(0,__import__('os').path.dirname(__file__));from mk import I
MID=("중점으로 내적 모으기",[r"$\vec{\mathrm{PA}}\cdot\vec{\mathrm{PB}}=|\vec{\mathrm{PK}}|^2-|\vec{\mathrm{KA}}|^2$ (K: AB의 중점)."])
DIR=("초점에서 한 가지로 향하는 방향",[r"초점 F'에서 쌍곡선의 반대쪽 가지 위의 점으로 향하는 방향은 기울기 절댓값이 점근선 기울기보다 작은 방향."])

I('추가30·기하-26',"예상 오답 **80** — $|\\vec{\\mathrm{PN}}|^2$만 쓰고 반지름 제곱을 빼지 않은 경우",
 ["$\\vec{\\mathrm{XF}}\\cdot\\vec{\\mathrm{XH}}=0$ → FH를 지름으로 하는 원. 포물선의 정의 $\\overline{\\mathrm{PF}}=\\overline{\\mathrm{PH}}$ 때문에 P에서 FH의 중점 N으로 가는 직선이 FH에 **수직**입니다.",
  "그래서 두 번째 조건의 직선은 PN이고, $\\mathrm X_1$, $\\mathrm X_2$는 지름의 양 끝. 내적은 중점 공식 하나로 끝납니다."],
 {'C1':("포물선과 준선",r"$y^2=8x$: F$(2,0)$, 준선 $x=-2$."),
  'C2':("거리 조건",r"$\overline{\mathrm{PF}}=x_P+2=10$ → P$(8,8)$, H$(-2,8)$."),
  'C3':("두 조건",r"원(지름 FH) 위이면서 P를 지나 FH에 수직인 직선 위.")},
 [("포물선의 정의",[r"초점까지 거리 = 준선까지 거리. $\overline{\mathrm{PF}}=\overline{\mathrm{PH}}$이면 삼각형 PFH는 이등변."]),MID],
 [("P, H",['C1','C2']),("지름 원",['C3']),("직선 PN",['C3']),("답",['C3'])],
 [("$\\mathrm X_1$, $\\mathrm X_2$가 지름 양 끝",'C3',[r"직선 PN은 원의 중심 N을 지나므로 원과 만나는 두 점은 N에 대해 대칭. 그래서 $\vec{\mathrm{NX_2}}=-\vec{\mathrm{NX_1}}$."])],
 [("변형 · $|\\vec{\\mathrm{PF}}|=6$",[r"초점이 F인 포물선 $y^2=8x$ 위의 제1사분면의 점 P에서 준선에 내린 수선의 발을 H라 하자. $|\vec{\mathrm{PF}}|=6$이고 $\vec{\mathrm{XF}}\cdot\vec{\mathrm{XH}}=0$, $\vec{\mathrm{PX}}\cdot\vec{\mathrm{FH}}=0$을 모두 만족시키는 서로 다른 두 점 X를 $\mathrm X_1$, $\mathrm X_2$라 할 때, $\vec{\mathrm{PX_1}}\cdot\vec{\mathrm{PX_2}}$의 값을 구하시오."],12,r"P$(4,4\sqrt2)$, H$(-2,4\sqrt2)$, N$(0,2\sqrt2)$. $|\vec{\mathrm{PN}}|^2=24$, 반지름$^2=\frac{48}4=12$.")],
 "포물선의 정의로 이등변 → 중점과의 수직. 지름 양 끝 두 점의 내적은 중점 공식.")

I('추가30·기하-27',"예상 오답 **16** — 최솟값 대신 $13+3$을 쓴 경우",
 ["$|\\vec{\\mathrm{PX}}|=|\\vec{\\mathrm{PF}}|$와 쌍곡선의 정의로 $\\overline{\\mathrm{F'X}}=6$. 그리고 O, M이 각각 FF', FX의 중점이니 **중점연결정리**로 $\\vec{\\mathrm{OM}}=\\frac12\\vec{\\mathrm{F'X}}$.",
  "M은 원점 중심 반지름 3인 원 위(허용 방향만). A 방향이 허용 범위 안이면 최솟값은 $13-3$."],
 {'C1':("쌍곡선과 점 X",r"$\overline{\mathrm{PF'}}-\overline{\mathrm{PF}}=6$, X는 PF' 위에서 $\overline{\mathrm{PX}}=\overline{\mathrm{PF}}$ → $\overline{\mathrm{F'X}}=6$."),
  'C2':("중점 M과 묻는 것",r"$\vec{\mathrm{OM}}=\frac12\vec{\mathrm{F'X}}$, $|\vec{\mathrm{OM}}|=3$. A$(12,5)$까지 최소 거리.")},
 [("중점연결정리",[r"삼각형 FF'X에서 두 변의 중점을 이은 선분은 나머지 변의 절반이고 평행."]),DIR],
 [("$\\overline{\\mathrm{F'X}}=6$",['C1']),("$\\vec{\\mathrm{OM}}$",['C2']),("방향 확인",['C1']),("답",['C2'])],
 [("방향 제한",'C1',[r"M의 방향은 $\vec{\mathrm{F'P}}$ 방향. 오른쪽 가지라 기울기 $|k|<\frac43$. A의 기울기 $\frac5{12}$가 범위 안."])],
 [("변형 · A$(8,6)$",[r"두 초점이 F$(5,0)$, F'$(-5,0)$인 쌍곡선 $\frac{x^2}9-\frac{y^2}{16}=1$ 위의 $x$좌표가 양수인 점 P에 대하여 선분 PF' 위의 점 X가 $|\vec{\mathrm{PX}}|=|\vec{\mathrm{PF}}|$를 만족시킨다. 선분 FX의 중점을 M이라 할 때, 점 A$(8,6)$에 대하여 $|\vec{\mathrm{AM}}|$의 최솟값을 구하시오."],7,r"기울기 $\frac34<\frac43$ → 허용. $10-3$.")],
 "정의로 길이를 고정하고 중점연결정리로 원을 얻는다. 방향 제한 확인.")

I('추가30·기하-28',"예상 오답 **20** — $\\theta$의 범위를 $(0,\\frac\\pi2)$로 두고 다른 각에서 최대를 잡은 경우",
 ["$\\vec{\\mathrm{PX}}$의 계수가 $\\frac{\\overline{\\mathrm{PF}}}{\\overline{\\mathrm{PF'}}}$이라 $\\overline{\\mathrm{F'X}}=\\overline{\\mathrm{PF'}}+\\overline{\\mathrm{PF}}=10$ (타원의 정의). 중점연결정리로 $|\\vec{\\mathrm{OM}}|=5$.",
  "P의 범위(제1사분면, $x\\ge0$)가 방향각을 $(0,\\theta_0]$으로 자릅니다. 그 안에서 내적이 증가하므로 끝 $\\theta_0$에서 최대."],
 {'C1':("타원과 P의 범위",r"$\frac{x^2}{25}+\frac{y^2}9=1$, 초점 $(\pm4,0)$. P는 $x\ge0$, $y>0$."),
  'C2':("벡터 조건",r"$\vec{\mathrm{F'X}}=\left(1+\frac{\overline{\mathrm{PF}}}{\overline{\mathrm{PF'}}}\right)\vec{\mathrm{F'P}}$ → 길이 $10$."),
  'C4':("묻는 것",r"$\vec{\mathrm{OM}}\cdot\vec{\mathrm{OB}}$의 최댓값.")},
 [("타원의 정의",[r"$\overline{\mathrm{PF}}+\overline{\mathrm{PF'}}=2a$."]),("중점연결정리",[r"$\vec{\mathrm{OM}}=\frac12\vec{\mathrm{F'X}}$."])],
 [("$\\overline{\\mathrm{F'X}}=10$",['C2']),("$\\vec{\\mathrm{OM}}$",['C2']),("각의 범위",['C1']),("최댓값",['C4'])],
 [("각의 끝 $\\theta_0$",'C1',[r"P$(0,3)$일 때 $\vec{\mathrm{F'P}}=(4,3)$. 이 이상 기울면 P의 $x$좌표가 음수."]),
  ("증가 확인",'C4',[r"$-\cos\theta+7\sin\theta$는 $0<\theta<\frac\pi2$에서 증가. 그래서 끝점에서 최대."])],
 [("변형 · B$(1,7)$",[r"두 초점이 F$(4,0)$, F'$(-4,0)$인 타원 $\frac{x^2}{25}+\frac{y^2}9=1$ 위의 $x$좌표가 $0$ 이상이고 $y$좌표가 양수인 점 P에 대하여 점 X가 $\vec{\mathrm{PX}}=\frac{|\vec{\mathrm{PF}}|}{|\vec{\mathrm{PF'}}|}\vec{\mathrm{F'P}}$를 만족시킨다. 선분 FX의 중점을 M이라 할 때, 점 B$(1,7)$에 대하여 $\vec{\mathrm{OM}}\cdot\vec{\mathrm{OB}}$의 최댓값을 구하시오."],25,r"$5(\cos\theta+7\sin\theta)$, $\tan\theta_0=\frac34<7$이라 범위에서 증가 → $\theta_0$: $5\left(\frac45+\frac{21}5\right)=25$.")],
 "정의 + 중점연결정리로 길이 고정. 방향각의 범위 끝을 확인.")

I('추가30·기하-29',"예상 오답 **36** — X를 무게중심으로 잡은 경우",
 ["$\\vec{\\mathrm{XA}}\\cdot\\vec{\\mathrm{XB}}=\\vec{\\mathrm{XB}}\\cdot\\vec{\\mathrm{XC}}$ ⇔ $\\vec{\\mathrm{XB}}\\cdot\\vec{\\mathrm{CA}}=0$. 세 내적이 같다 = X에서 꼭짓점으로 가는 벡터가 대변에 수직 → **수심**.",
  "그 다음은 중점 공식 하나: $\\vec{\\mathrm{PX}}\\cdot\\vec{\\mathrm{PA}}=|\\vec{\\mathrm{PK}}|^2-(\\frac{\\overline{\\mathrm{XA}}}2)^2$."],
 {'C1':("세 점",r"A$(0,6)$, B$(-2,0)$, C$(4,0)$."),
  'C2':("세 내적이 같다",r"차를 만들면 $\vec{\mathrm{XB}}\cdot\vec{\mathrm{CA}}=0$, $\vec{\mathrm{XC}}\cdot\vec{\mathrm{AB}}=0$ → 수심."),
  'C4':("묻는 것",r"선분 BC 위의 P에 대해 $\vec{\mathrm{PX}}\cdot\vec{\mathrm{PA}}$의 최대·최소.")},
 [("내적이 같다 → 수직",[r"$\vec u\cdot\vec v=\vec u\cdot\vec w$ ⇔ $\vec u\cdot(\vec v-\vec w)=0$."]),MID],
 [("수심",['C2']),("X의 좌표",['C1']),("중점 공식",['C4']),("$t^2+8$",['C4']),("답",['C4'])],
 [("수심의 좌표",'C1',[r"A에서의 수선은 $x=0$(BC가 $x$축). B에서 CA에 수직인 직선과의 교점 $\left(0,\frac43\right)$."]),
  ("최댓값은 먼 끝점",'C4',[r"$t^2$은 $|t|$가 큰 쪽. $t=4$ (C)에서 최대."])],
 [("변형 · B$(-3,0)$, C$(2,0)$",[r"좌표평면 위의 세 점 A$(0,6)$, B$(-3,0)$, C$(2,0)$에 대하여 점 X가 $\vec{\mathrm{XA}}\cdot\vec{\mathrm{XB}}=\vec{\mathrm{XB}}\cdot\vec{\mathrm{XC}}=\vec{\mathrm{XC}}\cdot\vec{\mathrm{XA}}$를 만족시킨다. 선분 BC 위를 움직이는 점 P에 대하여 $\vec{\mathrm{PX}}\cdot\vec{\mathrm{PA}}$의 최댓값을 $M$, 최솟값을 $m$이라 할 때, $M+m$의 값을 구하시오."],21,r"수심 X$(0,1)$, 값 $=t^2+6$, $t\in[-3,2]$ → $m=6$, $M=15$.")],
 "세 내적이 같으면 수심. 두 점에 대한 내적은 중점 공식.")

I('추가30·기하-30',"예상 오답 **122** — (ii)의 경우를 범위에 넣지 않거나 최솟값을 $p=4$에서 잡은 경우",
 ["(가)는 PQ가 $x$축 또는 $y$축과 평행. (나)·(다)는 P, Q가 놓일 변을 정합니다: P는 변 AB의 $x\\ge1$ 부분, Q는 $x\\ge-1$, $y\\le0$인 둘레.",
  "평행 방향으로 경우를 나누면 각 경우가 한 변수 식이 되어 범위를 바로 구합니다."],
 {'C2':("(가) 평행",r"$\vec{\mathrm{PQ}}\cdot\vec{\mathrm{OA}}=0$ ($y$축 평행) 또는 $\vec{\mathrm{PQ}}\cdot\vec{\mathrm{OB}}=0$ ($x$축 평행)."),
  'C3':("(나) P의 위치",r"$x_P\ge1$, $y_P\ge0$ → 변 AB: P$(p,4-p)$, $1\le p\le4$."),
  'C4':("(다) Q의 위치",r"$x_Q\ge-1$, $y_Q\le0$."),
  'C5':("묻는 것",r"R$(-1,6)$에 대해 $\vec{\mathrm{RP}}\cdot\vec{\mathrm{RQ}}$의 최대·최소.")},
 [("내적이 0 = 수직",[r"$\vec{\mathrm{PQ}}\perp\vec{\mathrm{OA}}$(=$x$축 방향)이면 PQ는 $y$축 평행."]),
  ("좌표로 내적",[r"$\vec{\mathrm{RP}}\cdot\vec{\mathrm{RQ}}=(x_P-x_R)(x_Q-x_R)+(y_P-y_R)(y_Q-y_R)$."])],
 [("(가) 정리",['C2']),("P의 위치",['C3']),("Q의 위치",['C4']),("(i) $y$축 평행",['C2','C4']),("(i) 식",['C5']),("(i) 범위",['C5']),("(ii) $x$축 평행",['C2']),("답",['C5'])],
 [("$x$축 평행은 한 점뿐",'C2',[r"P는 $y\ge0$, Q는 $y\le0$이라 같은 높이는 $y=0$뿐 → 둘 다 A."])],
 [("변형 · R$(0,6)$",[r"정사각형 ABCD (A$(4,0)$, B$(0,4)$, C$(-4,0)$, D$(0,-4)$)의 네 변 위의 두 점 P, Q가 (가) $(\vec{\mathrm{PQ}}\cdot\vec{\mathrm{OA}})(\vec{\mathrm{PQ}}\cdot\vec{\mathrm{OB}})=0$, (나) $\vec{\mathrm{OA}}\cdot\vec{\mathrm{OP}}\ge4$, $\vec{\mathrm{OB}}\cdot\vec{\mathrm{OP}}\ge0$, (다) $\vec{\mathrm{OA}}\cdot\vec{\mathrm{OQ}}\ge-4$, $\vec{\mathrm{OB}}\cdot\vec{\mathrm{OQ}}\le0$을 만족시킨다. 점 R$(0,6)$에 대하여 $\vec{\mathrm{RP}}\cdot\vec{\mathrm{RQ}}$의 최댓값을 $M$, 최솟값을 $m$이라 할 때, $M+m$의 값을 구하시오."],80,r"(i) $p^2-(p+2)(p-10)=8p+20\in[28,52]$, (ii) $|\vec{\mathrm{RA}}|^2=52$.")],
 "평행 조건으로 경우를 나누고, 위치 조건으로 변을 고른다.")
