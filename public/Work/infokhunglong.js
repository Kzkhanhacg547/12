exports.name = '/khunglong';
exports.index = async(req, res, next) => {
  if (require('../API_KEY/data/check_api_key.js').check_api_key(req, res)) return;
	const data = require('./data/data_khunglong.json');
	var id = req.query.id;
	if(!id) return res.json({ error: 'thiếu "id" truyện cần tìm' })
	var info = data.find(i => i.ID == id);
	if(info == undefined) return res.json({ error: 'không tìm thấy ID này!' });
	var ID = info.ID
	var name = info.name;
	var data1 = info.data1;
  var foot = info.foot;
  var money = info.money;
  var eat = info.eat;
  var danger = info.danger;
  var des = info.des;
	return res.json({
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