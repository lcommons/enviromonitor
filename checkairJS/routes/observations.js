//const { get } = require("../lib/database");
const ds18b20 = require("../lib/ds18b20");

module.exports.getCurrentObservations = function (req, res) {
  let temp;
  //setTimeout(() => {
  temp = ds18b20.getCurrentTemp();
  res.json({ currentTemp: temp });
  return;
  //}, 5000);
  //let temp = ds18b20.getCurrentTempX();
};

//module.exports = getCurrentObservations;
