# 컴퓨터 만드는 설명서

# 1. 운영체제 설치(node 14버전과 npm과 yarn이 모두 설치되어있는 리눅스)
FROM node:14

# 2. 내 컴퓨터에 있는 폴더나 파일을 도커 컴퓨터 안으로 복사하기
COPY ./package.json /myfolder/
COPY ./yarn.lock /myfolder/
WORKDIR /myfolder/
RUN yarn install

COPY . /myfolder/

# 3. 도커안에서 index.js 실행시키기
CMD yarn start:dev