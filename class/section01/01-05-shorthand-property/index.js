// index.js

// 1. shorthand-property
function qqq(aaa){
    console.log(aaa) // 객체
    console.log(aaa.name) // 철수
    console.log(aaa.age) // 12
    console.log(aaa.school) // 다람쥐초등학교
}

const name = "철수"
const age = 12
const school = "다람쥐초등학교"
// const profile = {
//     name: name,
//     age: age,
//     school: school
// }
//
// const profile = { name, age, school } // 키와 밸류가 같아서 밸류를 생략함 => shorthand-property

qqq({ name, age, school }) // qqq(profile)과 같음