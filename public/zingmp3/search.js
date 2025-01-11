const axios = require("axios");

exports.name = '/zingmp3/search';
exports.index = async (req, res, next) => {
	if (require('../API_KEY/data/check_api_key.js').check_api_key(req, res)) return;
	const keyWord = req.query.keyword;
	if (!keyWord)
		return res.json({ error: 'Thiếu dữ liệu để khởi chạy chương trình ' });
	const response = await axios.get('http://ac.mp3.zing.vn/complete?type=artist,song,key,code&num=500&query=' + encodeURIComponent(keyWord));
	const data = response.data;
	return res.type('json').send(JSON.stringify(data, null, 2));
};
