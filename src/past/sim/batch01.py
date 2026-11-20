"""기출관 유사문항(쌍둥이 문제) 1차: 2026학년도 수능 17문항
q: 문제(KaTeX $...$, 줄바꿈 <br>, 조건 상자 [[ ... ]]), ch: 보기 5개(없으면 단답형), a: 정답(보기 번호 또는 정수), sol: 풀이
모든 정답은 원문항 풀이를 코드로 옮겨 원문항 정답이 재현되는지 먼저 확인한 뒤, 조건만 바꿔 다시 계산해 검증했다."""
S = {
'2026-11-c11': dict(
    q='시각 $t=0$일 때 원점을 출발하여 수직선 위를 움직이는 점 P가 있다. 실수 $k$에 대하여 시각 $t\\,(t\\ge0)$일 때 점 P의 속도 $v(t)$가<br>$v(t)=t^2-kt+9$<br>이다. <보기>에서 옳은 것만을 있는 대로 고른 것은?'
      '[[ㄱ. $k=0$이면, 시각 $t=1$일 때 점 P의 위치는 $\\dfrac{28}{3}$이다.<br>ㄴ. $k=6$이면, 출발한 후 점 P의 운동 방향이 한 번 바뀐다.<br>ㄷ. $k=10$이면, 시각 $t=0$에서 $t=3$까지 점 P가 움직인 거리는 $\\dfrac{53}{3}$이다.]]',
    ch=['$\\text{ㄱ}$', '$\\text{ㄱ, ㄴ}$', '$\\text{ㄱ, ㄷ}$', '$\\text{ㄴ, ㄷ}$', '$\\text{ㄱ, ㄴ, ㄷ}$'], a=3,
    sol='ㄱ. $\\displaystyle\\int_0^1 (t^2+9)\\,dt=\\frac13+9=\\frac{28}{3}$ (참)<br>'
        'ㄴ. $v(t)=t^2-6t+9=(t-3)^2\\ge0$. $t=3$에서 $0$이 되지만 부호가 바뀌지 않으므로 운동 방향은 바뀌지 않는다. (거짓)<br>'
        'ㄷ. $v(t)=(t-1)(t-9)$이므로 $0\\le t\\le1$에서 $v\\ge0$, $1\\le t\\le3$에서 $v\\le0$.<br>'
        '$\\displaystyle\\int_0^1 v\\,dt=\\frac{13}{3},\\ \\int_1^3 v\\,dt=-\\frac{40}{3}$ 이므로 거리는 $\\dfrac{13}{3}+\\dfrac{40}{3}=\\dfrac{53}{3}$ (참)<br>답: ㄱ, ㄷ'),
'2026-11-c12': dict(
    q='등비수열 $\\{a_n\\}$이<br>$3(a_1+a_4+a_7)=a_4+a_7+a_{10}=12$<br>를 만족시킬 때, $a_{10}$의 값은?',
    ch=['$\\frac{100}{13}$', '$\\frac{104}{13}$', '$\\frac{108}{13}$', '$\\frac{112}{13}$', '$\\frac{116}{13}$'], a=3,
    sol='공비를 $r$라 하면 $a_4+a_7+a_{10}=r^3(a_1+a_4+a_7)$.<br>'
        '$a_1+a_4+a_7=4$이고 $a_4+a_7+a_{10}=12$이므로 $r^3=3$.<br>'
        '$a_1(1+r^3+r^6)=a_1(1+3+9)=4$에서 $a_1=\\dfrac{4}{13}$.<br>'
        '$a_{10}=a_1 r^9=\\dfrac{4}{13}\\times27=\\dfrac{108}{13}$'),
'2026-11-c13': dict(
    q='함수 $f(x)=x^2-3x-5$에 대하여 곡선 $y=f(x)$ 위의 점 $(1,\\,-7)$에서의 접선을 $l$이라 하고, 함수 $g(x)=(x^3-3x)f(x)$에 대하여 곡선 $y=g(x)$ 위의 점 $(1,\\,14)$에서의 접선을 $m$이라 하자. 두 직선 $l,\\ m$과 $y$축으로 둘러싸인 도형의 넓이는?',
    ch=['$36$', '$45$', '$54$', '$63$', '$72$'], a=3,
    sol='$f\'(x)=2x-3$이므로 $f\'(1)=-1$. $l:\\ y=-x-6$<br>'
        '$g\'(x)=(3x^2-3)f(x)+(x^3-3x)f\'(x)$이므로 $g\'(1)=0\\cdot(-7)+(-2)(-1)=2$. $m:\\ y=2x+12$<br>'
        '두 직선의 $y$절편은 $-6,\\ 12$이고, $-x-6=2x+12$에서 교점의 $x$좌표는 $-6$.<br>'
        '넓이 $=\\dfrac12\\times\\{12-(-6)\\}\\times6=54$'),
'2026-11-c14': dict(
    q='$\\overline{\\mathrm{AB}}=3,\\ \\overline{\\mathrm{BC}}=4$이고 $\\angle\\mathrm{B}=\\dfrac{\\pi}{2}$인 직각삼각형 ABC가 있다. 선분 AB의 중점을 D, 점 A를 중심으로 하고 반지름의 길이가 $\\overline{\\mathrm{AD}}$인 원이 선분 AC와 만나는 점을 E, 직선 AB가 이 원과 만나는 점 중 D가 아닌 점을 F라 하고, 호 EF 위의 점 G를 $\\overline{\\mathrm{CG}}=\\sqrt{26}$이 되도록 잡는다. 세 점 C, E, G를 지나는 원 위의 점 H가 $\\angle\\mathrm{HCG}=\\angle\\mathrm{BAC}$를 만족시킬 때, 선분 GH의 길이는? (단, 호 EF는 점 C와 같은 쪽에 있는 호이다.)',
    ch=['$\\frac{12\\sqrt3}{5}$', '$\\frac{14\\sqrt3}{5}$', '$\\frac{16\\sqrt3}{5}$', '$\\frac{18\\sqrt3}{5}$', '$4\\sqrt3$'], a=3,
    sol='A를 원점, B$(3,0)$, C$(3,4)$로 두면 $\\overline{\\mathrm{AD}}=\\dfrac32$, E$\\left(\\dfrac{9}{10},\\dfrac{6}{5}\\right)$.<br>'
        'G$\\left(\\dfrac32\\cos\\theta,\\dfrac32\\sin\\theta\\right)$에서 $\\overline{\\mathrm{CG}}^2=25+\\dfrac94-9\\cos\\theta-12\\sin\\theta=26$, 즉 $3\\cos\\theta+4\\sin\\theta=\\dfrac{5}{12}$ 를 만족시키는 호 EF 위의 점이 G.<br>'
        '삼각형 CEG의 외접원의 반지름을 $R$라 하면, 원주각 $\\angle\\mathrm{HCG}$에 대한 현이 GH이므로 $\\overline{\\mathrm{GH}}=2R\\sin(\\angle\\mathrm{BAC})=2R\\times\\dfrac45$.<br>'
        '사인법칙으로 $R$를 구하면 $\\overline{\\mathrm{GH}}=\\dfrac{16\\sqrt3}{5}$'),
'2026-11-c15': dict(
    q='함수 $f(x)$가<br>$f(x)=\\begin{cases}-x^2 & (x<0)\\\\ x^2-2x & (x\\ge0)\\end{cases}$<br>이고, 양수 $a$에 대하여 함수 $g(x)$를<br>$g(x)=\\begin{cases}ax+a & (x<-1)\\\\ 0 & (-1\\le x<1)\\\\ ax-a & (x\\ge1)\\end{cases}$<br>이라 하자. 함수 $h(x)=\\displaystyle\\int_0^x\\{g(t)-f(t)\\}\\,dt$가 오직 하나의 극값을 갖도록 하는 $a$의 최댓값을 $k$라 하자. $a=k$일 때, $k+h(3)$의 값은?',
    ch=['$10$', '$11$', '$12$', '$13$', '$14$'], a=3,
    sol='$h\'(x)=g(x)-f(x)$의 부호가 바뀌는 곳에서 극값을 갖는다.<br>'
        '$x\\ge1$: $g-f=-x^2+(a+2)x-a$, $x=1$에서 값이 $1>0$이므로 $x>1$에서 부호가 꼭 한 번 바뀐다.<br>'
        '$-1\\le x<1$: $g-f$는 $x^2$ 또는 $2x-x^2$로 $0$ 이상.<br>'
        '$x<-1$: $g-f=x^2+ax+a$. $x=-1$에서 $1>0$이고 꼭짓점이 $x=-\\frac a2$. 판별식 $a^2-4a>0$, 즉 $a>4$이면 부호가 두 번 바뀌어 극값이 3개.<br>'
        '따라서 $k=4$. $h(3)=\\displaystyle\\int_0^1(2t-t^2)dt+\\int_1^3(-t^2+6t-4)dt=\\frac23+\\frac{22}{3}=8$.<br>$k+h(3)=12$'),
'2026-11-c20': dict(
    q='수열 $\\{a_n\\}$이 다음 조건을 만족시킨다.'
      '[[$a_1=5$<br>2 이상의 자연수 $n$에 대하여 $\\displaystyle\\sum_{k=1}^{n}a_k=\\frac23a_n+\\frac13n^2-\\frac13n+6$ 이다.]]'
      '다음은 $\\displaystyle\\sum_{k=1}^{12}a_k+\\sum_{k=1}^{5}a_{2k+1}$의 값을 구하는 과정이다.'
      '[[2 이상의 자연수 $n$에 대하여 $a_{n+1}=\\displaystyle\\sum_{k=1}^{n+1}a_k-\\sum_{k=1}^{n}a_k$ 이므로<br>$a_{n+1}=\\dfrac23(a_{n+1}-a_n)+$ (가)<br>이고, 이 식을 정리하면 $2a_n+a_{n+1}=3\\times$ (가) …… ㉠<br>주어진 식에 $n=2$를 대입하면 $a_2=$ (나) …… ㉡<br>㉠과 ㉡에 의하여<br>$\\displaystyle\\sum_{k=1}^{12}a_k+\\sum_{k=1}^{5}a_{2k+1}=a_1+a_2+\\sum_{k=1}^{5}(2a_{2k+1}+a_{2k+2})=$ (다)]]'
      '위의 (가)에 알맞은 식을 $f(n)$이라 하고, (나), (다)에 알맞은 수를 각각 $p,\\ q$라 할 때, $\\dfrac{p\\times q}{f(12)}$의 값을 구하시오.',
    ch=None, a=50,
    sol='(가): $\\dfrac13\\{(n+1)^2-(n+1)\\}-\\dfrac13(n^2-n)=\\dfrac{2n}{3}$, 즉 $f(n)=\\dfrac{2n}{3}$이고 ㉠은 $2a_n+a_{n+1}=2n$.<br>'
        '(나): $n=2$이면 $5+a_2=\\dfrac23a_2+\\dfrac43-\\dfrac23+6$에서 $a_2=5$. $p=5$<br>'
        '(다): $2a_{2k+1}+a_{2k+2}=2(2k+1)$이므로 $5+5+\\displaystyle\\sum_{k=1}^{5}2(2k+1)=10+70=80$. $q=80$<br>'
        '$\\dfrac{p\\times q}{f(12)}=\\dfrac{400}{8}=50$'),
'2026-11-c21': dict(
    q='최고차항의 계수가 양수인 삼차함수 $f(x)$와 실수 $t$에 대하여 함수<br>$g(x)=\\begin{cases}-f(x) & (x<t)\\\\ f(x) & (x\\ge t)\\end{cases}$<br>는 실수 전체의 집합에서 연속이고 다음 조건을 만족시킨다.'
      '[[(가) 모든 실수 $a$에 대하여 $\\displaystyle\\lim_{x\\to a+}\\frac{g(x)}{x(x-3)}$의 값이 존재한다.<br>(나) $\\displaystyle\\lim_{x\\to m+}\\frac{g(x)}{x(x-3)}$의 값이 음수가 되도록 하는 자연수 $m$의 집합은 $\\left\\{g(-1),\\ -\\dfrac94g(1)\\right\\}$이다.]]'
      '$g(-4)$의 값을 구하시오. (단, $g(-1)\\ne-\\dfrac94g(1)$)',
    ch=None, a=42,
    sol='연속이므로 $f(t)=0$. (가)에서 $x\\to0+,\\ x\\to3+$일 때 분모가 $0$이므로 $f(0)=f(3)=0$. $f(x)=cx(x-3)(x-\\beta)\\ (c>0)$<br>'
        '$x\\ne0,3$에서 $\\dfrac{g(x)}{x(x-3)}$는 $x\\ge t$이면 $c(x-\\beta)$, $x<t$이면 $-c(x-\\beta)$.<br>'
        '(나)의 집합이 원소 2개가 되는 경우는 $t=3,\\ 4<\\beta\\le5$일 때 $\\{3,4\\}$ 뿐이다. (다른 경우는 원소가 1개 이하이거나 $-\\frac94g(1)$이 음수가 된다.)<br>'
        '$g(-1)=-f(-1)=4c(1+\\beta)$, $-\\dfrac94g(1)=\\dfrac94f(1)=\\dfrac92c(\\beta-1)$.<br>'
        '$g(-1)=4,\\ -\\frac94g(1)=3$이면 $c=\\dfrac{1}{1+\\beta}$, $\\dfrac{9(\\beta-1)}{2(\\beta+1)}=3$에서 $\\beta=5,\\ c=\\dfrac16$. (반대로 놓으면 $\\beta<0$이 되어 모순)<br>'
        '$g(-4)=-f(-4)=-\\dfrac16(-4)(-7)(-9)=42$'),
'2026-11-c22': dict(
    q='곡선 $y=\\log_{16}(8x+2)$ 위의 점 A$(a,\\,b)$와 곡선 $y=4^{x-1}-\\dfrac12$ 위의 점 B가 제1사분면에 있다. 점 A를 직선 $y=x$에 대하여 대칭이동한 점이 직선 OB 위에 있고 선분 AB의 중점의 좌표가 $\\left(\\dfrac{43}{8},\\ \\dfrac{17}{2}\\right)$일 때, $a\\times b=\\dfrac qp$이다. $p+q$의 값을 구하시오. (단, O는 원점이고, $p$와 $q$는 서로소인 자연수이다.)',
    ch=None, a=101,
    sol='A를 $y=x$에 대하여 대칭이동한 점 A$\'(b,a)$는 곡선 $y=\\dfrac{16^x}{8}-\\dfrac14$ 위에 있다.<br>'
        '$y=4^{x-1}-\\dfrac12=2\\left(\\dfrac{16^{x/2}}{8}-\\dfrac14\\right)$이므로 이 곡선은 앞 곡선을 원점 기준으로 2배 확대한 것. 따라서 B$=(2b,\\,2a)$.<br>'
        '중점: $\\dfrac{a+2b}{2}=\\dfrac{43}{8},\\ \\dfrac{b+2a}{2}=\\dfrac{17}{2}$에서 $a=\\dfrac{31}{4},\\ b=\\dfrac32$. (확인: $\\log_{16}64=\\dfrac32$)<br>'
        '$a\\times b=\\dfrac{93}{8}$, $p+q=101$'),
'2026-11-k28': dict(
    q='16개의 공과 1부터 6까지의 자연수가 하나씩 적혀 있는 여섯 개의 빈 상자가 있다. 한 개의 주사위를 사용하여 다음 시행을 한다.'
      '[[주사위를 한 번 던져 나온 눈의 수가 $k$일 때,<br>$k$가 홀수이면 1, 3, 5가 적힌 상자에 공을 각각 1개씩 넣고,<br>$k$가 짝수이면 $k$의 약수가 적힌 상자에 공을 각각 1개씩 넣는다.]]'
      '이 시행을 4번 반복한 후 여섯 개의 상자에 들어 있는 모든 공의 개수의 합이 홀수일 때, 3이 적힌 상자에 들어 있는 공의 개수와 2가 적힌 상자에 들어 있는 공의 개수가 같을 확률은?',
    ch=['$\\frac18$', '$\\frac{3}{20}$', '$\\frac{9}{40}$', '$\\frac14$', '$\\frac{3}{10}$'], a=3,
    sol='한 번 던질 때 넣는 공: 홀수(1,3,5) → 3개(상자 1,3,5), 2 → 2개(상자 1,2), 4 → 3개(상자 1,2,4), 6 → 4개(상자 1,2,3,6).<br>'
        '합이 홀수 ⟺ 홀수 개(3개)를 넣는 경우(홀수 눈 또는 4)가 홀수 번. 이런 경우는 $6^4$가지 중 $640$가지.<br>'
        '상자 3의 공 = (홀수 눈 횟수)+(6 횟수), 상자 2의 공 = (2 횟수)+(4 횟수)+(6 횟수)이므로 조건은 (홀수 눈 횟수) = (2 횟수)+(4 횟수).<br>'
        '두 조건을 모두 만족시키는 경우를 세면 $144$가지. 확률 $=\\dfrac{144}{640}=\\dfrac{9}{40}$'),
'2026-11-k29': dict(
    q='6 이하의 자연수 $a$에 대하여 한 개의 주사위와 한 개의 동전을 사용하여 다음 시행을 한다.'
      '[[주사위를 한 번 던져<br>나온 눈의 수가 $a$보다 작거나 같으면 동전을 4번 던져 앞면이 나온 횟수를 기록하고,<br>나온 눈의 수가 $a$보다 크면 동전을 2번 던져 앞면이 나온 횟수를 기록한다.]]'
      '이 시행을 16200번 반복하여 기록한 수가 2인 횟수를 확률변수 $X$라 하자. $\\mathrm{E}(X)=5400$일 때, $\\mathrm{P}(X\\ge5400-15a)$의 값을 표준정규분포표를 이용하여 구한 값이 $k$이다. $1000\\times k$의 값을 구하시오. (단, $\\mathrm{P}(0\\le Z\\le1)=0.341,\\ \\mathrm{P}(0\\le Z\\le2)=0.477,\\ \\mathrm{P}(0\\le Z\\le3)=0.499$로 계산한다.)',
    ch=None, a=841,
    sol='한 번의 시행에서 2가 기록될 확률은 $p=\\dfrac a6\\cdot\\dfrac{{}_4\\mathrm{C}_2}{16}+\\dfrac{6-a}{6}\\cdot\\dfrac14=\\dfrac{a+12}{48}$.<br>'
        '$\\mathrm{E}(X)=16200p=5400$에서 $p=\\dfrac13$, $a=4$.<br>'
        '$\\mathrm{V}(X)=16200\\cdot\\dfrac13\\cdot\\dfrac23=3600$, $\\sigma=60$. $X$는 근사적으로 $\\mathrm{N}(5400,60^2)$.<br>'
        '$\\mathrm{P}(X\\ge5340)=\\mathrm{P}(Z\\ge-1)=0.5+0.341=0.841$, $1000k=841$'),
'2026-11-k30': dict(
    q='비어 있는 주머니 9개가 일렬로 놓여 있고, 공 7개가 있다. 각 주머니에 들어 있는 공의 개수가 2 이하가 되도록 공을 주머니에 남김없이 나누어 넣을 때, 다음 조건을 만족시키는 경우의 수를 구하시오. (단, 공끼리는 서로 구별하지 않는다.)'
      '[[(가) 들어 있는 공의 개수가 1인 주머니는 3개 또는 5개이다.<br>(나) 들어 있는 공의 개수가 2인 주머니와 이웃한 주머니에는 공이 들어 있지 않다.]]',
    ch=None, a=184,
    sol='공 1개 주머니가 3개이면 공 2개 주머니는 2개, 5개이면 1개.<br>'
        '(i) 2개짜리 2개, 1개짜리 3개, 빈 주머니 4개: 2개짜리 주머니 양옆은 비어야 한다. 빈 주머니로 둘러싸도록 배치하는 경우를 세면 $100$가지.<br>'
        '(ii) 2개짜리 1개, 1개짜리 5개, 빈 주머니 3개: 같은 방법으로 $84$가지.<br>'
        '합 $100+84=184$ (모든 배치를 하나씩 확인하여 검증)'),
'2026-11-m28': dict(
    q='함수 $f(x)=\\dfrac12x^2+x-\\ln(1+x)$와 양수 $t$에 대하여 점 $(s,\\,f(s))\\,(s>0)$에서 $y$축에 내린 수선의 발과 곡선 $y=f(x)$ 위의 점 $(s,\\,f(s))$에서의 접선이 $y$축과 만나는 점 사이의 거리가 $t$가 되도록 하는 $s$의 값을 $g(t)$라 하자. $\\displaystyle\\int_{\\frac32}^{\\frac{16}{3}}g(t)\\,dt$의 값은?',
    ch=['$\\frac{19}{3}+\\ln\\frac23$', '$\\frac{19}{3}-\\ln2$', '$6+\\ln\\frac23$', '$\\frac{20}{3}+\\ln\\frac23$', '$\\frac{19}{3}+\\ln3$'], a=1,
    sol='접선의 $y$절편은 $f(s)-sf\'(s)$이므로 거리는 $t=sf\'(s)=s\\left(s+1-\\dfrac{1}{1+s}\\right)=\\dfrac{s^2(s+2)}{s+1}$ (증가함수).<br>'
        '$t=\\dfrac32 \\Leftrightarrow s=1$, $t=\\dfrac{16}{3}\\Leftrightarrow s=2$. 역함수의 적분으로<br>'
        '$\\displaystyle\\int_{\\frac32}^{\\frac{16}{3}}g(t)dt=2\\cdot\\frac{16}{3}-1\\cdot\\frac32-\\int_1^2\\frac{s^2(s+2)}{s+1}ds$<br>'
        '$\\dfrac{s^3+2s^2}{s+1}=s^2+s-1+\\dfrac{1}{s+1}$이므로 $\\displaystyle\\int_1^2=\\frac{17}{6}+\\ln\\frac32$.<br>'
        '값 $=\\dfrac{32}{3}-\\dfrac32-\\dfrac{17}{6}-\\ln\\dfrac32=\\dfrac{19}{3}+\\ln\\dfrac23$'),
'2026-11-m29': dict(
    q='첫째항과 공차가 같은 등차수열 $\\{a_n\\}$과 등비수열 $\\{b_n\\}$이 다음 조건을 만족시킨다.'
      '[[어떤 자연수 $k$에 대하여 $b_{k+i}=\\dfrac{2}{a_i}-1\\ (i=1,2,3)$ 이다.]]'
      '부등식 $5<\\displaystyle\\sum_{n=1}^{\\infty}\\left(b_n-\\frac{1}{a_na_{n+1}}\\right)<20$ 이 성립할 때, $a_2\\times\\displaystyle\\sum_{n=1}^{\\infty}b_{2n}=\\dfrac qp$이다. $p+q$의 값을 구하시오. (단, $a_1\\ne0$이고, $p$와 $q$는 서로소인 자연수이다.)',
    ch=None, a=35,
    sol='$a_n=nd$로 두고 $u=\\dfrac2d$라 하면 $b_{k+i}=\\dfrac ui-1$. 등비 조건 $\\left(\\dfrac u2-1\\right)^2=(u-1)\\left(\\dfrac u3-1\\right)$에서 $u=4$, $d=\\dfrac12$.<br>'
        '$b_{k+1}=3,\\ b_{k+2}=1,\\ b_{k+3}=\\dfrac13$이므로 공비 $\\dfrac13$, $b_1=3^{k+1}$, $\\displaystyle\\sum b_n=\\frac92\\cdot3^k$.<br>'
        '$\\displaystyle\\sum\\frac{1}{a_na_{n+1}}=4\\sum\\frac{1}{n(n+1)}=4$. $5<\\dfrac92\\cdot3^k-4<20$에서 $k=1$.<br>'
        '$b_2=3$이므로 $\\displaystyle\\sum b_{2n}=\\frac{3}{1-\\frac19}=\\frac{27}{8}$, $a_2=1$. 값은 $\\dfrac{27}{8}$, $p+q=35$'),
'2026-11-m30': dict(
    q='실수 전체의 집합에서 증가하는 연속함수 $f(x)$의 역함수 $f^{-1}(x)$가 다음 조건을 만족시킨다.'
      '[[(가) $|x|\\le1$일 때, $4\\times\\{f^{-1}(x)\\}^2=x^2(x^2-5)^2$이다.<br>(나) $|x|>1$일 때, $|f^{-1}(x)|=2e^{|x|-1}$이다.]]'
      '실수 $m$에 대하여 기울기가 $m$이고 점 $(1,\\,0)$을 지나는 직선이 곡선 $y=f(x)$와 만나는 점의 개수를 $g(m)$이라 하자. 함수 $g(m)$이 $m=a,\\ m=b\\ (a<b)$에서 불연속일 때, $g(a)\\times\\left(\\displaystyle\\lim_{m\\to a+}g(m)\\right)+g(b)\\times\\dfrac{1}{be^{b}}$의 값을 구하시오. (단, $\\displaystyle\\lim_{x\\to\\infty}\\frac{\\ln x}{x}=0$)',
    ch=None, a=7,
    sol='(가)에서 $f^{-1}(x)=\\dfrac{5x-x^3}{2}\\ (|x|\\le1)$ (증가), $f^{-1}(\\pm1)=\\pm2$. (나)에서 $x>1$이면 $f^{-1}(x)=2e^{x-1}$, $x<-1$이면 $f^{-1}(x)=-2e^{-x-1}$.<br>'
        '즉 $f(x)=1+\\ln\\dfrac x2\\ (x>2)$, $f(x)=-1-\\ln\\left(-\\dfrac x2\\right)\\ (x<-2)$, $f(0)=0$.<br>'
        '$m\\le0$이면 교점 1개. $m=0$에서 $g(0)=1$이고, $m$이 $0$보다 조금 크면 오른쪽 아주 먼 곳의 교점이 생겨 교점 3개: $\\displaystyle\\lim_{m\\to0+}g(m)=3$, $a=0$.<br>'
        '$m$이 커지다가 직선이 $x<-2$ 부분에 접하면 교점 2개가 되고, 그보다 크면 1개. 접점을 $(x_0,f(x_0))$, $s=-\\dfrac{x_0}{2}$라 하면 $m=\\dfrac{1}{2s}$이고 $\\ln s=\\dfrac{1}{2s}$, 즉 $b=\\dfrac{1}{2s}$, $s=e^b$에서 $2be^b=1$.<br>'
        '값 $=1\\times3+2\\times2=7$'),
'2026-11-g28': dict(
    q='$\\overline{\\mathrm{AB}}=\\overline{\\mathrm{CD}}=6,\\ \\overline{\\mathrm{BC}}=\\overline{\\mathrm{BD}}=3\\sqrt5$인 사면체 ABCD가 있고, 점 A에서 직선 CD에 내린 수선의 발 H에 대하여 두 평면 ABH와 BCD는 서로 수직이고 $\\overline{\\mathrm{AH}}=6$이다. 삼각형 ABH의 무게중심을 G라 하고, 점 G를 중심으로 하고 평면 ACD에 접하는 구를 $S$라 하자. $\\angle\\mathrm{APG}=\\dfrac{\\pi}{2}$인 구 $S$ 위의 모든 점 P가 나타내는 도형을 $T$라 할 때, 도형 $T$의 평면 ABC 위로의 정사영의 넓이는?',
    ch=['$\\frac{\\pi}{4}$', '$\\frac{3\\pi}{8}$', '$\\frac{7\\pi}{16}$', '$\\frac{9\\pi}{16}$', '$\\frac{5\\pi}{8}$'], a=4,
    sol='$\\overline{\\mathrm{BC}}=\\overline{\\mathrm{BD}}$이고 평면 ABH ⊥ 평면 BCD, AH ⊥ CD에서 H는 CD의 중점이고 BH ⊥ CD. $\\overline{\\mathrm{BH}}=\\sqrt{45-9}=6$이므로 삼각형 ABH는 한 변이 6인 정삼각형.<br>'
        'H를 원점, C$(-3,0,0)$, D$(3,0,0)$, B$(0,-6,0)$, A$(0,-3,3\\sqrt3)$로 두면 G$(0,-3,\\sqrt3)$.<br>'
        '구 $S$의 반지름은 G에서 평면 ACD까지의 거리 $\\sqrt3$. $\\angle\\mathrm{APG}=\\dfrac\\pi2$인 점 P는 AG를 지름으로 하는 구 위에 있으므로 $T$는 두 구의 교선인 원이다.<br>'
        '$\\overline{\\mathrm{AG}}=2\\sqrt3$, $\\overline{\\mathrm{GP}}=\\sqrt3$이므로 $\\angle\\mathrm{GAP}=\\dfrac\\pi6$, 원 $T$의 반지름은 $\\overline{\\mathrm{GP}}\\cos\\dfrac\\pi6=\\dfrac32$이고 원 $T$의 평면은 직선 AG에 수직.<br>'
        '직선 AG와 평면 ABC의 법선이 이루는 각의 코사인이 $\\dfrac14$이므로 정사영의 넓이 $=\\pi\\left(\\dfrac32\\right)^2\\times\\dfrac14=\\dfrac{9\\pi}{16}$'),
'2026-11-g29': dict(
    q='초점이 F$(p,\\,0)\\,(p>0)$이고 준선이 $x=-p$인 포물선 위의 점 중 제1사분면에 있는 점 A에서 포물선의 준선에 내린 수선의 발을 H라 하고, 두 초점이 $x$축 위에 있고 세 점 F, A, H를 지나는 타원의 $x$좌표가 양수인 초점을 B라 하자. 삼각형 AHB의 둘레의 길이가 $p+24$, 넓이가 $5p$일 때, 선분 HF의 길이를 $k$라 하자. $k^2$의 값을 구하시오.',
    ch=None, a=320,
    sol='A$(x_1,y_1)$, H$(-p,y_1)$. 타원은 A, H를 지나므로 중심의 $x$좌표는 $c=\\dfrac{x_1-p}{2}$, F는 꼭짓점이므로 장축의 절반은 $p-c$.<br>'
        'H와 A는 타원의 축에 대하여 대칭이므로 $\\overline{\\mathrm{HB}}+\\overline{\\mathrm{AB}}=2(p-c)$. 둘레 $=\\overline{\\mathrm{AH}}+2(p-c)=(x_1+p)+(3p-x_1)=4p=p+24$에서 $p=8$.<br>'
        '넓이 $\\dfrac12(x_1+8)\\cdot\\sqrt{32x_1}=40$에서 $(x_1+8)\\sqrt{2x_1}=10$, $x_1=2$, $y_1=8$.<br>'
        '$k^2=\\overline{\\mathrm{HF}}^2=(2p)^2+y_1^2=256+64=320$'),
'2026-11-g30': dict(
    q='좌표평면에서 길이가 $10$인 선분 AB를 지름으로 하는 원 위의 두 점 P, Q가<br>$(\\overrightarrow{\\mathrm{PA}}+\\overrightarrow{\\mathrm{PB}})\\cdot(\\overrightarrow{\\mathrm{PQ}}+\\overrightarrow{\\mathrm{PB}})=2|\\overrightarrow{\\mathrm{PQ}}|^2$<br>을 만족시킨다. $|\\overrightarrow{\\mathrm{PB}}|=8$일 때, $|\\overrightarrow{\\mathrm{PA}}\\cdot\\overrightarrow{\\mathrm{QB}}|=\\dfrac qp$이다. $p+q$의 값을 구하시오. (단, $|\\overrightarrow{\\mathrm{QB}}|>0$이고, $p$와 $q$는 서로소인 자연수이다.)',
    ch=None, a=1177,
    sol='원의 중심을 O라 하면 $\\overrightarrow{\\mathrm{PA}}+\\overrightarrow{\\mathrm{PB}}=2\\overrightarrow{\\mathrm{PO}}$.<br>'
        'O를 원점, A$(-5,0)$, B$(5,0)$으로 두면 $|\\overrightarrow{\\mathrm{PB}}|=8$, $|\\overrightarrow{\\mathrm{PA}}|=6$에서 P$\\left(-\\dfrac{7}{5},\\dfrac{24}{5}\\right)$.<br>'
        '조건식을 Q$(5\\cos\\theta,5\\sin\\theta)$에 대해 정리하면 Q$=$B 또는 Q$\\left(-\\dfrac{527}{125},-\\dfrac{336}{125}\\right)$.<br>'
        '$\\overrightarrow{\\mathrm{PA}}=\\left(-\\dfrac{18}{5},-\\dfrac{24}{5}\\right)$, $\\overrightarrow{\\mathrm{QB}}=\\left(\\dfrac{1152}{125},\\dfrac{336}{125}\\right)$에서 $|\\overrightarrow{\\mathrm{PA}}\\cdot\\overrightarrow{\\mathrm{QB}}|=\\dfrac{1152}{25}$, $p+q=1177$'),
}
