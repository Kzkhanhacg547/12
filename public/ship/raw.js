const { join } = require('path');
const { readFileSync, existsSync } = require('fs');

exports.name = '/raw/:code';
exports.index = (req, res) => {
  try {
    const code = req.params.code;
    const clmm = join(__dirname, "..", "..", "post/ship/cache", code + '.txt');
    
    if (!existsSync(clmm))
      return res.status(404).send({
        error: true,
        message: 'Không tìm thấy file'
      });
    const dataJson = (readFileSync(clmm, "utf-8"));
    res.type('json').send(readFileSync(clmm));
  }
  catch (e) {
    console.log(e);
    return res.send({
      status: 404,
      data: "Vui lòng thử lại"
    });
  }
};