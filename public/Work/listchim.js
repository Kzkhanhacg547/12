exports.name = '/listchim';
exports.index = async(req, res, next) => {
  if (require('../API_KEY/data/check_api_key.js').check_api_key(req, res)) return;
	const data = require('./data/data_chim.json');

	const list = []
	for(let i of data) {
		var ID = i.ID
	var name = i.name;
	var data1 = i.data1;
  var type = i.type;
  var money = i.money;
  var level = i.level;
  var species = i.species;
  var calculation = i.calculation;
		list.push({
		ID,
		name,
    money,
		data1,
    type,
    level,
    species,
    calculation
		})
	}
	return res.json(list)
}