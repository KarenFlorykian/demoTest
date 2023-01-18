// pages
const ColdNavigations = require('./ui_utils/pages/coldNavigations');
const util = require('util');
const measureColdPage = new ColdNavigations().openPage;
const Pages = require('./ui_utils/pages/goto');
const goto = new Pages();

// flows
const Demo = require('./ui_utils/flows/todos');
const openTodos = new Demo().openTodos;
const login = new Demo().Login;

// links
const Links = require('./ui_utils/links/links');
const directLinks = new Links.DirectLinks();

// reports
const CreateReport = require('./ui_utils/reporting/createReport');
const createReports = new CreateReport().createReports;

// helpers
const BrowserActions = require('./ui_utils/helpers/browserActions');
const startBrowserWithLighthouse = new BrowserActions().startBrowserWithLighthouse;
const restartBrowser = new BrowserActions().restartBrowser;
const closeBrowser = new BrowserActions().closeBrowser;
const PageStatus = require('./ui_utils/helpers/pageStatus');
const withPageStatusCheck = new PageStatus().withPageStatusCheck;

async function captureReport() {
    console.time('Execution Time');
    let env          = process.argv[2]; //env link
    let testuser     = process.argv[3]; //username
    let testpassword = process.argv[4]; //password
    let configString = "desktop"; //desktop or mobile
    let browserType  = "headless";//"headful"; //headless (docker) or headful (node.js)

    let browser = ''; let page = ''; let flow = '';

    // set env URL in links.js class
    directLinks.link = env;

    // set vars depending on passed configString, browserType
    [browser, page, flow] = await startBrowserWithLighthouse(configString, browserType);

    //TEST STEPS
    let filename = '/tmp/timeout.png'

    try {
        await withPageStatusCheck(page, () => measureColdPage(page, flow, directLinks.mainPage, "Main Page"));
        await withPageStatusCheck(page, () => openTodos(page, flow));
        await withPageStatusCheck(page, () => new Demo().getTodos(page, flow));
        await withPageStatusCheck(page, () => measureColdPage(page, flow, directLinks.login, "Login"));
        if (testuser != null && testpassword != null){
            await withPageStatusCheck(page, () => login(page,testuser, testpassword, flow));
        } else {
            console.log ("Login skipped cause no credentials provided")
        }       
    } catch (error) {
        if (error.name === "TimeoutError") {
            console.log (error.name)
            console.log (`Screenshot saved as ${filename}`)
            await page.screenshot({ path: filename, fullPage: true })
        } else {
            console.log (error)
        }
    }

    //REPORTING
    await createReports(flow, configString);
    await closeBrowser(browser);
    console.timeEnd('Execution Time');
}
captureReport();
