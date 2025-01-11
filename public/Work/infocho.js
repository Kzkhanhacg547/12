exports.name = '/cho';
exports.index = async(req, res, next) => {
  if (require('../API_KEY/data/check_api_key.js').check_api_key(req, res)) return;
	const data = require('./data/data_cho.json');
	var id = req.query.id;
	if(!id) return res.json({ error: 'thiếu "id" truyện cần tìm' })
	var info = data.find(i => i.ID == id);
	if(info == undefined) return res.json({ error: 'không tìm thấy ID này!' });
	var ID = info.ID
	var name = info.name;
	var data1 = info.data1;
  var type = info.type;
  var money = info.money;
  var color = info.color;
  var danger = info.danger;
  var des = info.des;
	return res.json({
		ID,
		name,
    money,
		data1,
    type,
    danger,
    color,
    des
	})
}