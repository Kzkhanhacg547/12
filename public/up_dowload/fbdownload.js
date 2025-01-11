exports.name = '/fbdownload';
exports.index = async(req, res, next) => {

		function isUrlValid(link) {
				var res = link.match(/(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g);
				if (res == null)
						return !1;
				else return !0
		};
		var link = req.query.url
		if (!link) return res.jsonp({ error: "Vui lòng nhập URL video Facebook cần tải" })
		if (!isUrlValid(link)) return res.jsonp({ error: "Vui lòng nhập URL hợp lệ" })
		const axios = require('axios')
		axios
				.post('https://www.thetechlearn.com/video-downloader/wp-json/aio-dl/video-data/', {
						url: link
				})
				.then(ress => {
						const data = ress.data
						return res.jsonp({
								data,
								author: "Kz Khánhh"
						})
				})
				.catch(error => {
						return res.jsonp({
								error: 'Không thể xử lí yêu cầu của bạn'
						})
				})
}