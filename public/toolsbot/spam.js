const axios = require('axios');

exports.name = '/spamsms';

exports.index = async (req, res, next) => {
  try {

    const phone = req.query.phone;
    if (!phone) {
      return res.status(400).json({ error: 'Vui lòng nhập số điện thoại.' });
    }

    const huykaiser = await axios.get(`http://botviet.me/api/spams?phone=${phone}`);
    const tong = huykaiser.data.APIREQUESTS;
    const thanhcong = huykaiser.data.SUCCESS;
    const thatbai = huykaiser.data.ERROR;
    const momo = huykaiser.data.data['DATA'].MOMO;
    const meta = huykaiser.data.data['DATA'].META_VN;
    const fpt = huykaiser.data.data['DATA'].FPTSHOP;
    const tv = huykaiser.data.data['DATA'].TV360;
    const atm = huykaiser.data.data['DATA'].ATM;
    const f88 = huykaiser.data.data['DATA'].F88;
    const lo = huykaiser.data.data['DATA'].LOSHIP;
    const zalo = huykaiser.data.data['DATA'].ZALOPAY;
    const money = huykaiser.data.data['DATA'].MONEYVEO;
    const tienoi = huykaiser.data.data['DATA'].TIENOI;
    const vt = huykaiser.data.data['DATA'].VIETTELL;
    const vt2 = huykaiser.data.data['DATA'].VT2;
    const vtpay = huykaiser.data.data['DATA'].VIETTELLPAY;
    const tamo = huykaiser.data.data['DATA'].TAMO;
    const vayvnd = huykaiser.data.data['DATA'].VAYVND;
    const tt = huykaiser.data.data['DATA'].TT;
    const lozi = huykaiser.data.data['DATA'].LOZI;
    const dong = huykaiser.data.data['DATA'].DONGPLUS;
    const vayno = huykaiser.data.data['DATA'].VAYNO;
    const pops = huykaiser.data.data['DATA'].POPS;
    const vieon = huykaiser.data.data['DATA'].VIEON;

    res.json(`[ SPAM SMS ]\n----------\nTỔNG: ${tong}\n----------\nTHÀNH CÔNG: ${thanhcong}\n----------\n THẤT BẠI: ${thatbai}\n----------\n1.MOMO: ${momo}\n----------\n2.META: ${meta}\n----------\n3.FPTSHOP: ${fpt}\n----------\n4.TV360: ${tv}\n----------\n5.ATM: ${atm}\n----------\n6.F88: ${f88}\n----------\n7.LOSHIP: ${lo}\n----------\n8.ZALOPAY: ${zalo}\n----------\n9.MONEYVEO: ${money}\n----------\n10.TIENOI: ${tienoi}\n----------\n11.VIETTELL: ${vt}\n----------\n12.VT2: ${vt2}\n----------\n13.VIETTELLPAY: ${vtpay}\n----------\n14.TAMO: ${tamo}\n----------\n15.VAYVND: ${vayvnd}\n----------\n16.TT: ${tt}\n----------\n17.LOZI${lozi}\n----------\n18.DONGPLUS: ${dong}\n----------\n19.VAYNO: ${vayno}\n----------\n20.POPS: ${pops}\n----------\n21.VIEON: ${vieon}`);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Đã xảy ra lỗi trong quá trình xử lý yêu cầu.' });
  }
};