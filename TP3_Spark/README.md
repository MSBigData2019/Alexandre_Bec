Modifications pour lancement :

Modifier dans **build_and_submit.sh** :

```
path_to_spark="$HOME/spark-2.2.0-bin-hadoop2.7"
```

Modifier dans **Trainer.scala** chemin vers le training set :

```
val input = ".../trainingset"
```


**Execution**

```
./build_and_submit.sh Trainer
```

**Result : f1score = 0,6297**


+------------+-----------+-----+
|final_status|predictions|count|
+------------+-----------+-----+
|           1|        0.0|  886|
|           0|        1.0| 3189|
|           1|        1.0| 2508|
|           0|        0.0| 4067|
+------------+-----------+-----+