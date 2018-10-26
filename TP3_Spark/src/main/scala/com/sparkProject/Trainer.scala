package com.sparkProject

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.ml.feature._
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.evaluation.{MulticlassClassificationEvaluator, RegressionEvaluator}
import org.apache.spark.ml.tuning.{ParamGridBuilder, TrainValidationSplit}
import org.apache.spark.mllib.evaluation.MulticlassMetrics
import org.apache.spark.mllib.evaluation.{BinaryClassificationMetrics, MultilabelMetrics}


object Trainer {

  def main(args: Array[String]): Unit = {

    val conf = new SparkConf().setAll(Map(
      "spark.scheduler.mode" -> "FIFO",
      "spark.speculation" -> "false",
      "spark.reducer.maxSizeInFlight" -> "48m",
      "spark.serializer" -> "org.apache.spark.serializer.KryoSerializer",
      "spark.kryoserializer.buffer.max" -> "1g",
      "spark.shuffle.file.buffer" -> "32k",
      "spark.default.parallelism" -> "12",
      "spark.sql.shuffle.partitions" -> "12",
      "spark.driver.maxResultSize" -> "2g"
    ))

    val spark = SparkSession
      .builder
      .config(conf)
      .appName("TP_spark")
      .getOrCreate()


    /*******************************************************************************
      *
      *       TP 3
      *
      *       - lire le fichier sauvegardé précédemment
      *       - construire les Stages du pipeline, puis les assembler
      *       - trouver les meilleurs hyperparamètres pour l'entraînement du pipeline avec une grid-search
      *       - Sauvegarder le pipeline entraîné
      *
      *       if problems with unimported modules => sbt plugins update
      *
      ********************************************************************************/

    // IN & OUT paths
    val input = "/Users/Alex/programs/git-msbgd/Alexandre_Bec/TP3_Spark/trainingset"


    // Chargement du dataset
    println("hello world ! from Trainer")
    var df = spark.read.parquet(input)
    println(df.count())


    /**
      * Create Pipeline steps and classification model
       */

    println("1. Tokenizer")
    // Split text into tokenized words
    val tokenizer = new RegexTokenizer()
      .setPattern("\\W+")
      .setGaps(true)
      .setInputCol("text")
      .setOutputCol("tokens")

    println("2. StopWordsRemover")
    val swremover = new StopWordsRemover()
        .setInputCol("tokens")
        .setOutputCol("filtered")

    println("3. TF : Count vectorizer")
    // Convert a collection of text documents to vectors of token counts
    val countvect = new CountVectorizer()
      .setInputCol("filtered")
      .setOutputCol("td")
      .setVocabSize(3)

    println("4. IDF")
    // It down-weights columns which appear frequently in a corpus.
    val idf = new IDF()
      .setInputCol("td")
      .setOutputCol("tfidf")

    println("5,6. Convert categorical columns to indexed")
    val index_country = new StringIndexer()
      .setInputCol("country2")
      .setOutputCol("country_indexed")
      .setHandleInvalid("skip")


    val index_currency = new StringIndexer()
      .setInputCol("currency2")
      .setOutputCol("currency_indexed")
      .setHandleInvalid("skip")

    println("7,8. OneHotEncoder")
    val country_encoder = new OneHotEncoder()
      .setInputCol("country_indexed")
      .setOutputCol("countryVec")

    val currency_encoder = new OneHotEncoder()
      .setInputCol("currency_indexed")
      .setOutputCol("currencyVec")


    println("9. Assemble features into vector")
    val assembler = new VectorAssembler()
      .setInputCols(Array("tfidf", "days_campaign", "hours_prepa", "goal", "countryVec", "currencyVec"))
      .setOutputCol("features")

    println("10. Declare Classification Model")
    val model_classifier = new LogisticRegression()
      .setElasticNetParam(0.0)
      .setFitIntercept(true)
      .setFeaturesCol("features")
      .setLabelCol("final_status")
      .setStandardization(true)
      .setPredictionCol("predictions")
      .setRawPredictionCol("raw_predictions")
      .setThresholds(Array(0.7, 0.3))
      .setTol(1.0e-6)
      .setMaxIter(300)

    /**
      * Pipeline and Training
      */
    println("11. Pipeline de la win")
    val pipeline = new Pipeline()
      .setStages(Array(tokenizer,
        swremover, countvect, idf,
        index_country, country_encoder, index_currency,currency_encoder,
        assembler, model_classifier))

    val Array(training, test) = df.randomSplit(Array(0.9, 0.1), seed = 12345)

    pipeline.fit(training)

    /**
      * Model parameters with grid-search
      * - Create a grid with parameters values
      * - Use a validation Set to evaluate parameters
      * - Then keep parameters where validation error is minimal
      */
    println("12. Model Parameters estimation")

    val paramGrid = new ParamGridBuilder()
      .addGrid(model_classifier.regParam, Array(10e-8, 10e-6, 10e-4, 10e-2))
      .addGrid(countvect.minDF, Array(55.0, 75.0, 95.0))
      .build()

    val evaluator = new MulticlassClassificationEvaluator()
      .setLabelCol("final_status")
      .setPredictionCol("predictions")

    val trainvalidation = new TrainValidationSplit()
      .setEstimator(pipeline)
      .setEvaluator(evaluator)
      .setEstimatorParamMaps(paramGrid)
      // 70% of the data will be used for training and the remaining 30% for validation.
      .setTrainRatio(0.7)

    val validation_model = trainvalidation.fit(training)

    /**
      * Make predictions on the test-dataset
    **/

    val df_predictions = validation_model
      .transform(test)
      .select("features", "final_status", "predictions", "raw_predictions")

    val metrics = evaluator.evaluate(df_predictions)
    println("f1score : "+ metrics)

  }
}
