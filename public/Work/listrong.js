exports.name = '/listrong';
exports.index = async(req, res, next) => {
  if (require('../API_KEY/data/check_api_key.js').check_api_key(req, res)) return;
	const data = require('./data/data_rong.json');

const list = []
	for(let i of data) {
		var ID = i.ID
		var name = i.name;
		var data1 = i.data1;
    var asia = i.asia;
    var money = i.money;
   var danger = i.danger;
    var color = i.color;
		var des = i.des;
		list.push({
			ID,
			name,
			data1, 
      color,
      money,
      asia,
      danger,
			des
		})
	}
	return res.json(list)
}