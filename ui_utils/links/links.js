class DirectLinks {
	set link(env)   { this.env = env};
	get mainPage()  { return this.env};
	get login() {return this.env + "/login"}
}

module.exports = {DirectLinks: DirectLinks};
