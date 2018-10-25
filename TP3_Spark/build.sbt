name := "TP3_Spark"

version := "0.1"

scalaVersion := "2.11.11"

libraryDependencies ++= Seq(
  // Spark dependencies. Marked as provided because they must not be included in the uberjar
  "org.apache.spark" %% "spark-core" % "2.2.0" % "provided",
  "org.apache.spark" %% "spark-sql" % "2.2.0" % "provided",
  "org.apache.spark" %% "spark-mllib" % "2.2.0" % "provided",

  // Third-party libraries
  "org.apache.hadoop" % "hadoop-aws" % "2.6.0" % "provided",
  "com.amazonaws" % "aws-java-sdk" % "1.7.4" % "provided",
  "org.scala-lang" % "scala-reflect" % "2.11" % "provided" // To run Spark in IntelliJ
  //"com.github.scopt" %% "scopt" % "3.4.0"        // to parse options given to the jar in the spark-submit
)