// Selectors
const Selectors = require('../selectors/selectors');
const demoSelectors = new Selectors.DemoSelectors();

// Actions
const FindAndClick = require('../actions/findAndClick');
const FindAndType = require('../actions/findAndType.js');
const Find = require('../actions/find');
const HtmlWaiter = require('../actions/htmlWaiter');
const findAndClickXpath = new FindAndClick().XPATH;
const FindAndTypeXPATH = new FindAndType().XPATH;

const waitTillHTMLRendered = new HtmlWaiter().waitTillHTMLRendered;

class Demo {
    async openTodos(page, flow) {
        var step = 'openTodos'
        console.log(step);
        await flow.startTimespan({stepName: step});
        await findAndClickXpath('//span[text()="tasks"]', page);
        await findAndClickXpath('//div[contains(text(),"List all tasks")]', page);
        await waitTillHTMLRendered(page);
        await flow.endTimespan();
        console.log(step);
    }
    async getTodos(page, flow) {
            var step = 'getTodos'
            console.log(step);
            await flow.startTimespan({stepName: step});
            await findAndClickXpath('//button[contains(text(),"Try it out ")]', page);
            await findAndClickXpath('//button[contains(text(),"Execute")]', page);
            await findAndClickXpath('//span[contains(text(),"home/profile")]', page);

            await waitTillHTMLRendered(page);
            await flow.endTimespan();
            console.log(step);
        }

    async Login(page, testuser, tespwd, flow) {
        var step = 'Login'
        console.log(step);
        if (page.isSuccess) {
            await flow.startTimespan({stepName: step});
            await FindAndTypeXPATH(demoSelectors.username, testuser, page);
            await FindAndTypeXPATH(demoSelectors.password, tespwd, page);
            await findAndClickXpath(demoSelectors.submit, page);
            await page
                .waitForXPath(demoSelectors.home)
                .then(() => console.log('logged in'));
            await new HtmlWaiter().waitTillHTMLRendered(page);
            await flow.endTimespan();
        }
        console.log(step);
    }
}

module.exports = Demo;
