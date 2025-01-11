const { unlinkSync } = require('fs-extra');

exports.name = '/del';
exports.index = async (req, res) => {
  try {
    const { code } = req.query;

    unlinkSync(__dirname + '/../post/ship/cache/' + code + ".json");
    return res.jsonp({
      status: 200,
      data: `Đã xóa thành công file có code: ${code}`
    });
  } catch (e) {
    console.log(e);
    return res.json({
      status: 404,
      data: "Vui lòng thử lại"
    });
  }
};