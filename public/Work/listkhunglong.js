exports.name = '/listkhunglong';
exports.index = async(req, res, next) => {
  if (require('../API_KEY/data/check_api_key.js').check_api_key(req, res)) return;
	const data = require('./data/data_khunglong.json');

	const list = []
	for(let info of data) {
		var ID = info.ID
	var name = info.name;
	var data1 = info.data1;
  var foot = info.foot;
  var money = info.money;
  var eat = info.eat;
  var danger = info.danger;
  var des = info.des;
		list.push({
		ID,
		name,
    money,
		data1,
    foot,
    danger,
    eat,
    des
		})
	}
	return res.json(list)
}