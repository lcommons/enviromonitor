const sensor = require("ds18b20-raspi");
//const getCurrentObservations = require("../routes/observations");
//https://www.npmjs.com/package/ds18b20-raspi

module.exports.getCurrentTempX = () => 62;

module.exports.getCurrentTemp = () => {
  // const tempF = sensor.readSimpleF(1);
  const tempF = sensor.readSimpleF();
  console.log(`${tempF} degF`);
  return tempF;
};
//export default getCurrentTemp;
