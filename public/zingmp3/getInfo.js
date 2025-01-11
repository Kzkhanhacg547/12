const axios = require("axios");

exports.name = '/zingmp3/info';
exports.index = async (req, res, next) => {
	if (require('../API_KEY/data/check_api_key.js').check_api_key(req, res)) return;
	const link = req.query.link;
	if (!link)
		return res.json({ error: 'Thiếu dữ liệu để khởi chạy chương trình ' });
	const id = link.match(/\/([a-zA-Z0-9]+)\.html/)?.[1] || link.match(/([a-zA-Z0-9]+)$/)?.[1];
	try {
		const response = await axios.get(`http://api.mp3.zing.vn/api/mobile/video/getvideoinfo?keycode=fafd463e2131914934b73310aa34a23f&requestdata={%22id%22:%22${id}%22}`);
		res.type('json').send(JSON.stringify(response.data, null, 2))
	}
	catch (error) {
		res.status(500).json({ error: 'Đã xảy ra lỗi' });
	}
};
