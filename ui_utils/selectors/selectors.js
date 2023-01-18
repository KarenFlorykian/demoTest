class DemoSelectors {
  get username()     { return "//input[@name='username']"};
  get password()     { return "//input[@name='password']"};
  get submit()       { return "//input[@type='submit']"};
  get home()       { return "//h2[text()='Home Page']"};
  
}

module.exports = {DemoSelectors: DemoSelectors};
