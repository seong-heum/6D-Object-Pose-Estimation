# 도커 이미지 만들기
# - 도커 이미지명과 태그명을 적절하게 수정 (필요시)

\cp -f docker_images/cfg/Dockerfile Dockerfile
docker build --tag nia-ssp:0.6 .
rm -f Dockerfile
