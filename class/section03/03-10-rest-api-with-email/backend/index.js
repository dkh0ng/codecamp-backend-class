import express from 'express';
import { checkEmail, getWelcomeTemplate, sendTemplateToEmail } from './email.js';
import { getToday } from './utils.js';

const app = express();
app.use(express.json());

app.post('/users', (req, res) => {
    const { name, age, school, email } = req.body;

    const isValid = checkEmail(email);
    if (!isValid) {
        return res.status(400).send("Invalid email address");
    }

    const createdAt = getToday();
    const mytemplate = getWelcomeTemplate({ name, age, school, createdAt });

    sendTemplateToEmail(email, mytemplate)
        .then(() => {
            res.status(200).send("Welcome email sent successfully");
        })
        .catch((error) => {
            console.error(error);
            res.status(500).send("Failed to send email");
        });
});

app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
