exports.name = '/instagram/downloadpost';
exports.index = async(req, res, next) => {
const url = req.query.url;
if (!url) return res.json({ error: 'Thiếu dữ liệu để khởi chạy chương trình ' });
const axios = require('axios');

const options = {
  method: 'GET',
  url: 'https://instagram-looter2.p.rapidapi.com/id',
  params: {
    username: 'abdallhdev'
  },
  headers: {
    'X-RapidAPI-Key': 'e5ba826ae5mshb7fbd95e446b378p161b41jsnabe9db7a75ac',
    'X-RapidAPI-Host': 'instagram-looter2.p.rapidapi.com'
  }
};

try {
	const response = await axios.request(options);
	console.log(response.data);
} catch (error) {
	console.error(error);
}

axios.request(options).then(function (response) {
	console.log(response.data);
  return res.json(response.data)
}).catch(function (error) {
	console.error(error);
});
}