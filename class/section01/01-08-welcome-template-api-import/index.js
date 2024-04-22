// index.js

import {checkEmail, getWelcomeTemplate, sendTemplateToEmail} from './email.js'

function createUser({ name, age, school, email }){
    // 1. 이메일이 정상인지 확인(1-존재여부, 2-"@"포함여부)
    const isValid = checkEmail(email)
    if(isValid === false) return

    // 2. 가입환영 템플릿 만들기
    const mytemplate = getWelcomeTemplate({ name, age, school })

    // 3. 이메일에 가입환영 템플릿 전송하기
    sendTemplateToEmail(email, mytemplate)
}

const name = "철수"
const age = 8
const school = "다람쥐초등학교"
const email = "a@a.com"
createUser({ name, age, school, email })