import coolsms from 'coolsms-node-sdk';
const mysms = coolsms.default;

export async function sendTokenToSMS(myphone, token) {
  const SMS_KEY = process.env.SMS_KEY;
  const SMS_SECRET = process.env.SMS_SECRET;
  const SMS_SENDER = process.env.SMS_SENDER;

  const messageService = new mysms(SMS_KEY, SMS_SECRET);
  const result = await messageService.sendOne({
    to: myphone,
    from: SMS_SENDER,
    text: `[코드캠프] 안녕하세요?! 요청하신 인증번호는 [${token}] 입니다.`,
  });
  console.log(result);
}
