Modifications pour lancement :

Modifier dans **build_and_submit.sh** :

```
path_to_spark="$HOME/spark-2.2.0-bin-hadoop2.7"
```

Modifier dans **Trainer.scala** le chemin vers le training set :

```
val input = ".../trainingset"
```


**Execution**

```
./build_and_submit.sh Trainer
```

**Result : f1score = 0,6480**


| final_status | predictions | count |
|:---------:|:-----------:|:-------:|
| 1         | 0           |   1016  |
| 0         | 1           |   2865  |
| 1         | 1           |   2378  |
| 0         | 1           |   4391  |
