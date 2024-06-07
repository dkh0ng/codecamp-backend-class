// email.js
import { getToday } from './utils.js';
import nodemailer from 'nodemailer';
import 'dotenv/config';

export function checkEmail(myemail) {
    if (myemail === undefined || !myemail.includes("@")) {
        console.log("에러 발생!!! 이메일 주소를 제대로 입력해 주세요!!!");
        return false;
    } else {
        return true;
    }
}

export function getWelcomeTemplate({ name, age, school, createdAt }) {
    const mytemplate = `
        <html>
            <body>
                <h1>${name}님 가입을 환영합니다!!!</h1>
                <hr />
                <div>이름: ${name}</div>
                <div>나이: ${age}</div>
                <div>학교: ${school}</div>
                <div>가입일: ${createdAt}</div>
            </body>
        </html>
    `;
    return mytemplate;
}

export async function sendTemplateToEmail(myemail, mytemplate) {
    const EMAIL_USER = process.env.EMAIL_USER;
    const EMAIL_PASS = process.env.EMAIL_PASS;
    const EMAIL_SENDER = process.env.EMAIL_SENDER;

    const transporter = nodemailer.createTransport({
        host: 'smtp.naver.com',
        port: 587,
        secure: false, // true for 465, false for other ports
        auth: {
            user: EMAIL_USER,
            pass: EMAIL_PASS,
        },
    });

    const result = await transporter.sendMail({
        from: EMAIL_SENDER,
        to: myemail,
        subject: "[코드캠프] 가입을 축하합니다!!!",
        html: mytemplate,
    });
    console.log(result);
}
