exports.name = '/game/pubg';
exports.index = async(req, res, next) => {
const resp = require("./data/pubg.json");
const length = resp.length
return res.json({ 
  author: '',
	data: resp[Math.floor(Math.random() * length)]
 })
}