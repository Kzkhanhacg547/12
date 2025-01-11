const axios = require("axios");

exports.name = '/zingmp3/download';
exports.index = async (req, res, next) => {
	if (require('../API_KEY/data/check_api_key.js').check_api_key(req, res)) return;
	const link = req.query.link;
	if (!link)
		return res.json({ error: 'Thiếu dữ liệu để khởi chạy chương trình ' });
	const id = link.match(/\/([a-zA-Z0-9]+)\.html/)?.[1] || link.match(/([a-zA-Z0-9]+)$/)?.[1];
	try {
		const response = await axios.get('http://api.mp3.zing.vn/api/streaming/audio/' + id + '/128', {
			responseType: 'stream'
		});
		// if response.data is stream empty
		if (response.data.readableLength == 0)
			throw new Error('Không thể tải xuống bài hát này');

		res.setHeader('Content-Disposition', 'attachment; filename="zingmp3.mp3"');
		res.set('Content-Type', 'audio/mpeg');
		response.data.pipe(res);
	}
	catch (error) {
		res.status(500).json({ error: 'Không thể tải xuống bài hát này' });
	}
};
