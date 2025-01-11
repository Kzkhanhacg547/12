exports.name = '/listthu';
exports.index = async(req, res, next) => {
  if (require('../API_KEY/data/check_api_key.js').check_api_key(req, res)) return;
	const data = require('./data/data_thu.json');

	const list = []
	for(let i of data) {
		var ID = i.ID
		var name = i.name;
		var data2 = i.data;
    var money = i.money;
    var type = i.type;
		var level = i.level;
		list.push({
			ID,
			name,
			data2, 
      money,
			type,
      level
		})
	}
	return res.json(list)
}