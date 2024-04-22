function getWelcomeTemplate({ name, age, school, createdAt }){
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
    `
    console.log(mytemplate)
}

const name = "철수"
const age = 10
const school = "공룡초등학교"
const createdAt = "2022-10-12"
getWelcomeTemplate({ name, age, school, createdAt })