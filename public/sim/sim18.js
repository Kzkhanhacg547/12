exports.name = '/sim18';
exports.index = async (req, res, next) => {
  const fs = require('fs');
  const path = require('path');
  const dataSim = require('./data/sim18.json');
  const stringSimilarity = require('string-similarity');

  if (!req.query.type) {
    return res.status(400).json({ error: 'Thiếu dữ liệu để khởi chạy.' });
  }

  const type = req.query.type;

  if (type === 'ask') {
    const ask = decodeURI(req.query.ask);
    if (!ask) {
      return res.status(400).json({ error: 'Thiếu dữ liệu để khởi chạy chương trình.' });
    }

    const messages = dataSim.map(entry => entry.ask);
    const bestMatch = stringSimilarity.findBestMatch(ask, messages);

    // Đặt ngưỡng rating thấp hơn (0.3) để yêu cầu gần giống cũng phản hồi.
    if (bestMatch.bestMatch.rating < 0.3) {
      return res.status(404).json({ answer: 'Xin lỗi, tôi không hiểu câu hỏi của bạn.' });
    }

    const matchedQuestion = bestMatch.bestMatch.target;
    const matchedEntry = dataSim.find(entry => entry.ask.toLowerCase() === matchedQuestion.toLowerCase());

    if (!matchedEntry) {
      return res.status(404).json({ answer: 'Xin lỗi, tôi không tìm thấy câu trả lời phù hợp.' });
    }

    const randomAnswer = matchedEntry.ans[Math.floor(Math.random() * matchedEntry.ans.length)];
    return res.json({ answer: randomAnswer });
  }

  if (type === 'teach') {
    const ask = req.query.ask;
    const ans = req.query.ans;

    if (!ask || !ans) {
      return res.status(400).json({ error: 'Thiếu dữ liệu để thực thi lệnh.' });
    }

    const existingEntry = dataSim.find(entry => entry.ask.toLowerCase() === ask.toLowerCase());

    if (existingEntry) {
      if (existingEntry.ans.includes(ans)) {
        return res.status(400).json({ error: 'Câu trả lời đã tồn tại.' });
      }
      existingEntry.ans.push(ans);
    } else {
      dataSim.push({
        ID: dataSim.length,
        ask,
        ans: [ans]
      });
    }

    fs.writeFileSync(path.join(__dirname, 'data', 'sim18.json'), JSON.stringify(dataSim, null, 2), 'utf-8');
    return res.json({
      msg: 'Cập nhật dữ liệu thành công.',
      data: {
        ask,
        ans
      }
    });
  }

  return res.status(400).json({ error: 'Loại yêu cầu không hợp lệ.' });
};
