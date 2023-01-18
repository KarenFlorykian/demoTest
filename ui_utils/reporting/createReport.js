// Import the util module 
const util = require('util');
const fs = require('fs');

// need to write to the parent directory for Carrier
var name = 'flow.report';
var date = Date.now();
const reportPath = util.format("/tmp/%s_%s.html", date, name);
const reportPathJson = util.format("/tmp/%s_%s.json", date, name);

class CreateReport {
    async createReports(flow, configString) {
      const reportHTML = flow.generateReport();
      const reportJSON = JSON.stringify(flow.getFlowResult()).replace(/</g, '\\u003c').replace(/\u2028/g, '\\u2028').replace(/\u2029/g, '\\u2029');
      fs.writeFileSync(reportPath, reportHTML);
      fs.writeFileSync(reportPathJson, reportJSON);
      console.log("HTML report path: " + reportPath);
      console.log("JSON report path: " + reportPathJson);
    }
}

module.exports = CreateReport;
