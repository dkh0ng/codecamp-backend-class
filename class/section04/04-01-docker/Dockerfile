# # 1. 운영체제 및 프로그램 설치
# FROM ubuntu:22.04

# RUN sudo apt install nodejs
# RUN sudo npm install -g yarn

# 1. install OS and software (이미 리눅스, node, npm, yarn 까지 모두 설치된 컴퓨터 다운로드하는 방식)
FROM node:14

# 2. 내 PC에 있는 index.js를 docekr로 복사
COPY ./index.js /index.js

# 3. docker 안에서 index.js 실행
CMD node index.js