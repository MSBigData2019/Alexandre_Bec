package com.sparkProject

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.ml
import org.apache.spark.ml.feature.{CountVectorizer, IDF, RegexTokenizer, StopWordsRemover}


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


    /** TF-IF **/

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

  }
}
