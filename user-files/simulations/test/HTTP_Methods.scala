package test

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import io.gatling.core.structure.ScenarioBuilder

class HTTP_Methods extends Simulation {
  val target = System.getProperty("target")
  val ramp_users = Integer.getInteger("ramp_users")
  val ramp_duration = Integer.getInteger("ramp_duration")
  val duration = Integer.getInteger("duration")

  val webProtocol = http
    .baseUrl(target)
    .disableCaching
    .disableFollowRedirect

  def warmup: ScenarioBuilder = {
    scenario("HTTP_Methods")
      .during(duration, exitASAP = true) {
        exec(
          http("GET_API_new")
            .get("/get")
        ).exitHereIfFailed
          .pause(1, 2)
          .exec(
            http("POST_API")
              .post("/post")
          )
      }.exitHereIfFailed

  }

  setUp(warmup.inject(atOnceUsers(ramp_users))).protocols(webProtocol)
}