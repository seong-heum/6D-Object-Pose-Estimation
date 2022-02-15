# 객체 3D 데이터 유효성 검증
## https://github.com/seongheum-ssu/nia-ssp
<br>

## * 전체/객체별 실행 (Quick start)
      git clone https://github.com/seongheum-ssu/nia-ssp
      cd nia-ssp
      ./build.sh
      ./run.sh 070308
      ./run.sh all
<br>

## * 객체별 샘플링 평가 (단계별 실행/분석)
### 1. docker image 생성 --> build.sh
      ./build.sh <br>
또는, <br>

      wget https://www.dropbox.com/s/o16mx914up6oen2/nia-ssp.tar?dl=0 -O docker_images/nia-ssp.tar
            
(참고) docker image 로드: docker load -i docker_images/nia-ssp.tar <br>
(참고) docker image 저장: docker save -o docker_images/nia-ssp.tar nia-ssp:1.0 <br>
<br>

### 2. 객체 ID 별 자료 준비 (샘플)--> prepare.sh

      ./prepare.sh 070308

(평가용 데이터셋) ./test_datasets/ <br>
* **0101:	남자**<br>
[010101](https://www.dropbox.com/s/9snrohm0hni10ew/010101.zip?dl=0): 20대남자<br>
[010102](https://www.dropbox.com/s/jgvzk3uvcluwih7/010102.zip?dl=0): 30대남자<br>
[010103](https://www.dropbox.com/s/d3s0sifm4dyvic4/010103.zip?dl=0): 40대남자<br>
[010104](https://www.dropbox.com/s/lws3n0vqwd3t8aq/010104.zip?dl=0): 50대남자<br>
[010105](https://www.dropbox.com/s/60v2wzxktc29v4i/010105.zip?dl=0): 60대이상남자<br>
* **0102:	여자**<br>
[010201](https://www.dropbox.com/s/iu7y8fc2fcm48j8/010201.zip?dl=0): 20대여자<br>
[010202](https://www.dropbox.com/s/3cppj7wbyseayd2/010202.zip?dl=0): 30대여자<br>
[010203](https://www.dropbox.com/s/c4nfl8lxmtmy2q6/010203.zip?dl=0): 40대여자<br>
[010204](https://www.dropbox.com/s/jxmz9v989vmtbac/010204.zip?dl=0): 50대여자<br>
[010205](https://www.dropbox.com/s/d0ufbk9fvwy66lj/010205.zip?dl=0): 60대이상여자<br>
* **0301:	생활가전**<br>
[030101](https://www.dropbox.com/s/s8bjpvt4bl65mqk/030101.zip?dl=0): 로봇청소기<br>
[030102](https://www.dropbox.com/s/ydtnhwvysg2fvvo/030102.zip?dl=0): 쉐이커<br>
[030103](https://www.dropbox.com/s/fawm17mrc8o2num/030103.zip?dl=0): 스팀다리미<br>
[030105](https://www.dropbox.com/s/wpfcpmvkon0cmii/030105.zip?dl=0): 선풍기<br>
[030106](https://www.dropbox.com/s/49amt8qmdwkk4fs/030106.zip?dl=0): 가습기<br>
[030107](https://www.dropbox.com/s/0j8jdbs1on8wam4/030107.zip?dl=0): 공기청정기<br>
* **0302:	컴퓨터/주변기기**<br>
[030201](https://www.dropbox.com/s/jjzhgz6z2uv196m/030201.zip?dl=0): 게임컨트롤러<br>
[030203](https://www.dropbox.com/s/bxlhcvp52ztbgnu/030203.zip?dl=0): 마우스<br>
[030204](https://www.dropbox.com/s/687fv3oe83rjpzz/030204.zip?dl=0): 키보드<br>
[030205](https://www.dropbox.com/s/ftnwz3nmvr9br7y/030205.zip?dl=0): 외장하드<br>
[030206](https://www.dropbox.com/s/1722yali8kik21e/030206.zip?dl=0): 인터넷공유기<br>
[030209](https://www.dropbox.com/s/7b7h2qox0o98xxg/030209.zip?dl=0): 스캐너<br>
* **0303:	디지털기기/용품**<br>
[030301](https://www.dropbox.com/s/97u3dy2q1esxa47/030301.zip?dl=0): 마이크<br>
[030302](https://www.dropbox.com/s/l3qr9m2tl4vvt0u/030302.zip?dl=0): 헤드셋<br>
[030303](https://www.dropbox.com/s/3dp3un5euwsxch5/030303.zip?dl=0): 디지털펜<br>
[030304](https://www.dropbox.com/s/hzhqe2droklik0f/030304.zip?dl=0): 멀티탭<br>
[030305](https://www.dropbox.com/s/c935yjhcg1xtt06/030305.zip?dl=0): 스피커<br>
[030306](https://www.dropbox.com/s/un4j0sznr6bsr8f/030306.zip?dl=0): 블루투스 스피커<br>
[030307](https://www.dropbox.com/s/orme4jzfr41a40b/030307.zip?dl=0): 핸드폰보조배터리<br>
[030308](https://www.dropbox.com/s/odvq5tyngao32hl/030308.zip?dl=0): 휴대폰충전기<br>
[030309](https://www.dropbox.com/s/fyq1ubmowrrs71a/030309.zip?dl=0): 휴대폰<br>
* **0403:	신발**<br>
[040301](https://www.dropbox.com/s/fggmp32rkn6pbn5/040301.zip?dl=0): 로퍼<br>
[040302](https://www.dropbox.com/s/f6lbv1x2echyjjt/040302.zip?dl=0): 남성운동화<br>
[040303](https://www.dropbox.com/s/ck184u5h6ccgn2e/040303.zip?dl=0): 남성단화<br>
[040304](https://www.dropbox.com/s/eaidbmu38gbavgz/040304.zip?dl=0): 여성슬리퍼<br>
[040305](https://www.dropbox.com/s/pt6elynbuknoqf0/040305.zip?dl=0): 욕실슬리퍼<br>
[040306](https://www.dropbox.com/s/bwpfp5ga0r4jr08/040306.zip?dl=0): 크록스<br>
[040307](https://www.dropbox.com/s/u2xki85v6czzdrx/040307.zip?dl=0): 슬리퍼<br>
[040308](https://www.dropbox.com/s/2fsllo2td93vsbp/040308.zip?dl=0): 실내화<br>
[040309](https://www.dropbox.com/s/2937sgpmzvw9ceo/040309.zip?dl=0): 골프화<br>
[040310](https://www.dropbox.com/s/ml3cme6ulmn3fkm/040310.zip?dl=0): 아동고무신<br>
[040311](https://www.dropbox.com/s/kasdustroncu9ic/040311.zip?dl=0): 거실화<br>
* **0404:	모자**<br>
[040402](https://www.dropbox.com/s/ltpgmseovziysv2/040402.zip?dl=0): 중절모<br>
[040403](https://www.dropbox.com/s/pavssok5yfhik0c/040403.zip?dl=0): 썬캡<br>
[040404](https://www.dropbox.com/s/mqhc0qngjwpgyom/040404.zip?dl=0): 야구모자<br>
[040407](https://www.dropbox.com/s/w5mew9t3fqrfiq7/040407.zip?dl=0): 자전거헬멧<br>
[040408](https://www.dropbox.com/s/tfr1pnxwjwbga6b/040408.zip?dl=0): 밀짚모자<br>
[040409](https://www.dropbox.com/s/y42zs7ytz5fti69/040409.zip?dl=0): 안전모<br>
* **0501:	스포츠용품**<br>
[050101](https://www.dropbox.com/s/thnil0vtgvmssk2/050101.zip?dl=0): 럭비공<br>
[050102](https://www.dropbox.com/s/aij7lmjupg0eu05/050102.zip?dl=0): 셔틀콕<br>
[050103](https://www.dropbox.com/s/j3tfpz22ssz75s5/050103.zip?dl=0): 야구배트<br>
[050104](https://www.dropbox.com/s/6qatmt5wdsgh950/050104.zip?dl=0): 권투글러브<br>
[050105](https://www.dropbox.com/s/5ha1repmljnp8o9/050105.zip?dl=0): 탁구채<br>
[050106](https://www.dropbox.com/s/qex9odrz87feqaj/050106.zip?dl=0): 탁구공<br>
[050107](https://www.dropbox.com/s/qv875ik0lan77go/050107.zip?dl=0): 축구공<br>
[050108](https://www.dropbox.com/s/532j3qen21rw7sm/050108.zip?dl=0): 야구공<br>
[050109](https://www.dropbox.com/s/22edmwpuryu106x/050109.zip?dl=0): 볼링핀<br>
[050110](https://www.dropbox.com/s/ld7zfoe9pr86qu2/050110.zip?dl=0): 테니스공<br>
[050111](https://www.dropbox.com/s/o52fkzpzl1crox1/050111.zip?dl=0): 정강이보호대<br>
[050112](https://www.dropbox.com/s/c5l5j7t3cuz2rwj/050112.zip?dl=0): 탱탱볼<br>
* **0502:	레저/캠핑**<br>
[050201](https://www.dropbox.com/s/9fb3hnd40rhz68d/050201.zip?dl=0): 부탄가스<br>
[050202](https://www.dropbox.com/s/k6lsp2rlmbedsyl/050202.zip?dl=0): 코펠<br>
[050203](https://www.dropbox.com/s/1e4j61awfl1p3cu/050203.zip?dl=0): 토치<br>
[050204](https://www.dropbox.com/s/l3rw3u37mt4cgct/050204.zip?dl=0): 접이식등산컵<br>
[050205](https://www.dropbox.com/s/x3gz3ikcvrccj9z/050205.zip?dl=0): 돗자리<br>
[050206](https://www.dropbox.com/s/nxot5kvix3hlpb2/050206.zip?dl=0): 피크닉바구니<br>
[050207](https://www.dropbox.com/s/o387khtaon6stpr/050207.zip?dl=0): 로프<br>
[050208](https://www.dropbox.com/s/pzvz9jjevbepue9/050208.zip?dl=0): 아이스박스<br>
[050209](https://www.dropbox.com/s/bd3hkcretcb3946/050209.zip?dl=0): 등산용방석<br>
[050210](https://www.dropbox.com/s/gk1b1bg4e931dsh/050210.zip?dl=0): 망원경<br>
[050211](https://www.dropbox.com/s/5uoy51ytgx386lv/050211.zip?dl=0): 모기향<br>
[050212](https://www.dropbox.com/s/zxflz957arpxyw9/050212.zip?dl=0): 반합<br>
* **0503:	홈트레이닝**<br>
[050301](https://www.dropbox.com/s/961rf2b9uevbhry/050301.zip?dl=0): 밸런스보드<br>
[050302](https://www.dropbox.com/s/kyy2fjzzag7lq78/050302.zip?dl=0): 육각덤벨<br>
[050303](https://www.dropbox.com/s/jywzkukwvkh94jv/050303.zip?dl=0): 원형덤벨<br>
[050304](https://www.dropbox.com/s/vykfi90tjsux3i0/050304.zip?dl=0): 요가링<br>
[050305](https://www.dropbox.com/s/pcb1vwizq1uaxjz/050305.zip?dl=0): 케틀벨<br>
[050306](https://www.dropbox.com/s/77ivla2fgc2yra1/050306.zip?dl=0): 무게원판<br>
[050307](https://www.dropbox.com/s/otm0j93dwgvaj89/050307.zip?dl=0): 슬라이더<br>
[050308](https://www.dropbox.com/s/ame421lsprxgq0k/050308.zip?dl=0): 만보기<br>
[050309](https://www.dropbox.com/s/bsfmfwg57d1o0aw/050309.zip?dl=0): 악력기<br>
[050310](https://www.dropbox.com/s/vg0k319ilchohhg/050310.zip?dl=0): 폼롤러<br>
[050311](https://www.dropbox.com/s/utwec26vvjnmie5/050311.zip?dl=0): 마사지용공<br>
[050312](https://www.dropbox.com/s/si1c526uq7mg06j/050312.zip?dl=0): 푸시업바<br>
* **0601:	과일**<br>
[060102](https://www.dropbox.com/s/q5nann3qvjw0hac/060102.zip?dl=0): 석류<br>
[060103](https://www.dropbox.com/s/sp9gy82mx2t0337/060103.zip?dl=0): 참외<br>
[060104](https://www.dropbox.com/s/3z5q22dzx9c487h/060104.zip?dl=0): 오렌지<br>
[060105](https://www.dropbox.com/s/mn6otpcnsfmg5av/060105.zip?dl=0): 바나나<br>
[060106](https://www.dropbox.com/s/0cw8zt71f8u4hy1/060106.zip?dl=0): 망고스틴<br>
[060107](https://www.dropbox.com/s/nmxf2nxljjxujj6/060107.zip?dl=0): 키위<br>
[060108](https://www.dropbox.com/s/r84wv871l88zwj7/060108.zip?dl=0): 토마토<br>
[060109](https://www.dropbox.com/s/fa9wi8s2qmcr97d/060109.zip?dl=0): 사과<br>
[060110](https://www.dropbox.com/s/lsdbpdo6c6628qh/060110.zip?dl=0): 감<br>
[060111](https://www.dropbox.com/s/8v11s6touwzudi7/060111.zip?dl=0): 배<br>
[060112](https://www.dropbox.com/s/ew81q03x0eqt4vl/060112.zip?dl=0): 복숭아<br>
* **0602:	야채**<br>
[060201](https://www.dropbox.com/s/4cj57g1tm18mnr3/060201.zip?dl=0): 무우<br>
[060203](https://www.dropbox.com/s/lrxlc2k9mgt60a3/060203.zip?dl=0): 고추<br>
[060204](https://www.dropbox.com/s/e5cr5xnbhtw4ogl/060204.zip?dl=0): 단호박<br>
[060205](https://www.dropbox.com/s/9w02qnuqus0xqm0/060205.zip?dl=0): 양파<br>
[060206](https://www.dropbox.com/s/7m1sruu8wxdg8nf/060206.zip?dl=0): 감자<br>
[060207](https://www.dropbox.com/s/dxwt1ast6b3cetb/060207.zip?dl=0): 당근<br>
[060208](https://www.dropbox.com/s/a6gin6pi402arwm/060208.zip?dl=0): 피망<br>
[060209](https://www.dropbox.com/s/6ddbfjcudiy7er9/060209.zip?dl=0): 버섯<br>
[060210](https://www.dropbox.com/s/r1v6wdfy8p1egzd/060210.zip?dl=0): 옥수수<br>
[060211](https://www.dropbox.com/s/vwnucm61dlntp2b/060211.zip?dl=0): 고구마<br>
[060212](https://www.dropbox.com/s/zsdrngtss9fiqss/060212.zip?dl=0): 가지<br>
* **0603:	제과/제빵**<br>
[060301](https://www.dropbox.com/s/u6t41qpqtx64ff3/060301.zip?dl=0): 마카롱<br>
[060302](https://www.dropbox.com/s/nk32bsbfgycpp78/060302.zip?dl=0): 모닝빵<br>
[060303](https://www.dropbox.com/s/fuvhfgt9v8uev5v/060303.zip?dl=0): 바게트<br>
[060304](https://www.dropbox.com/s/r9yaceqbp5r6je1/060304.zip?dl=0): 샌드위치<br>
[060305](https://www.dropbox.com/s/jzsz6kbvhwyv65d/060305.zip?dl=0): 크림빵<br>
[060306](https://www.dropbox.com/s/2sq9n1xeae5ivwj/060306.zip?dl=0): 식빵<br>
[060307](https://www.dropbox.com/s/ch3mkwg7pa93ed0/060307.zip?dl=0): 크로와상<br>
[060308](https://www.dropbox.com/s/7u3ouqyaueouotv/060308.zip?dl=0): 베이글<br>
[060309](https://www.dropbox.com/s/n3umsxmoy5tair4/060309.zip?dl=0): 조각케이크<br>
* **0701:	영유아용품**<br>
[070101](https://www.dropbox.com/s/qrva40hyfklhxf4/070101.zip?dl=0): 장난감자동차<br>
[070102](https://www.dropbox.com/s/kb0qd0sg0o9mt0y/070102.zip?dl=0): 유아변기커버<br>
[070103](https://www.dropbox.com/s/l89jprce0ah5vz5/070103.zip?dl=0): 젖병<br>
[070105](https://www.dropbox.com/s/lixxl837xk1bfmw/070105.zip?dl=0): 비눗방울총<br>
[070106](https://www.dropbox.com/s/knsk2vqt63nukom/070106.zip?dl=0): 유아용식판<br>
[070107](https://www.dropbox.com/s/dlcpm1kn5e5z5xj/070107.zip?dl=0): 딸랑이<br>
[070108](https://www.dropbox.com/s/vv6iw8otujdr4cc/070108.zip?dl=0): 블록<br>
[070109](https://www.dropbox.com/s/0s54ogt6v2ptr4a/070109.zip?dl=0): 인형<br>
[070110](https://www.dropbox.com/s/1epbes40n2l9ckx/070110.zip?dl=0): 유아용물총<br>
[070111](https://www.dropbox.com/s/4n7wwl3a9oj6ngu/070111.zip?dl=0): 치아발육기<br>
[070112](https://www.dropbox.com/s/jvuyapt4agwkha0/070112.zip?dl=0): 젖병세척솔<br>
[070113](https://www.dropbox.com/s/skwu2msbvs8dyhm/070113.zip?dl=0): 유아용빨대컵<br>
* **0702:	주방용품**<br>
[070201](https://www.dropbox.com/s/q4d2vo19onvldgu/070201.zip?dl=0): 식칼<br>
[070202](https://www.dropbox.com/s/ht5oel9q7jjbtu3/070202.zip?dl=0): 도마<br>
[070203](https://www.dropbox.com/s/v6bchwrb6bj8ar1/070203.zip?dl=0): 접시<br>
[070204](https://www.dropbox.com/s/b818ij7sw09dbup/070204.zip?dl=0): 국그릇<br>
[070205](https://www.dropbox.com/s/ificlxyaol943tv/070205.zip?dl=0): 물컵<br>
[070206](https://www.dropbox.com/s/jsmqbngeuydq0dj/070206.zip?dl=0): 수동착즙기<br>
[070207](https://www.dropbox.com/s/8ruvb7177wl1u1i/070207.zip?dl=0): 냄비<br>
[070208](https://www.dropbox.com/s/aomc21nxwtf3eo0/070208.zip?dl=0): 프라이팬<br>
[070209](https://www.dropbox.com/s/kt9c5a139cnltrh/070209.zip?dl=0): 뒤집개<br>
[070210](https://www.dropbox.com/s/2js76qt6vzxgj7z/070210.zip?dl=0): 커피포트<br>
[070212](https://www.dropbox.com/s/sjojd1572xgvglj/070212.zip?dl=0): 얼음틀<br>
[070213](https://www.dropbox.com/s/auri3llydp9hea9/070213.zip?dl=0): 전자레인지용기<br>
* **0703:	청소용품**<br>
[070302](https://www.dropbox.com/s/nlhpadd28skav5s/070302.zip?dl=0): 분무기<br>
[070303](https://www.dropbox.com/s/u7e9px1ynu284y4/070303.zip?dl=0): 대야<br>
[070304](https://www.dropbox.com/s/l32qpb67gcmsgv3/070304.zip?dl=0): 바가지<br>
[070305](https://www.dropbox.com/s/rcm9m5ryghe4lgw/070305.zip?dl=0): 돌돌이<br>
[070306](https://www.dropbox.com/s/3314gaz0blzp0f7/070306.zip?dl=0): 쓰레받기<br>
[070307](https://www.dropbox.com/s/2yphcq12odc8k3i/070307.zip?dl=0): 양동이<br>
[070308](https://www.dropbox.com/s/x278nx4yxc01c9r/070308.zip?dl=0): 물조리개<br>
[070309](https://www.dropbox.com/s/7n2teoa83y4yv3x/070309.zip?dl=0): 청소솔<br>
[070312](https://www.dropbox.com/s/fzmx5rznalli3n0/070312.zip?dl=0): 변기솔<br>
[070313](https://www.dropbox.com/s/0k9j9lem0xlsthm/070313.zip?dl=0): 소형빗자루<br>
* **0704:	미용**<br>
[070401](https://www.dropbox.com/s/1bmz4k5vhcgdegu/070401.zip?dl=0): 헤어드라이어<br>
[070402](https://www.dropbox.com/s/qeqob3rpnqev3er/070402.zip?dl=0): 고데기<br>
[070403](https://www.dropbox.com/s/6ay4d8j56p3ugps/070403.zip?dl=0): 입욕제<br>
[070404](https://www.dropbox.com/s/gppzsflpzvmjxkg/070404.zip?dl=0): 화장용브러쉬<br>
[070405](https://www.dropbox.com/s/y582fmpvqnyagaa/070405.zip?dl=0): 뷰러<br>
[070406](https://www.dropbox.com/s/f2q44ci3t0zvx28/070406.zip?dl=0): 토너패드<br>
[070407](https://www.dropbox.com/s/1voy77z9fh3q12o/070407.zip?dl=0): 샴푸<br>
[070408](https://www.dropbox.com/s/5x1s86crqvjehgt/070408.zip?dl=0): 미용비누<br>
[070409](https://www.dropbox.com/s/031mq094h37upot/070409.zip?dl=0): 립밤<br>
[070410](https://www.dropbox.com/s/cxv86vbvtx4i3p3/070410.zip?dl=0): 폼클렌저<br>
[070411](https://www.dropbox.com/s/04a3gjfdlqqot0f/070411.zip?dl=0): 렌즈세척액<br>
[070413](https://www.dropbox.com/s/r9o9y7ibn3glel8/070413.zip?dl=0): 왁스<br>
[070414](https://www.dropbox.com/s/27shcuxwb1107ro/070414.zip?dl=0): 썬크림<br>
[070415](https://www.dropbox.com/s/slccp1rb59bee85/070415.zip?dl=0): 핸드크림<br>
[070416](https://www.dropbox.com/s/5xt56lx3no0yewg/070416.zip?dl=0): 매니큐어<br>
* **0705:	공구**<br>
[070501](https://www.dropbox.com/s/0bdy9iz8q75c30g/070501.zip?dl=0): 전선탈피기<br>
[070502](https://www.dropbox.com/s/2joqo1tamqxt6fh/070502.zip?dl=0): 니퍼<br>
[070503](https://www.dropbox.com/s/1ddv1l9vkynciic/070503.zip?dl=0): 스패너<br>
[070504](https://www.dropbox.com/s/rx54t68v7nitjhm/070504.zip?dl=0): 건타카<br>
[070506](https://www.dropbox.com/s/tb0uf3iyzjc0xao/070506.zip?dl=0): 망치<br>
[070507](https://www.dropbox.com/s/sc6g9s2xpjdiuld/070507.zip?dl=0): 방청윤활제<br>
[070508](https://www.dropbox.com/s/1hp8bknzi1ymay3/070508.zip?dl=0): 톱<br>
[070509](https://www.dropbox.com/s/8uy0qul0kdfkyk1/070509.zip?dl=0): 줄자<br>
[070510](https://www.dropbox.com/s/hq9htivk5ksv6iv/070510.zip?dl=0): 펜치<br>
[070511](https://www.dropbox.com/s/dityuontk15x07n/070511.zip?dl=0): 글루건<br>
[070512](https://www.dropbox.com/s/270y5szx9q6cw5g/070512.zip?dl=0): 건전지<br>
* **0706:	위생용품**<br>
[070601](https://www.dropbox.com/s/0t6d08ydyiyplle/070601.zip?dl=0): 일반면도기<br>
[070602](https://www.dropbox.com/s/r6prswt4kdj4bma/070602.zip?dl=0): 핸드워시<br>
[070603](https://www.dropbox.com/s/1m196kif3shloal/070603.zip?dl=0): 칫솔<br>
[070604](https://www.dropbox.com/s/z4we38zsy3f1mhc/070604.zip?dl=0): 치약<br>
[070605](https://www.dropbox.com/s/wzhz2eubjcfnp8v/070605.zip?dl=0): 손소독제<br>
[070606](https://www.dropbox.com/s/asuyvgdre3fazwf/070606.zip?dl=0): 혀클리너<br>
[070607](https://www.dropbox.com/s/on6zm0kmda4sl3o/070607.zip?dl=0): 롤화장지<br>
[070608](https://www.dropbox.com/s/jte74l0eq1byazq/070608.zip?dl=0): 각티슈<br>
[070609](https://www.dropbox.com/s/b73u4rucapr48mi/070609.zip?dl=0): 키친타올<br>
[070610](https://www.dropbox.com/s/cva2x3tw9h3p7nh/070610.zip?dl=0): 구강청정제<br>
[070611](https://www.dropbox.com/s/b0vgj2yfgcfbgg1/070611.zip?dl=0): 락스<br>
[070612](https://www.dropbox.com/s/i609ofgoudkg56k/070612.zip?dl=0): 치실<br>
[070613](https://www.dropbox.com/s/n85i10pcg5pi068/070613.zip?dl=0): 면도크림<br>
* **0707:	생활잡화**<br>
[070701](https://www.dropbox.com/s/70g4wdtez98xj6k/070701.zip?dl=0): 옷걸이<br>
[070702](https://www.dropbox.com/s/7zof15nzxr1a7cq/070702.zip?dl=0): 라이터<br>
[070703](https://www.dropbox.com/s/mqfw732u4imyhyb/070703.zip?dl=0): 탈취제<br>
[070704](https://www.dropbox.com/s/nfahelwydczjfbe/070704.zip?dl=0): 살충제<br>
[070705](https://www.dropbox.com/s/rtsunva1yyjmata/070705.zip?dl=0): 휴대폰거치대<br>
[070706](https://www.dropbox.com/s/6h2kwu0y4c0wepd/070706.zip?dl=0): 종이컵<br>
[070707](https://www.dropbox.com/s/484kyjvvuh8qvdc/070707.zip?dl=0): 여행용멀티어댑터<br>
[070708](https://www.dropbox.com/s/2fctsxq21oidcd4/070708.zip?dl=0): 휴지통<br>
[070709](https://www.dropbox.com/s/vndb1s602bgt7ix/070709.zip?dl=0): 안경집<br>
[070710](https://www.dropbox.com/s/b6wixfagu0s1uq0/070710.zip?dl=0): 향초<br>
[070711](https://www.dropbox.com/s/8t3vm9t74v43ydi/070711.zip?dl=0): 구두약<br>
[070712](https://www.dropbox.com/s/l5o8tlcs4rcu39k/070712.zip?dl=0): 섬유탈취제<br>
* **0708:	애완용품**<br>
[070801](https://www.dropbox.com/s/n7qschebrdeif1k/070801.zip?dl=0): 애완용밥그릇<br>
[070802](https://www.dropbox.com/s/gihvr9sffzg5dbu/070802.zip?dl=0): 애완용개껌<br>
[070803](https://www.dropbox.com/s/65g32a9zeauf4kk/070803.zip?dl=0): 애완용배변봉투케이스<br>
[070804](https://www.dropbox.com/s/cyzjp4pus2qqs93/070804.zip?dl=0): 애완용발톱깎이<br>
[070805](https://www.dropbox.com/s/7gt2enbf85y1qrw/070805.zip?dl=0): 애완용간식통조림<br>
[070806](https://www.dropbox.com/s/1ckq5h3syij257c/070806.zip?dl=0): 애완용장난감삑삑이<br>
[070807](https://www.dropbox.com/s/3r6kpz8t86zh1sj/070807.zip?dl=0): 고양이스크래쳐<br>
[070808](https://www.dropbox.com/s/y4gd1puspiurjqx/070808.zip?dl=0): 애완용목욕브러쉬<br>
[070809](https://www.dropbox.com/s/c5802b54fpno09e/070809.zip?dl=0): 애완용목줄<br>
[070810](https://www.dropbox.com/s/8ndn900azeaq57j/070810.zip?dl=0): 애완용배변판<br>
* **0709:	자동차용품**<br>
[070901](https://www.dropbox.com/s/tlk0b6lbhet4ip3/070901.zip?dl=0): 소화기<br>
[070902](https://www.dropbox.com/s/6va40eyyhog7l7t/070902.zip?dl=0): 차량용청소용솔<br>
[070903](https://www.dropbox.com/s/1xo9viu4wmgtit7/070903.zip?dl=0): 목쿠션<br>
[070904](https://www.dropbox.com/s/7bo79700et92nxg/070904.zip?dl=0): 차량용휴대폰거치대<br>
[070906](https://www.dropbox.com/s/ee1dy2krxkqs59i/070906.zip?dl=0): 차량용청소기<br>
[070907](https://www.dropbox.com/s/w29qtwyh6urspc3/070907.zip?dl=0): 주차고깔<br>
[070909](https://www.dropbox.com/s/ydbuupz4payvh76/070909.zip?dl=0): 차량용방향제<br>
[070910](https://www.dropbox.com/s/4f7szl0575kbd0a/070910.zip?dl=0): 차량용USB소켓<br>
[070911](https://www.dropbox.com/s/7ymvccb7iurwvhf/070911.zip?dl=0): 차량용도어가드<br>
[070912](https://www.dropbox.com/s/am6qzdc5prk2mnl/070912.zip?dl=0): 차량용안전망치<br>
[070913](https://www.dropbox.com/s/cb400auhsxx70pl/070913.zip?dl=0): 엔진오일<br>
* **0710:	세탁용품**<br>
[071001](https://www.dropbox.com/s/59bb314umbtx1hn/071001.zip?dl=0): 가루세제<br>
[071002](https://www.dropbox.com/s/bapda881c3xrp5m/071002.zip?dl=0): 액체세제<br>
[071003](https://www.dropbox.com/s/1ym8kfv5cgy8j42/071003.zip?dl=0): 빨래비누<br>
[071004](https://www.dropbox.com/s/gwohpgvpfzv3cj5/071004.zip?dl=0): 소매용다리미판<br>
[071005](https://www.dropbox.com/s/6y6v8tc7dx7ig0v/071005.zip?dl=0): 빨래집게<br>
[071006](https://www.dropbox.com/s/vc8itspk2t8r3ez/071006.zip?dl=0): 찌든때용세제<br>
[071008](https://www.dropbox.com/s/7vc7dcdk2kq8p2g/071008.zip?dl=0): 세제계량스푼<br>
[071009](https://www.dropbox.com/s/6yfvvsp72uekfs6/071009.zip?dl=0): 빨래방망이<br>
[071010](https://www.dropbox.com/s/7tqel8wpuyae3km/071010.zip?dl=0): 의류먼지제거기<br>
* **0801:	즉석/편의식품**<br>
[080101](https://www.dropbox.com/s/l45m9t6fehz3yzg/080101.zip?dl=0): 컵라면<br>
[080102](https://www.dropbox.com/s/i6emjqi8eqg3r1r/080102.zip?dl=0): 스팸<br>
[080103](https://www.dropbox.com/s/7lvazhg419k2ihv/080103.zip?dl=0): 통조림<br>
[080104](https://www.dropbox.com/s/qolha6ej23zhr68/080104.zip?dl=0): 즉석짜장<br>
[080105](https://www.dropbox.com/s/qmmecn2beskdkl4/080105.zip?dl=0): 즉석밥<br>
[080106](https://www.dropbox.com/s/au5ny0uez6a3tlx/080106.zip?dl=0): 즉석죽<br>
[080107](https://www.dropbox.com/s/9a1wxjbwvqdtp6g/080107.zip?dl=0): 시리얼<br>
[080108](https://www.dropbox.com/s/eypja3ekdr7pw2p/080108.zip?dl=0): 간편미소국<br>
[080109](https://www.dropbox.com/s/jvhl8xy0chw8nhz/080109.zip?dl=0): 참치캔<br>
* **0901:	문구/사무용품**<br>
[090103](https://www.dropbox.com/s/6skbcyfoux8xlto/090103.zip?dl=0): 다이어리<br>
[090104](https://www.dropbox.com/s/3lirqpkfp42ezl8/090104.zip?dl=0): 바인더<br>
[090105](https://www.dropbox.com/s/maav9grhxukapkb/090105.zip?dl=0): 딱풀<br>
[090107](https://www.dropbox.com/s/vkudwt0vbephwmv/090107.zip?dl=0): 가위<br>
[090109](https://www.dropbox.com/s/xxakeyh3h22116f/090109.zip?dl=0): 순간접착제<br>
[090110](https://www.dropbox.com/s/9d2ogyxf75h4uz0/090110.zip?dl=0): 스테이플러<br>
[090113](https://www.dropbox.com/s/cgo0s4uyrq1tosq/090113.zip?dl=0): 큐브<br>
* **0902:	악기**<br>
[090201](https://www.dropbox.com/s/uhws18sdm4japty/090201.zip?dl=0): 리코더<br>
[090202](https://www.dropbox.com/s/o47cbma6vppjp4p/090202.zip?dl=0): 단소<br>
[090203](https://www.dropbox.com/s/wrxgos251lhc5f2/090203.zip?dl=0): 우쿨렐레<br>
[090204](https://www.dropbox.com/s/vkt1mp9x3mwx4c3/090204.zip?dl=0): 실로폰<br>
[090205](https://www.dropbox.com/s/d986n8czfobqsb8/090205.zip?dl=0): 소금<br>
[090206](https://www.dropbox.com/s/3bovmeiyka7yef5/090206.zip?dl=0): 하모니카<br>
[090207](https://www.dropbox.com/s/10dxkq74eeizzg3/090207.zip?dl=0): 캐스터네츠<br>
[090209](https://www.dropbox.com/s/vioatoa6ps1ac59/090209.zip?dl=0): 소고<br>
[090210](https://www.dropbox.com/s/onjkiwtxcxnhycx/090210.zip?dl=0): 핸드벨<br>
[090211](https://www.dropbox.com/s/qzzfiava273q8o3/090211.zip?dl=0): 리듬타악기<br>
[090212](https://www.dropbox.com/s/qzzfiava273q8o3/090211.zip?dl=0): 마라카스<br>
* **0903:	미술용품**<br>
[090301](https://www.dropbox.com/s/trjjvjzm6x4ab9u/090301.zip?dl=0): 팔레트<br>
[090302](https://www.dropbox.com/s/qv6k0c36at6nn61/090302.zip?dl=0): 물감<br>
[090303](https://www.dropbox.com/s/hww64vqo90854f1/090303.zip?dl=0): 파스텔<br>
[090304](https://www.dropbox.com/s/refvqfqdmcdq4cx/090304.zip?dl=0): 필통<br>
[090305](https://www.dropbox.com/s/89l309ar3wgjrwo/090305.zip?dl=0): 물통<br>
[090306](https://www.dropbox.com/s/7z6cpqdoc4nd35x/090306.zip?dl=0): 색연필<br>
[090307](https://www.dropbox.com/s/9t94dlqq3i74ktl/090307.zip?dl=0): 점토조각칼<br>
[090308](https://www.dropbox.com/s/zpfyyj4stk6cezp/090308.zip?dl=0): 크레파스<br>
[090309](https://www.dropbox.com/s/w29z6ng1ul9xhad/090309.zip?dl=0): 연필깎이<br>
[090310](https://www.dropbox.com/s/r4i8pr1hymkbyas/090310.zip?dl=0): 포스터칼라<br>
* **0904:	게임용품**<br>
[090404](https://www.dropbox.com/s/yw0f3mn5mbwdrub/090404.zip?dl=0): 악어이빨게임<br>
[090405](https://www.dropbox.com/s/h9j7e751uk6se0c/090405.zip?dl=0): 젠가<br>
[090406](https://www.dropbox.com/s/ntdtvjko4m94hyz/090406.zip?dl=0): 피젯스피너<br>
[090407](https://www.dropbox.com/s/r9p1plhvrzpuep7/090407.zip?dl=0): 주사위<br>
[090408](https://www.dropbox.com/s/p31s48d5f9tn2gn/090408.zip?dl=0): 윷가락<br>
[090409](https://www.dropbox.com/s/92zppd7h35g3m5w/090409.zip?dl=0): 해적룰렛<br>
[090410](https://www.dropbox.com/s/iupp1ty7ipk9z59/090410.zip?dl=0): 링쌓기<br>
* **0905:	이벤트용품**<br>
[090502](https://www.dropbox.com/s/kaa6ycgkv1lcdyp/090502.zip?dl=0): LED장식초<br>
[090504](https://www.dropbox.com/s/q3lavbzletbz54g/090504.zip?dl=0): 호박바구니<br>
[090505](https://www.dropbox.com/s/1o117dgml8m58uy/090505.zip?dl=0): 크리스마스트리<br>
[090506](https://www.dropbox.com/s/zj3m223og8ugalm/090506.zip?dl=0): 폭죽<br>
[090507](https://www.dropbox.com/s/cgxts1y5ov60p3l/090507.zip?dl=0): 응원나팔<br>
[090509](https://www.dropbox.com/s/5uzewl9chqtekb7/090509.zip?dl=0): 응원짝짝이<br>
[090510](https://www.dropbox.com/s/9sj37idrhp4p756/090510.zip?dl=0): 응원봉<br>
* **1001:	가구**<br>
[100101](https://www.dropbox.com/s/3j4kaohxv9yifio/100101.zip?dl=0): 접이식상<br>
[100103](https://www.dropbox.com/s/c8yd6ezyglqxk5h/100103.zip?dl=0): 접이식의자<br>
[100105](https://www.dropbox.com/s/9318lrckov0wvxv/100105.zip?dl=0): 스툴<br>
[100107](https://www.dropbox.com/s/qim0qbynbifz5b7/100107.zip?dl=0): 협탁<br>
[100108](https://www.dropbox.com/s/ol8h79bvdsttup1/100108.zip?dl=0): 리빙테이블<br>
[100109](https://www.dropbox.com/s/l7wafszxv7h9w37/100109.zip?dl=0): 서랍장<br>
* **1002:	인테리어**<br>
[100201](https://www.dropbox.com/s/fftu0uo61d6eynj/100201.zip?dl=0): 사각형벽시계<br>
[100203](https://www.dropbox.com/s/zjpbrx4c8y94kgd/100203.zip?dl=0): 전자알람시계<br>
[100204](https://www.dropbox.com/s/dh3xeyovrj7jpkx/100204.zip?dl=0): 원형액자<br>
[100205](https://www.dropbox.com/s/lt1vd49tvqeom11/100205.zip?dl=0): 사각형액자<br>
[100206](https://www.dropbox.com/s/cqms7zuf5lsu6ui/100206.zip?dl=0): 벽옷걸이<br>
[100207](https://www.dropbox.com/s/wrtqujspjpyr5xt/100207.zip?dl=0): 꽃화분<br>
[100208](https://www.dropbox.com/s/i8h4fma3mdp57aw/100208.zip?dl=0): 말장식소품<br>
[100210](https://www.dropbox.com/s/pfgjbkydhqtok3v/100210.zip?dl=0): 스탠드<br>
[100211](https://www.dropbox.com/s/2fvabie5mtwsft1/100211.zip?dl=0): 무드등<br>
[100212](https://www.dropbox.com/s/ykxsx046mac38jo/100212.zip?dl=0): 원형탁자시계<br>
* **1101:	의료기기**<br>
[110101](https://www.dropbox.com/s/90qwok6ygz3xpt5/110101.zip?dl=0): 바르는모기약용기<br>
[110102](https://www.dropbox.com/s/wy5wucq7c739erx/110102.zip?dl=0): 약병<br>
[110103](https://www.dropbox.com/s/zl77kojk5h10nz2/110103.zip?dl=0): 귀체온계<br>
[110104](https://www.dropbox.com/s/npd2rfqe9benfuc/110104.zip?dl=0): 체중계<br>
[110105](https://www.dropbox.com/s/d66bsxm95jczerx/110105.zip?dl=0): 면봉<br>
[110106](https://www.dropbox.com/s/d5xdhm6c7uyohir/110106.zip?dl=0): 구급상자<br>
[110107](https://www.dropbox.com/s/mstha9g5e0j2wg0/110107.zip?dl=0): 상처소독약병<br>
[110108](https://www.dropbox.com/s/1ez1116vy3vwh0k/110108.zip?dl=0): 물약병<br>
[110109](https://www.dropbox.com/s/mtrmi2jvw84l8sp/110109.zip?dl=0): 연고<br>
[110110](https://www.dropbox.com/s/2f8yal4pq02npyv/110110.zip?dl=0): 주사기<br>
[110111](https://www.dropbox.com/s/0q6tzgbocarmbow/110111.zip?dl=0): 얼굴마사지기<br>
[110112](https://www.dropbox.com/s/9ijku739cse0oyq/110112.zip?dl=0): 목마사지기<br>
[110113](https://www.dropbox.com/s/3sz7xyq2wykddzr/110113.zip?dl=0): 압박붕대<br>
<br>

### 3. 객체 ID 별 유효성 검증 --> test.sh

      ./test.sh 070308

(평가 결과/로그 파일) ./experimental_results/ <br>
<br>

## * 유효성 검증 보고서
https://github.com/seongheum-ssu/nia-ssp/tree/main/docker_images/doc

## * 참고자료

