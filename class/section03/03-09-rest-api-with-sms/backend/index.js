import swaggerUi from 'swagger-ui-express';
import swaggerJSDoc from 'swagger-jsdoc';
import { options } from './swagger/config.js';
import express from 'express';
import cors from 'cors';
import 'dotenv/config';
import { sendTokenToSMS } from './phone.js';

const app = express();
app.use(express.json());
app.use(cors());

// 기존 엔드포인트들
app.get('/boards', (req, res) => {
  const result = [
    { number: 1, writer: "철수", title: "제목입니다~~", contents: "내용이에요!!!" },
    { number: 2, writer: "영희", title: "영희입니다~~", contents: "영희이에요!!!" },
    { number: 3, writer: "훈이", title: "훈이입니다~~", contents: "훈이이에요!!!" },
  ];
  res.send(result);
});

app.post('/boards', (req, res) => {
  console.log(req);
  console.log("=========================");
  console.log(req.body);
  res.send("게시물 등록에 성공하였습니다.");
});

// 새로운 /tokens/phone 엔드포인트 추가
app.post('/tokens/phone', async (req, res) => {
  const phone = req.body.qqq;
  console.log(`Phone number received: ${phone}`);

  // 랜덤 6자리 숫자 생성
  const token = Math.floor(100000 + Math.random() * 900000);
  console.log(`Generated token: ${token}`);

  // SMS 전송
  try {
    await sendTokenToSMS(phone, token);
    res.status(200).send(`인증번호가 ${phone}로 전송되었습니다.`);
  } catch (error) {
    console.error(error);
    res.status(500).send('인증번호 전송에 실패했습니다.');
  }
});

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerJSDoc(options)));

app.listen(3000, () => {
  console.log("Backend is running");
});
