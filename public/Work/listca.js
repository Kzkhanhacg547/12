exports.name = '/listca';
exports.index = async(req, res, next) => {
  if (require('../API_KEY/data/check_api_key.js').check_api_key(req, res)) return;
	const data = require('./data/data_ca.json');

	const list = []
	for(let i of data) {
		var ID = i.ID
		var name = i.name;
		var data1 = i.data1;
    var rarity = i.rarity;
    var money = i.money;
		var des = i.des;
		list.push({
			ID,
			name,
			data1, 
      rarity,
      money,
			des
		})
	}
	return res.json(list)
}