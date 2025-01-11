exports.name = '/game/csgo';
exports.index = async(req, res, next) => {
const resp = require("./data/csgo.json");
const length = resp.length
return res.json({ 
  author: '',
	data: resp[Math.floor(Math.random() * length)]
 })
}