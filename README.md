# 객체 3D 데이터 유효성 검증
## https://github.com/seongheum-ssu/nia-ssp
<br>

## * 전체 실행 (build & test)
> git clone https://github.com/seongheum-ssu/nia-ssp <br>
> ./build.sh <br>
> ./run.sh all <br>
<br>

## * 객체별 샘플링 평가
### 1. docker image 생성 --> build.sh
> ./build.sh <br>

wget https://www.dropbox.com/s/o16mx914up6oen2/nia-ssp.tar?dl=0 -O docker_images/nia-ssp.tar <br>
(참고) docker image 로드: docker load -i docker_images/nia-ssp.tar <br>
(참고) docker image 저장: docker save -o docker_images/nia-ssp.tar nia-ssp:1.0 <br>
<br>

### 2. 객체 ID 별 자료 준비 (샘플)--> prepare.sh
> ./prepare.sh 100211 <br>

(평가용 데이터셋) ./test_datasets/ <br>
--> [030102](https://www.dropbox.com/s/ydtnhwvysg2fvvo/030102.zip?dl=0) <br>
--> [050110](https://www.dropbox.com/s/ld7zfoe9pr86qu2/050110.zip?dl=0) <br>
--> [050201](https://www.dropbox.com/s/9fb3hnd40rhz68d/050201.zip?dl=0) <br>
--> [050202](https://www.dropbox.com/s/k6lsp2rlmbedsyl/050202.zip?dl=0) <br>
--> [050210](https://www.dropbox.com/s/gk1b1bg4e931dsh/050210.zip?dl=0) <br>
--> [050305](https://www.dropbox.com/s/pcb1vwizq1uaxjz/050305.zip?dl=0) <br>
--> [050311](https://www.dropbox.com/s/utwec26vvjnmie5/050311.zip?dl=0) <br>
--> [050312](https://www.dropbox.com/s/si1c526uq7mg06j/050312.zip?dl=0) <br>
--> [060106](https://www.dropbox.com/s/0cw8zt71f8u4hy1/060106.zip?dl=0) <br>
--> [060108](https://www.dropbox.com/s/r84wv871l88zwj7/060108.zip?dl=0) <br>
--> [060201](https://www.dropbox.com/s/4cj57g1tm18mnr3/060201.zip?dl=0) <br>
--> [060207](https://www.dropbox.com/s/dxwt1ast6b3cetb/060207.zip?dl=0) <br>
--> [060211](https://www.dropbox.com/s/vwnucm61dlntp2b/060211.zip?dl=0) <br>
--> [060302](https://www.dropbox.com/s/nk32bsbfgycpp78/060302.zip?dl=0) <br>
--> [070205](https://www.dropbox.com/s/ificlxyaol943tv/070205.zip?dl=0) <br>
--> [070308](https://www.dropbox.com/s/x278nx4yxc01c9r/070308.zip?dl=0) <br>
--> [070403](https://www.dropbox.com/s/6ay4d8j56p3ugps/070403.zip?dl=0) <br>
--> [070409](https://www.dropbox.com/s/031mq094h37upot/070409.zip?dl=0) <br>
--> [070605](https://www.dropbox.com/s/wzhz2eubjcfnp8v/070605.zip?dl=0) <br>
--> [070608](https://www.dropbox.com/s/jte74l0eq1byazq/070608.zip?dl=0) <br>
--> [070610](https://www.dropbox.com/s/cva2x3tw9h3p7nh/070610.zip?dl=0) <br>
--> [070611](https://www.dropbox.com/s/b0vgj2yfgcfbgg1/070611.zip?dl=0) <br>
--> [070702](https://www.dropbox.com/s/7zof15nzxr1a7cq/070702.zip?dl=0) <br>
--> [070704](https://www.dropbox.com/s/nfahelwydczjfbe/070704.zip?dl=0) <br>
--> [070708](https://www.dropbox.com/s/2fctsxq21oidcd4/070708.zip?dl=0) <br>
--> [070710](https://www.dropbox.com/s/b6wixfagu0s1uq0/070710.zip?dl=0) <br>
--> [070902](https://www.dropbox.com/s/6va40eyyhog7l7t/070902.zip?dl=0) <br>
--> [070911](https://www.dropbox.com/s/7ymvccb7iurwvhf/070911.zip?dl=0) <br>
--> [090105](https://www.dropbox.com/s/maav9grhxukapkb/090105.zip?dl=0) <br>
--> [090206](https://www.dropbox.com/s/3bovmeiyka7yef5/090206.zip?dl=0) <br>
--> [100205](https://www.dropbox.com/s/lt1vd49tvqeom11/100205.zip?dl=0) <br>
--> [100211](https://www.dropbox.com/s/2fvabie5mtwsft1/100211.zip?dl=0) <br>
<br>

### 3. 객체 ID 별 유효성 검증 --> test.sh
> ./test.sh 100211 <br>

(평가 결과/로그 파일) ./experimental_results/ <br>
<br>

## * 유효성 검증 보고서
https://github.com/seongheum-ssu/nia-ssp/tree/main/docker_images/doc
