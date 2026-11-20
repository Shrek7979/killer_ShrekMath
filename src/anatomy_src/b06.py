import sys;sys.path.insert(0,'/tmp/claude-0/-home-claude/6c68019e-cd2e-53f9-8137-25a894479233/scratchpad/an');from mk import I
CIR=("원 위의 점과 정점의 거리",[r"중심이 $\mathrm{P'}$, 반지름 $r$인 원 위의 점과 정점 B의 거리는 $|\overline{\mathrm{BP'}}-r|$에서 $\overline{\mathrm{BP'}}+r$까지."])

I('추가30·기하-06',"예상 오답 **35** — 가장 가까운 점을 $\\mathrm{C'}$로 잡아 $m$을 잘못 구한 경우",
 ["$\\vec{\\mathrm{AX}}=\\frac13\\vec{\\mathrm{AP}}+\\vec{\\mathrm{AQ}}$는 두 단계로 읽습니다. ① P를 A 중심으로 $\\frac13$ 축소한 점 $\\mathrm{P'}$ ② 거기서 길이 $1$인 벡터만큼 이동.",
  "그래서 X의 영역은 ‘작은 정삼각형의 둘레 + 반지름 1’. 고정점 B까지의 거리는 $\\overline{\\mathrm{BP'}}\\pm1$."],
 {'C1':("움직이는 두 점",r"P는 한 변 $6$인 정삼각형의 둘레, Q는 A 중심 반지름 $1$인 원 위."),
  'C2':("벡터 합",r"$\frac13\vec{\mathrm{AP}}$ = A를 중심으로 $\frac13$배 축소(닮음). 축소된 정삼각형 $\mathrm{AB'C'}$의 한 변은 $2$."),
  'C4':("묻는 것",r"$|\vec{\mathrm{BX}}|$의 최대·최소의 곱.")},
 [("벡터의 실수배 = 닮음 축소",[r"$\vec{\mathrm{AP'}}=k\vec{\mathrm{AP}}$이면 P의 자취를 A 중심으로 $k$배 한 도형이 $\mathrm{P'}$의 자취."]),CIR],
 [("축소된 삼각형과 단위원",['C1','C2']),("$\\overline{\\mathrm{BP'}}\\pm1$",['C2']),("B에서 가장 먼 점·가까운 점",['C4']),("답",['C4'])],
 [("가장 가까운 점",'C4',[r"축소된 삼각형 위에서 B와 가장 가까운 점은 $\mathrm{B'}$(거리 $4$). $\mathrm{C'}$까지는 $\sqrt{28}$로 더 멉니다."]),
  ("등호가 실제로 성립하는가",'C2',[r"Q의 방향을 자유롭게 고를 수 있으므로 $\overline{\mathrm{BP'}}+1$, $\overline{\mathrm{BP'}}-1$을 모두 만들 수 있습니다."])],
 [("변형 · $|\\vec{\\mathrm{AQ}}|=2$",[r"한 변의 길이가 $6$인 정삼각형 ABC의 세 변 위를 움직이는 점 P와 $|\vec{\mathrm{AQ}}|=2$를 만족시키는 점 Q에 대하여 점 X가 $\vec{\mathrm{AX}}=\frac13\vec{\mathrm{AP}}+\vec{\mathrm{AQ}}$를 만족시킨다. $|\vec{\mathrm{BX}}|$의 최댓값을 $M$, 최솟값을 $m$이라 할 때, $M\times m$의 값을 구하시오."],16,r"$M=6+2$, $m=4-2$.")],
 "$k\\vec{\\mathrm{AP}}$는 축소, $+\\vec{\\mathrm{AQ}}$ ($|\\vec{\\mathrm{AQ}}|=r$)는 반지름 $r$로 두르기.")

I('추가30·기하-07',"예상 오답 **120** — P, Q를 대각선 방향이 아닌 변 방향으로 잡은 경우",
 ["$\\vec{\\mathrm{AP}}+\\vec{\\mathrm{AQ}}$를 쪼개면 $\\vec{\\mathrm{AB}}+\\vec{\\mathrm{AD}}=\\vec{\\mathrm{AC}}$와 두 단위벡터의 합. 크기가 최대가 되려면 **세 벡터가 모두 같은 방향**이어야 합니다.",
  "그 방향은 대각선 AC. 그래서 P, Q의 위치가 하나로 정해지고 넓이를 계산할 수 있습니다."],
 {'C2':("단위원",r"$|\vec{\mathrm{BP}}|=|\vec{\mathrm{DQ}}|=1$: P는 B 중심, Q는 D 중심의 반지름 1인 원 위."),
  'C4':("최대 조건과 넓이",r"$|\vec{\mathrm{AX}}|$가 최대일 때의 삼각형 APQ의 넓이 $S$.")},
 [("삼각부등식",[r"$|\vec a+\vec b+\vec c|\le|\vec a|+|\vec b|+|\vec c|$, 등호는 모두 같은 방향."]),
  ("좌표로 삼각형 넓이",[r"$\frac12|x_1y_2-x_2y_1|$ (한 꼭짓점이 원점일 때)."])],
 [("$\\vec{\\mathrm{AC}}$로 묶기",['C2']),("최댓값 12",['C2']),("등호 조건",['C4']),("P, Q 좌표",['C4']),("넓이",['C4']),("답",['C4'])],
 [("등호 조건을 확인하지 않기",'C4',[r"최댓값 $12$만 구하고 멈추면 넓이를 못 구합니다. $\vec{\mathrm{BP}}=\vec{\mathrm{DQ}}=\frac1{10}\vec{\mathrm{AC}}$가 핵심."])],
 [("변형 · 반지름 2",[r"좌표평면에서 $\overline{\mathrm{AB}}=6$, $\overline{\mathrm{AD}}=8$인 직사각형 ABCD와 $|\vec{\mathrm{BP}}|=2$, $|\vec{\mathrm{DQ}}|=2$인 두 점 P, Q에 대하여 $\vec{\mathrm{AX}}=\vec{\mathrm{AP}}+\vec{\mathrm{AQ}}$일 때, $|\vec{\mathrm{AX}}|$가 최대가 되도록 하는 P, Q에 대하여 삼각형 APQ의 넓이를 $S$라 하자. $5S$의 값을 구하시오."],168,r"$\vec{\mathrm{BP}}=\vec{\mathrm{DQ}}=\left(\tfrac65,\tfrac85\right)$, P$\left(\tfrac{36}5,\tfrac85\right)$, Q$\left(\tfrac65,\tfrac{48}5\right)$, $S=\tfrac{168}5$.")],
 "벡터 합의 크기 최대 = 모두 같은 방향. 그 방향이 위치를 정해 준다.")

I('추가30·기하-08',"예상 오답 **216** — 최솟값을 끝점에서, 최댓값을 수선의 발에서 잡은 경우",
 ["$\\vec{\\mathrm{XA}}+\\vec{\\mathrm{XB}}+\\vec{\\mathrm{XC}}=3\\vec{\\mathrm{XG}}$ (G는 무게중심). 세 벡터의 합이 **무게중심까지의 거리 하나**로 바뀝니다.",
  "선분 위의 점에서 G까지의 거리: 최소는 수선의 발(선분 위에 있으면), 최대는 끝점."],
 {'C1':("직각이등변삼각형",r"A$(0,0)$, B$(6,0)$, C$(0,6)$, 무게중심 G$(2,2)$."),
  'C2':("선분 BC 위의 점 X",r"$|\vec{\mathrm{XA}}+\vec{\mathrm{XB}}+\vec{\mathrm{XC}}|=3|\vec{\mathrm{XG}}|$의 최대·최소.")},
 [("무게중심과 벡터의 합",[r"$\vec{\mathrm{XA}}+\vec{\mathrm{XB}}+\vec{\mathrm{XC}}=3\vec{\mathrm{XG}}$. 두 점이면 중점, 세 점이면 무게중심."]),
  ("선분까지의 거리",[r"수선의 발이 선분 위에 있으면 그것이 최소, 최대는 두 끝점 중 먼 쪽."])],
 [("무게중심으로 묶기",['C1','C2']),("최솟값",['C2']),("최댓값",['C2']),("답",['C2'])],
 [("수선의 발이 선분 안에 있는지",'C2',[r"$(3,3)$은 BC의 중점이라 선분 위. 밖에 있으면 최솟값도 끝점에서 납니다."])],
 [("변형 · 한 변 12",[r"좌표평면에서 $\overline{\mathrm{AB}}=\overline{\mathrm{AC}}=12$, $\angle\mathrm{BAC}=\frac\pi2$인 직각삼각형 ABC의 선분 BC 위를 움직이는 점 X에 대하여 $|\vec{\mathrm{XA}}+\vec{\mathrm{XB}}+\vec{\mathrm{XC}}|$의 최댓값을 $M$, 최솟값을 $m$이라 할 때, $M^2+m^2$의 값을 구하시오."],792,r"G$(4,4)$, 거리 최소 $2\sqrt2$ → $m^2=72$, 최대 $\sqrt{80}$ → $M^2=720$.")],
 "세 벡터의 합은 무게중심으로. 선분 위 점까지 거리: 수선의 발과 끝점.")

I('추가30·기하-09',"예상 오답 **16** — 영역을 $3x+y\\le\\sqrt{13}$의 반평면 전체가 아니라 타원 내부로 본 경우",
 ["X = P + Q에서 P는 직선 $3x+y=0$ 위를 **자유롭게** 움직입니다. 그러면 직선 방향으로는 어디든 갈 수 있고, 제약은 직선에 수직인 방향, 즉 $3x+y$의 값뿐입니다.",
  "$3x+y$의 값은 Q가 결정하므로 범위는 $|3x+y|\\le\\sqrt{13}$. 영역은 띠, 제1사분면 부분은 삼각형."],
 {'C1':("직선과 타원",r"P: $3x+y=0$ 위, Q: 타원 $x^2+\frac{y^2}4=1$ 위."),
  'C2':("벡터 합",r"$3x+y$는 일차식이라 X에서의 값 = P에서의 값($0$) + Q에서의 값."),
  'C3':("영역",r"$x,y\ge0$인 부분의 넓이 $\frac qp$.")},
 [("일차식 값의 덧셈",[r"$\ell(x,y)=3x+y$이면 $\ell(\mathrm P+\mathrm Q)=\ell(\mathrm P)+\ell(\mathrm Q)$."]),
  ("타원의 매개변수",[r"$(\cos\theta,2\sin\theta)$, $3\cos\theta+2\sin\theta$의 범위 $[-\sqrt{13},\sqrt{13}]$."])],
 [("$3x+y$의 값",['C2']),("Q로 범위",['C1']),("역으로 모든 점 가능",['C2']),("삼각형 넓이",['C3']),("답",['C3'])],
 [("영역이 띠인 이유",'C2',[r"P가 직선 전체를 움직이므로 X는 직선 방향으로 무한히 뻗습니다. 타원 모양이 남지 않습니다."])],
 [("변형 · 직선 $x+2y=0$",[r"직선 $x+2y=0$ 위를 움직이는 점 P와 타원 $x^2+\frac{y^2}4=1$ 위를 움직이는 점 Q에 대하여 $\vec{\mathrm{OX}}=\vec{\mathrm{OP}}+\vec{\mathrm{OQ}}$를 만족시키고 $x$, $y$좌표가 모두 $0$ 이상인 점 X가 나타내는 영역의 넓이가 $\frac qp$일 때, $p+q$의 값을 구하시오. (단, $p$, $q$는 서로소인 자연수)"],21,r"$\cos\theta+4\sin\theta\in[-\sqrt{17},\sqrt{17}]$, 삼각형 $(\sqrt{17},0)$, $(0,\tfrac{\sqrt{17}}2)$ → 넓이 $\tfrac{17}4$.")],
 "직선 위 점 + 곡선 위 점 = 직선에 수직인 방향의 폭만 남는 띠.")

I('추가30·기하-10',"예상 오답 **48** — Q의 위치를 한 가지만 생각해 $(4\\sqrt3+3)^2$을 답한 경우",
 ["$\\vec{\\mathrm{PA}}+\\vec{\\mathrm{PB}}=2\\vec{\\mathrm{PO}}$ (O는 AB의 중점=원의 중심). 조건식은 $\\vec{\\mathrm{OP}}\\cdot\\vec{\\mathrm{OQ}}$에 대한 식이 되어 **중심각 $\\frac\\pi3$**이 나옵니다.",
  "Q는 P에서 중심각 $\\frac\\pi3$만큼 양쪽으로 갈 수 있으니 $|\\vec{\\mathrm{AQ}}|$의 값이 두 개."],
 {'C1':("원",r"지름 AB$=10$, 중심 O, 반지름 $5$."),
  'C2':("조건식",r"$4\vec{\mathrm{OP}}\cdot\vec{\mathrm{OQ}}=2|\vec{\mathrm{PQ}}|^2$ → $\vec{\mathrm{OP}}\cdot\vec{\mathrm{OQ}}=\frac{25}2$, $\angle\mathrm{POQ}=\frac\pi3$."),
  'C4':("묻는 것",r"$|\vec{\mathrm{PA}}|=8$일 때 가능한 $|\vec{\mathrm{AQ}}|$의 값의 곱.")},
 [("중점 벡터",[r"$\vec{\mathrm{PA}}+\vec{\mathrm{PB}}=2\vec{\mathrm{PO}}$."]),("지름 위의 원주각",[r"$\angle\mathrm{APB}=90°$, $\overline{\mathrm{PA}}=10\cos\frac\theta2$ ($\theta=\angle\mathrm{POB}$)."])],
 [("중점으로 묶기",['C2']),("내적 식 정리",['C2']),("중심각 $\\frac\\pi3$",['C2']),("P의 위치",['C4']),("Q의 두 위치",['C4']),("두 값",['C4']),("곱",['C4'])],
 [("Q는 두 곳",'C4',[r"$\angle\mathrm{QOB}=\theta\pm\frac\pi3$. 한쪽만 쓰면 답이 하나뿐입니다."])],
 [("변형 · $|\\vec{\\mathrm{PA}}|=6$",[r"좌표평면에서 길이가 $10$인 선분 AB를 지름으로 하는 원 위의 두 점 P, Q가 $(\vec{\mathrm{PA}}+\vec{\mathrm{PB}})\cdot(\vec{\mathrm{QA}}+\vec{\mathrm{QB}})=2|\vec{\mathrm{PQ}}|^2$을 만족시킨다. $|\vec{\mathrm{PA}}|=6$일 때, 가능한 모든 $|\vec{\mathrm{AQ}}|$의 값의 곱을 구하시오."],11,r"$\cos\frac\theta2=\frac35$, $\sin\frac\theta2=\frac45$: $10\left(\tfrac35\cdot\tfrac{\sqrt3}2\mp\tfrac45\cdot\tfrac12\right)=3\sqrt3\mp4$, 곱 $27-16$.")],
 "$\\vec{\\mathrm{PA}}+\\vec{\\mathrm{PB}}=2\\vec{\\mathrm{PO}}$로 중심각을 얻는다. 원 위 다른 점은 양쪽 두 곳.")
