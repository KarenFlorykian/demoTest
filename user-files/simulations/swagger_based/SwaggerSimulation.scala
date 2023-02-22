import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class SwaggerSimulation extends Simulation {
  val baseUrl = "https://karens.pythonanywhere.com"

  val httpProtocol = http
    .baseUrl(baseUrl)
    .acceptHeader("application/json")
    .contentTypeHeader("application/json")

  val scn = scenario("Test Scenario")
    .exec(http("Login")
      .post("/api/login")
      .body(StringBody("""{"username": "temp", "password": "temp"}"""))
      .asJson
      .check(status.is(200)))
    .pause(1 second)
    .exec(http("Create Task")
      .post("/todos/")
      .body(StringBody("""{"task": "test task"}"""))
      .asJson
      .header("X-Fields", "id,task")
      .check(status.is(201), jsonPath("$.task").is("test task")))
    .pause(1 second)
    .exec(http("List Tasks")
      .get("/todos/")
      .header("X-Fields", "id,task")
      .check(status.is(200), jsonPath("$[0].task").exists))
    .pause(1 second)
    .exec(http("Get All Task")
      .get("/todos")
      .check(status.is(200), jsonPath("$[-1].id").saveAs("latestId")))
    .exec(session => {
        val latestId = session("latestId").as[String]
        println(s"Latest id is ${latestId}")
        session
    })
    .pause(1 second)
    .exec(http("Get Task")
      .get("/todos/${latestId}")
      .header("X-Fields", "id,task")
      .check(status.is(200), jsonPath("$.task").is("test task"), jsonPath("$").saveAs("resp_body"))
    )
    .doIf(session => session.isFailed) {
      exec(session => {
        val response = session("resp_body").as[String]
        println("Here")
        println(response)
        session
      })
    }
    .pause(1 second)
    .exec(http("Update Task")
      .put("/todos/1")
      .body(StringBody("""{"task": "updated task"}"""))
      .asJson
      .header("X-Fields", "id,task")
      .check(status.is(200), jsonPath("$.task").is("updated task")))
    .pause(1 second)
    .exec(http("Delete Task")
      .delete("/todos/1")
      .check(status.in(204, 404)))

  setUp(scn.inject(atOnceUsers(1)))
      .protocols(httpProtocol)
}
