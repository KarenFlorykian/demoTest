package test

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import io.gatling.core.structure.ScenarioBuilder

class NewDemo extends Simulation {

  val webProtocol = http
    .baseUrl("https://www.google.com/")
    .disableCaching
    .disableFollowRedirect

  def warmup: ScenarioBuilder = {
    scenario("test")
      .during(60, exitASAP = true) {
        exec(http("GET_TEST_PAGE").get("/")).exitHereIfFailed
          .pause(5, 10)
          .exec(http("GET_TRANSLATE_PAGE").get("https://translate.google.com/"))
      }.exitHereIfFailed

  }

  setUp(warmup.inject(atOnceUsers(5))).protocols(webProtocol)
}
