// const express = require('express') // 옛날 방식 => commonjs

import express from 'express'         // 요즘 방식 => module
const app = express()

app.get('/', function (req, res) {
  res.send('Hello World')
})

app.listen(3000)