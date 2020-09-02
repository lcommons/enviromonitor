//const { get } = require("../lib/database");
const ds18b20 = require("../lib/ds18b20");

module.exports.getCurrentObservations = function (req, res) {
  let temp = ds18b20.getCurrentTempX();
  res.json({ currentTemp: temp });
  return;
};

//module.exports = getCurrentObservations;
