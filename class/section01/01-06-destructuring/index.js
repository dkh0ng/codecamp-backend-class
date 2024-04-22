// 3. 객체 전달하기 => 구조분해할당 방식으로 전달하기
function zzz(apple, banana){
    console.log(apple)
    console.log(banana)
}

const basket = {
    apple: 3,
    banana: 10
}
zzz(basket)